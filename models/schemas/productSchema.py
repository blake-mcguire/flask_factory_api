from marshmallow import fields
from . import ma

class ProductSchema(ma.Schema):
    product_id = fields.Integer(dump_only=True)
    product_name = fields.String(required=True)
    description = fields.String()
    price = fields.Decimal(as_string=True, required=True)
    stock_quantity = fields.Integer(required=True)

    class Meta:
        fields = ('product_id', 'product_name', 'description', 'price', 'stock_quantity')

product_schema = ProductSchema()
products_schema = ProductSchema(many=True)