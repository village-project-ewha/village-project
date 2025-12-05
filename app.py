from flask import Flask, render_template, request, flash, redirect, url_for, session, jsonify
from database import DBhandler
from datetime import datetime
from PIL import Image
Image.MAX_IMAGE_PIXELS = None
from werkzeug.utils import secure_filename
import os
import uuid
import hashlib
import sys
import math

application = Flask(__name__)
application.config["SECRET_KEY"] = "helloosp"

DB = DBhandler()

#시간 계산용
def time_since(ts):
    if isinstance(ts, str):
        ts = float(ts)

    past = datetime.fromtimestamp(ts)
    now = datetime.now()
    diff = now - past

    seconds = diff.total_seconds()
    minutes = seconds // 60
    hours = seconds // 3600
    days = seconds // 86400

    if minutes < 1:
        return "방금 전"
    elif minutes < 60:
        return f"{int(minutes)}분 전"
    elif hours < 24:
        return f"{int(hours)}시간 전"
    else:
        return f"{int(days)}일 전"

@application.route("/")
def hello():
    # 홈 화면에 최근 포토 리뷰 추가
    recent_reviews = DB.get_recent_photo_reviews(limit=8)
    # 홈 화면에 리뷰 개수 정확하게 출력
    review_count = len(recent_reviews) if recent_reviews else 0
    
    posts = DB.get_all_posts()
    post_list = []
    if posts:
        for post_id, data in posts.items():

            if "created_at" in data:
                data["time_ago"] = time_since(data["created_at"])
            else:
                data["time_ago"] = ""

            post_list.append({
                "id": post_id,
                "title": data.get("title"),
                "user_id": data.get("user_id"),
                "content": data.get("content"),
                "time_ago": data["time_ago"],
                "created_at": data.get("created_at"),
                "comment_count": DB.get_comment_count(post_id)
            })

    post_list.sort(key=lambda x: x["created_at"], reverse=True)
    post_list = post_list[:10]

    return render_template(
        "home.html",
        recent_reviews=recent_reviews,
        review_count = review_count,
        posts = post_list
    )

@application.route("/login")
def login():
    return render_template("login.html")

@application.route("/login-form", methods=['POST'])
def login_user():
    id_=request.form['id'] 
    pw=request.form['pw']
    pw_hash = hashlib.sha256(pw.encode('utf-8')).hexdigest() # 입력받은 비밀번호의 해시값 생성
    if DB.find_user(id_, pw_hash): # 매칭되는 사용자 존재
        session['user_id'] = id_
        return redirect(url_for('hello')) # home 화면 이동 수정
    else:
        flash("Wrong ID or PW!")
        return render_template("login.html")    

@application.route("/logout")
def logout_user():
    session.clear()
    return redirect(url_for('hello'))

@application.route("/signup")
def signup():
    return render_template("signup.html")

@application.route("/signup_post", methods=['POST'])
def register_user():
    mode = request.form.get("mode")  # 요청 구분 키 (중복 확인 vs 실제 회원가입)

    # 아이디 중복 확인 
    if mode == "id_check":
        user_id = request.form.get("id")

        if DB.user_duplicate_check(user_id):
            return {"result": "ok"}
        else:
            return {"result": "duplicate"}

    # 실제 회원가입 로직
    data = request.form.to_dict()

    # 학교 이메일 도메인 강제 처리
    email_id = data['email']
    data['email'] = f"{email_id}@ewha.ac.kr"

    # 비밀번호 해싱
    pw = data['pw']
    pw_hash = hashlib.sha256(pw.encode('utf-8')).hexdigest()

    # DB 저장
    if DB.insert_user(data, pw_hash):
        return render_template("login.html")
    else:
        flash("user id already exist!")
        return render_template("signup.html")
    



import time # 상단에 import 추가

@application.route("/products")
def view_products():
    page = request.args.get("page", 0, type=int)
    category = request.args.get("category", "all")
    sort_method = request.args.get("sort", "recent") 

    per_page = 16 
    per_row = 4

    # 1. DB에서 데이터 가져오기
    if category == "all":
        data = DB.get_items() 
    else:
        data = DB.get_items_bycategory(category) 
        
    # 2. 데이터 유무 확인 및 정렬
    if not data: 
        item_counts = 0
        data_for_page = {}
    else:
        item_counts = len(data)
        data_list = list(data.items())

        # 정렬 로직
        if sort_method == "low_price":
            data_list.sort(key=lambda x: int(str(x[1].get("price") or "0").replace(",", "")))
        elif sort_method == "high_price":
            data_list.sort(key=lambda x: int(str(x[1].get("price") or "0").replace(",", "")), reverse=True)
        else:
            data_list.sort(key=lambda x: x[1].get("created_at", 0), reverse=True)

        # 페이징 (Slicing)
        start_idx = per_page * page
        end_idx = per_page * (page + 1)
        
        paged_data_list = data_list[start_idx:end_idx]

        # 3. 시간 계산 및 데이터 가공
        processed_data_list = [] 
        
        for key, value in paged_data_list:
            if "created_at" in value:
                value["time_ago"] = time_since(value["created_at"])
            else:
                value["time_ago"] = ""

            value["heart_count"] = DB.get_heart_count(key)
            value["review_count"] = DB.get_review_count(key)


            processed_data_list.append((key, value)) 
        
        # 딕셔너리로 변환
        data_for_page = dict(processed_data_list)
        
    # 5. 템플릿에 전달할 row 데이터 생성 
    rows_to_render = {}
    page_items_list = list(data_for_page.items()) 
    tot_count_in_page = len(page_items_list)
    
    # row 생성 로직
    for i in range(int(per_page / per_row)): 
        start = i * per_row
        end = (i + 1) * per_row
        
        if start < tot_count_in_page:
            row_data = dict(page_items_list[start:end])
            rows_to_render[f'row{i+1}'] = row_data.items()
        else:
            break

    return render_template(
        "products.html",
        limit = per_page,
        page = page,
        page_count = int((item_counts/per_page) + 1) if item_counts % per_page != 0 else int(item_counts/per_page),
        total = item_counts,
        category = category,
        sort = sort_method,
        **rows_to_render 
    )

@application.route("/product_detail/<name>/")
def product_detail(name):
    print("###name:", name)
    data = DB.get_item_byname(str(name))
    print("###data:", data)
    
    my_heart = 'N'
    if 'user_id' in session:
        my_heart = DB.get_heart_byname(session['user_id'], name)
    
    return render_template(
        "product_detail.html", 
        name=name, 
        data=data, 
        price=int(data['price']), 
        deposit=int(data['price'])*2,
        my_heart=my_heart 
    )
@application.route("/list")
def view_list():
    page = request.args.get("page", 0, type=int)
    # 현재 설정으로 테스트 진행

    category = request.args.get("category", "all") # 셀렉트 박스에서 선택한 카테고리 값 받아옴

    per_page = 2 
    per_row = 2 
    row_count = int(per_page / per_row) # 현재는 1

    start_idx = per_page * page
    end_idx = per_page * (page + 1)

    # 카테고리로 DB에서 데이터 받아오기
    if category == "all":
        data = DB.get_items() 
    else:
        data = DB.get_items_bycategory(category)
    
    data = dict(sorted(data.items(), key=lambda x:x[0], reverse=False))  #sorting
    
    if not data: # 데이터가 아예 없을 때 처리
        item_counts = 0
        data_for_page = {}
        tot_count = 0
    else:
        item_counts = len(data)

        # 딕셔너리를 리스트로 변환하여 페이징 인덱스를 사용
        data_list = list(data.items()) 
        data_for_page = dict(data_list[start_idx:end_idx])

        tot_count = len(data_for_page)

    # 템플릿에 전달할 데이터를 담을 딕셔너리
    rows_to_render = {}
    row_count = int(per_page / per_row) # 실제 필요한 행의 수 계산

    for i in range(row_count): 
        start = i * per_row
        end = (i + 1) * per_row

        # 페이지에 보여줄 데이터가 남아있는 경우에만 row 딕셔너리 생성
        if start < tot_count:
            if end > tot_count: # 마지막 줄 처리
                end = tot_count
            
            # data_for_page 딕셔너리에서 현재 행의 데이터를 잘라냄
            row_data = dict(list(data_for_page.items())[start:end])
            
            # row1, row2, row3... 형식으로 저장하고 전달
            rows_to_render[f'row{i+1}'] = row_data.items()
        else:
            break

    # 템플릿 렌더링 시, 딕셔너리 언패킹으로 동적으로 변수 전달
    return render_template(
        "list.html",
        limit = per_page,
        page = page,
        page_count = int((item_counts/per_page)+1),
        total=item_counts,
        category=category,  #카테고리를 html 코드로 전달
        **rows_to_render # 생성된 row만 동적으로 전달
    )

@application.route("/review")
def view_review():
    page = request.args.get("page", 1, type=int) 
    per_page = 8 
    
    reviews_data = DB.get_all_reviews()

    if not reviews_data:
        return render_template("review.html", reviews={}, page=1, page_count=1, total=0)

    # 1. 딕셔너리를 리스트로 변환 [(key, value), ...]
    data_list = list(reviews_data.items())

    # 2. 최신순(created_at)으로 정렬
    data_list.sort(
        key=lambda x: float(x[1].get("created_at", 0)), 
        reverse=True
    )

    # 3. 전체 아이템 수 및 총 페이지 수 계산
    total_count = len(data_list)
    page_count = math.ceil(total_count / per_page) 

    # 4. 현재 페이지에 해당하는 데이터 슬라이싱
    start_idx = (page - 1) * per_page
    end_idx = start_idx + per_page
    
    # 리스트 슬라이싱 (범위를 벗어나도 에러 안 남)
    sliced_list = data_list[start_idx:end_idx]

    # 5. 템플릿 호환성을 위해 다시 딕셔너리로 변환
    paginated_reviews = dict(sliced_list)

    return render_template(
        "review.html", 
        reviews=paginated_reviews, 
        page=page, 
        page_count=page_count, 
        total=total_count
    )

def get_reviews(self):
    reviews = self.db.child("review").get().val()

    if not reviews:
        return {}

    review_list = []

    for key, value in reviews.items():
        img = value.get("img_path")

        # 썸네일에는 무조건 대표 이미지 한 장만 보여줌
        if isinstance(img, list) and len(img) > 0:
            value["thumb"] = img[0]
        elif isinstance(img, str):
            value["thumb"] = img
        else:
            value["thumb"] = None

        review_list.append((key, value))

    # 최신 등록순으로 리뷰 보여주기
    review_list.sort(
    key=lambda x: int(x[1].get("created_at", 0)) if str(x[1].get("created_at", 0)).isdigit() else 0,
    reverse=True
    )

    return dict(review_list)


@application.route("/review_detail")
def review_detail():
    return render_template("review_detail.html")

@application.route("/view_review_detail/<review_id>/")
def view_review_detail(review_id):
    reviews = DB.get_reviews()
    review = reviews.get(review_id)

    if not review:
        flash("리뷰를 찾을 수 없습니다.")
        return redirect(url_for('view_review'))
    
    return render_template("view_review_detail.html", review=review)

@application.route("/reg_items")
def reg_items():
    return render_template("reg_items.html")

@application.route("/reg_review_init/<tx_id>")
def reg_review_init(tx_id):
    if 'user_id' not in session:
        flash("로그인이 필요합니다.")
        return redirect(url_for('login'))

    tx_data = DB.db.child("transactions").child(tx_id).get().val()
    
    if not tx_data:
        flash("유효하지 않은 거래 정보를 요청했습니다.")
        return redirect(url_for('select_review'))
    
    product_info = {
        'name': tx_data.get('product_name', '상품 이름 없음'),
        'tx_id': tx_id,
        'price': tx_data.get('price', '가격 정보 없음'),
        'seller_id': tx_data.get('seller_id', '판매자 ID 없음'),
        'category': tx_data.get('category', '미분류'),
        'mid_category': tx_data.get('mid_category', ''),
        'img_path': tx_data.get('product_image_url', 'images/sample.webp')
    }

    return render_template("reg_reviews.html", product=product_info)

@application.route("/reg_review", methods=['POST'])
def reg_review():
    if 'user_id' not in session:
        flash("로그인이 필요합니다.")
        return redirect(url_for('login'))
        
    data = request.form.to_dict()
    image_file = request.files.get("file")
    data['user_id'] = session['user_id']
    
    # DB에 저장될 이미지 경로 초기화 (이미지 없을 경우 대비)
    db_img_path = None 

    if image_file and image_file.filename:
        # 1. 저장 경로 설정 (static/images/reviews)
        # 폴더가 없으면 자동으로 생성
        save_dir = os.path.join("static", "images", "reviews")
        if not os.path.exists(save_dir):
            os.makedirs(save_dir)

        # 2. 파일명 안전하게 생성 (UUID 사용 + jpg 강제)
        filename = f"{uuid.uuid4().hex}.jpg"
        save_path = os.path.join(save_dir, filename)

        # 3. 이미지 리사이징 및 압축 저장
        try:
            img = Image.open(image_file)
            
            # 투명 배경(PNG) 대응: 흰색 배경으로 변경
            if img.mode in ("RGBA", "P"):
                img = img.convert("RGB")
            
            # 리사이징 (긴 변 기준 800px)
            img.thumbnail((800, 800))
            
            # JPG 포맷으로 압축 저장 (퀄리티 85%)
            img.save(save_path, "JPEG", quality=85, optimize=True)

            # 4. DB에 저장할 경로 설정 (static/ 제외)
            db_img_path = f"images/reviews/{filename}"

        except Exception as e:
            print(f"리뷰 이미지 처리 실패: {e}")
            flash("이미지 업로드 중 오류가 발생했습니다.")
            return redirect(url_for('view_review')) # 혹은 적절한 에러 페이지

    # 5. DB 저장 호출
    # 이미지가 없으면 db_img_path는 None으로 전달됨
    DB.reg_review(data, db_img_path)

    flash("리뷰가 성공적으로 등록되었습니다. 감사합니다!")
    return redirect(url_for('view_review'))


@application.route("/select_review")
def select_review():
    if 'user_id' not in session:
        flash("로그인이 필요합니다.")
        return redirect(url_for('login'))
        
    current_user_id = session['user_id']
    transactions = []
    
    tx_data = DB.get_user_transactions(current_user_id) 
    
    if tx_data:
        for tx_id, data in tx_data.items():
            
            completion_ts = data.get('completion_ts') 
            date_str = '날짜 미정'
            if completion_ts:
                try:
                    completion_date = datetime.fromtimestamp(completion_ts / 1000) 
                    date_str = completion_date.strftime('%Y-%m-%d')
                except Exception as e:
                    print(f"날짜 변환 오류: {e}")
                    pass

            transactions.append({
                'id': tx_id, 
                'product_name': data.get('product_name', '상품 이름 없음'),
                'date': date_str,
                # DB에 저장된 product_image_url 사용
                'img': data.get('product_image_url', 'resource/Photo Review_svg/default.svg') 
            })

    print(f"조회된 거래 데이터 (tx_data): {tx_data}")
            
    return render_template("select_review.html", transactions=transactions)

@application.route("/reg_item_submit_post", methods=['POST'])
def reg_item_submit_post():
    if 'user_id' not in session:
        flash("로그인이 필요한 서비스입니다.")
        return redirect(url_for('login'))
    
    user_id = session["user_id"]
    image_file = request.files["file"]

    # 1. 이미지가 있는지 확인
    if image_file:
        # 2. 저장할 경로 설정 (static/images/products)
        # 폴더가 없으면 알아서 생성합니다.
        save_dir = os.path.join("static", "images", "products")
        if not os.path.exists(save_dir):
            os.makedirs(save_dir)

        # 3. 파일명 안전하게 생성 (UUID 사용으로 중복 방지)
        # 원래 확장자가 무엇이든 jpg로 저장할 것이므로 .jpg 붙임
        filename = f"{uuid.uuid4().hex}.jpg"
        save_path = os.path.join(save_dir, filename)

        # 4. 이미지 처리 (Pillow 사용)
        try:
            img = Image.open(image_file)
            
            # 투명 배경(PNG)이 있을 경우 흰색 배경으로 변경 (JPG 저장을 위해 필수)
            if img.mode in ("RGBA", "P"):
                img = img.convert("RGB")
            
            # 5. 리사이징 (최대 긴 변을 800px로 줄임 - 비율 유지)
            img.thumbnail((800, 800))

            # 6. 저장 및 압축
            img.save(save_path, "JPEG", quality=85, optimize=True)

            # DB에 저장할 경로 문자열 (static/ 제외하고 상대경로로 저장하거나 필요에 따라 조정)
            # HTML에서 <img src="{{ url_for('static', filename=...) }}">를 쓰기 편하게
            # 여기서는 DB에 'images/products/파일명' 형태로 저장한다고 가정
            db_img_path = f"images/products/{filename}"

        except Exception as e:
            print(f"이미지 처리 중 오류 발생: {e}")
            flash("이미지 업로드 중 오류가 발생했습니다.")
            return redirect(url_for('reg_item_submit'))

    else:
        # 이미지가 없을 경우 기본 이미지 처리 (선택 사항)
        db_img_path = "" 

    # 7. 데이터베이스 저장
    data = request.form.to_dict()
    data["created_at"] = datetime.now().timestamp()
    data["img_path"] = db_img_path # 처리된 경로 저장

    DB.insert_item(data['name'], data, data["img_path"], user_id)
    
    return redirect(url_for('product_detail', name=data['name']))

@application.route("/submit_item")
def reg_item_submit():
    name=request.args.get("name")
    category=request.args.get("category")
    mid_category=request.args.get("mid_category")
    low_category=request.args.get("low_category")
    way=request.args.get("way")
    price=request.args.get("price")
    method=request.args.get("method")
    status=request.args.get("status")
    place=request.args.get("place")
    explain=request.args.get("explain")

    print(name, category, mid_category, low_category, status, way, price, method, place, explain)

    return render_template("reg_items.html")

@application.template_filter('datetimeformat')
def datetimeformat(value):
    try:
        return datetime.fromtimestamp(value).strftime('%Y-%m-%d')
    except:
        return ""


from flask import session, jsonify 

@application.route('/show_heart/<name>/', methods=['GET'])
def show_heart(name):
    user_id = session.get('user_id')
    
    # 로그인 상태 확인 및 좋아요 상태 조회
    if not user_id:
        return jsonify({'my_heart': 'N'})
    
    heart_status_int = DB.get_heart_byname(user_id, name)
        
    if heart_status_int == 'Y':
        return jsonify({'my_heart': 'Y'})
    else:
        return jsonify({'my_heart': 'N'})

@application.route('/like/<name>/', methods=['POST'])
def like(name):
    my_heart = DB.update_heart(session['user_id'],'Y',name)
    return jsonify({'msg': '좋아요 완료!'})

@application.route('/unlike/<name>/', methods=['POST'])
def unlike(name):
    my_heart = DB.update_heart(session['user_id'],'N',name)
    return jsonify({'msg': '좋아요 취소 완료!'}) # 문구 수정

@application.route("/heart_list")
def view_heart_list():
    if 'user_id' not in session:
        flash("로그인이 필요한 서비스입니다.")
        return redirect(url_for('login'))
        
    user_id = session['user_id']
    liked_items = DB.get_heart_list(user_id)
    
    return render_template("heart_list.html", liked_items=liked_items)

@application.route("/request_rental/<name>/", methods=['POST'])
def request_rental(name):
    if 'user_id' not in session:
        return jsonify({'success': False, 'message': '로그인이 필요합니다.'}), 401

    user_id = session['user_id']
    
    item_data = DB.get_item_byname(name)
    
    if not item_data:
        return jsonify({'success': False, 'message': '상품 정보를 찾을 수 없습니다.'}), 404

    way = item_data.get("way", "대여")
    success = DB.insert_transaction(name, user_id, item_data, way)
    
    if success:
        return jsonify({'success': True, 'message': '신청이 완료되었습니다.'})
    else:
        return jsonify({'success': False, 'message': '거래 정보 저장에 실패했습니다.'}), 500

@application.route("/my_transactions")
def my_transactions():
    if 'user_id' not in session:
        flash("로그인이 필요합니다.")
        return redirect(url_for('login'))
        
    current_user_id = session['user_id']
    transactions = []
    
    tx_data = DB.get_user_transactions(current_user_id) 
    
    if tx_data:
        for tx_id, data in tx_data.items():
            
            ts = data.get('request_ts') 
            date_str = '날짜 미정'
            if ts:
                try: 
                    date_str = datetime.fromtimestamp(ts).strftime('%Y-%m-%d')
                except Exception as e:
                    print(f"날짜 변환 오류: {e}")

            transactions.append({
                'id': tx_id, 
                'product_name': data.get('product_name', '상품 이름 없음'),
                'date': date_str,
                'timestamp': ts or 0,
                # DB에 저장된 product_image_url 사용
                'img': data.get('product_image_url', 'resource/Photo Review_svg/default.svg') 
            })

    print(f"조회된 거래 데이터 (tx_data): {tx_data}")
    transactions.sort(key=lambda x: x['timestamp'], reverse=True)
            
    return render_template("transactions.html", transactions=transactions)

@application.route("/request_board")
def request_board():
    posts = DB.get_all_posts()
    post_list = []
    if posts:
        for post_id, data in posts.items():

            if "created_at" in data:
                data["time_ago"] = time_since(data["created_at"])
            else:
                data["time_ago"] = ""

            post_list.append({
                "id": post_id,
                "title": data.get("title"),
                "user_id": data.get("user_id"),
                "content": data.get("content"),
                "time_ago": data["time_ago"],
                "created_at": data.get("created_at"),
                "comment_count": DB.get_comment_count(post_id)
            })

    post_list.sort(key=lambda x: x["created_at"], reverse=True)

    return render_template("request_board.html", posts=post_list)

@application.route("/request_write")
def request_write():
    if 'user_id' not in session:
        flash("로그인이 필요합니다.")
        return redirect(url_for('login'))

    return render_template("request_write.html")

@application.route("/request_write", methods=["POST"])
def request_write_post():
    if 'user_id' not in session:
        return redirect(url_for('login'))

    title = request.form.get("title")
    content = request.form.get("content")
    user_id = session["user_id"]

    DB.insert_post(user_id, title, content)

    return redirect(url_for("request_board"))

@application.route("/request_view/<post_id>")
def request_view(post_id):
    post = DB.get_post(post_id)
    comments = DB.get_comments(post_id)

    comment_count = len(comments) if comments else 0

    post["time_ago"] = time_since(post.get("created_at", 0))
    post["comment_count"] = comment_count
    

    comment_list = []
    for cid, c in comments:
        c["time_ago"] = time_since(c["created_at"])
        comment_list.append((cid, c))

    return render_template(
        "request_view.html",
        post_id=post_id,
        post=post,
        comments=comment_list
    )

@application.route("/request_comment/<post_id>", methods=["POST"])
def request_comment(post_id):
    if 'user_id' not in session:
        return redirect(url_for('login'))

    comment = request.form.get("comment")
    user_id = session["user_id"]

    DB.insert_comment(post_id, user_id, comment)

    return redirect(url_for("request_view", post_id=post_id))


@application.template_filter('format_currency')
def format_currency(value):
    try:
       
        if value is None or value == "":
            return "0원"
            
       
        value = int(str(value).replace(',', ''))
        
        if value >= 10000:
            man = value // 10000
            remainder = value % 10000
            if remainder == 0:
                return f"{man}만원"
            else:
                return f"{man}만 {remainder:,}원"
        else:
            return f"{value:,}원"
    except (ValueError, TypeError):
        
        return f"{value}원"
    
    
if __name__ == "__main__":
    application.run(host='0.0.0.0')
    
    



