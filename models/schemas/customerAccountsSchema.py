from marshmallow import fields
from . import ma

class CustomerAccountSchema(ma.Schema):
    id = fields.Integer(dump_only=True)
    customer_id = fields.Integer(required=True)
    username = fields.String(required=True)
    password = fields.String(required=True, load_only=True)  # Hide password in output
    role_id = fields.Integer(required=True)

    # Nested Customer schema
    customer = fields.Nested("CustomerSchema", dump_only=True)
    
    class Meta:
        fields = ('id', 'customer_id', 'username', 'password', 'role_id', )   
    
account_schema = CustomerAccountSchema()
accounts_schema = CustomerAccountSchema(many=True)


