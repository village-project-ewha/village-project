from flask import Flask, render_template, request, abort
from flask_sqlalchemy import SQLAlchemy
import sys
import os
import uuid 
from datetime import datetime
from werkzeug.utils import secure_filename 

application = Flask(__name__)

# --- 1. DB 설정 (SQLAlchemy) ---
basedir = os.path.abspath(os.path.dirname(__file__))
application.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'app.db')
application.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(application) 


# -----------------------------------------------------------------
# 🚨 [임시 코드] 여기에 추가!
# 모든 템플릿에서 'current_user' 변수를 사용할 수 있도록
# 가짜(Mock) 사용자 객체를 주입
@application.context_processor
def inject_mock_user():
    
    # 템플릿이 {{ current_user.username }} 등 다른 속성도 사용한다면
    # 여기에 (예: username = "임시사용자")를 추가하세요.
    class MockUser:
        is_authenticated = False # (기본값: 로그인 안 된 상태)
        # is_authenticated = True # (로그인 된 상태를 테스트하려면 이걸로) 
        # username = "테스트유저" 

    return dict(current_user=MockUser())
# -----------------------------------------------------------------

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

class Review(db.Model):  
    id = db.Column(db.Integer, primary_key=True)
    product_id = db.Column(db.Integer, db.ForeignKey('product.id'), nullable=False)
    author = db.Column(db.String(50), nullable=False)
    title = db.Column(db.String(100), nullable=False)
    content = db.Column(db.Text, nullable=False)
    rating = db.Column(db.Float, nullable=False)
    image_url = db.Column(db.String(200))
    created_at = db.Column(db.DateTime, default=datetime.now)
    product = db.relationship('Product', backref=db.backref('reviews', lazy=True))


# -----------------------------------------------------------------
# 🎯 Mock Pagination 클래스 (Flask-SQLAlchemy 인터페이스 모방)
# 이 클래스는 DB 쿼리 없이, 순수 Python 리스트로 페이지네이션을 처리
# -----------------------------------------------------------------
class MockPagination:
    def __init__(self, query, page, per_page, total):
        self.items = query 
        self.page = page
        self.per_page = per_page
        self.total = total
        
        # 총 페이지 수 계산
        self.pages = (total + per_page - 1) // per_page
        
        # 이전/다음 페이지 정보 계산
        self.has_prev = page > 1
        self.prev_num = page - 1 if self.has_prev else None
        self.has_next = page < self.pages
        self.next_num = page + 1 if self.has_next else None

    # iter_pages 메서드 모방 (템플릿에서 사용하는 핵심 기능)
    def iter_pages(self, left_edge=1, right_edge=1, left_current=2, right_current=2):
        last = 0
        for num in range(1, self.pages + 1):
            if num <= left_edge or \
                (self.page - left_current - 1 < num < self.page + right_current + 1) or \
                num > self.pages - right_edge:
                if last + 1 != num:
                    yield None  # ... 표시를 위해 None 반환
                yield num
                last = num

# -----------------------------------------------------------------
# 🎯 Mock 상품 클래스 (Product 모델 대신 사용)
# -----------------------------------------------------------------
class MockProduct:
    def __init__(self, id, name, image_url, price, deposit, comment_count, like_count, trade_type, **kwargs):
        self.id = id
        self.name = name
        self.image_url = image_url
        self.price = price
        self.deposit = deposit
        self.comment_count = comment_count
        self.like_count = like_count
        self.trade_type = trade_type
        for key, value in kwargs.items():
            setattr(self, key, value)

# -----------------------------------------------------------------
# 🎯 Mock 데이터 생성 (총 25개...)
# -----------------------------------------------------------------
mock_products = [
    MockProduct(
        id=i, 
        name=f"Mock 상품 {i}", 
        image_url="resource/sample.jpg", 
        price=10000 + i * 1000, 
        deposit=5000 + i * 500,
        comment_count=i % 5,
        like_count=i % 7,
        trade_type="대여" if i % 2 == 0 else "판매",
        seller=f"임시판매자_{i}" 
    ) for i in range(1, 26) 
]

# ------------------------------
# Mock 클래스 정의
# ------------------------------
class MockReview:
    def __init__(self, id, product_id, title, content, author, image_url, date, rating, created_at):
        self.id = id
        self.product_id = product_id 
        self.title = title
        self.content = content
        self.author = author
        self.image_url = image_url
        self.date = date
        self.rating = rating
        self.created_at = created_at

# ------------------------------
# Mock 데이터
# ------------------------------
mock_reviews = [
    MockReview(1, 1, "첫치피티 공유팟", "...", "송한결", "resource/sample.jpg", "2025.10.08", 5, "2025.10.08"),
    MockReview(2, 1, "빌리지에서 기타 피크까지 빌리지", "...", "김민지", "resource/sample.jpg", "2025.10.08", 5, "2025.10.08"),
    MockReview(3, 1, "샴푸", "...", "박서연", "resource/sample.jpg", "2025.10.08", 4, "2025.10.08"),
    MockReview(4, 1, "애플펜슬 공유팟", "...", "이하늘", "resource/sample.jpg", "2025.10.08", 5, "2025.10.08"),
    MockReview(5, 1, "애플펜슬", "...", "정수빈", "resource/sample.jpg", "2025.10.08", 4, "2025.10.08"),
    MockReview(6, 1, "후드집업 빌렸어요~", "...", "전다은", "resource/sample.jpg", "2025.10.08", 5, "2025.10.08"),
    MockReview(7, 2, "첫치피티 공유팟", "...", "송한결", "resource/sample.jpg", "2025.10.08", 6, "2025.10.08"),
    MockReview(8, 2, "빌리지에서 기타 피크까지 빌리지", "...", "김민지", "resource/sample.jpg", "2025.10.08", 7, "2025.10.08"),
    MockReview(9, 2, "샴푸", "...", "박서연", "resource/sample.jpg", "2025.10.08", 8, "2025.10.08"),
    MockReview(10, 2, "애플펜슬 공유팟", "...", "이하늘", "resource/sample.jpg", "2025.10.08", 9, "2025.10.08"),
    MockReview(11, 2, "애플펜슬", "...", "정수빈", "resource/sample.jpg", "2025.10.08", 10, "2025.10.08"),
    MockReview(12, 2, "후드집업 빌렸어요~", "...", "전다은", "resource/sample.jpg", "2025.10.08", 11, "2025.10.08")
]


# --- 4. 라우트 정의 ---

@application.route('/')
def hello():
    page = request.args.get('page', 1, type=int)
    ITEMS_PER_PAGE = 12

    # ------------------------------
    # 🎯 Mock 데이터 기반 페이지네이션 로직
    # ------------------------------
    total_items = len(mock_products)
    start = (page - 1) * ITEMS_PER_PAGE
    end = start + ITEMS_PER_PAGE
    paginated_items = mock_products[start:end] # 현재 페이지의 Mock 데이터 슬라이싱

    # Flask-SQLAlchemy의 paginate() 인터페이스를 모방하는 MockPagination 객체 생성
    pagination = MockPagination(
        query=paginated_items, 
        page=page, 
        per_page=ITEMS_PER_PAGE, 
        total=total_items
    )

    # ------------------------------
    # 템플릿으로 전달
    # ------------------------------
    return render_template(
        "home.html",
        pagination=pagination 
    )



@application.route("/login")
def login():
    return render_template("login.html")

@application.route("/signup")
def signup():
    return render_template("signup.html")

@application.route('/review/<int:review_id>') 
def review_detail(review_id):

    # 1. ID로 '리뷰' 찾기
    review_to_show = None
    for review in mock_reviews:
        if review.id == review_id:
            review_to_show = review
            break
            
    if review_to_show is None:
        abort(404) # 404 오류 발생시킴

    # ----------------------------------------------------
    # 2. 찾은 리뷰의 'product_id'를 이용해 '상품' 찾기
    
    target_product_id = review_to_show.product_id
    product_to_show = None
    
    for product in mock_products:
        if product.id == target_product_id:
            product_to_show = product
            break
            
    # (예외 처리) 만약 product_id로 상품을 못 찾으면 404
    if product_to_show is None:
        abort(404)
    # ----------------------------------------------------

    # 3. 'review'와 'product'를 둘 다 전달
    return render_template(
        'review_detail.html', 
        review=review_to_show,
        product=product_to_show 
    )


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



@application.route("/reg_items")
def reg_items():
    return render_template("reg_items.html")




@application.route('/select_review')
def select_review_target():
    # TODO (백엔드):
    # 1. DB에서 '현재 로그인한 유저'의 '거래 완료' 내역들을 조회해야 함.
    # 2. 지금은 가짜(Mock) 거래 내역 3개를 만듦.
    
    # 템플릿에서 쓸 가짜(Mock) 클래스 정의
    class MockProduct:
        def __init__(self, name, image_url):
            self.name = name
            self.image_url = image_url

    class MockTransaction:
        def __init__(self, id, product_name, image_url):
            self.id = id
            self.product = MockProduct(product_name, image_url)

    # 가짜 거래 내역 리스트 (transactions, 복수형)
    mock_transactions = [
        MockTransaction(1, "테스트 상품 1 (거래 ID: 1)", "resource/sample.jpg"),
        MockTransaction(5, "테스트 상품 5 (거래 ID: 5)", "resource/sample.jpg"),
        MockTransaction(9, "테스트 상품 9 (거래 ID: 9)", "resource/sample.jpg")
    ]
    
    # 3. 새 HTML 파일('select_review.html')로 가짜 리스트를 전달
    return render_template(
        'select_review.html', 
        transactions=mock_transactions # 'transactions' (복수형)로 전달
    )



@application.route('/reg_review/<int:transaction_id>') 
def reg_review(transaction_id):
    
    # ----------------------------------------------------
    # 🚨 [임시 코드]
    # 프론트엔드 화면 확인을 위해 가짜(Mock) 데이터를 만듦

    # TODO (백엔드): 
    # 1. DB 모델 정의 부분에 'Transaction' 모델을 추가해야 함
    # 2. 이 함수에서 transaction_id를 사용해 실제 DB에서 데이터를 조회해야 함

    class MockProduct: # 가짜 상품
        name = "테스트 상품명입니다"
        image_url = "resource/sample.jpg"
        brand = "나이키"
        category = "패션/잡화"
        price = 35000           
        seller = "임시판매자_이름"
        trade_type = "택배거래" 

    class MockTransaction: # 가짜 거래내역
        id = transaction_id
        product = MockProduct() 

    transaction_data = MockTransaction()
    # ----------------------------------------------------

    # 2. 템플릿으로 'transaction'이라는 이름으로 데이터를 전달
    return render_template(
        'reg_reviews.html', 
        transaction=transaction_data  # 가짜 데이터를 전달
    )


@application.route("/submit_item_post", methods=['POST'])
def reg_item_submit_post():
    data = request.form
    
    # --- 이미지 파일 처리 ---
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

    # --- DB에 상품 저장 ---
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
            image_url=img_path_for_db 
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