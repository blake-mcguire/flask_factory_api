from marshmallow import fields 
from . import ma

class OrderProductSchema(ma.Schema):
    order_id = fields.Integer(required=True)
    product_id = fields.Integer(required=True)
    quantity = fields.Integer(required=True)
    
    class Meta:
        fields = ('order_id', 'product_id', 'quantity')
        
order_product_schema = OrderProductSchema()
order_products_schema = OrderProductSchema(many=True)

