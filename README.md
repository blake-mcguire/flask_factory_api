# E-Commerce API

## Overview

This E-Commerce API allows for managing customers, customer accounts, products, and orders. It includes endpoints for creating, updating, retrieving, and deleting records for these entities. The API also supports user authentication and rate limiting.

## Features

- **Customer Management**: Create, retrieve, update, and delete customers.
- **Account Management**: Manage customer accounts, including login functionality.
- **Product Management**: Create, retrieve, update, and delete products.
- **Order Management**: Create and retrieve orders associated with customer accounts.
- **Rate Limiting**: Protects the API from excessive requests with rate limiting.
- **Caching**: Implements caching for performance optimization.
- **Swagger Documentation**: Integrated Swagger UI for easy API exploration.

## Installation

### Prerequisites

- Python 3.8+
- Virtualenv (optional but recommended)

### Setup

1. Clone the repository:
   ```bash
   git clone https://github.com/your-repo/ecommerce-api.git
   cd ecommerce-api

2. Create and activate a virtual enviroment:
   python3 -m venv venv
    source venv/bin/activate  # On Windows use `venv\Scripts\activate`

3. Install the reequired packages
   pip install -r requirements.txt

4. Run the Application
   flask run

The API will be available at http://127.0.0.1:5000/.

### API Documentation

The API documentation is available via Swagger UI:

 - Visit http://127.0.0.1:5000/api/docs to explore the API.

### Running Tests

To run the unit test:
 `python -m unittest test_mock.py`


### API Endpoints

##### Auth
- POST /login: Authenticate a customer account.

##### Customers
- POST /customers: Create a new customer.
- GET /customers: Retrieve all customers.
- GET /customers/{id}: Retrieve a specific customer by ID.
- PUT /customers/{id}: Update a specific customer by ID.
- DELETE /customers/{id}: Delete a specific customer by ID.

##### Customer Accounts
- POST /accounts: Create a new customer account.
- GET /accounts: Retrieve all customer accounts.
- GET /accounts/{account_id}: Retrieve a specific customer      account by ID.
- PUT /accounts/{account_id}: Update a specific customer account by ID.
- DELETE /accounts/{account_id}: Delete a specific customer account by ID.

##### Products
- POST /products: Create a new product.
- GET /products: Retrieve all products.
- GET /products/{product_id}: Retrieve a specific product by ID.
- PUT /products/{product_id}: Update a specific product by ID.
- DELETE /products/{product_id}: Delete a specific product by ID.