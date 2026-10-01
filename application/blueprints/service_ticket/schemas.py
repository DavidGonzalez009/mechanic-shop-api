from application.extensions import ma
from application.models import ServiceTicket


class ServiceTicketSchema(ma.SQLAlchemyAutoSchema):
    mechanics = ma.Method("get_mechanics")

    class Meta:
        model = ServiceTicket

    def get_mechanics(self, obj):
        return [
            {
                "id": mechanic.id,
                "name": mechanic.name,
                "email": mechanic.email,
                "phone": mechanic.phone,
                "salary": mechanic.salary
            }
            for mechanic in obj.mechanics
        ]


service_ticket_schema = ServiceTicketSchema()
service_tickets_schema = ServiceTicketSchema(many=True)