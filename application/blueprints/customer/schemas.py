from application.extensions import ma
from application.models import Customer
from marshmallow import fields


class CustomerSchema(ma.SQLAlchemyAutoSchema):
    password = fields.String(load_only=True)

    class Meta:
        model = Customer


customer_schema = CustomerSchema()
customers_schema = CustomerSchema(many=True)
login_schema = CustomerSchema(only=("email", "password"))