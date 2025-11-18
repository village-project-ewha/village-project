import pyrebase
import json

class DBhandler:
    def __init__(self):
        with open('./authentication/firebase_auth.json') as f:
            config=json.load(f)

        firebase = pyrebase.initialize_app(config)
        self.db = firebase.database()

    def insert_item(self, name, data, img_path):
        item_info = {
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
            "created_at":data["created_at"]
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

        #아이디 중복 체크
        if self.user_duplicate_check(str(data['id'])):
            self.db.child("user").push(user_info)
            print(data)
            return True
        else:
            return False
        
    def user_duplicate_check(self, id_string):
        users = self.db.child("user").get()

        print("users###",users.val())
        if str(users.val()) == "None": # first registration
            return True
        else:
            for res in users.each():
                value = res.val()

                if value['id'] == id_string:
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
        print("##########", name)
        for res in items.each():
            key_value = res.key()

            if key_value == name:
                target_value = res.val()
        return target_value
    
    