from flask import Flask, render_template, request, url_for, redirect

app = Flask(__name__)

@app.route("/", methods = ['POST', 'GET'])
def login():
    if request.method == "POST":
        print("Post has executed")
        # return redirect(url_for("search"))
    else:
        print("Get has executed")
        # return render_template("login.html")

@app.route("/register", methods = ['POST', 'GET'])
def register():
    if request.method == "POST":
        print("Post has executed")
        # return redirect(url_for("search"))
    else:
        print("Get has executed")
        # return render_template("register.html")

@app.route("/search", methods = ['POST', 'GET'])
def search():
    if request.method == "POST":
        print("Post has executed")
        # return redirect(url_for("searchProduct", product))
    else:
        print("Get has executed")
        # return render_template("search.html")

@app.route("/search/<product>", methods = ['POST', 'GET'])
def searchProduct(product):
    if request.method == "POST":
        print("Post has executed")
        # return redirect(url_for("productInfo", productName))
    else:
        print("Get has executed")
        # return render_template("listProducts.html")
        # will return database information corresponding to the product

@app.route("/<productName>", methods = ['POST', 'GET'])
def productInfo(productName):
    if request.method == "POST":
        print("Post has executed")
        # return redirect(url_for("shoppingCart"))
    else:
        print("Get has executed")
        # return render_template("productPage.html")

@app.route("/cart", methods = ['POST', 'GET'])
def shoppingCart():
    if request.method == "POST":
        print("Post has executed")
        # if request.form['action'] == "removeItem":
        #   removeItemFromCart()
        # elif request.form['action'] == "addItemQuantity":
        #   addItemQuantity()
        # else:
        #   return redirect(url_for("checkout"))
    else:
        print("Get has executed")
        # return render_template("shoppingCart.html")

@app.route("/checkout", methods = ['POST', 'GET'])
def checkout():
    if request.method == "POST":
        print("Post has executed")
        # if request.form['action'] == "editAddress":
        #   editAddress()
        # elif request.form['action'] == "editPayment":
        #   editPayment()
        # else:
        #   return redirect(url_for("orderConfirmation"))
    else:
        print("Get has executed")
        # return render_template("checkout.html")

@app.route("/orderconfirmation", methods = ['POST', 'GET'])
def orderConfirmation():
    if request.method == "POST":
        print("Post has executed")
        # return redirect(url_for("productInfo", productName))
    else:
        print("Get has executed")
        # return render_template("orderconfirmation.html")


if __name__ == "__main__":
    app.run()