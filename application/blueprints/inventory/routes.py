from flask import request, jsonify

from application.extensions import db
from application.models import Inventory
from application.blueprints.inventory import inventory_bp
from application.blueprints.inventory.schemas import (
    inventory_schema,
    inventories_schema
)


@inventory_bp.route('/', methods=['POST'])
def create_inventory():
    data = request.get_json()

    new_inventory = Inventory(
        name=data['name'],
        price=data['price']
    )

    db.session.add(new_inventory)
    db.session.commit()

    return inventory_schema.jsonify(new_inventory), 201


@inventory_bp.route('/', methods=['GET'])
def get_inventory():
    inventory = db.session.query(Inventory).all()

    return inventories_schema.jsonify(inventory), 200


@inventory_bp.route('/<int:id>', methods=['GET'])
def get_inventory_item(id):
    inventory = db.session.get(Inventory, id)

    if inventory is None:
        return jsonify({"message": "Inventory item not found"}), 404

    return inventory_schema.jsonify(inventory), 200


@inventory_bp.route('/<int:id>', methods=['PUT'])
def update_inventory(id):
    inventory = db.session.get(Inventory, id)

    if inventory is None:
        return jsonify({"message": "Inventory item not found"}), 404

    data = request.get_json()

    inventory.name = data.get('name', inventory.name)
    inventory.price = data.get('price', inventory.price)

    db.session.commit()

    return inventory_schema.jsonify(inventory), 200


@inventory_bp.route('/<int:id>', methods=['DELETE'])
def delete_inventory(id):
    inventory = db.session.get(Inventory, id)

    if inventory is None:
        return jsonify({"message": "Inventory item not found"}), 404

    db.session.delete(inventory)
    db.session.commit()

    return jsonify({"message": "Inventory item deleted successfully"}), 200