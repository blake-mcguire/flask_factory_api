from marshmallow import fields
from . import ma 

class RoleSchema(ma.schema):
    role_id = fields.Integer(required=False)
    role_name = fields.String(required=True)
    
    class Meta:
        fields = ('role_id', 'role_name')
    
role_schema = RoleSchema()
roles_schema = RoleSchema(many=True)

