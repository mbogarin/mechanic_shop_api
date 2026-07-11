# Mechanic Shop API

## Author

**Magali Bogarin**

GitHub: https://github.com/mbogarin

---

## Project Description

The Mechanic Shop API is a RESTful backend application built with Flask, SQLAlchemy, Marshmallow, and MySQL. It demonstrates relational database design, CRUD operations, the Application Factory Pattern, Flask Blueprints, and Marshmallow serialization.

The API manages customers, mechanics, service tickets, and inventory while supporting many-to-many relationships between mechanics, inventory, and service tickets. This advanced version expands the original project by introducing JWT authentication, protected routes, rate limiting, response caching, and advanced database queries, making the API more secure, scalable, and production-ready.

### Features:

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

- Mechanic ranking based on completed service tickets

- Update mechanic assignments through a single endpoint

- Many-to-many relationship management between:
    - Mechanics and Service Tickets

    - Inventory and Service Tickets

### Technologies Used:

- Flask

- Flask-Caching

- Flask-Limiter

- Flask-Marshmallow

- Flask-SQLAlchemy

- Marshmallow

- MySQL

- Postman

- PyMySQL

- Python

- python-jose

- SQLAlchemy

---

## Table of Contents

- [Project Description](#project-description)

- [Features](#features)

- [Technologies Used](#technologies-used)

- [Installation & Setup](#installation--setup)

- [API Endpoints](#api-endpoints)

- [Project Structure](#project-structure)

- [Usage](#usage)

- [Roadmap](#roadmap)

- [Collaborators](#collaborators)

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

| PUT | `/customers/<id>` | Update a customer _(Protected)_ |

| DELETE | `/customers/<id>` | Delete a customer _(Protected)_ |

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
│   │
│   ├── utils/
│   │   └── utils.py
│   │
│   ├── extensions.py
│   ├── models.py
│   └── __init__.py
│
├── config.py
├── app.py
├── requirements.txt
├── README.md
└── mechanic_shop.postman_collection.json
```

---

## Usage

Use Postman or another API testing tool to interact with the API.

A typical workflow is:

1. Register a customer.

2. Log in to receive a JWT.

3. Use the Bearer token to access protected endpoints.

4. Create mechanics and inventory parts.

5. Create a service ticket.

6. Assign mechanics to the service ticket.

7. Add inventory parts to the service ticket.

8. Retrieve customer tickets using the protected endpoint.

9. Use advanced query endpoints such as mechanic rankings and customer pagination.

---

## Roadmap

Potential future improvements include:

- Role-based authentication for mechanics and administrators

- Inventory quantity tracking through junction models

- Search and filtering across resources

- Service ticket status tracking

- Automated unit and integration testing

- API documentation using Swagger/OpenAPI

- Docker containerization

- CI/CD pipeline for automated testing and deployment

---

## Collaborators

This project was developed independently as part of the Coding Temple Backend Software Engineering curriculum.

### Credits

- Classmates and mentors at Coding Temple
