from flask import Blueprint, request, jsonify

from application.extensions import db, limiter, cache
from application.models import Customer
from application.blueprints.customer.schemas import (
    customer_schema,
    customers_schema
)


customer_bp = Blueprint('customer_bp', __name__)


@customer_bp.route('/customers', methods=['POST'])
# Rate limiting prevents excessive customer creation requests.
@limiter.limit("3 per hour")
def create_customer():
    data = request.get_json()

    new_customer = Customer(
        name=data['name'],
        email=data['email'],
        phone=data['phone']
    )

    db.session.add(new_customer)
    db.session.commit()

    return customer_schema.jsonify(new_customer), 201


@customer_bp.route('/customers', methods=['GET'])
# Caching reduces repetitive database queries for frequently requested customer data.
@cache.cached(timeout=60)
def get_customers():
    customers = db.session.query(Customer).all()

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