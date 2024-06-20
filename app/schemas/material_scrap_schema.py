from marshmallow import Schema, fields, validate

from app.models.enums import ProductScrapType
from app.schemas.query_schema import QuerySchema


class MaterialScrapSchema(Schema):
    material_part_no = fields.Integer(required=True)
    quantity = fields.Integer(required=True)
    date = fields.Date(required=True, format='%Y-%m-%d')
    scrap_type = fields.String(required=True, validate=validate.OneOf([type.value for type in ProductScrapType]))


class MaterialScrapUpdateSchema(Schema):
    quantity = fields.Integer()


class MaterialScrapQuerySchema(QuerySchema):
    material_part_no = fields.Integer()
    min_quantity = fields.Integer()
    max_quantity = fields.Integer()
    start_date = fields.Date(format='%Y-%m-%d')
    end_date = fields.Date(format='%Y-%m-%d')
    scrap_type = fields.String(validate=validate.OneOf([type.value for type in ProductScrapType]))
    sort_by = fields.String(validate=validate.OneOf(['quantity', 'date', 'scrap_type']), load_default='date')
