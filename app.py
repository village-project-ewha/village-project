from flask import Flask, render_template, request, flash, redirect, url_for, session
from database import DBhandler
import hashlib
import sys

application = Flask(__name__)
application.config["SECRET_KEY"] = "helloosp"

DB = DBhandler()

@application.route("/")
def hello():
    return render_template("home.html")

@application.route("/login")
def login():
    return render_template("login.html")

@application.route("/signup")
def signup():
    return render_template("signup.html")

@application.route("/signup_post", methods=['POST'])
def register_user():
    data=request.form
    pw=request.form['pw']
    pw_hash = hashlib.sha256(pw.encode('utf-8')).hexdigest()    #id 중복 체크 필요
    if DB.insert_user(data,pw_hash):
        return render_template("login.html")
    else:   # 중복 아이디 존재 시 플래시 메세지 띄움
        flash("user id already exist!")
        return render_template("signup.html")

@application.route("/products")
def view_products():
    return render_template("products.html")

@application.route("/product_detail")
def product_detail():
    return render_template("product_detail.html")

@application.route("/list")
def view_list():
    return render_template("list.html")

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
    data=request.form
    DB.insert_item(data['name'], data, f"resource/{image_file.filename}")

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
