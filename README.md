# Mechanic Shop API

## Author

**Magali Bogarin**

GitHub: https://github.com/mbogarin

---

## Project Description

The Mechanic Shop API is a RESTful backend application built with Flask, SQLAlchemy, Marshmallow, and MySQL. The project follows the Application Factory Pattern and uses Flask Blueprints to organize resources into modular components.

### What the API Does

The API manages customers, mechanics, service tickets, and inventory through RESTful endpoints. It supports CRUD operations, many-to-many relationships, customer authentication, and inventory management for a mechanic shop.

### How It Was Enhanced

This advanced version expands the original API by introducing JWT authentication, protected routes, rate limiting, response caching, advanced database queries, and inventory management, making the application more secure, scalable, and production-ready.

### How It's Documented

The project includes interactive Swagger documentation for every endpoint, complete with request parameters, payload definitions, response definitions, authentication requirements, and example request and response data.

### How It's Tested

A comprehensive unittest suite validates every API resource with both positive and negative test cases, helping ensure endpoint functionality and reliability.

---

## Table of Contents

- [Project Description](#project-description)

- [Features](#features)

- [Tech Stack](#tech-stack)

- [Installation & Setup](#installation--setup)

- [API Endpoints](#api-endpoints)

- [Project Structure](#project-structure)

- [Usage](#usage)

- [API Documentation](#api-documentation)

- [Testing](#testing)

- [Roadmap](#roadmap)

- [Collaborators](#collaborators)

---

## Features

### Core API Features

- Built using the Application Factory Pattern

- Organized with Flask Blueprints

- SQLAlchemy ORM models

- Marshmallow schemas for serialization and validation

- MySQL database integration

- JSON REST API responses

### Resource Management

- Full CRUD operations for Customers

- Full CRUD operations for Mechanics

- Full CRUD operations for Inventory

- Create, retrieve, and update Service Tickets

- Assign and remove Mechanics from Service Tickets

- Add Inventory Parts to Service Tickets

### Security

- JWT Authentication

- Customer login endpoint

- Bearer Token authorization

- Protected API routes

- Customer-specific protected ticket endpoint

### Performance

- Rate limiting using Flask-Limiter

- Response caching using Flask-Caching

### Advanced API Features

- Customer pagination

- Retrieve mechanics ranked by the number of assigned service tickets

- Update mechanic assignments through a single endpoint

- Many-to-many relationship management between
    - Mechanics and Service Tickets

    - Inventory and Service Tickets

### API Documentation

- Interactive Swagger UI
- Endpoint documentation
- Request/response examples
- Payload definitions
- Response definitions

### Testing

- unittest framework
- One test file per blueprint
- Positive test cases
- Negative test cases
- Full endpoint coverage

---

## Tech Stack

- Flask
- Flask-Caching
- Flask-Limiter
- Flask-Marshmallow
- Flask-Swagger
- Flask-Swagger-UI
- Flask-SQLAlchemy
- Marshmallow
- MySQL
- Postman
- PyMySQL
- Python
- python-jose
- SQLAlchemy
- unittest

---

## Prerequisites

Before running this project, ensure you have the following installed:

- Python 3.x

- MySQL Server

- MySQL Workbench (recommended)

- Postman (for testing API endpoints)

---

## Installation & Setup

### 1. Clone the Repository

```bash

git clone https://github.com/mbogarin/mechanic_shop_api.git

cd mechanic_shop_api

```

### 2. Create a Virtual Environment

```bash

python -m venv venv

```

### 3. Activate the Virtual Environment

#### macOS / Linux:

```bash

source venv/bin/activate

```

#### Windows:

```bash

venv\Scripts\activate

```

### 4. Install Dependencies

Install the required packages:

```bash

pip install -r requirements.txt

```

### 5. Configure the Database

Open `config.py` and update the MySQL connection string with your own database credentials before running the application.

### 6. Run the Application

```bash
python app.py
```

---

## API Endpoints

### Customers

| Method | Endpoint | Description |

|--------|----------|-------------|

| POST | `/customers/` | Create a customer |

| POST | `/customers/login` | Authenticate a customer and return a JWT |

| GET | `/customers/` | Retrieve a paginated list of customers |

| GET | `/customers/<id>` | Retrieve a customer by ID |

| PUT | `/customers/` | Update a customer _(Protected)_ |

| DELETE | `/customers/` | Delete a customer _(Protected)_ |

| GET | `/customers/my-tickets` | Retrieve service tickets for the authenticated customer _(Protected)_ |

### Mechanics

| Method | Endpoint | Description |

|--------|----------|-------------|

| POST | `/mechanics/` | Create a mechanic |

| GET | `/mechanics/` | Retrieve all mechanics |

| GET | `/mechanics/most-tickets` | Retrieve mechanics ranked by completed service tickets |

| PUT | `/mechanics/<id>` | Update a mechanic |

| DELETE | `/mechanics/<id>` | Delete a mechanic |

### Service Tickets

| Method | Endpoint | Description |

|--------|----------|-------------|

| POST | `/service-tickets/` | Create a service ticket |

| GET | `/service-tickets/` | Retrieve all service tickets |

| PUT | `/service-tickets/<ticket_id>/edit` | Add and remove mechanics from a ticket |

| PUT | `/service-tickets/<ticket_id>/assign-mechanic/<mechanic_id>` | Assign a mechanic to a service ticket |

| PUT | `/service-tickets/<ticket_id>/remove-mechanic/<mechanic_id>` | Remove a mechanic from a service ticket |

| PUT | `/service-tickets/<ticket_id>/add-part/<inventory_id>` | Add an inventory part to a service ticket |

### Inventory

| Method | Endpoint | Description |

|--------|----------|-------------|

| POST | `/inventory/` | Create an inventory part |

| GET | `/inventory/` | Retrieve all inventory parts |

| GET | `/inventory/<id>` | Retrieve an inventory part by ID |

| PUT | `/inventory/<id>` | Update an inventory part |

| DELETE | `/inventory/<id>` | Delete an inventory part |

---

## Project Structure

```bash
mechanic_shop_api/
├── app/
│   ├── blueprints/
│   │   ├── customers/
│   │   ├── inventory/
│   │   ├── mechanics/
│   │   └── service_tickets/
│   ├── static/
│   │   └── swagger.yaml
│   ├── utils/
│   │   └── util.py
│   ├── extensions.py
│   ├── models.py
│   └── __init__.py
│
├── tests/
│   ├── test_customers.py
│   ├── test_inventory.py
│   ├── test_mechanics.py
│   └── test_service_tickets.py
│
├── app.py
├── config.py
├── README.md
├── requirements.txt
└── mechanic_shop.postman_collection.json
```

---

## Usage

Use Postman or another API testing tool to interact with the API.

1. Register or log in as a customer.
2. Authenticate using a JWT.
3. Interact with protected API endpoints.
4. Manage mechanics, service tickets, and inventory.
5. View interactive API documentation through Swagger UI.
6. Run the unittest suite to verify endpoint functionality.

---

## API Documentation

Interactive API documentation is available through Swagger UI, allowing developers to explore and test API endpoints while viewing request parameters, authentication requirements, payload definitions, and example responses.

The documentation includes:

- endpoint summaries

- request parameters

- payload definitions

- response definitions

- authentication requirements

- example request and response bodies

---

## Testing

The project includes a comprehensive unittest suite to verify API functionality. Each blueprint has its own dedicated test module, making the test suite easier to organize and maintain as the API grows.

Tests include:

- Customer endpoints

- Mechanic endpoints

- Service Ticket endpoints

- Inventory endpoints

- Positive test cases

- Negative test cases

Run all tests with:

```bash

python -m unittest discover tests
```

---

## Roadmap

Potential future improvements include:

- CI/CD pipeline

- Automated API testing in GitHub Actions

- Docker support

- Role-based authorization

- Test coverage reporting

- OpenAPI 3.0 migration

---

## Collaborators

This project was developed independently as part of the Coding Temple Backend Software Engineering curriculum.

### Credits

- Coding Temple instructors
- Coding Temple mentors
- Coding Temple classmates
