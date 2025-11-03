from flask import Blueprint, jsonify
from models import Trig

records_bp = Blueprint('records', __name__)

@records_bp.route('', methods=['GET'])
def list_records():
    recs = Trig.query.order_by(Trig.timestamp.desc()).all()
    return jsonify([r.to_dict() for r in recs]), 200