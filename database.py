import pyrebase
import json
from datetime import datetime

class DBhandler:
    def __init__(self):
        with open('./authentication/firebase_auth.json') as f:
            config=json.load(f)

        firebase = pyrebase.initialize_app(config)
        self.db = firebase.database()

    def insert_item(self, name, data, img_path, user_id):
        item_info = {
            "seller_id": user_id,
            "name": data["name"],
            "category": data["category"],
            "mid_category": data.get("mid_category", ""),
            "low_category": data.get("low_category", ""),
            "way": data["way"],
            "price": data["price"],
            "status": data["status"],
            "place": data["place"],
            "explain":data["explain"],
            "img_path": img_path,
            "created_at":data["created_at"],
            "heart_count": 0,
            "review_count": 0
        }

        self.db.child("item").child(name).set(item_info)
        print(data, img_path)
        return True
    
    def insert_user(self, data, pw):
        user_info ={
            "id": data['id'],
            "pw": pw,
            "email": data['email']
        }

        user_id = str(data['id'])

        #아이디 중복 체크
        if self.user_duplicate_check(user_id):
            self.db.child("user").child(user_id).set(user_info) # push -> set
            print(data)
            return True
        else:
            return False
        
    def user_duplicate_check(self, id_string):
        users = self.db.child("user").get()

        if users.val() is None:
            return True

        for res in users.each():
            value = res.val()

            # 기존 push 구조로 들어간 id 확인
            if isinstance(value, dict) and value.get("id") == id_string:
                return False

            # 새로운 child 구조로 들어간 id 확인
            if res.key() == id_string:
                return False

        return True

        
    # 매칭되는 user 찾기    
    def find_user(self, id_, pw_):
        # 'user' 노드에서 'id' 필드의 값이 id_와 일치하는 사용자만 조회
        result = self.db.child("user").order_by_child("id").equal_to(id_).get()
    
        # 해당 ID를 가진 사용자가 존재하는지 확인
        if result.val():
        # 하나의 사용자만 있다고 가정하고 반복
            for key, user_data in result.val().items():
                # ID와 PW 해시가 모두 일치하는지 확인
                if user_data['id'] == id_ and user_data['pw'] == pw_:
                    return True
    
        return False
    
    def get_items(self):
        items = self.db.child("item").get().val()
        return items
    
    
    def get_item_byname(self, name):
        items = self.db.child("item").get()
        target_value = ""
        # print("##########", name) # 디버깅용 print 주석처리
        for res in items.each():
            key_value = res.key()

            if key_value == name:
                target_value = res.val()
        return target_value
    
    def get_items_bycategory(self, cate):
        items = self.db.child("item").get()
        new_dict = {}

        for res in items.each():
            value = res.val()
            key_value = res.key()

            if value.get("category") == cate:
                new_dict[key_value] = value
        
        return new_dict
    
    def get_user_transactions(self, user_id):
        transactions = self.db.child("transactions").order_by_child("user_id").equal_to(user_id).get()
        return transactions.val()
    
    def reg_review(self, data, img_path):
        review_info = {
            "title": data['title'],
            "rate": data['reviewStar'],        
            "review": data['reviewContents'],
            "img_path" : img_path,
            "product_name": data['name'],
            "product_img": data.get('product_img', ''),
            "user_id": data['user_id'],
            "created_at": datetime.now().timestamp(),
            "tx_id": data.get('tx_id')
        }

        self.db.child("reviews").push(review_info)
        print("Review registered:", review_info)

        # [최적화] 리뷰 등록 시 해당 상품의 review_count 증가
        try:
            item_name = data['name']
            item_ref = self.db.child("item").child(item_name)
            item_data = item_ref.get().val()
            
            if item_data:
                current_count = int(item_data.get("review_count", 0))
                item_ref.update({"review_count": current_count + 1})
        except Exception as e:
            print(f"Error updating review count: {e}")

        return True
    
    def get_transaction_status(self, user_id, item_name):
        """
        특정 사용자가 특정 상품에 대해 'pending' 상태의 거래가 있는지 조회합니다.
        """
        try:
            # 1. user_id로 거래 목록을 필터링합니다. (이전에 정의한 get_user_transactions 활용)
            transactions_data = self.get_user_transactions(user_id) 
            
            if not transactions_data:
                return None # 거래 기록 없음

            # 2. 거래 목록을 순회하며 'pending' 상태의 해당 상품 거래를 찾습니다.
            for tx_id, transaction in transactions_data.items():
                if (transaction.get("product_name") == item_name and 
                    transaction.get("status") == "pending"):
                    
                    return "pending" # 대기 중인 거래가 있으면 상태 반환

            return None # 대기 중인 거래 없음

        except Exception as e:
            print(f"Error checking transaction status: {e}")
            return None

    def insert_transaction(self, item_name, user_id, item_data, way):
        """새로운 대여 신청(거래) 정보를 Firebase에 저장합니다."""
        
        transaction_info = {
            "product_name": item_name,
            "product_image_url": item_data.get("img_path"), 
            "price": item_data.get("price"),
            "seller_id": item_data.get("seller_id", "미정"), 
            "user_id": user_id,
            "type": way,
            "status": "pending",
            "request_ts": datetime.now().timestamp(),
        }

        # transactions 노드에 PUSH하여 고유 ID 생성
        self.db.child("transactions").push(transaction_info)
        print("Transaction registered:", transaction_info)
        return True
    
    def get_reviews(self):
        reviews = self.db.child("reviews").get().val()
        return reviews if reviews else {}
    
    def get_recent_photo_reviews(self, limit=8):
        reviews = self.db.child("reviews").get()
        raw = reviews.val()

        if not raw:
            return {}

        review_list = []
        # 홈 화면에 사진이 있는 리뷰만 띄울 예정
        for key, value in raw.items():

            img = value.get("img_path")

            # 이미지가 여러장이라면 첫 번째 사진을 대표 이미지로 선택
            if isinstance(img, list):
                value["thumb"] = img[0]
            else:
                value["thumb"] = img
            
            # 이미지가 있는 리뷰만 홈 화면에 표시
            if value.get("thumb"):
                review_list.append((key, value))

        # 최신순
        review_list.sort(
            key=lambda x: x[1].get("created_at", 0),
            reverse=True
        )

        return dict(review_list[:limit])

    def get_all_reviews(self):
        reviews = self.db.child("reviews").get()

        # 리뷰가 없다면
        if reviews is None:
            return {}

        raw = reviews.val()

        if not raw:
            return {}

        review_list = []

        for key, value in raw.items():
            img = value.get("img_path")

            # 홈화면과 동일하게 대표 이미지 선정
            if isinstance(img, list) and len(img) > 0:
                value["thumb"] = img[0]
            elif isinstance(img, str):
                value["thumb"] = img
            else:
                value["thumb"] = ""

            review_list.append((key, value))

        # 리뷰 최신 등록순으로 정렬
        review_list.sort(
            key=lambda x: x[1].get("created_at", 0),
            reverse=True
        )

        return dict(review_list) 
    
    
    # [최적화] 루프 없이 아이템 정보에서 바로 가져오기
    def get_review_count(self, product_name):
        item = self.db.child("item").child(product_name).get().val()
        if item:
            return item.get("review_count", 0)
        return 0


    def get_heart_byname(self, uid, name):
        hearts = self.db.child("heart").child(uid).get()
        
        if hearts.val() is None:
            return ""

        heart_data = hearts.val().get(name) 

        if heart_data and heart_data.get('interested') == 'Y':
            return 'Y'
        elif heart_data and heart_data.get('interested') == 'N':
            return 'N'
        else:
            return ""
        
    def update_heart(self, user_id, isHeart, item):
        heart_info ={
            "interested": isHeart
        }
        # 1. 유저의 하트 정보 업데이트
        self.db.child("heart").child(user_id).child(item).set(heart_info)
        
        # 2. [최적화] 상품 자체의 heart_count 업데이트 (여기가 핵심)
        try:
            item_ref = self.db.child("item").child(item)
            item_data = item_ref.get().val()
            
            if item_data:
                current_count = int(item_data.get("heart_count", 0))
                
                if isHeart == 'Y':
                    new_count = current_count + 1
                else:
                    new_count = max(0, current_count - 1) # 0보다 작아지지 않게 방지
                
                item_ref.update({"heart_count": new_count})
        except Exception as e:
            print(f"Error updating heart count: {e}")

        return True
    
    def get_heart_list(self, user_id):
        hearts = self.db.child("heart").child(user_id).get()
        if hearts.val() is None:
            return {}
        
        liked_item_names = []
        for item_name, is_liked in hearts.val().items():
            if isinstance(is_liked, dict) and is_liked.get('interested') == 'Y':
                liked_item_names.append(item_name)

        liked_items = {}
        all_items = self.db.child("item").get().val()
        
        if all_items:
            for item_name in liked_item_names:
                if item_name in all_items:
                    liked_items[item_name] = all_items[item_name]
        return liked_items
    
    # [최적화] 루프 없이 아이템 정보에서 바로 가져오기
    def get_heart_count(self, item_name):
        item = self.db.child("item").child(item_name).get().val()
        if item:
            return item.get("heart_count", 0)
        return 0

    def insert_post(self, user_id, title, content):
        post_info = {
            "user_id": user_id,
            "title": title,
            "content": content,
            "created_at": datetime.now().timestamp()
        }
        self.db.child("posts").push(post_info)
        return True
    
    def get_all_posts(self):
        posts = self.db.child("posts").get().val()
        return posts if posts else {}
    
    def get_post(self, post_id):
        post = self.db.child("posts").child(post_id).get().val()
        return post

    def insert_comment(self, post_id, user_id, comment):
        comment_info = {
            "user_id": user_id,
            "comment": comment,
            "created_at": datetime.now().timestamp()
        }
        self.db.child("comments").child(post_id).push(comment_info)
        return True
    
    def get_comments(self, post_id):
        comments = self.db.child("comments").child(post_id).get().val()
        if not comments:
            return {}

        # 오래된 순으로 정렬
        sorted_comments = sorted(
            comments.items(),
            key=lambda x: x[1].get("created_at", 0)
        )
        return sorted_comments
    
    def get_comment_count(self, post_id):
        comments = self.db.child("comments").child(post_id).get().val()
        return len(comments) if comments else 0