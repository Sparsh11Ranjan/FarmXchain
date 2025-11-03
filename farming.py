from flask import Blueprint, request, jsonify
from app import db
from models import Farming
from schemas import FarmingSchema

farming_bp = Blueprint('farming', __name__)

farming_schema = FarmingSchema()

@farming_bp.route('', methods=['GET'])
def list_farming_types():
    types = Farming.query.all()
    return jsonify([t.to_dict() for t in types]), 200

@farming_bp.route('/<int:fid>', methods=['GET'])
def get_farming_type(fid):
    t = Farming.query.get(fid)
    if not t:
        return jsonify({'error': 'Farming type not found'}), 404
    return jsonify(t.to_dict()), 200

@farming_bp.route('', methods=['POST'])
def create_farming_type():
    json_data = request.get_json() or {}
    try:
        data = farming_schema.load(json_data)
    except Exception as e:
        return jsonify({'error': str(e)}), 400

    if Farming.query.filter_by(farmingtype=data.get('name')).first():
        return jsonify({'error': 'Farming type already exists'}), 400

    t = Farming(farmingtype=data.get('name'))
    db.session.add(t)
    db.session.commit()
    return jsonify(t.to_dict()), 201

@farming_bp.route('/<int:fid>', methods=['PUT'])
def update_farming_type(fid):
    t = Farming.query.get(fid)
    if not t:
        return jsonify({'error': 'Farming type not found'}), 404
    json_data = request.get_json() or {}
    try:
        data = farming_schema.load(json_data, partial=True)
    except Exception as e:
        return jsonify({'error': str(e)}), 400

    t.farmingtype = data.get('name', t.farmingtype)
    db.session.commit()
    return jsonify(t.to_dict()), 200

@farming_bp.route('/<int:fid>', methods=['DELETE'])
def delete_farming_type(fid):
    t = Farming.query.get(fid)
    if not t:
        return jsonify({'error': 'Farming type not found'}), 404
    db.session.delete(t)
    db.session.commit()
    return jsonify({'message': 'Farming type deleted successfully'}), 200