from marshmallow import Schema, fields


class ProductMaterialSchema(Schema):
    product_part_no = fields.Int(required=True)
    material_part_no = fields.Int(required=True)
    quantity = fields.Int(required=True)


class ProductMaterialUpdateSchema(Schema):
    quantity = fields.Int(required=True)
