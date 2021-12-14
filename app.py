from flask import Flask, render_template, request, url_for, redirect, session
from os import linesep
from flask_cors import CORS
from wtforms.widgets.core import Input
from db import app
from db import *
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, IntegerField
from wtforms.validators import InputRequired, Length, ValidationError, Email, email_validator
from flask_bcrypt import Bcrypt
from flask_login import login_manager, login_user, LoginManager, login_required, logout_user, current_user
import stripe

from datetime import datetime

user_is_logged_in = False

# session['cart items'] = []

# app = Flask(__name__)
app.config['SECRET_KEY'] = 'testkey'
stripe.api_key = 'sk_test_4eC39HqLyjWDarjtT1zdp7dc'
bcrypt = Bcrypt(app) 
CORS(app)

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = "login"

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(user_id)


class RegisterForm(FlaskForm):
    username = StringField(validators=[InputRequired(), Length(min=4,max=15)], render_kw={"placeholder": "Username"})
    name = StringField(validators=[InputRequired(), Length(min=2,max=50)], render_kw={"placeholder": "Name"})
    email = StringField(validators=[InputRequired(), Email(message="Invalid email response"), Length(max=50)], render_kw={"placeholder": "Email"})
    password = PasswordField(validators=[InputRequired(), Length(min=8, max=80)], render_kw={"placeholder": "Password"})
    submit = SubmitField('Create account')
    # rememberMe = BooleanField('Remember Me')

    def validate_username(self, username):
        exist = User.query.filter_by(username=username.data).first()
        if exist:
            raise ValidationError("Username already exists. Please enter another username.")


class LoginForm(FlaskForm):
    username = StringField(validators=[InputRequired(), Length(min=4,max=15)], render_kw={"placeholder": "Username"})
    password = PasswordField(validators=[InputRequired(), Length(min=8, max=80)], render_kw={"placeholder": "Password"})
    submit = SubmitField('Sign in')
    # rememberMe = BooleanField('Remember Me')

cart = []

class MinMaxForm(FlaskForm):
    min = IntegerField(render_kw={"placeholder": "Min"})
    max = IntegerField(render_kw={"placeholder": "Max"})
    search = SubmitField('Search')


# This is the home page (aka the products page)
@app.route("/", methods = ['GET', 'POST'])
def index():
    if request.method == 'POST': 
        if request.form.get('item') is None:
            content_type = request.headers.get('Content-Type')
            if content_type == 'application/json':
                data = request.json
                print('json is ', data)
                # cart.append(item)
        else:
            item = request.form.get('item')
            cart.append(item)


    allProducts = Product.query.all()
    listOfAllProductDics = []
    for i in allProducts:
        temp = {
            'name':i.name,
            'description':i.description,
            'price':i.price,
            'picture':i.picture,
            'brand':i.brand,
            'category':i.category,
            'stock count':i.stock_count
        }
        listOfAllProductDics.append(temp)
        session['cart items'] = []


    # listOfAllProductDics looks like this when outputted
    #[{'name': 'iPhone 13 Pro', 'description': 'The newest iPhone right now!', 'price': 1199.99, 'picture': 'default.jpg', 'brand': 'Apple', 'category': 'Electronics', 'stock count': 5}, 
    # {'name': 'MacBook Pro 2021', 'description': 'The newest MacBook Pro right now!', 'price': 1999.99, 'picture': 'default.jpg', 'brand': 'Apple', 'category': 'Electronics', 'stock count': 5}, 
    # {'name': 'Wilson Basketball 2021', 'description': 'The new NBA basketball!', 'price': 39.99, 'picture': 'default.jpg', 'brand': 'Wilson', 'category': 'Sports', 'stock count': 5}, 
    # {'name': 'Adidas Comfort Slides', 'description': 'Adidas comfort slides for your feet!', 'price': 34.99, 'picture': 'default.jpg', 'brand': 'Adidas', 'category': 'Clothes', 'stock count': 5}, 
    # {'name': 'Cracking the Coding Interview', 'description': 'The best book to prepare for technical interviews!', 'price': 39.99, 'picture': 'default.jpg', 'brand': 'Gayle Laakmann McDowell', 'category': 'Books', 'stock count': 5}]
    return render_template('home.html', show_navbar=True, signed_in=False, products=listOfAllProductDics, user_is_logged_in=user_is_logged_in)


@app.route("/login", methods=['POST', 'GET'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user:
            if bcrypt.check_password_hash(user.password, form.password.data):
                session['user'] = user.name
                user_is_logged_in = True
                login_user(user)
                return redirect(url_for('index'))

    # POST request - Handle form data from client
    # if request.method == "POST":
        # if form.validate_on_submit():
        #     return '<h1>' + form.username.data + ' '

        # # print("Post executed")
        # Username = request.form["username"]
        # Password = request.form["password"]
        # user = User.query.filter_by(username=Username).first()

        # if user is None or not user.check_password(password):
        #     return render_template("login.html")
        # return redirect(url_for('index'))

    # Otherwise, GET request - Return login page to client
    return render_template('login.html', form=form)


@app.route('/logout', methods=['GET', 'POST'])
@login_required
def logout():
    cart = []
    user_is_logged_in = False 
    logout_user()
    return redirect(url_for('login'))


@app.route("/register", methods=['POST', 'GET'])
def register():
    form = RegisterForm()
    if request.method == "POST":
        if form.validate_on_submit():
            hash = bcrypt.generate_password_hash(form.password.data)
            user = User(name=form.name.data, email=form.email.data, username=form.username.data, password=hash)
            db.session.add(user)
            db.session.commit()
            return redirect(url_for('login'))
    
    # Otherwise GET request - Return register page to client
    return render_template('register.html', form=form)


@app.route("/search/<product>", methods=['GET', 'POST'])
def searchProduct(product):
    param = ''.join(['%', product, '%'])
    results = db.session.execute('SELECT * FROM Product WHERE name LIKE :product_name', {'product_name': param}).fetchall()
    products = []
    # else:
    #     param = ''.join(['%', product, '%'])
    #     results = db.session.execute('SELECT * FROM Product WHERE name LIKE :product_name AND price > :min AND price < :max', {'product_name': param, 'min': min, 'max': max}).fetchall()
    #     products = []
            
    for result in results:
        # productInfoDic looks like this when outputted with the example of 'iPhone 13 Pro':
        # {
            #  'name': 'iPhone 13 Pro', 
            #  'price': 1199.99,
            #  'picture': 'default.jpg',
            #  'stock count': 5,
        # }

        auxReview = db.session.execute('SELECT AVG(rating) FROM review WHERE product_id = :product GROUP BY product_id', {'product': result[0]}).first()

        
        if auxReview is None:
            review = 0
        else:
            review = int(auxReview[0])

        # print(auxReview)

        productInfoDic = {
            'name':result[1],
            'price':result[3],
            'picture':result[4],
            'stock count':result[-1],
            'review': review
        }
        products.append(productInfoDic)
    
    # print(product)
    # print(products[0]['name'])

    # Retrieve database information corresponding to the searched product


    return render_template('search_results.html', show_navbar=True, products=products, product=product, user_is_logged_in=user_is_logged_in)



@app.route("/product/<product_name>", methods = ['GET', 'POST'])
def productInfo(product_name):
    # user = User.query.filter_by(username = Username).first()
    if request.method == 'GET':
        productName = product_name
        product = Product.query.filter_by(name = productName).first()
        productInfoDic = {
            'name':product.name,
            'description':product.description,
            'price':product.price,
            'picture':product.picture,
            'brand':product.brand,
            'category':product.category,
            'stock count':product.stock_count
        }
        productReview = Review.query.filter_by(product_id = product.id).all()
        listOfReviewsForProduct = []
        print(productReview)

        sum = 0

        for eachReview in productReview:
            temp = {
                'Review':eachReview.description,
                'User':eachReview.user.name,
                'Rating':eachReview.rating
            }
            sum += eachReview.rating
            listOfReviewsForProduct.append(temp)
        
        avg_rating = int(sum / len(productReview))

        productInfoDic['Reviews'] = listOfReviewsForProduct
        productInfoDic['avg_rating'] = avg_rating
        # productInfoDic looks like this when outputted with the example of 'iPhone 13 Pro':
        # {
            #  'name': 'iPhone 13 Pro', 
            #  'description': 'The newest iPhone right now!',
            #  'price': 1199.99,
            #  'picture': 'default.jpg',
            #  'brand': 'Apple', 
            #  'category': 'Electronics',
            #  'stock count': 5,
            #  'Reviews': [{'Review': 'This phone is absolutely amazing!', 'Rating': 5}, {'Review': 'This phone sucks!', 'Rating': 1}]
        # }

        return render_template('product_details.html', show_navbar=True, product_info=productInfoDic, user_is_logged_in=user_is_logged_in)
    else:
        print("do something")
        # DISREGARD ----------------------------------------------------------------------------------------------------------------------------------------------------------------------
        # This is the hypothetical POST method to add to cart
        # Date is something I assume can be pulled from the front end directly, and shipping fee as well as address is something that can be calculated/added in the 'checkout' app route
        # Adding something to cart
        # user = User.query.filter_by(username = Username).first()
        # productName = product_name
        # p = Product.query.filter_by(name = productName).first()
        # newOrder = Order(user_id = user.id, address_id = 0, date = '', subtotal = 0, tax = 0, shipping_fee = 0)
        # o = Order.query.filter_by(id=newOrder.id).first()
        # c = quantityOfProduct
        # newProductAddition = OrderDetail(order = o, product = p, count = c)
        # db.session.add(newOrder)
        # db.session.add(newProductAddition)
        # db.session.commit()
        # Order.query.filter_by(newOrder.id).update({'subtotal': (Order.subtotal + p.price)})
        # Order.query.filter_by(newOrder.id).update({'tax': (Order.subtotal*0.1)})
        # DISREGARD -------------------------------------------------------------------------------------------------------------------------------------------------------------------
        cart.append(product_name)

# Not sure whether to add a username argument for this app route or if username will be a variable you can call throughout the program with the use of Flask Login

@app.route("/cart", methods = ['POST', 'GET'])
def shoppingCart():
    # user = User.query.filter_by(username = session['user']).first()
    # newOrder = Order(user_id = user.id, address_id = 0, date = '', subtotal = 0, tax = 0, shipping_fee = 0)
    # db.session.add(newOrder)
    # o = Order.query.filter_by(id=newOrder.id).first()
    # c = 1
    cart_items = []

    for cart_item in cart:
        item = Product.query.filter_by(name = cart_item).first()
        cart_items.append(item)

    subtotal = 0
    for cart_item in cart_items:
        subtotal += cart_item.price

    shipping = 0
    total = subtotal + shipping
    #     newProductAddition = OrderDetail(order = o, product = p, count = c)
    #     db.session.add(newProductAddition)
    # db.session.commit()
    # Order.query.filter_by(newOrder.id).update({'subtotal': (Order.subtotal + p.price)})
    # Order.query.filter_by(newOrder.id).update({'tax': (Order.subtotal*0.1)})

    
    # POST request - Handle change in quantity removing an item from the cart
    if request.method == "POST":
        print('Change in quantity or removing an item from the cart')
        action = request.form.get('action').split(" ")
        if action[0] == 'remove':
            item_to_remove = " ".join(action[1:])
            print(item_to_remove)
            # remove product from cart_items
            cart.remove(item_to_remove)
            cart_items=[]
            for cart_item in cart:
                item = Product.query.filter_by(name=cart_item).first()
                cart_items.append(item)
            return render_template("cart.html", show_navbar=True, cart_items=cart_items, subtotal=subtotal, total=total, user_is_logged_in=user_is_logged_in)
        elif action[0] == 'add':
            pass
    # GET request - return cart page to the client
    # lebronUsername = 'ljames'
    

    # user = User.query.filter_by(username = Username).first()
    # orderForUser = Order.query.filter_by(user_id = user.id).first()

    # orderDetailsForUser = OrderDetail.query.filter_by(order_id = orderForUser.id).all()

    # orderProductsForUserList = []
    # for orderProduct in orderDetailsForUser:
    #     orderProductsForUserList.append({"Product":orderProduct.product.name, "Count":orderProduct.count, "Price":orderProduct.product.price, "Image":orderProduct.product.picture})

    # orderForUserDic = {}
    # orderForUserDic['Name'] = user.name
    # orderForUserDic['Products'] = orderProductsForUserList
    # orderForUserDic['Subtotal'] = orderForUser.subtotal
    
    # orderForUserDic looks like this when outputted with 'ljames' username as an example
    # {
        # 'Name': 'Lebron James', 
        # 'Products': [{'Product': 'Wilson Basketball 2021', 'Count': 1, 'Price': 39.99, 'Image': 'default.jpg'}, {'Product': 'Adidas Comfort Slides', 'Count': 1, 'Price': 34.99, 'Image': 'default.jpg'}], 
        # 'Subtotal': 74.98
    # }


    # Using session list ----------------------------------------------------------------------------------------------------------------------------------------------
    # subtotal = 0
    # user = User.query.filter_by(username = session['user']).first()
    # orderProductsForUserList = []
    # for orderProduct in session['cart_items']:
    #     p = Product.query.filter_by(name = orderProduct).first()
    #     orderProductsForUserList.append({"Product":p.product.name, "Count":p.count, "Price":p.product.price, "Image":p.product.picture})
    #     subtotal += p.product.price

    # orderForUserDic = {}
    # orderForUserDic['Name'] = user.name
    # orderForUserDic['Products'] = orderProductsForUserList
    # orderForUserDic['Subtotal'] = subtotal

    # Adding to the database for data storing purposes

    # shippingFee = 0 
    # newOrder = Order(user_id = user.id, address_id = 0, date = datetime.now(), subtotal = subtotal, tax = subtotal*0.1, shipping_fee = shippingFee)
    # db.session.add(newOrder)
    # o = Order.query.filter_by(id=newOrder.id).first()
    # c = 1
    # for i in session['cart_items']:
    #     p = Product.query.filter_by(name = i).first()
    #     newProductAddition = OrderDetail(order = o, product = p, count = c)
    #     db.session.add(newProductAddition)
    # db.session.commit()

    # Using session list ----------------------------------------------------------------------------------------------------------------------------------------------

    return render_template("cart.html", show_navbar=True, cart_items=cart_items, subtotal=subtotal, total=total, user_is_logged_in=user_is_logged_in)


@app.route("/checkout", methods=['POST', 'GET'])
def checkout():
    # POST request - Handle form data from the client
    if request.method == "POST":
        print('User submitted the checkout form')\

        card_name = request.form.get('card_name')
        card_num = request.form.get('card_num')
        card_exp_date = request.form.get('card_exp')
        card_cvc = request.form.get('card_cvc')

        first_name = request.form.get('first_name')
        last_name = request.form.get('last_name')
        address = request.form.get('address')
        city = request.form.get('city')
        state = request.form.get('state')
        zip_code = request.form.get('zip_code')

        card_data = {
            'number': str(card_num),
            'exp_month': int(card_exp_date[0:2]),
            'exp_year': int(card_exp_date[3:5]),
            'cvc': str(card_cvc)
        }

        amount = 100
        
        try:
            token = generate_card_token(card_data)
            paid = create_payment_charge(token, amount)
            
            if paid:
                # render template for order confirmation
                print("render template for order confirmation")
                return render_template('order_confirmation.html', show_navbar=True)
            else:
                # payment was for some reason unsuccessful
                print("payment was for some reason unsuccessful")
        except stripe.error.CardError as e:
            # issue with processing the card inputs (i.e. invalid card number, invalid exp_month/exp_year, invalid cvc)
            print(f"ERROR: {e.user_message}")
        
    # GET request - return checkout page to client

    # user = User.query.filter_by(username = Username).first()
    # orderForUser = Order.query.filter_by(user_id = user.id).first()

    # orderDetailsForUser = OrderDetail.query.filter_by(order_id = orderForUser.id).all()

    # orderProductsForUserList = []
    # for orderProduct in orderDetailsForUser:
    #     orderProductsForUserList.append({"Product":orderProduct.product.name, "Count":orderProduct.count, "Price":orderProduct.product.price, "Image":orderProduct.product.picture})

    # orderForUserDic = {}
    # orderForUserDic['Name'] = user.name
    # orderForUserDic['Products'] = orderProductsForUserList
    # orderForUserDic['Subtotal'] = orderForUser.subtotal
    # orderForUserDic['Tax'] = orderForUser.tax
    # orderForUserDic['Shipping Fee'] = orderForUser.shipping_fee
    # orderForUserDic['Total'] = orderForUserDic['Subtotal'] + orderForUserDic['Tax'] + orderForUserDic['Shipping Fee']

    # orderForUserDic looks like this when outputted with 'ljames' username as an example
    # {
        # 'Name': 'Lebron James', 
        # 'Products': [{'Product': 'Wilson Basketball 2021', 'Count': 1, 'Price': 39.99, 'Image': 'default.jpg'}, {'Product': 'Adidas Comfort Slides', 'Count': 1, 'Price': 34.99, 'Image': 'default.jpg'}], 
        # 'Subtotal': 74.98, 
        # 'Tax': 7.49, 
        # 'Shipping Fee': 5.0,
        # 'Total': 87.47
    # }

    cart_items = []

    for cart_item in cart:
        item = Product.query.filter_by(name = cart_item).first()
        cart_items.append(item)

    subtotal = 0
    for cart_item in cart_items:
        subtotal += cart_item.price

    shipping = 0
    tax = round(0.1 * (subtotal + shipping), 2)
    total = tax + subtotal + shipping

    return render_template("checkout.html", show_navbar=True, cart_items=cart_items, subtotal=subtotal, tax=tax, total=total, user_is_logged_in=user_is_logged_in)


@app.route("/order_confirmation", methods=['GET'])
def orderConfirmation():
    print("Order confirmation")

    return render_template("order_confirmation.html", show_navbar=True)


def generate_card_token(card_data):
    data = stripe.Token.create(card=card_data)
    card_token = data['id']

    return card_token

def create_payment_charge(token, amount):
    payment = stripe.Charge.create(
                amount=int(amount * 100),
                currency='usd',
                source=token,
                description='Test charge'
            )

    payment_check = payment['paid']

    return payment_check

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000)
