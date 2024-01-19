from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from flask_login import UserMixin, login_user, LoginManager,login_required,logout_user


app = Flask(__name__)
app.config['SECRET_KEY'] = "mykey-123"
app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///ecommerce.db"

login_manager =  LoginManager()
db = SQLAlchemy(app)
login_manager.init_app(app)
login_manager.login_view = 'login'
CORS(app)

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(120), nullable=False, unique=True)
    password = db.Column(db.String(120), nullable=False)
    cart = db.relationship('CartItem', backref='user', lazy=True)

class Product(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), nullable=False)
    price = db.Column(db.Float, nullable=False)
    description = db.Column(db.Text, nullable=True)

class CartItem(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    product_id = db.Column(db.Integer, db.ForeignKey('product.id'), nullable=False)
    user = db.relationship('User', backref=db.backref('cart_items', lazy=True))
    product = db.relationship('Product', backref=db.backref('cart_items', lazy=True))
    
@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))
@app.route("/api/products/add", methods=["POST"])
@login_required
def add_product():
    data = request.json
    if "name" in data  and "price" in data:
        
        product = Product(
            name=data['name'], 
            price=data['price'], 
            description=data.get("description","")
        )
        db.session.add(product)
        db.session.commit()
        
        
        return jsonify({
            "message": "product added successfully"
        }), 201
        
    return jsonify({
        "message": "invalid product data"
    }), 400
  
@app.route("/api/products/delete/<int:product_id>", methods=["DELETE"]) 
@login_required
def deleteProduct(product_id):
    product = Product.query.get(product_id)
    
    if product :
        db.session.delete(product)
        db.session.commit()
        
        return jsonify({
            "message": "product was deleted successfully"
        }), 200
        
    return jsonify({
        "message": "product not found"
    }), 404
    
    
@app.route("/api/products/<int:product_id>",methods=["GET"])
def get_product_by_id(product_id=0):
    product = Product.query.get(product_id)
    hasProduct = product != None
    
    if hasProduct == False:
        return jsonify({
            "message": "product not found"
        }), 404
    
  
    
    return jsonify({
        "id": product.id,
        "name": product.name,
        "description": product.description
    }), 200
        
@app.route("/api/products/update/<int:product_id>", methods=['PUT'])
@login_required
def update_product(product_id):
    product_data_to_update = request.json
    
    product = Product.query.get(product_id)
   
    if not product:
        return jsonify({
            "message": "Product not found"
        }), 404
        
    productUpdated = {
        "id": product.id,
        "name": product_data_to_update.get("name",product.name),
        "description": product_data_to_update.get("description",product.description),
        "price": product_data_to_update.get("price",product.price)   
    }
    
    product.name = productUpdated["name"]
    product.description = productUpdated["description"]
    product.price = productUpdated["price"]
    
    db.session.commit()
    return jsonify({
        "message": "Product updated successfully"
    })
    
@app.route("/api/products", methods=["GET"])
def list_all_products():
    productsQuery = Product.query.all()
    products = [
        {
            "id": product.id,
            "name": product.name,
        }
        for product in productsQuery
    ]
       
    return jsonify(products)
        
@app.route("/login", methods=["POST"])
def login():
    userData = request.json
    if not "username" in userData or not "password" in userData:
        return jsonify({
            "message": "you must provide a  username and password"
        }), 400
    
    user = User.query.filter_by(username =userData["username"]).first()
    
    if not user :
         return jsonify({
            "message": "you not registered"
        }), 401
        
    
    if userData['password'] != user.password :
        return jsonify({
            "message": "Incorrect Credentials"
        }), 401
    
    login_user(user)
    
    return jsonify({
        "username": "you're the right person"
    })
    
@app.route("/logout",methods=["POST"])
@login_required
def logout():
    logout_user()
    return jsonify({
        "username": "logout successfully"
    })
    

@app.route("/")

@app.route('/api/card/add/<int:product_id>',methods=["POST"])
def add_product_in_Cart(product_id):
    return jsonify({
        
    })

def hello_word():
    return 'Index Pagess '



    

if __name__ == "__main__":
    app.run(debug=True)

