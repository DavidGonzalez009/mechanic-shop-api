from flask import request, jsonify

from application.extensions import db
from application.models import Mechanic
from application.blueprints.mechanic import mechanic_bp
from application.blueprints.mechanic.schemas import (
    mechanic_schema,
    mechanics_schema
)


@mechanic_bp.route('/', methods=['POST'])
def create_mechanic():
    data = request.get_json()

    new_mechanic = Mechanic(
        name=data['name'],
        email=data['email'],
        phone=data['phone'],
        salary=data['salary']
    )

    db.session.add(new_mechanic)
    db.session.commit()

    return mechanic_schema.jsonify(new_mechanic), 201


@mechanic_bp.route('/', methods=['GET'])
def get_mechanics():
    mechanics = db.session.query(Mechanic).all()

    return mechanics_schema.jsonify(mechanics), 200

@mechanic_bp.route('/<int:id>', methods=['PUT'])
def update_mechanic(id):
    mechanic = db.session.get(Mechanic, id)

    if mechanic is None:
        return jsonify({"message": "Mechanic not found"}), 404

    data = request.get_json()

    mechanic.name = data.get('name', mechanic.name)
    mechanic.email = data.get('email', mechanic.email)
    mechanic.phone = data.get('phone', mechanic.phone)
    mechanic.salary = data.get('salary', mechanic.salary)

    db.session.commit()

    return mechanic_schema.jsonify(mechanic), 200


@mechanic_bp.route('/<int:id>', methods=['DELETE'])
def delete_mechanic(id):
    mechanic = db.session.get(Mechanic, id)

    if mechanic is None:
        return jsonify({"message": "Mechanic not found"}), 404

    db.session.delete(mechanic)
    db.session.commit()

    return jsonify({"message": "Mechanic deleted successfully"}), 200