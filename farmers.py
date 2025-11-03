from flask import Blueprint, request, jsonify
from app import db
from models import Register, Trig
from schemas import FarmerSchema
from flask_jwt_extended import jwt_required

farmers_bp = Blueprint('farmers', __name__)
farmer_schema = FarmerSchema()

@farmers_bp.route('', methods=['GET'])
def list_farmers():
    farmers = Register.query.all()
    return jsonify([f.to_dict() for f in farmers]), 200

@farmers_bp.route('/<int:rid>', methods=['GET'])
def get_farmer(rid):
    farmer = Register.query.get(rid)
    if not farmer:
        return jsonify({'error': 'Farmer not found'}), 404
    return jsonify(farmer.to_dict()), 200

@farmers_bp.route('', methods=['POST'])
@jwt_required(optional=True)
def create_farmer():
    json_data = request.get_json() or {}
    try:
        data = farmer_schema.load(json_data)
    except Exception as e:
        return jsonify({'error': str(e)}), 400

    farmer = Register(
        farmername=data.get('name'),
        adharnumber=data.get('adharnumber'),
        age=data.get('age'),
        gender=data.get('gender'),
        phonenumber=data.get('phone'),
        address=data.get('address'),
        farming=data.get('farmingType')
    )
    db.session.add(farmer)
    db.session.commit()

    record = Trig(fid=farmer.rid, action='Farmer created')
    db.session.add(record)
    db.session.commit()

    return jsonify(farmer.to_dict()), 201

@farmers_bp.route('/<int:rid>', methods=['PUT'])
@jwt_required(optional=True)
def update_farmer(rid):
    farmer = Register.query.get(rid)
    if not farmer:
        return jsonify({'error': 'Farmer not found'}), 404

    json_data = request.get_json() or {}
    try:
        data = farmer_schema.load(json_data, partial=True)
    except Exception as e:
        return jsonify({'error': str(e)}), 400

    farmer.farmername = data.get('name', farmer.farmername)
    farmer.adharnumber = data.get('adharnumber', farmer.adharnumber)
    farmer.age = data.get('age', farmer.age)
    farmer.gender = data.get('gender', farmer.gender)
    farmer.phonenumber = data.get('phone', farmer.phonenumber)
    farmer.address = data.get('address', farmer.address)
    farmer.farming = data.get('farmingType', farmer.farming)

    db.session.commit()
    return jsonify(farmer.to_dict()), 200

@farmers_bp.route('/<int:rid>', methods=['DELETE'])
@jwt_required(optional=True)
def delete_farmer(rid):
    farmer = Register.query.get(rid)
    if not farmer:
        return jsonify({'error': 'Farmer not found'}), 404
    db.session.delete(farmer)
    db.session.commit()
    return jsonify({'message': 'Farmer deleted successfully'}), 200