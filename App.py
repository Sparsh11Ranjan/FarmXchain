from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from datetime import datetime

# Initialize Flask app
app = Flask(__name__)
CORS(app, resources={r"/api/*": {"origins": "http://localhost:3000"}})

# Database configuration
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:Prakhar%403009@127.0.0.1:3306/farmers'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

# -------------------- MODELS --------------------

class Test(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))

class Farming(db.Model):
    fid = db.Column(db.Integer, primary_key=True)
    farmingtype = db.Column(db.String(100))

    def to_dict(self):
        return {
            'id': self.fid,
            'name': self.farmingtype,
            'description': f"Type of farming: {self.farmingtype}",
            'farmersCount': len(Register.query.filter_by(farming=self.farmingtype).all())
        }

class Addagroproducts(db.Model):
    username = db.Column(db.String(50))
    email = db.Column(db.String(50))
    pid = db.Column(db.Integer, primary_key=True)
    productname = db.Column(db.String(100))
    productdesc = db.Column(db.String(300))
    price = db.Column(db.Integer)

    def to_dict(self):
        return {
            'id': self.pid,
            'name': self.productname,
            'description': self.productdesc,
            'price': f"${self.price}",
            'owner': self.username,
            'ownerEmail': self.email,
            'image': "/placeholder.svg?height=200&width=300"
        }

class Trig(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    fid = db.Column(db.String(100))
    action = db.Column(db.String(100))
    timestamp = db.Column(db.String(100))

    def to_dict(self):
        return {
            'id': self.id,
            'farmerId': self.fid,
            'farmerName': get_farmer_name(self.fid),
            'action': self.action,
            'timestamp': self.timestamp
        }

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50))
    email = db.Column(db.String(50), unique=True)
    password = db.Column(db.String(1000))

class Register(db.Model):
    rid = db.Column(db.Integer, primary_key=True)
    farmername = db.Column(db.String(50))
    adharnumber = db.Column(db.String(50))
    age = db.Column(db.Integer)
    gender = db.Column(db.String(50))
    phonenumber = db.Column(db.String(50))
    address = db.Column(db.String(50))
    farming = db.Column(db.String(50))

    def to_dict(self):
        return {
            'id': self.rid,
            'name': self.farmername,
            'adharNumber': self.adharnumber,
            'age': self.age,
            'gender': self.gender,
            'phone': self.phonenumber,
            'address': self.address,
            'farmingType': self.farming
        }

# -------------------- HELPER --------------------

def get_farmer_name(farmer_id):
    try:
        farmer = Register.query.filter_by(rid=farmer_id).first()
        return farmer.farmername if farmer else "Unknown"
    except:
        return "Unknown"

# -------------------- ROUTES --------------------

@app.route('/api/test', methods=['GET'])
def test_connection():
    try:
        Test.query.all()
        return jsonify({"message": "Database connection successful"}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# FARMERS API
@app.route('/api/farmers', methods=['GET'])
def get_farmers():
    try:
        farmers = Register.query.all()
        return jsonify([farmer.to_dict() for farmer in farmers]), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/api/farmers/<id>', methods=['GET'])
def get_farmer(id):
    try:
        farmer = Register.query.filter_by(rid=id).first()
        if not farmer:
            return jsonify({"error": "Farmer not found"}), 404
        return jsonify(farmer.to_dict()), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/api/farmers', methods=['POST'])
def create_farmer():
    try:
        data = request.json
        new_farmer = Register(
            farmername=data.get('name'),
            adharnumber=data.get('adharNumber'),
            age=data.get('age'),
            gender=data.get('gender'),
            phonenumber=data.get('phone'),
            address=data.get('address'),
            farming=data.get('farmingType')
        )
        db.session.add(new_farmer)
        db.session.commit()
        return jsonify(new_farmer.to_dict()), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 500

@app.route('/api/farmers/<id>', methods=['PUT'])
def update_farmer(id):
    try:
        farmer = Register.query.filter_by(rid=id).first()
        if not farmer:
            return jsonify({"error": "Farmer not found"}), 404

        data = request.json
        farmer.farmername = data.get('name', farmer.farmername)
        farmer.adharnumber = data.get('adharNumber', farmer.adharnumber)
        farmer.age = data.get('age', farmer.age)
        farmer.gender = data.get('gender', farmer.gender)
        farmer.phonenumber = data.get('phone', farmer.phonenumber)
        farmer.address = data.get('address', farmer.address)
        farmer.farming = data.get('farmingType', farmer.farming)

        db.session.commit()
        return jsonify(farmer.to_dict()), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 500

@app.route('/api/farmers/<id>', methods=['DELETE'])
def delete_farmer(id):
    try:
        farmer = Register.query.filter_by(rid=id).first()
        if not farmer:
            return jsonify({"error": "Farmer not found"}), 404

        db.session.delete(farmer)
        db.session.commit()
        return jsonify({"message": "Farmer deleted successfully"}), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 500

# PRODUCTS API
@app.route('/api/products', methods=['GET'])
def get_products():
    try:
        products = Addagroproducts.query.all()
        return jsonify([product.to_dict() for product in products]), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/api/products/<id>', methods=['GET'])
def get_product(id):
    try:
        product = Addagroproducts.query.filter_by(pid=id).first()
        if not product:
            return jsonify({"error": "Product not found"}), 404
        return jsonify(product.to_dict()), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/api/products', methods=['POST'])
def create_product():
    try:
        data = request.json
        new_product = Addagroproducts(
            username=data.get('ownerName'),
            email=data.get('ownerEmail'),
            productname=data.get('name'),
            productdesc=data.get('description'),
            price=int(data.get('price').replace('$', '').split('/')[0].strip()) if isinstance(data.get('price'), str) else data.get('price')
        )
        db.session.add(new_product)
        db.session.commit()
        return jsonify(new_product.to_dict()), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 500

@app.route('/api/products/<id>', methods=['PUT'])
def update_product(id):
    try:
        product = Addagroproducts.query.filter_by(pid=id).first()
        if not product:
            return jsonify({"error": "Product not found"}), 404

        data = request.json
        product.productname = data.get('name', product.productname)
        product.productdesc = data.get('description', product.productdesc)

        if 'price' in data:
            price_str = data.get('price')
            if isinstance(price_str, str):
                price_value = price_str.replace('$', '').split('/')[0].strip()
                product.price = int(float(price_value))
            else:
                product.price = data.get('price')

        db.session.commit()
        return jsonify(product.to_dict()), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 500

@app.route('/api/products/<id>', methods=['DELETE'])
def delete_product(id):
    try:
        product = Addagroproducts.query.filter_by(pid=id).first()
        if not product:
            return jsonify({"error": "Product not found"}), 404

        db.session.delete(product)
        db.session.commit()
        return jsonify({"message": "Product deleted successfully"}), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 500

# FARMING TYPES API
@app.route('/api/farming-types', methods=['GET'])
def get_farming_types():
    try:
        farming_types = Farming.query.all()
        return jsonify([farming_type.to_dict() for farming_type in farming_types]), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/api/farming-types/<id>', methods=['GET'])
def get_farming_type(id):
    try:
        farming_type = Farming.query.filter_by(fid=id).first()
        if not farming_type:
            return jsonify({"error": "Farming type not found"}), 404
        return jsonify(farming_type.to_dict()), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/api/farming-types', methods=['POST'])
def create_farming_type():
    try:
        data = request.json
        new_farming_type = Farming(farmingtype=data.get('name'))
        db.session.add(new_farming_type)
        db.session.commit()
        return jsonify(new_farming_type.to_dict()), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 500

@app.route('/api/farming-types/<id>', methods=['PUT'])
def update_farming_type(id):
    try:
        farming_type = Farming.query.filter_by(fid=id).first()
        if not farming_type:
            return jsonify({"error": "Farming type not found"}), 404

        data = request.json
        farming_type.farmingtype = data.get('name', farming_type.farmingtype)
        db.session.commit()
        return jsonify(farming_type.to_dict()), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 500

@app.route('/api/farming-types/<id>', methods=['DELETE'])
def delete_farming_type(id):
    try:
        farming_type = Farming.query.filter_by(fid=id).first()
        if not farming_type:
            return jsonify({"error": "Farming type not found"}), 404

        db.session.delete(farming_type)
        db.session.commit()
        return jsonify({"message": "Farming type deleted successfully"}), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 500

# RECORDS API
@app.route('/api/records', methods=['GET'])
def get_records():
    try:
        records = Trig.query.all()
        return jsonify([record.to_dict() for record in records]), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# -------------------- RUN --------------------
if __name__ == '__main__':
    app.run(debug=True, port=5000)
