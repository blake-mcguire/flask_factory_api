from sqlalchemy import select, delete
from models.customer import Customer
from models.customerAccount import CustomerAccount
from database import db
from utils.util import encode_token, admin_required

def create_customer(data):
    name = data.get('name')
    email = data.get('email')
    phone = data.get('phone')
    username = data.get('username')
    password = data.get('password')
    role_id