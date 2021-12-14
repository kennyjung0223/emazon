from os import linesep
from flask import Flask, render_template, request, url_for, redirect
from flask_cors import CORS
from wtforms.widgets.core import Input
from db import app
from db import *
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import InputRequired, Length, ValidationError, Email, email_validator
from flask_bcrypt import Bcrypt
from flask_login import login_manager, login_user, LoginManager, login_required, logout_user, current_user
import stripe


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
    return User.query.get(int(user_id))


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

# This is the home page (aka the products page)
@app.route("/")
def index():
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

    # listOfAllProductDics looks like this when outputted
    #[{'name': 'iPhone 13 Pro', 'description': 'The newest iPhone right now!', 'price': 1199.99, 'picture': 'default.jpg', 'brand': 'Apple', 'category': 'Electronics', 'stock count': 5}, 
    # {'name': 'MacBook Pro 2021', 'description': 'The newest MacBook Pro right now!', 'price': 1999.99, 'picture': 'default.jpg', 'brand': 'Apple', 'category': 'Electronics', 'stock count': 5}, 
    # {'name': 'Wilson Basketball 2021', 'description': 'The new NBA basketball!', 'price': 39.99, 'picture': 'default.jpg', 'brand': 'Wilson', 'category': 'Sports', 'stock count': 5}, 
    # {'name': 'Adidas Comfort Slides', 'description': 'Adidas comfort slides for your feet!', 'price': 34.99, 'picture': 'default.jpg', 'brand': 'Adidas', 'category': 'Clothes', 'stock count': 5}, 
    # {'name': 'Cracking the Coding Interview', 'description': 'The best book to prepare for technical interviews!', 'price': 39.99, 'picture': 'default.jpg', 'brand': 'Gayle Laakmann McDowell', 'category': 'Books', 'stock count': 5}]
    return render_template('home.html', show_navbar=True, signed_in=False)


@app.route("/login", methods=['POST', 'GET'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user:
            if bcrypt.check_password_hash(user.password, form.password.data):
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
    logout_user()
    return redirect(url_for('login'))



@app.route("/register", methods=['POST', 'GET'])
def register():
    form = RegisterForm()
    if form.validate_on_submit():
        hash = bcrypt.generate_password_hash(form.password.data)
        user = User(name=form.name.data, email=form.email.data, username=form.username.data, password=hash)
        db.session.add(user)
        db.session.commit()
        return redirect(url_for('login'))

    # POST request - Handle form data from client
    # if request.method == "POST":
    #     print('Register')
    #     Name = name
    #     Username = username
    #     Password = password

    #     newUser = User(name = Name, username = Username, password = Password)
    #     db.session.add(newUser)
    # db.session.commit()
    
    # Otherwise GET request - Return register page to client
    return render_template('register.html', form=form)


@app.route("/search/<product>", methods=['GET'])
def searchProduct(product):
    param = ''.join(['%', product, '%'])
    results = db.session.execute('SELECT * FROM Product WHERE name LIKE :product_name', {'product_name': param}).fetchall()
    products = []
    
    for result in results:
        # productInfoDic looks like this when outputted with the example of 'iPhone 13 Pro':
        # {
            #  'name': 'iPhone 13 Pro', 
            #  'price': 1199.99,
            #  'picture': 'default.jpg',
            #  'stock count': 5,
        # }
        productInfoDic = {
            'name':result[1],
            'price':result[3],
            'picture':result[4],
            'stock count':result[-1]
        }
        products.append(productInfoDic)
    
    print(products)

    # Retrieve database information corresponding to the searched product

    return render_template('search_results.html', show_navbar=True, search_phrase=product, search_results=products)


@app.route("/product/<product_name>", methods=['GET'])
def productInfo(product_name):
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
            'Rating':eachReview.rating
        }
        sum += eachReview.rating
        listOfReviewsForProduct.append(temp)

    avg_rating = int(sum / len(productReview))

    productInfoDic['reviews'] = listOfReviewsForProduct
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
    return render_template('product_details.html', show_navbar=True, product_info=productInfoDic)

  
# Not sure whether to add a username argument for this app route or if username will be a variable you can call throughout the program with the use of Flask Logun
@app.route("/cart", methods = ['POST', 'GET'])
def shoppingCart():
    # POST request - Handle change in quantity removing an item from the cart
    if request.method == "POST":
        print('Change in quantity or removing an item from the cart')
    # GET request - return cart page to the client
    # lebronUsername = 'ljames'
    user = User.query.filter_by(username = Username).first()
    orderForUser = Order.query.filter_by(user_id = user.id).first()

    orderDetailsForUser = OrderDetail.query.filter_by(order_id = orderForUser.id).all()

    orderProductsForUserList = []
    for orderProduct in orderDetailsForUser:
        orderProductsForUserList.append({"Product":orderProduct.product.name, "Count":orderProduct.count, "Price":orderProduct.product.price, "Image":orderProduct.product.picture})

    orderForUserDic = {}
    orderForUserDic['Name'] = user.name
    orderForUserDic['Products'] = orderProductsForUserList
    orderForUserDic['Subtotal'] = orderForUser.subtotal
    # orderForUserDic looks like this when outputted with 'ljames' username as an example
    # {
        # 'Name': 'Lebron James', 
        # 'Products': [{'Product': 'Wilson Basketball 2021', 'Count': 1, 'Price': 39.99, 'Image': 'default.jpg'}, {'Product': 'Adidas Comfort Slides', 'Count': 1, 'Price': 34.99, 'Image': 'default.jpg'}], 
        # 'Subtotal': 74.98
    # }
    return render_template("cart.html", show_navbar=True)


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
        
        try:
            token = generate_card_token(card_data)
            paid = create_payment_charge(token, amount)
            
            if paid:
                # render template for order confirmation
                print("render template for order confirmation")
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
    return render_template("checkout.html", show_navbar=True)


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
    app.run()
