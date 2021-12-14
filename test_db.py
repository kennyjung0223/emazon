from db import db, User, Order, Product, OrderDetail, Review, Address

users = User.query.all()
products = Product.query.all()
reviews = Review.query.all()
addresses = Address.query.all()
orders = Order.query.all()
order_details = OrderDetail.query.all()

''' 
returns a list of tuples

i.e. iphones = [
	(1, 'iPhone 13 Pro', 'The newest iPhone right now!', 1199.99, 'default.jpg', 'Apple', 'Electronics', 5)
	(6, 'iPhone 13 Pro Max', 'The best iPhone right now!', 1399.99, 'default.jpg', 'Apple', 'Electronics', 5)
]
'''
iphones = db.session.execute('SELECT * FROM Product WHERE name LIKE :product_name', {'product_name': '%iPhone%'}).fetchall()


print("------------------- USERS -------------------")
for user in users:
	print(user.id, user.name, user.username, user.password)
 
print("------------------- PRODUCTS -------------------")
for product in products:
	print(product.id, product.name, product.description, product.price, product.picture, product.brand, product.category, product.stock_count)
 
print("------------------- REVIEWS -------------------")
for review in reviews:
	print(review.id, review.product_id, review.product.name, review.user_id, review.user.name, review.description, review.rating)
 
print("------------------- ADDRESSES -------------------")
for address in addresses:
	print(address.id, address.street, address.city, address.postal_code, address.country)
 
print("------------------- ORDERS -------------------")
for order in orders:
    print(order.id, order.user_id, order.user.username, order.address_id, order.address.street, order.date, order.subtotal, order.tax, order.shipping_fee)
    
print("------------------- ORDER DETAILS -------------------")
for order_detail in order_details:
    print(order_detail.id, order_detail.order_id, order_detail.product.name, order_detail.count)

print("------------------- SEARCHING FOR iPHONES -------------------")
for iphone in iphones:
    print(iphone)
