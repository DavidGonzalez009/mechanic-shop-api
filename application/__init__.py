import os
from dotenv import load_dotenv
from flask import Flask
from flask_swagger_ui import get_swaggerui_blueprint

from application.extensions import db, ma, limiter, cache
from application.blueprints.customer.routes import customer_bp
from application.blueprints.mechanic import mechanic_bp
from application.blueprints.service_ticket import service_ticket_bp
from application.blueprints.inventory import inventory_bp

load_dotenv()

SWAGGER_URL = '/api/docs'
API_URL = '/static/swagger.yaml'

swaggerui_blueprint = get_swaggerui_blueprint(
    SWAGGER_URL,
    API_URL,
    config={
        'app_name': "Mechanic Shop API"
    }
)

def create_app(test_config=None):
    app = Flask(__name__)

    app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('SQLALCHEMY_DATABASE_URI')

    if test_config:
     app.config.from_object(test_config)

    if not app.config.get('SQLALCHEMY_DATABASE_URI'):
     raise RuntimeError("Database configuration is missing.")

    db.init_app(app)
    ma.init_app(app)
    limiter.init_app(app)
    cache.init_app(app)

    app.register_blueprint(customer_bp)
    app.register_blueprint(mechanic_bp, url_prefix='/mechanics')
    app.register_blueprint(service_ticket_bp, url_prefix='/service-tickets')
    app.register_blueprint(inventory_bp, url_prefix='/inventory')
   
    app.register_blueprint(
    swaggerui_blueprint,
    url_prefix=SWAGGER_URL
)
    with app.app_context():
        db.create_all()

    return app

