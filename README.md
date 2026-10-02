# Mechanic Shop API

A RESTful API built with Flask for managing customers, mechanics, service tickets, and inventory for a mechanic shop.

## Features

- Customer management
- Mechanic CRUD operations
- Service ticket creation and retrieval
- Inventory CRUD operations
- Assign and remove mechanics from service tickets
- Add inventory parts to service tickets
- Customer token authentication using JWT
- Protected customer service ticket route
- Rate limiting with Flask-Limiter
- Caching with Flask-Caching
- Customer pagination using query parameters
- Advanced SQLAlchemy relationship queries
- Many-to-many relationships
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
- Marshmallow-SQLAlchemy
- Flask-Limiter
- Flask-Caching
- python-jose
- MySQL
- Postman
- Flask-Swagger
- Flask-Swagger-UI

## Setup

1. Clone the repository.

2. Create a virtual environment:

```bash
python3 -m venv venv
```

3. Activate the virtual environment:

```bash
source venv/bin/activate
```

4. Install the required packages:

```bash
pip install -r requirements.txt
```

5. Create a MySQL database named:

```text
mechanic_shop_db
```

6. Create a `.env` file and configure your database connection:

```text
DATABASE_URL=your_database_connection_string
```

7. Run the application:

```bash
python3 app.py
```

The API will run at:

```text
http://127.0.0.1:5000
```

## API Documentation

Swagger documentation is available while the application is running.

Open the following URL in your browser:

```text
http://127.0.0.1:5000/api/docs/
```

The Swagger documentation includes the API endpoints, request methods, parameters, request and response schemas, and authentication requirements.

## Testing

Unit tests are included for the customer, mechanic, service ticket, and inventory routes.

Run the complete test suite with:

```bash
python -m unittest discover -s tests
```

The test suite includes positive and negative test cases for API functionality.

## API Endpoints

### Customers

- `POST /customers` — Create a customer
- `POST /customers/login` — Log in and receive an authentication token
- `GET /customers` — Retrieve customers with pagination support
- `GET /customers/<id>` — Retrieve a customer
- `PUT /customers/<id>` — Update a customer
- `DELETE /customers/<id>` — Delete a customer

Pagination example:

```text
/customers?limit=2&offset=0
```

### Mechanics

- `POST /mechanics/` — Create a mechanic
- `GET /mechanics/` — Retrieve all mechanics
- `PUT /mechanics/<id>` — Update a mechanic
- `DELETE /mechanics/<id>` — Delete a mechanic
- `GET /mechanics/most-active` — Retrieve mechanics ordered by number of service tickets worked

### Service Tickets

- `POST /service-tickets/` — Create a service ticket
- `GET /service-tickets/` — Retrieve all service tickets
- `GET /service-tickets/my-tickets` — Retrieve the authenticated customer's service tickets
- `PUT /service-tickets/<ticket_id>/assign-mechanic/<mechanic_id>` — Assign a mechanic
- `PUT /service-tickets/<ticket_id>/remove-mechanic/<mechanic_id>` — Remove a mechanic
- `PUT /service-tickets/<ticket_id>/edit` — Add or remove multiple mechanics
- `PUT /service-tickets/<ticket_id>/add-inventory/<inventory_id>` — Add an inventory item to a service ticket

### Inventory

- `POST /inventory/` — Create an inventory item
- `GET /inventory/` — Retrieve all inventory items
- `GET /inventory/<id>` — Retrieve an inventory item
- `PUT /inventory/<id>` — Update an inventory item
- `DELETE /inventory/<id>` — Delete an inventory item

## Authentication

Customers can log in using their email and password. A successful login returns a JWT authentication token.

Protected routes require the token to be sent using Bearer Token authorization.

Example protected route:

```text
GET /service-tickets/my-tickets
```

## Postman

A Postman collection containing API endpoint tests is included in this repository.

## Author

David Gonzalez
