# from app import db

from flask import Flask
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///data.sqlite"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
db = SQLAlchemy(app)

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)
    username = db.Column(db.String(15), unique=True, nullable=False)
    password = db.Column(db.String, nullable=False)
    
class Order(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    address_id = db.Column(db.Integer, db.ForeignKey('address.id'), nullable=False)
    # date should be db.DateTime but for testing purposes, it is db.String
    date = db.Column(db.String, nullable=False)
    subtotal = db.Column(db.Float(precision=2), nullable=False)
    tax = db.Column(db.Float(precision=2), nullable=False)
    shipping_fee = db.Column(db.Float(precision=2), nullable=False)
    
    user = db.relationship('User', backref=db.backref('users', lazy=True))
    address = db.relationship('Address', backref=db.backref('addresses', lazy=True))
    products = db.relationship('OrderDetail', back_populates='order')
    
class Product(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)
    description = db.Column(db.String, nullable=False)
    price = db.Column(db.Float(precision=2), nullable=False)
    picture = db.Column(db.String, nullable=False)
    brand = db.Column(db.String, nullable=False)
    category = db.Column(db.String, nullable=False)
    stock_count = db.Column(db.Integer, nullable=False)
    
    orders = db.relationship('OrderDetail', back_populates='product')
    
class OrderDetail(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    order_id = db.Column(db.Integer, db.ForeignKey('order.id'), nullable=False)
    product_id = db.Column(db.Integer, db.ForeignKey('product.id'), nullable=False)
    count = db.Column(db.Integer, nullable=False)
    
    order = db.relationship('Order', back_populates='products')
    product = db.relationship('Product', back_populates='orders')

class Review(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    product_id = db.Column(db.Integer, db.ForeignKey('product.id'), nullable=False)
    description = db.Column(db.String, nullable=False)
    rating = db.Column(db.Integer, nullable=False)
    
    product = db.relationship('Product', backref=db.backref('products', lazy=True))
    
class Address(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    street = db.Column(db.String, nullable=False)
    city = db.Column(db.String, nullable=False)
    postal_code = db.Column(db.String, nullable=False)
    country = db.Column(db.String, nullable=False)