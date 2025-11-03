from marshmallow import Schema, fields, validate

class FarmerSchema(Schema):
    name = fields.String(required=True, validate=validate.Length(min=1))
    adharnumber = fields.String(required=False, allow_none=True)
    age = fields.Integer(required=False, allow_none=True)
    gender = fields.String(required=False, allow_none=True)
    phone = fields.String(required=False, allow_none=True)
    address = fields.String(required=False, allow_none=True)
    farmingType = fields.String(required=False, allow_none=True)

class ProductSchema(Schema):
    name = fields.String(required=True)
    description = fields.String(required=False, allow_none=True)
    price = fields.Float(required=True)
    ownerId = fields.Integer(required=False, allow_none=True)

class FarmingSchema(Schema):
    name = fields.String(required=True)