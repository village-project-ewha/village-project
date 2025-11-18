from flask import Flask, render_template, request, flash, redirect, url_for, session
from database import DBhandler
from datetime import datetime
import hashlib
import sys

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
    page = request.args.get("page", 0, type=int)
    per_page = 12
    per_row = 4
    row_count = int(per_page / per_row)

    start_idx = per_page * page
    end_idx = per_page * (page + 1)

    data = DB.get_items() 
    
    if not data: # 데이터가 아예 없을 때 처리
        item_counts = 0
        data_for_page = {}
        tot_count = 0
    else:
        item_counts = len(data)
        # 딕셔너리를 리스트로 변환하여 페이징 인덱스를 사용
        data_list = list(data.items())
        data_list.sort(key=lambda x: x[1].get("created_at", 0), reverse=True) #시간순 정렬

        processed_data_list = []
        for key, value in data_list:
            if "created_at" in value:
                value["time_ago"] = time_since(value["created_at"])
            else:
                value["time_ago"] = ""
            processed_data_list.append((key, value))
        data_for_page = dict(processed_data_list[start_idx:end_idx])
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
    return render_template(
        "home.html",
        limit = per_page,
        page = page,
        page_count = int((item_counts/per_page)+1),
        total=item_counts,
        **rows_to_render # 생성된 row만 동적으로 전달
    )
    #return render_template("home.html")
    #return redirect(url_for('view_list')) # 11주차 수정: index 페이지 호출 대신 list 화면으로 연결

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
        return redirect(url_for('view_list')) # 11주차 실습 기준 home 화면 이동 아님
    else:
        flash("Wrong ID or PW!")
        return render_template("login.html")    

@application.route("/logout")
def logout_user():
    session.clear()
    return redirect(url_for('view_list'))

@application.route("/signup")
def signup():
    return render_template("signup.html")

@application.route("/signup_post", methods=['POST'])
def register_user():
    data=request.form
    pw=request.form['pw']
    pw_hash = hashlib.sha256(pw.encode('utf-8')).hexdigest() #id 중복 체크 필요
    if DB.insert_user(data,pw_hash):
        return render_template("login.html")
    else:   # 중복 아이디 존재 시 플래시 메세지 띄움
        flash("user id already exist!")
        return render_template("signup.html")

@application.route("/products")
def view_products():
    page = request.args.get("page", 0, type=int)
    per_page = 16 
    per_row = 4
    row_count = int(per_page / per_row)

    start_idx = per_page * page
    end_idx = per_page * (page + 1)

    data = DB.get_items() 
    
    if not data: # 데이터가 아예 없을 때 처리
        item_counts = 0
        data_for_page = {}
        tot_count = 0
    else:
        item_counts = len(data)
        # 딕셔너리를 리스트로 변환하여 페이징 인덱스를 사용
        data_list = list(data.items())
        data_list.sort(key=lambda x: x[1].get("created_at", 0), reverse=True) #시간순 정렬

        processed_data_list = []
        for key, value in data_list:
            if "created_at" in value:
                value["time_ago"] = time_since(value["created_at"])
            else:
                value["time_ago"] = ""
            processed_data_list.append((key, value))
        data_for_page = dict(processed_data_list[start_idx:end_idx])
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
    return render_template(
        "products.html",
        limit = per_page,
        page = page,
        page_count = int((item_counts/per_page)+1),
        total=item_counts,
        **rows_to_render # 생성된 row만 동적으로 전달
    )

@application.route("/product_detail/<name>/")
def product_detail(name):
    print("###name:", name)
    data = DB.get_item_byname(str(name))
    print("###data:", data)
    return render_template("product_detail.html", name=name, data=data)


@application.route("/list")
def view_list():
    page = request.args.get("page", 0, type=int)
    # 현재 설정으로 테스트 진행
    per_page = 2 
    per_row = 2 
    row_count = int(per_page / per_row) # 현재는 1

    start_idx = per_page * page
    end_idx = per_page * (page + 1)

    data = DB.get_items() 
    
    if not data: # 데이터가 아예 없을 때 처리
        item_counts = 0
        data_for_page = {}
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
        **rows_to_render # 생성된 row만 동적으로 전달
    )

@application.route("/review")
def view_review():
    return render_template("review.html")

@application.route("/review_detail")
def review_detail():
    return render_template("review_detail.html")

@application.route("/reg_items")
def reg_items():
    return render_template("reg_items.html")

@application.route("/reg_reviews")
def reg_reviews():
    return render_template("reg_reviews.html")

@application.route("/select_review")
def select_review():
    return render_template("select_review.html")

@application.route("/submit_item_post", methods=['POST'])
def reg_item_submit_post():
    image_file=request.files["file"]
    image_file.save("static/resource/{}".format(image_file.filename))
    '''
    data=request.form
    DB.insert_item(data['name'], data, f"resource/{image_file.filename}")
    '''
    data = request.form.to_dict()
    data["created_at"] = datetime.now().timestamp()
    data["img_path"] = f"resource/{image_file.filename}"
    DB.insert_item(data['name'], data, data["img_path"])
    return render_template("result.html", data=data, img_path="static/resource/{}".format(image_file.filename))

@application.route("/submit_item")
def reg_item_submit():
    name=request.args.get("name")
    category=request.args.get("category")
    mid_category=request.args.get("mid_category")
    low_category=request.args.get("low_category")
    way=request.args.get("way")
    price=request.args.get("price")
    status=request.args.get("status")
    place=request.args.get("place")
    explain=request.args.get("explain")

    print(name, category, mid_category, low_category, status, way, price, place, explain)

    return render_template("reg_item.html")


if __name__ == "__main__":
    application.run(host='0.0.0.0')
