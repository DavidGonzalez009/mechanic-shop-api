from flask import request, jsonify

from application.extensions import db
from application.models import ServiceTicket, Mechanic
from application.blueprints.service_ticket import service_ticket_bp
from application.blueprints.service_ticket.schemas import (
    service_ticket_schema,
    service_tickets_schema
)
from application.utils.util import token_required


@service_ticket_bp.route('/', methods=['POST'])
def create_service_ticket():
    data = request.get_json()

    new_ticket = ServiceTicket(
        VIN=data['VIN'],
        service_date=data['service_date'],
        service_desc=data['service_desc'],
        customer_id=data['customer_id']
    )

    db.session.add(new_ticket)
    db.session.commit()

    return service_ticket_schema.jsonify(new_ticket), 201


@service_ticket_bp.route('/', methods=['GET'])
def get_service_tickets():
    service_tickets = db.session.query(ServiceTicket).all()

    return service_tickets_schema.jsonify(service_tickets), 200


@service_ticket_bp.route('/my-tickets', methods=['GET'])
@token_required
def get_my_tickets(customer_id):
    service_tickets = db.session.query(ServiceTicket).filter_by(
        customer_id=int(customer_id)
    ).all()

    return service_tickets_schema.jsonify(service_tickets), 200

@service_ticket_bp.route(
    '/<string:ticket_id>/assign-mechanic/<int:mechanic_id>',
    methods=['PUT']
)
def assign_mechanic(ticket_id, mechanic_id):
    service_ticket = db.session.get(ServiceTicket, ticket_id)
    mechanic = db.session.get(Mechanic, mechanic_id)

    if service_ticket is None:
        return jsonify({"message": "Service ticket not found"}), 404

    if mechanic is None:
        return jsonify({"message": "Mechanic not found"}), 404

    if mechanic not in service_ticket.mechanics:
        service_ticket.mechanics.append(mechanic)
        db.session.commit()

    return jsonify({"message": "Mechanic assigned successfully"}), 200

@service_ticket_bp.route(
    '/<string:ticket_id>/remove-mechanic/<int:mechanic_id>',
    methods=['PUT']
)
def remove_mechanic(ticket_id, mechanic_id):
    service_ticket = db.session.get(ServiceTicket, ticket_id)
    mechanic = db.session.get(Mechanic, mechanic_id)

    if service_ticket is None:
        return jsonify({"message": "Service ticket not found"}), 404

    if mechanic is None:
        return jsonify({"message": "Mechanic not found"}), 404

    if mechanic in service_ticket.mechanics:
        service_ticket.mechanics.remove(mechanic)
        db.session.commit()

    return jsonify({"message": "Mechanic removed successfully"}), 200

@service_ticket_bp.route('/<string:ticket_id>/edit', methods=['PUT'])
def edit_service_ticket_mechanics(ticket_id):
    service_ticket = db.session.get(ServiceTicket, ticket_id)

    if service_ticket is None:
        return jsonify({"message": "Service ticket not found"}), 404

    data = request.get_json()

    add_ids = data.get('add_ids', [])
    remove_ids = data.get('remove_ids', [])

    for mechanic_id in add_ids:
        mechanic = db.session.get(Mechanic, mechanic_id)

        if mechanic and mechanic not in service_ticket.mechanics:
            service_ticket.mechanics.append(mechanic)

    for mechanic_id in remove_ids:
        mechanic = db.session.get(Mechanic, mechanic_id)

        if mechanic and mechanic in service_ticket.mechanics:
            service_ticket.mechanics.remove(mechanic)

    db.session.commit()

    return service_ticket_schema.jsonify(service_ticket), 200