from flask import Blueprint, request, jsonify

from application.extensions import db, limiter, cache
from application.models import Customer
from application.blueprints.customer.schemas import (
    customer_schema,
    customers_schema,
    login_schema,
)
from application.utils.util import encode_token


customer_bp = Blueprint('customer_bp', __name__)


@customer_bp.route('/customers', methods=['POST'])
# Rate limiting prevents excessive customer creation requests.
@limiter.limit("3 per hour")
def create_customer():
    data = request.get_json()

    new_customer = Customer(
        name=data['name'],
        email=data['email'],
        phone=data['phone'],
        password=data['password']
    )

    db.session.add(new_customer)
    db.session.commit()

    return customer_schema.jsonify(new_customer), 201

@customer_bp.route('/customers/login', methods=['POST'])
def login():
    data = login_schema.load(request.get_json())

    customer = db.session.query(Customer).filter_by(
        email=data['email']
    ).first()

    if customer and customer.password == data['password']:
        auth_token = encode_token(customer.id)

        return jsonify({
            "status": "success",
            "message": "Successfully Logged In",
            "auth_token": auth_token
        }), 200

    return jsonify({"message": "Invalid email or password"}), 401


@customer_bp.route('/customers', methods=['GET'])
# Caching reduces repetitive database queries for frequently requested customer data.
@cache.cached(timeout=60, query_string=True)
def get_customers():
    limit = request.args.get('limit', 10, type=int)
    offset = request.args.get('offset', 0, type=int)

    customers = (
        db.session.query(Customer)
        .limit(limit)
        .offset(offset)
        .all()
    )

    return customers_schema.jsonify(customers), 200


@customer_bp.route('/customers/<int:id>', methods=['GET'])
def get_customer(id):
    customer = db.session.get(Customer, id)

    if customer is None:
        return jsonify({"message": "Customer not found"}), 404

    return customer_schema.jsonify(customer), 200


@customer_bp.route('/customers/<int:id>', methods=['PUT'])
def update_customer(id):
    customer = db.session.get(Customer, id)

    if customer is None:
        return jsonify({"message": "Customer not found"}), 404

    data = request.get_json()

    customer.name = data.get('name', customer.name)
    customer.email = data.get('email', customer.email)
    customer.phone = data.get('phone', customer.phone)

    db.session.commit()

    return customer_schema.jsonify(customer), 200


@customer_bp.route('/customers/<int:id>', methods=['DELETE'])
def delete_customer(id):
    customer = db.session.get(Customer, id)

    if customer is None:
        return jsonify({"message": "Customer not found"}), 404

    db.session.delete(customer)
    db.session.commit()

    return jsonify({"message": "Customer deleted successfully"}), 200