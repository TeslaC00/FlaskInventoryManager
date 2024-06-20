from marshmallow import Schema, fields, validate

from app.models.enums import MaterialScrapType
from app.schemas.query_schema import QuerySchema


class ProductScrapSchema(Schema):
    product_part_no = fields.Integer(required=True)
    quantity = fields.Integer(required=True)
    date = fields.Date(required=True, format='%Y-%m-%d')
    scrap_type = fields.String(required=True, validate=validate.OneOf([type.value for type in MaterialScrapType]))


class ProductScrapUpdateSchema(Schema):
    quantity = fields.Integer()


class ProductScrapQuerySchema(QuerySchema):
    product_part_no = fields.Integer()
    min_quantity = fields.Integer()
    max_quantity = fields.Integer()
    start_date = fields.Date(format='%Y-%m-%d')
    end_date = fields.Date(format='%Y-%m-%d')
    scrap_type = fields.String(validate=validate.OneOf([type.value for type in MaterialScrapType]))
    sort_by = fields.String(validate=validate.OneOf(['quantity', 'date', 'scrap_type']), load_default='date')
