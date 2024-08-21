from sqlalchemy import select, delete
from models.customer import Customer
from models.customerAccount import CustomerAccount
from database import db
from utils.util import encode_token, admin_required
from services.customerAccountServices import delete_account

def create_customer(data):
    name = data.get('name')
    email = data.get('email')
    phone = data.get('phone')

  
    if not name or not email or not phone:
        return {
            "status": "fail",
            "message": "Missing all required fields"
        }
    existing_email_query = select(Customer).where(Customer.email == email)
    existing_email = db.session.execute(existing_email_query).scalar_one_or_none()
    
    
    if existing_email:
        return {
            "status": "fail",
            "message": "Customer WIth this email already exists"
        }
    
    new_customer = Customer(
        name=name,
        email=email,
        phone=phone
    )
    
    try:
        db.session.add(new_customer)
        db.session.commit()
        db.session.refresh(new_customer)
        
        return {
            "status": "success",
            "message": "Customer Succesfully added"
        }
    
    except Exception as e:
        db.session.rollback()
        return {
            "status": "fail",
            "message": f"Failed to create account: {str(e)}"
        }
    
def get_all_customers():
    customers = db.session.query(Customer).all()
    return customers

def get_customer_by_id(id):
    customer = db.session.query(Customer).get(id)
    if customer:
        return {
            "status": "Success",
            "data": {
                "id": customer.id,
                "name": customer.name,
                "email": customer.email,
                "phone": customer.phone
            }
        }
        
    return {
        "status": "fail",
        "message": "Customer Not Found"
    }
    
def update_customer(id, data):
    customer_query = select(Customer).where(Customer.id == id)
    customer = db.session.execute(customer_query).scalar_one_or_none()
    
    if not customer:
        return {
            "status": "fail",
            "message": "Customer Not found"
        }
    
    if 'name' in data:
        customer.name = data['name']
    
    if 'email' in data:
        existing_email_query = select(Customer).where(Customer.email == data['email'])
        existing_email = db.session.execute(existing_email_query).scalar_one_or_none()
        
        if existing_email and existing_email.id != customer.id:
            return {
                'status': 'fail',
                'message': 'Email is already in use!'
            }
        customer.email = data['email']
    
    if 'phone' in data:
        customer.phone = data['phone']
        
    try:
        db.session.commit()
        return {
            "status": "success",
            "message": "Customer updated successfully"
        }

    except Exception as e:
        db.session.rollback()
        return {
            "status": "fail",
            "message": f"Failed to update account: {str(e)}"
        }
        
def delete_customer(id):
    customer_query = select(Customer).where(Customer.id == id)
    customer = db.session.execute(customer_query).scalar_one_or_none()
    
    if not customer:
        return {
            "status": "fail",
            "message": "Customer Not found"
        } 
        
    try:
        account_query = select(CustomerAccount.id).where(CustomerAccount.customer_id == id)
        account_id = db.session.execute(account_query).scalar_one_or_none()
        
        if account_id:
            delete_account(account_id)
            
            return {
                "status": "pending",
                "message": "account associated with customer being deleted"
            }
        
        db.session.delete(customer)
        db.session.commit()
        
    except Exception as e:
        db.session.rollback()
        return {
            "status": "fail",
            "message": f"Failed to delete Customer: {str(e)}"
        }
            
        
        