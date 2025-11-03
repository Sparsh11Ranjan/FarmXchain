from datetime import datetime
from app import db

class Test(db.Model):
    __tablename__ = 'test'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))

class Register(db.Model):
    __tablename__ = 'register'
    rid = db.Column(db.Integer, primary_key=True)
    farmername = db.Column(db.String(100), nullable=False)
    adharnumber = db.Column(db.String(50), unique=True, nullable=True)
    age = db.Column(db.Integer, nullable=True)
    gender = db.Column(db.String(20), nullable=True)
    phonenumber = db.Column(db.String(30), nullable=True)
    address = db.Column(db.String(255), nullable=True)
    farming = db.Column(db.String(100), nullable=True)

    products = db.relationship('Addagroproducts', backref='owner', lazy=True)
    records = db.relationship('Trig', backref='farmer', lazy=True)

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

class User(db.Model):
    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(255), nullable=False)

class Addagroproducts(db.Model):
    __tablename__ = 'addagroproducts'
    pid = db.Column(db.Integer, primary_key=True)
    productname = db.Column(db.String(150), nullable=False)
    productdesc = db.Column(db.String(1000), nullable=True)
    price = db.Column(db.Integer, nullable=False)  
    owner_id = db.Column(db.Integer, db.ForeignKey('register.rid'), nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    def to_dict(self):
        return {
            'id': self.pid,
            'name': self.productname,
            'description': self.productdesc,
            'price': self.price / 100.0 if self.price is not None else None,
            'ownerId': self.owner_id,
            'ownerName': self.owner.farmername if self.owner else None,
            'image': "/placeholder.svg?height=200&width=300"
        }

class Farming(db.Model):
    __tablename__ = 'farming'
    fid = db.Column(db.Integer, primary_key=True)
    farmingtype = db.Column(db.String(100), unique=True, nullable=False)

    def to_dict(self):
        from app import db
        farmers_count = db.session.query(Register).filter_by(farming=self.farmingtype).count()
        return {
            'id': self.fid,
            'name': self.farmingtype,
            'description': f"Type of farming: {self.farmingtype}",
            'farmersCount': farmers_count
        }

class Trig(db.Model):
    __tablename__ = 'trig'
    id = db.Column(db.Integer, primary_key=True)
    fid = db.Column(db.Integer, db.ForeignKey('register.rid'))
    action = db.Column(db.String(200))
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)

    def to_dict(self):
        return {
            'id': self.id,
            'farmerId': self.fid,
            'farmerName': self.farmer.farmername if self.farmer else 'Unknown',
            'action': self.action,
            'timestamp': self.timestamp.isoformat() if self.timestamp else None
        }