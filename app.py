from flask import Flask
from database import db
from models.schemas import ma
from caching import cache
from limiter import limiter
from routes.customerAccountsBP import account_blueprint
from routes.customerBP import customer_blueprint
from routes.productsBP import product_blueprint
from routes.ordersBP import order_blueprint
from config import DevelopmentConfig, ProductionConfig
from flask_swagger_ui import get_swaggerui_blueprint
from flask_cors import CORS


SWAGGER_URL = '/api/docs'  
API_URL = '/static/swagger.yaml'  

swagger_blueprint = get_swaggerui_blueprint(
    SWAGGER_URL,  
    API_URL, 
    config={'app_name': "E-commerce API"}  
)

def create_app(config_class):
    app = Flask(__name__)

    app.config.from_object(config_class)

    db.init_app(app)
    ma.init_app(app)
    cache.init_app(app)
    limiter.init_app(app)
    CORS(app)
    
    app.register_blueprint(swagger_blueprint, url_prefix=SWAGGER_URL)
    app.register_blueprint(order_blueprint, url_prefix='/orders')
    app.register_blueprint(product_blueprint, url_prefix='/products')
    app.register_blueprint(customer_blueprint, url_prefix='/customers')
    app.register_blueprint(account_blueprint, url_prefix='/accounts')

    print('Running')
    return app


app = create_app(ProductionConfig)  

with app.app_context():
    db.create_all()
    
    