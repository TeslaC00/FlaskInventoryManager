from marshmallow import Schema, fields


class ProductMaterialSchema(Schema):
    product_part_no = fields.Int(required=True)
    material_part_no = fields.Int(required=True)
    quantity = fields.Int(required=True)


class ProductMaterialResponseSchema(Schema):
    product_part_no = fields.Int(dump_only=True)
    material_part_no = fields.Int(dump_only=True)
    quantity = fields.Int(dump_only=True)


class ProductMaterialUpdateSchema(Schema):
    quantity = fields.Int(required=True)
