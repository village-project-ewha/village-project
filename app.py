from flask import Flask, render_template, request
import sys
application = Flask(__name__)

@application.route("/")
def hello():
    return render_template("index.html")

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
    image_file=request.files["file"]
    image_file.save("static/images/{}".format(image_file.filename))
    data=request.form

    name=data.get("name")
    seller=data.get("seller")
    addr=data.get("addr")
    email=data.get("email")
    category=data.get("category")
    card=data.get("card")
    status=data.get("status")
    phone=data.get("phone")
    print(name, seller, addr, email, category, card, status, phone)

    return render_template("templates\result.html", data=data, img_path="static/images/{}".format(image_file.filename))

@application.route("/submit_item")
def reg_item_submit():
    name=request.args.get("name")
    seller=request.args.get("seller")
    addr=request.args.get("addr")
    email=request.args.get("email")
    category=request.args.get("category")
    card=request.args.get("card")
    status=request.args.get("status")
    phone=request.args.get("phone")
    print(name, seller, addr, email, category, card, status, phone)

    return render_template("reg_item.html")


if __name__ == "__main__":
    application.run(host='0.0.0.0')
