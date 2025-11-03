from flask import Blueprint, request, jsonify
from app import db
from models import Addagroproducts, Register
from schemas import ProductSchema
from flask_jwt_extended import jwt_required

products_bp = Blueprint('products', __name__)
product_schema = ProductSchema()

@products_bp.route('', methods=['GET'])
def list_products():
    products = Addagroproducts.query.order_by(Addagroproducts.created_at.desc()).all()
    return jsonify([p.to_dict() for p in products]), 200

@products_bp.route('/<int:pid>', methods=['GET'])
def get_product(pid):
    p = Addagroproducts.query.get(pid)
    if not p:
        return jsonify({'error': 'Product not found'}), 404
    return jsonify(p.to_dict()), 200

@products_bp.route('', methods=['POST'])
@jwt_required(optional=True)
def create_product():
    json_data = request.get_json() or {}
    try:
        data = product_schema.load(json_data)
    except Exception as e:
        return jsonify({'error': str(e)}), 400

    price_rupees = data.get('price')
    price_paise = int(round(price_rupees * 100))

    owner_id = data.get('ownerId')
    if owner_id:
        owner = Register.query.get(owner_id)
        if not owner:
            return jsonify({'error': 'Owner (farmer) not found'}), 400
    else:
        owner = None

    product = Addagroproducts(
        productname=data.get('name'),
        productdesc=data.get('description'),
        price=price_paise,
        owner_id=owner.rid if owner else None
    )
    db.session.add(product)
    db.session.commit()

    return jsonify(product.to_dict()), 201

@products_bp.route('/<int:pid>', methods=['PUT'])
@jwt_required(optional=True)
def update_product(pid):
    p = Addagroproducts.query.get(pid)
    if not p:
        return jsonify({'error': 'Product not found'}), 404

    json_data = request.get_json() or {}
    try:
        data = product_schema.load(json_data, partial=True)
    except Exception as e:
        return jsonify({'error': str(e)}), 400

    if 'name' in data:
        p.productname = data.get('name')
    if 'description' in data:
        p.productdesc = data.get('description')
    if 'price' in data:
        p.price = int(round(data.get('price') * 100))

    db.session.commit()
    return jsonify(p.to_dict()), 200

@products_bp.route('/<int:pid>', methods=['DELETE'])
@jwt_required(optional=True)
def delete_product(pid):
    p = Addagroproducts.query.get(pid)
    if not p:
        return jsonify({'error': 'Product not found'}), 404
    db.session.delete(p)
    db.session.commit()
    return jsonify({'message': 'Product deleted successfully'}), 200