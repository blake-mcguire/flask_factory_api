import unittest
from unittest.mock import MagicMock, patch
from faker import Faker
from services import customerServices, customerAccountServices, productsServices
from werkzeug.security import generate_password_hash
from flask import Flask


app = Flask(__name__)

class TestCreateCustomer(unittest.TestCase):

    @patch('services.customerServices.db.session.execute')
    @patch('services.customerServices.db.session.commit')
    @patch('services.customerServices.db.session.add')
    def test_create_customer(self, mock_add, mock_commit, mock_execute):
        with app.app_context():
            faker = Faker()
            mock_customer = MagicMock()
            mock_customer.id = 1
            mock_execute.return_value.scalar_one_or_none.return_value = None

            data = {
                'name': faker.name(),
                'email': faker.email(),
                'phone': faker.phone_number()
            }

            response = customerServices.create_customer(data)
            self.assertIsNotNone(response)

class TestCreateProduct(unittest.TestCase):

    @patch('services.productsServices.db.session.add')
    @patch('services.productsServices.db.session.commit')
    @patch('services.productsServices.db.session.refresh')
    @patch('services.productsServices.db.session.execute')
    def test_create_product(self, mock_execute, mock_refresh, mock_commit, mock_add):
        with app.app_context():
            faker = Faker()
            mock_product = MagicMock()
            mock_product.product_name = faker.name()
            mock_product.description = faker.text()
            mock_product.price = faker.random_number(digits=2)
            mock_product.stock_quantity = faker.random_number(digits=2)
            mock_execute.return_value.scalar_one_or_none.return_value = None

            data = {
                'product_name': mock_product.product_name,
                'description': mock_product.description,
                'price': mock_product.price,
                'stock_quantity': mock_product.stock_quantity
            }
            returned_product = productsServices.create_product(data)

            self.assertIsNotNone(returned_product)

            self.assertEqual(returned_product.product_name, data['product_name'])
            self.assertEqual(returned_product.description, data['description'])
            self.assertEqual(returned_product.price, data['price'])
            self.assertEqual(returned_product.stock_quantity, data['stock_quantity'])

            mock_add.assert_called_once()

            mock_commit.assert_called_once()

            mock_refresh.assert_called_once()
            
class TestLoginCustomerAccount(unittest.TestCase):

    @patch('services.customerAccountServices.db.session.execute')
    @patch('services.customerAccountServices.db.session.commit')
    @patch('services.customerAccountServices.db.session.add')
    def test_login_customer_account(self, mock_add, mock_commit, mock_execute):
        with app.app_context():
            faker = Faker()
            mock_customer = MagicMock()
            mock_customer.id = 1
            mock_customer.username = faker.user_name()
            mock_customer.password = generate_password_hash(faker.password())
            mock_customer.role.role_name = 'customer'
            mock_execute.return_value.scalar_one_or_none.return_value = mock_customer

            response = customerAccountServices.login(mock_customer.username, mock_customer.password)
            self.assertIsNotNone(response)

if __name__ == '__main__':
    unittest.main()