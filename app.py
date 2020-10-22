"""Flask Login Example and instagram fallowing find"""

from flask import Flask, url_for, render_template, flash, request, redirect, session, logging, request,jsonify,current_app

import os

from flask import Flask
from sqlalchemy import create_engine,MetaData
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__, instance_relative_config=False)
app.config.from_object('config.Config')
db = SQLAlchemy(app)
# engine = create_engine('mssql+pymssql://sa:Maqsood_9211@hostname:1433/TestDB')

# m = MetaData()

class Buyer(db.Model):
    # table
    __tablename__ = 'buyer'

    # Columns
    user_id = db.Column('user_id', db.Integer, primary_key=True, autoincrement=True,unique=True)
    username = db.Column('username', db.String(100))
    password = db.Column('password', db.String(500))
    email = db.Column('email', db.String(200), unique=True)

    def __init__(self, username, password, email):
        self.username = username
        self.password = password
        self.email = email

    def create(self):
        db.session.add(self)
        db.session.commit()

    def to_json(self):
        return {
            'user_id':	self.user_id,
            'username': self.username,
            'password':	self.password,
            'email': self.email
        }


class Product(db.Model):
    __tablename__ = 'product'
    productId = db.Column('productId', db.Integer,
                          primary_key=True, autoincrement=True,unique=True)
    product_name = db.Column('productName', db.String(100), nullable=False)
    product_details = db.Column(
        'productDetails', db.String(100), nullable=True)

    def __init__(self, product_name, product_details=None):
        self.product_name = product_name
        self.product_details = product_details

    def create(self):
        db.session.add(self)
        db.session.commit()

    def to_json(self):
        return {
            
                'productId'			: self.productId,
                'product_name'		: self.product_name,
                'product_details'	: self.product_details
            
        }

class Seller(db.Model):
    __tablename__ = 'seller'
    user_id = db.Column('user_id', db.Integer, primary_key=True, autoincrement=True, unique=True)
    username = db.Column('username', db.String(45), nullable=False)
    password = db.Column('password', db.String(15), nullable=False)
    email = db.Column('email', db.String(45), unique=True, nullable=False)
    product = db.Column('product', db.ForeignKey("product.productId"), nullable=True)

    def __init__(self, username, password, email, product=None):
        self.username = username
        self.password = password
        self.email = email
        self.product = product

    def update_product(self,product):
        self.product = product


    def create(self):
        db.session.add(self)
        db.session.commit()

    def to_json(self):
        if self.product:
            return {
                'user_id'   :	self.user_id,
                'username' 	:	self.username,
                'password' 	:	self.password,
                'email' 	:	self.email,
                'product' 	:	self.product
            }
        else:
            return {
                    
                    'user_id':	self.user_id,
                    'username' 	:	self.username,
                    'password' 	:	self.password,
                    'email' 	:	self.email,
                }




class RFQ(db.Model):
    __tablename__ = 'rfq'
    rfq_id = db.Column('rfqId', db.Integer, primary_key=True, autoincrement=True,unique=True)
    buyer = db.Column(' requesteduser_id', db.Integer, db.ForeignKey("buyer.user_id"), nullable=False)
    product_name = db.Column('productName',db.String(45),nullable=False)
    quantity = db.Column('quantity', db.Integer, nullable=False)
    usage = db.Column('usage', db.String(45), nullable=False)
    product_type = db.Column('productType', db.String(45), nullable=False)
    voltage = db.Column('voltage', db.Integer, nullable=False)
    capacity = db.Column('capacity', db.Integer, nullable=False)

    def __init__(self, buyer,product_name, quantity, usage, capacity, product_type, voltage):
        self.buyer = buyer
        # self.product_id = product_id
        self.product_name = product_name
        self.quantity = quantity
        self.usage = usage
        self.capacity = capacity
        self.product_type = product_type
        self.voltage = voltage

    def create(self):
        db.session.add(self)
        db.session.commit()

    def to_json(self):
        return {
            'rfq_id' 		: self.rfq_id,
            'buyer' 		: self.buyer,
            'product' 		: self.product_name,
            'quantity' 		: self.quantity,
            'usage' 		: self.usage,
            'product_type' 	: self.product_type,
            'voltage' 		: self.voltage,
            'capacity' 		: self.capacity
        }


class Quotation(db.Model):
    __tablename__ = 'quotation'
    quotation_id = db.Column('quotationId', db.Integer,
                             primary_key=True, autoincrement=True,unique=True)
    buyer = db.Column(' buyer_id', db.Integer, db.ForeignKey(
        "buyer.user_id"), nullable=False)
    seller = db.Column('seller_id', db.Integer, db.ForeignKey(
        "seller.user_id"), nullable=False)
    product = db.Column('product_id', db.ForeignKey(
        "product.productId"), nullable=False)
    quantity = db.Column('quantity', db.Integer, nullable=False)
    capacity = db.Column('capacity', db.Integer, nullable=False)
    usage = db.Column('usage', db.String(45), nullable=False)
    product_type = db.Column('productType', db.String(45), nullable=False)
    voltage = db.Column('voltage', db.Integer, nullable=False)
    weight = db.Column('weight', db.Integer, nullable=False)
    color = db.Column('color', db.String(45), nullable=False)
    item = db.Column('item', db.String(45), nullable=False)
    cycle_life = db.Column('cycleLife', db.Integer, nullable=False)
    price = db.Column('price', db.Float, nullable=False)
    lead_time = db.Column('leadTime', db.Integer, nullable=False)
    battery_type = db.Column('batteryType', db.String(45), nullable=False)
    nominal_capacity = db.Column('nominalCapacity', db.Integer, nullable=False)
    nominal_voltage = db.Column('nominalVoltage', db.Integer, nullable=False)
    warranty = db.Column('warrenty', db.Integer, nullable=False)
    description = db.Column('description', db.String(200), nullable=False)
    customization = db.Column('custommzation', db.Boolean, default=False)
    customized_logo = db.Column('customzedLogo', db.Boolean, default=False)
    certificates = db.Column('certificates', db.String(45), nullable=False)

    def __init__(
            self,
            buyer,
            seller,
            product,
            quantity,
            capacity,
            usage,
            product_type,
            voltage,
            weight,
            color,
            item,
            cycle_life,
            price,
            lead_time,
            battery_type,
            nominal_voltage,
            nominal_capacity,
            warranty,
            description,
            customized_logo,
            customization,
            certificates
    ):

        self.buyer = buyer
        self.seller = seller
        self.product = product
        self.quantity = quantity
        self.capacity = capacity
        self.usage = usage
        self.product_type = product_type
        self.voltage = voltage
        self.weight = weight
        self.color = color
        self.item = item
        self.cycle_life = cycle_life
        self.price = price
        self.lead_time = lead_time
        self.battery_type = battery_type
        self.nominal_capacity = nominal_capacity
        self.nominal_voltage = nominal_voltage
        self.warranty = warranty
        self.description = description
        self.customization = customization
        self.customized_logo = customized_logo
        self.certificates = certificates

    def create(self):
        db.session.add(self)
        db.session.commit()

    def to_json(self):
        return {
            'quotation_id' 		: self.quotation_id,
            'buyer' 			: self.buyer,
            'seller' 			: self.seller,
            'product' 			: self.product,
            'quantity' 			: self.quantity,
            'capacity' 			: self.capacity,
            'usage' 			: self.usage,
            'product_type' 		: self.product_type,
            'voltage' 			: self.voltage,
            'weight' 			: self.weight,
            'color'		 		: self.color,
            'item' 				: self.item,
            'cycle_life' 		: self.cycle_life,
            'price' 			: self.price,
            'lead_time' 		: self.lead_time,
            'battery_type' 		: self.battery_type,
            'nominal_capacity' 	: self.nominal_capacity,
            'nominal_voltage' 	: self.nominal_voltage,
            'warranty' 			: self.warranty,
            'description'       : self.description,
            'customization' 	: self.customization,
            'customized_logo' 	: self.customized_logo,
            'certificates' 		: self.certificates
        }

# m.create_all(engine)


@app.route('/', methods=['GET', 'POST'])
def home():

    # if requst is get then user needs a non logged in home page

    if not session.get('logged_in'):
        return render_template('index.html')

    # if logged in then

    else:
        user = str(session.get('user_id'))

        all_sellers = [str(x.to_json()['user_id'])+str(x.to_json()['username']) for x in  Seller.query.all()]
        all_buyers = [str(x.to_json()['user_id'])+str(x.to_json()['username']) for x in  Buyer.query.all()]

        # print(all_sellers,all_buyers)

        # if user is  buyer

        if user in all_buyers:

            try: 
                rfqs = [x.to_json() for x in RFQ.query.filter_by(buyer=user[0] ) ]
            except Exception as e: 
                print(e)
                rfqs = []

            try:
                # print([x.to_json() for x in Quotation.query.filter_by( buyer=user[0] )])
                quotations = [(x.to_json()['seller'],x.to_json()['quotation_id'],x.to_json()['product']) for x in Quotation.query.filter_by( buyer=user[0] )]
                quotations = [(int(x[0][0]),x[0][1:],x[1],x[2]) for x in quotations]
            except Exception as e:
                print(e)
                quotations = []
            
            return render_template('buyerDashboard.html', rfqLenght=len(rfqs), rfqs=rfqs, quotations=quotations, quotsLenght=len(quotations))

        #  if user is seller

        elif user in all_sellers:
            user = Seller.query.filter_by(user_id = user[0]).first()
            product = Product.query.filter_by(productId=user.product).first()

            try:
            
                rfqs = [x.to_json() for x in RFQ.query.filter_by(product_name=product.product_name)]

                for rfq in rfqs:
                    try:
                        buyer = Buyer.query.filter_by(user_id=rfq['buyer']).first().to_json()
                        rfq['buyer'] = str(buyer['user_id']) + str(buyer['username'])
                    except:
                        buyer = Buyer.query.filter_by(user_id=rfq['buyer'][0]).first().to_json()
                        rfq['buyer'] = str(buyer['user_id']) + str(buyer['username'])
            except Exception as e:
                print(e)
                rfqs = []

            return render_template('sellersDashboard.html', rfqLenght=len(rfqs), rfqs=rfqs)
            
        else:
            session['logged_in'] = False
            return render_template('index.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'GET':
        return render_template('login.html')
    else:
        name = request.form['username']
        passw = request.form['password']
        try:

            try:
                if request.form['seller'] == "on": seller_check = True
                else: raise Exception
            except: seller_check = False

            if seller_check: data = Seller.query.filter_by(username=name, password=passw).first()
            else: data = Buyer.query.filter_by(username=name, password=passw).first()

            if data is not None:
                session['logged_in'] = True
                session['user_id'] = str(data.to_json()['user_id'])+str(data.to_json()['username'])

                return redirect(url_for('home'))
            else:
                return 'Incorrect Login'
        except Exception as e:
            print(e)
            return "Incorrect Login"


@app.route('/register/', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        try:
            if request.form['seller'] == "on": seller_check = True
            else: raise Exception
        except:
            seller_check = False

        if seller_check : new_user = Seller(username=request.form['username'], password=request.form['password'], email=request.form['email'])
        else: new_user = Buyer(username=request.form['username'], password=request.form['password'], email=request.form['email'])
        new_user.create()
        return render_template('login.html')
        
    else:
        return render_template('register.html')


@app.route('/RFQ/post', methods=['POST', 'GET'])
def post_RFQ():
    if request.method == 'GET':
        return render_template('rfq.html')
    else:

        user = str(session.get('user_id'))
        # all_sellers = [int(x.to_json()['user_id']) for x in  Seller.query.all()]
        all_buyers = [str(x.to_json()['user_id'])+str(x.to_json()['username']) for x in  Buyer.query.all()]

        # print(user,all_buyers)

        if user in all_buyers :

            # buyer = Buyer.query.filter_by(user_id=user).first()
            # print(dict(request.form))
            # try: product = Product.query.filter_by(product_name=request.form['productName']).first()
            # except Exception as e: return render_template('rfq.html')
            quantity = request.form['quantity']
            usage = request.form['usage']
            product_type = request.form['productType']
            voltage = request.form['voltage']
            capacity = request.form['capacity']

            request_for_quotation = RFQ(
                buyer=user[0],
                product_name=request.form['productName'],
                quantity=quantity,
                usage=usage,
                product_type=product_type,
                voltage=voltage,
                capacity=capacity
            )

            request_for_quotation.create()

            return redirect(url_for('home'))

        else:
            return jsonify(code=400, messege='invalid request')


@app.route('/quote/post/<string:buyer>', methods=['POST', 'GET'])
def post_quotation(buyer):
    if request.method == 'GET':
        return render_template('quote.html',buyer=buyer)
    else:
        user = str(session.get('user_id'))
        all_sellers = [str(x.to_json()['user_id'])+str(x.to_json()['username']) for x in  Seller.query.all()]

        if user in all_sellers:
            buyer = buyer[0]
            seller = session['user_id']
            product = request.form['productName']
            price = request.form['price']
            quantity = request.form['quantity']
            lead_time = request.form['leadTime']
            product_type = request.form['type']
            voltage = request.form['voltage']
            capacity = request.form['capacity']
            item = request.form['item']
            weight = request.form['weight']
            color = request.form['color']
            usage = request.form['usage']
            battery_type = request.form['batteryType']
            cycle_life = request.form['cycleLife']
            nominal_capacity = request.form['nominalCapacity']
            nominal_voltage = request.form['nominalVoltage']
            warranty = request.form['warranty']
            description = request.form['description']
            print(request.form)
            customization = bool(True if request.form['customization'] == 'yes' else False)
            customized_logo = bool(True if request.form['customizedLogo'] == 'yes' else False)
            certificates = request.form['certificates']


            img = request.files['image']

            quotation = Quotation(
                buyer=buyer,
                seller=seller,
                product=product,
                capacity=capacity,
                quantity=quantity,
                usage=usage,
                product_type=product_type,
                voltage=voltage,
                weight=weight,
                color=color,
                item=item,
                cycle_life=cycle_life,
                price=price,
                lead_time=lead_time,
                battery_type=battery_type,
                nominal_capacity=nominal_capacity,
                nominal_voltage=nominal_voltage,
                warranty=warranty,
                description=description,
                customization=customization,
                customized_logo=customized_logo,
                certificates=certificates
            )
            quotation.create()


            basedir = os.path.abspath(os.path.dirname(__file__))
            file_path = os.path.join(basedir,'storage', img.filename)

            # local_image_path = '/home/mubashir/python/Register-using-Flask/storage/' + str(quotation.quotation_id) + img.filename
            img.save(file_path)

            return redirect(url_for('home'))

        else:
            return jsonify(code=400, messege='invalid request')


# @app.route('/{rfq_id}/RFQ', methods=['GET'])
# def get_rfq(rfq_id):
#     rfq = RFQ.query.filter_by(rfq_id=rfq_id).first()
#     return rfq.to_json()


# @app.route('/quotations', methods=['GET'])
# def get_quotations():
#     if session.get('user_id') in buyer.query.all():
#         quotations = Quotation.query.filter_by(buyer = str(session.get('user_id'))[0])
#         return list(quotations)
#     else:
#         return jsonify(code=400, messege='invalid request')


@app.route('/<string:quote_id>/quote', methods=['GET'])
def get_quotation(quote_id):
    print(quote_id)
    quote = Quotation.query.filter_by(quotation_id=quote_id).first().to_json()
    print(quote)
    return render_template('submittedQuote.html', product=quote)


@app.route('/product/create', methods=['POST', 'GET'])
def create_product():
    user = str(session.get('user_id'))

    all_sellers = [str(x.to_json()['user_id'])+str(x.to_json()['username']) for x in  Seller.query.all()]

    # print([x.to_json() for x in Product.query.all()])

    if user in all_sellers:

        if request.method == 'GET':

            seller = Seller.query.filter_by(user_id = user[0]).first()

            context={}

            try:
                 context['product'] = Product.query.filter_by(productId=seller.product).first().to_json()
            except Exception as e: 
                print(e)
                context['product'] = {}

            return render_template('product.html', context=context)

        elif request.method == 'POST':
            product = Product(product_name=request.form['product_name'], product_details=request.form['description'])
            product.create()

            seller = Seller.query.filter_by(user_id=user[0]).first()
            seller.update_product(int(product.productId))
            db.session.commit()

            return redirect(url_for('home'))

    else:
        return jsonify(code=400, messege='invalid request')


@app.route("/logout")
def logout():
    session['logged_in'] = False
    session['user_id'] = None
    return redirect(url_for('home'))

if __name__ == "__main__":
    db.init_app(app)
    db.create_all()   
    app.run(port=8080,debug=True)