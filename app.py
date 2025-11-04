from flask import Flask, render_template, request
import sys
application = Flask(__name__)

@application.route("/")
def hello():
    return render_template("home.html")

@application.route("/login")
def login():
    return render_template("login.html")

@application.route("/signup")
def signup():
    return render_template("signup.html")

@application.route("/products")
def view_list():
    return render_template("products.html")

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
    image_file.save("static/resource/{}".format(image_file.filename))
    data=request.form

    name=data.get("name")
    category=data.get("category")
    mid_category=data.get("mid_category")
    low_category=data.get("low_category")
    way=data.get("way")
    price=data.get("price")
    status=data.get("status")
    place=data.get("place")
    print(name, category, mid_category, low_category, status, way, price, place)

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
    print(name, category, mid_category, low_category, status, way, price, place)

    return render_template("reg_item.html")


if __name__ == "__main__":
    application.run(host='0.0.0.0')
