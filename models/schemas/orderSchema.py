from marshmallow import fields
from . import ma

class OrderSchema(ma.Schema):
    order_id = fields.Integer(dump_only=True)
    account_id = fields.Integer(required=True)
    order_date = fields.DateTime(dump_only=True)
    total_amount = fields.Decimal(as_string=True, required=True)
    status = fields.String(missing='pending')
    product_ids = fields.List(fields.Integer(), required=True) 
    class Meta:
        fields = ('order_id', 'account_id', 'order_date', 'total_amount', 'status', 'products')

order_schema = OrderSchema()
orders_schema = OrderSchema(many=True)