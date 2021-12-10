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

# productName = 'iPhone 13 Pro'
# product = Product.query.filter_by(name = productName).first()
# print(product)
# print(product.id, product.name, product.description, product.price, product.picture, product.brand, product.category, product.stock_count)
# productInfoDic = {
# 	'name':product.name,
# 	'description':product.description,
# 	'price':product.price,
# 	'picture':product.picture,
# 	'brand':product.brand,
# 	'category':product.category,
# 	'stock count':product.stock_count
# }
# print(productInfoDic)
# productInfoDicJson = json.dumps(productInfoDic)
# print(productInfoDicJson)

# print("-------------------------------------------------------------\n\n\n")

# allProducts = Product.query.all()
# listOfAllProductDics = []
# for i in allProducts:
# 	print(i.id, i.name, i.description, i.price, i.picture, i.brand, i.category, i.stock_count)
# 	temp = {
# 		'name':i.name,
# 		'description':i.description,
# 		'price':i.price,
# 		'picture':i.picture,
# 		'brand':i.brand,
# 		'category':i.category,
# 		'stock count':i.stock_count
# 	}
# 	listOfAllProductDics.append(temp)

# listOfAllProductDicsJson = []
# for i in range(len(allProducts)):
# 	print(listOfAllProductDics[i])
# 	listOfAllProductDicsJson.append(json.dumps(listOfAllProductDics[i]))

# print("\n\nJSON versions")

# for i in range(len(allProducts)):
# 	print(listOfAllProductDicsJson[i])

lebronUsername = 'ljames'
lebron = User.query.filter_by(username = lebronUsername).first()
print("Name: " + lebron.name)
print("ID: " + str(lebron.id))

orderForLebron = Order.query.filter_by(user_id = lebron.id).first()
print(orderForLebron)
# print(orderForLebron.id, orderForLebron.user_id, orderForLebron.user.username, orderForLebron.address_id, orderForLebron.address.street, orderForLebron.date, orderForLebron.subtotal, orderForLebron.tax, orderForLebron.shipping_fee)

orderDetailsForLebron = OrderDetail.query.filter_by(order_id = orderForLebron.id).all()
print(orderDetailsForLebron)
for orderProducts in orderDetailsForLebron:
	print("Product: " + orderProducts.product.name + " Count: " + str(order_detail.count))