from flask import Flask 
from database import db
from models.schemas import ma
from caching import cache
from routes.customerAccountsBP import account_blueprint

def create_app(config_name):
    app = Flask(__name__)

    app.config.from_object(f'config.{config_name}')
    db.init_app(app)
    ma.init_app(app)
    cache.init_app(app)

    # Register the blueprint
    
    app.register_blueprint(account_blueprint, url_prefix='/accounts')

    print('Running')
    return app



if __name__ == '__main__':
    app = create_app('DevelopmentConfig')
    

    with app.app_context():
        db.create_all()
    
    for rule in app.url_map.iter_rules():
        print(rule)
    app.run()