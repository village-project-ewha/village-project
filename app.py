from flask import Flask, render_template, request
from flask_sqlalchemy import SQLAlchemy
import sys
import os
import uuid 
from werkzeug.utils import secure_filename 

application = Flask(__name__)

# --- 1. DB 설정 (SQLAlchemy) ---
basedir = os.path.abspath(os.path.dirname(__file__))
application.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'app.db')
application.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(application) 

# --- 2. DB 모델 정의 ---
class Product(db.Model):
    id = db.Column(db.Integer, primary_key=True) # 고유 ID
    name = db.Column(db.String(100), nullable=False) # 상품명
    price = db.Column(db.Integer, nullable=False) # 가격
    deposit = db.Column(db.Integer, nullable=False) # 보증금
    
    # 폼에서 받는 추가 정보들
    seller = db.Column(db.String(100))
    addr = db.Column(db.String(200))
    email = db.Column(db.String(100))
    category = db.Column(db.String(50))
    card = db.Column(db.String(50)) # 카드결제 여부
    status = db.Column(db.String(50)) # 상품상태
    phone = db.Column(db.String(50))
    trade_type = db.Column(db.String(50)) # 거래방식
    
    image_url = db.Column(db.String(200), nullable=True) # 이미지 저장 경로
    
    # 댓글/좋아요 (기본값 0)
    comment_count = db.Column(db.Integer, default=0)
    like_count = db.Column(db.Integer, default=0)

# 3. DB 파일 생성
with application.app_context():
    db.create_all()



# --- 4. 라우트 정의 ---

@application.route("/")
def hello():
    page = request.args.get('page', 1, type=int)
    
    ITEMS_PER_PAGE = 12

    pagination = Product.query.order_by(Product.id.desc()).paginate(
        page=page, per_page=ITEMS_PER_PAGE, error_out=False
    )
    
    return render_template("home.html", pagination=pagination)

@application.route("/login")
def login():
    return render_template("login.html")

@application.route("/signup")
def signup():
    return render_template("signup.html")

@application.route("/list")
def view_list():
    return render_template("list.html")

@application.route("/product_detail")
def product_detail():
    return render_template("product_detail.html")

'''
@application.route("/products")
def view_products():
    return render_template("products.html")
'''

@application.route("/review")
def view_review():
    return render_template("review.html")

@application.route("/reg_items")
def reg_items():
    return render_template("reg_items.html")

@application.route("/reg_reviews")
def reg_review():
    return render_template("reg_reviews.html")

@application.route("/submit_item_post", methods=['POST'])
def reg_item_submit_post():
    data = request.form
    
    # --- 5. 이미지 파일 처리 ---
    image_file = request.files.get("file") 
    
    if image_file: 
        filename = secure_filename(image_file.filename)
        extension = filename.split('.')[-1]
        new_filename = f"{uuid.uuid4()}.{extension}"
        upload_folder = os.path.join("static", "resource")
        os.makedirs(upload_folder, exist_ok=True) 
        img_path_to_save = os.path.join(upload_folder, new_filename)
        image_file.save(img_path_to_save)
        img_path_for_db = os.path.join("resource", new_filename)
    else:
        img_path_for_db = None 

    # --- 6. DB에 상품 저장 ---
    try:
        new_product = Product(
            name=data.get("name"),
            price=int(data.get("price")),
            deposit=int(data.get("deposit")),
            seller=data.get("seller"),
            addr=data.get("addr"),
            email=data.get("email"),
            category=data.get("category"),
            card=data.get("card"),
            status=data.get("status"),
            phone=data.get("phone"),
            trade_type=data.get("trade_type"), 
            image_url=img_path_for_db # DB에 저장할 이미지 경로
        )
        
        db.session.add(new_product)
        db.session.commit()
        
    except Exception as e:
        db.session.rollback() 
        print(f"DB 저장 오류 발생: {e}") 

    # 디버깅용
    print(data.get("name"), data.get("seller"), data.get("addr"), data.get("email"), 
          data.get("category"), data.get("card"), data.get("status"), data.get("phone"), 
          data.get("deposit"), data.get("trade_type"))

    # result.html 템플릿으로 폼 데이터와 이미지 경로 전달
    return render_template("result.html", data=data, img_path=img_path_for_db)


if __name__ == "__main__":
    # debug=True 모드: 코드 변경 시 서버 자동 재시작, 오류 페이지 표시
    application.run(host='0.0.0.0', port=5000, debug=True)
