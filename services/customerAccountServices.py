from sqlalchemy import select, delete
from models.customerAccount import CustomerAccount
from models.customer import Customer
from models.roles import Role
from models.order import Order
from database import db
from utils.util import encode_token



def mask_password(password):
    return '*' * len(password)


def login(username, password):
    query = select(CustomerAccount).where(CustomerAccount.username == username)
    customer = db.session.execute(query).scalar_one_or_none()
    
    if customer and customer.password == password:
        auth_token = encode_token(customer.id, customer.role.role_name)
        return {
            "status": "Success",
            "message": "Successfully Logged in",
            "auth_token": auth_token
        }
    return None  

def create_account(account_data):
    customer_id = account_data.get('customer_id')
    username = account_data.get('username')
    password = account_data.get('password')
    role_id = account_data.get('role_id')

    if not customer_id or not username or not password or not role_id:
        return {
            "status": "fail",
            "message": "Missing required fields"
        }

    customer_query = select(Customer).where(Customer.id == customer_id)
    customer = db.session.execute(customer_query).scalar_one_or_none()

    if not customer:
        return {
            "status": "fail",
            "message": "Customer not found"
        }

    role_query = select(Role).where(Role.role_id == role_id)
    role = db.session.execute(role_query).scalar_one_or_none()

    if not role:
        return {
            "status": "fail",
            "message": "Invalid role"
        }

    existing_account_query = select(CustomerAccount).where(CustomerAccount.username == username)
    existing_account = db.session.execute(existing_account_query).scalar_one_or_none()

    if existing_account:
        return {
            "status": "fail",
            "message": "Username already taken"
        }

    new_account = CustomerAccount(
        customer_id=customer_id,
        username=username,
        password=password,
        role_id=role_id
    )

    try:
        db.session.add(new_account)
        db.session.commit()
        db.session.refresh(new_account)

        auth_token = encode_token(new_account.id, role.role_name)

        return {
            "status": "success",
            "message": "Account successfully created",
            "auth_token": auth_token
        }

    except Exception as e:
        db.session.rollback()
        return {
            "status": "fail",
            "message": f"Failed to create account: {str(e)}"
        }

def get_all_customer_accounts():
    customer_accounts = db.session.query(CustomerAccount).all()
    return customer_accounts

def get_account_by_id(account_id):
    customer_account = db.session.query(CustomerAccount).get(account_id)
    if customer_account:
        return {
            "status": "success",
            "data": {
                'id': customer_account.id,
                'username': customer_account.username,
                'customer_id': customer_account.customer_id,
                'role_id': customer_account.role_id
            }
        }
    return {
        "status": "fail",
        "message": "Account not found"
    }
    
    
def update_customer_account(account_id, data):
    account_query = select(CustomerAccount).where(CustomerAccount.id == account_id)
    account = db.session.execute(account_query).scalar_one_or_none()
    
    if not account:
        return {
            "status": "fail",
            "message": "Customer Account Not found"
        }
    
    if 'customer_id' in data:
        account.customer_id = data['customer_id']

    if 'username' in data:
        existing_account_query = select(CustomerAccount).where(CustomerAccount.username == data['username'])
        existing_account = db.session.execute(existing_account_query).scalar_one_or_none()

        if existing_account and existing_account.id != account_id:
            return {
                "status": "fail",
                "message": "Username already taken by another account"
            }
        account.username = data['username']

    if 'password' in data:
        account.password = data['password'] 

    if 'role_id' in data:
        account.role_id = data['role_id']

    try:
        db.session.commit()
        return {
            "status": "success",
            "message": "Customer account updated successfully"
        }

    except Exception as e:
        db.session.rollback()
        return {
            "status": "fail",
            "message": f"Failed to update account: {str(e)}"
        }

def delete_account(account_id):
    account_query = select(CustomerAccount).where(CustomerAccount.id == account_id)
    account = db.session.execute(account_query).scalar_one_or_none()
    
    if not account:
        return {
            "status": "fail",
            "message": "Cannot delete an account that doesn't exist"
        }

    try:
        orders_delete_query = delete(Order).where(Order.account_id == account_id)
        db.session.execute(orders_delete_query)

        db.session.delete(account)
        db.session.commit()

        return {
            "status": "success",
            "message": "Account and all related orders deleted"
        }

    except Exception as e:
        db.session.rollback()
        return {
            "status": "fail",
            "message": f"Failed to delete account: {str(e)}"
        }
