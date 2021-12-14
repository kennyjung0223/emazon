from db import db, User, Order, Product, OrderDetail, Review, Address
from datetime import datetime

### add users ###

users = [
    ("Jeff Bezos", "jbezos@email.com", "jbezos", "helloworld123"),
    ("Lebron James", "ljames@email.com", "ljames", "helloworld123"),
    ("Ammon Hepworth", "ahepworth@email.com", "ahepworth", "helloworld123")
]

for user in users:
    name = user[0]
    email = user[1]
    username = user[2]
    password = user[3]
    
    u = User(name=name, email=email, username=username, password=password)
    db.session.add(u)

### add products ###

products = [
    ("iPhone 13 Pro", "The newest iPhone right now!", 1199.99, "default.jpg", "Apple", "Electronics", 5),
    ("MacBook Pro 2021", "The newest MacBook Pro right now!", 1999.99, "default.jpg", "Apple", "Electronics", 5),
    ("Wilson Basketball 2021", "The new NBA basketball!", 39.99, "default.jpg", "Wilson", "Sports", 5),
    ("Adidas Comfort Slides", "Adidas comfort slides for your feet!", 34.99, "default.jpg", "Adidas", "Clothes", 5),
    ("Cracking the Coding Interview", "The best book to prepare for technical interviews!", 39.99, "default.jpg", "Gayle Laakmann McDowell", "Books", 5),
    ("iPhone 13 Pro Max", "The best iPhone right now!", 1399.99, "default.jpg", "Apple", "Electronics", 5),
]

for product in products:
    name = product[0]
    description = product[1]
    price = product[2]
    picture = product[3]
    brand = product[4]
    category = product[5]
    stock_count = product[6]
    
    p = Product(name=name, description=description, price=price, picture=picture, brand=brand, category=category, stock_count=stock_count)
    db.session.add(p)

### add reviews ###

reviews = [
    (1, 1, "This phone is absolutely amazing!", 5),
    (1, 2, "This phone sucks!", 1),
    (2, 1, "This laptop is pretty good.", 4),
    (3, 2, "This basketball sucks, it is hard to get adjusted to.", 1),
    (4, 2, "These slides are so comfortable!", 5),
    (5, 3, "This book helped me land offers at Facebook, Google, Amazon, and Netflix!", 5)
]

for review in reviews:
    product_id = review[0]
    user_id = review[1]
    description = review[2]
    rating = review[3]
    
    p = Product.query.filter_by(id=product_id).first()
    u = User.query.filter_by(id=user_id).first()
    r = Review(
            # product_id=product_id,
            product=p,
            user=u,
            description=description,
            rating=rating
    )
    db.session.add(r)

### add addresses ###

addresses = [
    ("123 Amazon St", "Seattle, WA", "12345", "United States of America"),
    ("236 Lakers St", "Los Angeles, CA", "54321", "United States of America"),
    ("106 Full Stack St", "Merced, CA", "98765", "United States of America")
]

for address in addresses:
    street = address[0]
    city = address[1]
    postal_code = address[2]
    country = address[3]
    
    a = Address(street=street, city=city, postal_code=postal_code, country=country)
    db.session.add(a)

### add orders ###

orders = [
    (1, 1, datetime(2021, 12, 8), 3199.98, 319.99, 0),
    (2, 2, datetime(2021, 12, 9), 74.98, 7.49, 5),
    (3, 3, datetime(2021, 12, 10), 39.99, 3.99, 10)
]

for order in orders:
    user_id = order[0]
    address_id = order[1]
    date = order[2]
    subtotal = order[3]
    tax = order[4]
    shipping_fee = order[5]
    
    u = User.query.filter_by(id=user_id).first()
    a = Address.query.filter_by(id=address_id).first()
    o = Order(
            # user_id=user_id,
            user=u,
            # address_id=address_id,
            address=a,
            date=date,
            subtotal=subtotal,
            tax=tax,
            shipping_fee=shipping_fee
    )

order_details = [
    (1, 1, 1),
    (1, 2, 1),
    (2, 3, 1),
    (2, 4, 1),
    (3, 5, 1)
]

for order_detail in order_details:
    order_id = order_detail[0]
    product_id = order_detail[1]
    count = order_detail[2]
    
    o = Order.query.filter_by(id=order_id).first()
    p = Product.query.filter_by(id=product_id).first()
    od = OrderDetail(order=o, product=p, count=count)

db.session.commit()
