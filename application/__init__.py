import os
from dotenv import load_dotenv
from flask import Flask

from application.extensions import db, ma
from application.blueprints.customer.routes import customer_bp
from application.blueprints.mechanic import mechanic_bp
from application.blueprints.service_ticket import service_ticket_bp

load_dotenv()

def create_app():
    app = Flask(__name__)

    app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URL')

    db.init_app(app)
    ma.init_app(app)

    app.register_blueprint(customer_bp)
    app.register_blueprint(mechanic_bp, url_prefix='/mechanics')
    app.register_blueprint(service_ticket_bp, url_prefix='/service-tickets')

    with app.app_context():
        db.create_all()

    return app

