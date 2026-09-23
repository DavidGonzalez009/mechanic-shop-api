from datetime import date
from typing import List
from sqlalchemy.orm import Mapped, mapped_column

from application.extensions import db, Base


service_mechanics = db.Table(
    'service_mechanics',
    Base.metadata,
    db.Column('ticket_id', db.String(17), db.ForeignKey('service_tickets.VIN')),
    db.Column('mechanic_id', db.Integer, db.ForeignKey('mechanics.id'))
)


class Customer(Base):
    __tablename__ = 'customers'

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(db.String(255), nullable=False)
    email: Mapped[str] = mapped_column(db.String(360), unique=True, nullable=False)
    phone: Mapped[str] = mapped_column(db.String(20), nullable=False)

    service_tickets: Mapped[List["ServiceTicket"]] = db.relationship(
        back_populates='customer'
    )


class ServiceTicket(Base):
    __tablename__ = 'service_tickets'

    VIN: Mapped[str] = mapped_column(db.String(17), primary_key=True)
    service_date: Mapped[date] = mapped_column(db.Date, nullable=False)
    service_desc: Mapped[str] = mapped_column(db.String(255), nullable=False)
    customer_id: Mapped[int] = mapped_column(
        db.Integer,
        db.ForeignKey('customers.id')
    )

    customer: Mapped["Customer"] = db.relationship(
        back_populates='service_tickets'
    )

    mechanics: Mapped[List["Mechanic"]] = db.relationship(
        secondary=service_mechanics,
        back_populates='service_tickets'
    )


class Mechanic(Base):
    __tablename__ = 'mechanics'

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(db.String(255), nullable=False)
    email: Mapped[str] = mapped_column(db.String(360), unique=True, nullable=False)
    phone: Mapped[str] = mapped_column(db.String(20), nullable=False)
    salary: Mapped[float] = mapped_column(db.Float, nullable=False)

    service_tickets: Mapped[List["ServiceTicket"]] = db.relationship(
        secondary=service_mechanics,
        back_populates='mechanics'
    )