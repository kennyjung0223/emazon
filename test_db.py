from db import db, User, Order, Product, OrderDetail, Review, Address
import json

users = User.query.all()
products = Product.query.all()
reviews = Review.query.all()
addresses = Address.query.all()
orders = Order.query.all()
order_details = OrderDetail.query.all()

print("------------------- USERS -------------------")
for user in users:
	print(user.id, user.name, user.username, user.password)
 
print("------------------- PRODUCTS -------------------")
for product in products:
	print(product.id, product.name, product.description, product.price, product.picture, product.brand, product.category, product.stock_count)
 
print("------------------- REVIEWS -------------------")
for review in reviews:
	print(review.id, review.product_id, review.product.name, review.description, review.rating)
 
print("------------------- ADDRESSES -------------------")
for address in addresses:
	print(address.id, address.street, address.city, address.postal_code, address.country)
 
print("------------------- ORDERS -------------------")
for order in orders:
    print(order.id, order.user_id, order.user.username, order.address_id, order.address.street, order.date, order.subtotal, order.tax, order.shipping_fee)
    
print("------------------- ORDER DETAILS -------------------")
for order_detail in order_details:
    print(order_detail.id, order_detail.order_id, order_detail.product.name, order_detail.count)

productName = 'iPhone 13 Pro'
product = Product.query.filter_by(name = productName).first()
print(product)
print(product.id, product.name, product.description, product.price, product.picture, product.brand, product.category, product.stock_count)

allProducts = Product.query.all()
listOfAllProductDics = []
for i in allProducts:
	print(i.id, i.name, i.description, i.price, i.picture, i.brand, i.category, i.stock_count)
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

listOfAllProductDicsJson = []
for i in range(len(allProducts)):
	print(listOfAllProductDics[i])
	listOfAllProductDicsJson.append(json.dumps(listOfAllProductDics[i]))

for i in range(len(allProducts)):
	print(listOfAllProductDicsJson[i])