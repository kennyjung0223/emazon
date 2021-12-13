from flask import Flask, render_template, request, url_for, redirect

app = Flask(__name__)

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


@app.route("/login", methods = ['POST', 'GET'])
def login():
    # POST request - Handle form data from client
    if request.method == "POST":
        print('Login')

    # Otherwise, GET request - Return login page to client
    return render_template('login.html')


@app.route("/register", methods = ['POST', 'GET'])
def register():
    # POST request - Handle form data from client
    if request.method == "POST":
        print('Register')
    
    # Otherwise GET request - Return register page to client
    return render_template('register.html')


@app.route("/search/<product>", methods = ['GET'])
def searchProduct(product):
    productName = product
    product = Product.query.filter_by(name = productName).first()
    productInfoDic = {
        'name':product.name,
        'price':product.price,
        'picture':product.picture,
        'stock count':product.stock_count
    }
    # productInfoDic looks like this when outputted with the example of 'iPhone 13 Pro':
    # {
        #  'name': 'iPhone 13 Pro', 
        #  'price': 1199.99,
        #  'picture': 'default.jpg',
        #  'stock count': 5,
    # }

    # Retrieve database information corresponding to the searched product

    return render_template('search_results.html', show_navbar=True)


@app.route("/product/<product_name>", methods = ['GET'])
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
    for eachReview in productReview:
        temp = {
            'Review':eachReview.description,
            'Rating':eachReview.rating
        }
        listOfReviewsForProduct.append(temp)
    productInfoDic['Reviews'] = listOfReviewsForProduct
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
        
    return render_template('product_details.html', show_navbar=True)
    

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

@app.route("/checkout", methods = ['POST', 'GET'])
def checkout():
    # POST request - Handle form data from the client
    if request.method == "POST":
        print('User submitted the checkout form')
    
    # GET request - return checkout page to client
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
    orderForUserDic['Tax'] = orderForUser.tax
    orderForUserDic['Shipping Fee'] = orderForUser.shipping_fee
    orderForUserDic['Total'] = orderForUserDic['Subtotal'] + orderForUserDic['Tax'] + orderForUserDic['Shipping Fee']
    # orderForUserDic looks like this when outputted with 'ljames' username as an example
    # {
        # 'Name': 'Lebron James', 
        # 'Products': [{'Product': 'Wilson Basketball 2021', 'Count': 1, 'Price': 39.99, 'Image': 'default.jpg'}, {'Product': 'Adidas Comfort Slides', 'Count': 1, 'Price': 34.99, 'Image': 'default.jpg'}], 
        # 'Subtotal': 74.98, 
        # 'Tax': 7.49, 
        # 'Shipping Fee': 5.0,
        # 'Total': 87.47
    # }
    return render_template("checkout.html")

@app.route("/order_confirmation", methods = ['GET'])
def orderConfirmation():
    print("Order confirmation")
    
    return render_template("order_confirmation.html", show_navbar=True)


if __name__ == "__main__":
    app.run()