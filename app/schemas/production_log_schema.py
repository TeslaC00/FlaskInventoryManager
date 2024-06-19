from marshmallow import Schema, fields, validate

from app.schemas.query_schema import QuerySchema


class ProductionLogSchema(Schema):
    id = fields.Integer(dump_only=True)
    production_date = fields.Date(required=True)
    product_part_no = fields.Integer(required=True)
    quantity_produced = fields.Integer(required=True)


class ProductionLogUpdateSchema(Schema):
    quantity_produced = fields.Integer()


class ProductionLogQuerySchema(QuerySchema):
    start_date = fields.Date()
    end_date = fields.Date()
    product_part_no = fields.Integer()
    min_quantity = fields.Integer()
    max_quantity = fields.Integer()
    sort_by = fields.Str(validate=validate.OneOf(['production_date', 'product_part_no', 'quantity_produced']),
                         missing='production_date')
