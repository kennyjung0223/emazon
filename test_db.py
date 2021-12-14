from db import db, User, Order, Product, OrderDetail, Review, Address
# from app import stripe, generate_card_token, create_payment_charge
import json

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
	print(user.id, user.name, user.email, user.username, user.password)
 
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

print("\nSearching for one product (example: iPhone 13 Pro)-------------------------------------------")

productName = 'iPhone 13 Pro'
product = Product.query.filter_by(name = productName).first()
print(product)
# print(product.id, product.name, product.description, product.price, product.picture, product.brand, product.category, product.stock_count)

productInfoDic = {
	'name':product.name,
	'description':product.description,
	'price':product.price,
	'picture':product.picture,
	'brand':product.brand,
	'category':product.category,
	'stock count':product.stock_count
}
print(productInfoDic)
productInfoDicJson = json.dumps(productInfoDic)
print(productInfoDicJson)
print()
print("Product Name: " + productInfoDic['name'])
print("Description: " + productInfoDic['description'])
print("Price: " + str(productInfoDic['price']))
print("Image: " + productInfoDic['picture'])
print("Sold by: " + productInfoDic['brand'])
print("Category: " + productInfoDic['category'])
print("Available units: " + str(productInfoDic['stock count']))
productReview = Review.query.filter_by(product_id = product.id).all()
listOfReviewsForProduct = []
print(productReview)
for eachReview in productReview:
	temp = {
		'Review':eachReview.description,
		'Rating':eachReview.rating
	}
	listOfReviewsForProduct.append(temp)
print(listOfReviewsForProduct)
productInfoDic['Reviews'] = listOfReviewsForProduct
print("Reviews for "+ productInfoDic['name'] +": ")
for eachReview in productInfoDic['Reviews']:
	print("\tReview: " + eachReview['Review'])
	print("\tRating: " + str(eachReview['Rating']))
	print()
print(productInfoDic)
print(json.dumps(productInfoDic))

print("-------------------------------------------------------------\n\n\n")

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

print("\n\nJSON versions")

for i in range(len(allProducts)):
	print(listOfAllProductDicsJson[i])

print(listOfAllProductDics)

lebronUsername = 'ljames'
lebron = User.query.filter_by(username = lebronUsername).first()
print()
print("Name: " + lebron.name)
print("ID: " + str(lebron.id))

orderForLebron = Order.query.filter_by(user_id = lebron.id).first()
print(orderForLebron)
# print(orderForLebron.id, orderForLebron.user_id, orderForLebron.user.username, orderForLebron.address_id, orderForLebron.address.street, orderForLebron.date, orderForLebron.subtotal, orderForLebron.tax, orderForLebron.shipping_fee)

orderDetailsForLebron = OrderDetail.query.filter_by(order_id = orderForLebron.id).all()
print(orderDetailsForLebron)

orderProductsForLebronList = []
for orderProduct in orderDetailsForLebron:
	print("Product: " + orderProduct.product.name + " Count: " + str(orderProduct.count))
	orderProductsForLebronList.append({"Product":orderProduct.product.name, "Count":orderProduct.count, "Price":orderProduct.product.price, "Image":orderProduct.product.picture})

orderForLebronDic = {}
orderForLebronDic['Name'] = lebron.name
orderForLebronDic['Products'] = orderProductsForLebronList
orderForLebronDic['Subtotal'] = orderForLebron.subtotal
orderForLebronDic['Tax'] = orderForLebron.tax
orderForLebronDic['Shipping Fee'] = orderForLebron.shipping_fee
print("\n\n")
print(orderForLebronDic)
print()
print("Name: " + orderForLebronDic['Name'])
print("Products: ")
for eachProduct in orderForLebronDic['Products']:
	print("\t"+eachProduct['Product'])
	print("\tCount: "+ str(eachProduct['Count']))
	print("\tPrice: "+ str(eachProduct['Price']))
	print("\tImage: "+ str(eachProduct['Image']))
	print()
print("Subtotal: "+ str(orderForLebronDic['Subtotal']))
print("For adding to checkout-------------------------------------")
print("Tax: "+ str(orderForLebronDic['Tax']))
print("Shipping Fee: "+ str(orderForLebronDic['Shipping Fee']))

print("Total: " + str(orderForLebronDic['Subtotal'] + orderForLebronDic['Tax'] + orderForLebronDic['Shipping Fee']))
print("Address: \n\t"+ orderForLebron.address.street + "\n\t" + orderForLebron.address.city + " " + orderForLebron.address.postal_code)
print("payment information")
print(json.dumps(orderForLebronDic))

# print("TESTING STRIPE PAYMENT PROCESSING")
# card_number = "4242424242424242"
# exp_month = 12
# exp_year = 2021
# cvc = 314
# amount = 299.99

# card_data = {
# 	"number": str(card_number),
# 	"exp_month": int(exp_month),
# 	"exp_year": int(exp_year),
# 	"cvc": str(cvc)
# }

# try:
# 	token = generate_card_token(card_data)
# 	paid = create_payment_charge(token, amount)

# 	if paid:
# 		print("Payment was successful")
# 	else:
# 		print("Payment was unsuccessful")
# except stripe.error.CardError as e:
# 	print(f"ERROR: {e.user_message} ")