from flask import Flask, render_template, request, url_for, redirect
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField
from wtforms.validators import DataRequired, Email, Length

app = Flask(__name__)
app.config['SECRET_KEY'] = 'testkey'


class LoginForm(FlaskForm):
    username = StringField(label='username', validators=[DataRequired(), Length(min=3, max=15)])
    password = PasswordField(label='password', validators=[DataRequired(), Length(min=6, max=80)])
    rememberMe = BooleanField(label='remember me')
    submit = SubmitField(label='Sign in')


# This is the home page (aka the products page)
@app.route("/")
def index():
    return render_template('home.html', show_navbar=True, signed_in=False)


@app.route("/login", methods=['POST', 'GET'])
def login():
    form = LoginForm()
    # POST request - Handle form data from client
    if request.method == "POST":
        print('Login')

    # Otherwise, GET request - Return login page to client
    return render_template('login.html', form=form)


@app.route("/register", methods=['POST', 'GET'])
def register():
    # POST request - Handle form data from client
    if request.method == "POST":
        print('Register')

    # Otherwise GET request - Return register page to client
    return render_template('register.html')


@app.route("/search/<product>", methods=['GET'])
def searchProduct(product):
    print('Searching for ', product)

    # Retrieve database information corresponding to the searched product

    return render_template('search_results.html', show_navbar=True)


@app.route("/product/<product_name>", methods=['GET'])
def productInfo(product_name):
    print('Product details for ', product_name)

    return render_template('product_details.html', show_navbar=True)


@app.route("/cart", methods=['POST', 'GET'])
def shoppingCart():
    # POST request - Handle change in quantity removing an item from the cart
    if request.method == "POST":
        print('Change in quantity or removing an item from the cart')

        # if request.form['action'] == "removeItem":
        #   removeItemFromCart()
        # elif request.form['action'] == "addItemQuantity":
        #   addItemQuantity()
        # else:
        #   return redirect(url_for("checkout"))

    # GET request - return cart page to the client
    return render_template("cart.html", show_navbar=True)


@app.route("/checkout", methods=['POST', 'GET'])
def checkout():
    # POST request - Handle form data from the client
    if request.method == "POST":
        print('User submitted the checkout form')
        # if request.form['action'] == "editAddress":
        #   editAddress()
        # elif request.form['action'] == "editPayment":
        #   editPayment()
        # else:
        #   return redirect(url_for("orderConfirmation"))

    # GET request - return checkout page to client
    return render_template("checkout.html")


@app.route("/order_confirmation", methods=['GET'])
def orderConfirmation():
    print("Order confirmation")

    return render_template("order_confirmation.html", show_navbar=True)


if __name__ == "__main__":
    app.run()
