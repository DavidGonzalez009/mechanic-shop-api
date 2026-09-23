# Mechanic Shop API

A RESTful API built with Flask for managing customers, mechanics and service tickets for a mechanic shop.

## Features

- Customer management
- Mechanic CRUD operations
- Service ticket creation and retrieval
- Assign mechanics to service tickets
- Remove mechanics from service tickets
- MySQL database integration
- SQLAlchemy ORM
- Marshmallow serialization
- Flask Blueprints
- Application Factory Pattern

## Technologies Used

- Python
- Flask
- Flask-SQLAlchemy
- Flask-Marshmallow
- MySQL
- Marshmallow
- Postman

## Setup

1. Clone the repository.

2. Create a virtual environment:

   python3 -m venv venv

3. Activate the virtual environment:

   source venv/bin/activate

4. Install the required packages:

   pip install flask flask-sqlalchemy flask-marshmallow marshmallow-sqlalchemy mysql-connector-python

5. Create a MySQL database named:

   mechanic_shop_db

6. Configure the SQLAlchemy database connection in the application.

7. Run the application:

   python3 app.py

The API will run at:

    http://127.0.0.1:5000

## API Endpoints

### Customers

- POST `/customers` - Create a customer
- GET `/customers` - Retrieve all customers
- GET `/customers/<id>` - Retrieve a customer
- PUT `/customers/<id>` - Update a customer
- DELETE `/customers/<id>` - Delete a customer

### Mechanics

- POST `/mechanics/` - Create a mechanic
- GET `/mechanics/` - Retrieve all mechanics
- PUT `/mechanics/<id>` - Update a mechanic
- DELETE `/mechanics/<id>` - Delete a mechanic

### Service Tickets

- POST `/service-tickets/` - Create a service ticket
- GET `/service-tickets/` - Retrieve all service tickets
- PUT `/service-tickets/<ticket_id>/assign-mechanic/<mechanic_id>` - Assign a mechanic to a service ticket
- PUT `/service-tickets/<ticket_id>/remove-mechanic/<mechanic_id>` - Remove a mechanic from a service ticket

## Postman

A Postman collection containing the API endpoint tests is included in this repository.

## Author

David Gonzalez
