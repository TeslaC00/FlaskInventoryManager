from marshmallow import Schema, fields

from app.schemas.material_schema import MaterialSchema
from app.schemas.product_schema import ProductSchema


class ProductMaterialSchema(Schema):
    product_part_no = fields.Int(required=True)
    material_part_no = fields.Int(required=True)
    quantity = fields.Int(required=True)


class ProductMaterialResponseSchema(Schema):
    quantity = fields.Int(dump_only=True)
    product = fields.Nested(ProductSchema, dump_only=True)
    material = fields.Nested(MaterialSchema, dump_only=True)


class ProductMaterialUpdateSchema(Schema):
    quantity = fields.Int(required=True)
