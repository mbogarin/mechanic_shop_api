# Mechanic Shop API

## Author

**Magali Bogarin**

GitHub: https://github.com/mbogarin

---

## Project Description

The Mechanic Shop API is a RESTful backend application built with Flask, SQLAlchemy, Marshmallow, and MySQL. It demonstrates relational database design, CRUD operations, the Application Factory Pattern, Blueprints, and Marshmallow serialization.

The API manages customers, mechanics, and service tickets while supporting many-to-many relationships between mechanics and service tickets. Users can create and manage service tickets, assign mechanics to jobs, remove mechanics from jobs, and retrieve related data through organized REST endpoints.

### Features:

- Built using the Application Factory Pattern

- Organized with Flask Blueprints

- SQLAlchemy ORM models

- Marshmallow schemas for serialization and validation

- Full CRUD operations for Customers

- Full CRUD operations for Mechanics

- Create and retrieve Service Tickets

- Assign Mechanics to Service Tickets

- Remove Mechanics from Service Tickets

- Many-to-many relationship management

- Foreign key validation

- JSON API responses

- MySQL database integration

### Technologies Used:

- Python

- Flask

- Flask SQLAlchemy

- Flask Marshmallow

- Marshmallow

- SQLAlchemy

- MySQL

- PyMySQL

- Postman

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

pip install Flask Flask-SQLAlchemy Flask-Marshmallow marshmallow-sqlalchemy

```

### 5. Configure the Database

Open `config.py` and update the MySQL connection string with your own database credentials before running the application.

### 6. Run the Application

```bash
python app.py
```

---

## API Endpoints

### Customers:

| Method | Endpoint | Description |

|--------|----------|-------------|

| POST | `/customers/` | Create a customer |

| GET | `/customers/` | Retrieve all customers |

| GET | `/customers/<id>` | Retrieve a customer by ID |

| PUT | `/customers/<id>` | Update a customer |

| DELETE | `/customers/<id>` | Delete a customer |

### Mechanics:

| Method | Endpoint | Description |

|--------|----------|-------------|

| POST | `/mechanics/` | Create a mechanic |

| GET | `/mechanics/` | Retrieve all mechanics |

| PUT | `/mechanics/<id>` | Update a mechanic |

| DELETE | `/mechanics/<id>` | Delete a mechanic |

### Service Tickets:

| Method | Endpoint | Description |

|--------|----------|-------------|

| POST | `/service-tickets/` | Create a service ticket |

| GET | `/service-tickets/` | Retrieve all service tickets |

| PUT | `/service-tickets/<ticket_id>/assign-mechanic/<mechanic_id>` | Assign a mechanic to a service ticket |

| PUT | `/service-tickets/<ticket_id>/remove-mechanic/<mechanic_id>` | Remove a mechanic from a service ticket |

---

## Project Structure

```bash
mechanic_shop_api/
├── app/
│   ├── blueprints/
│   │   ├── customers/
│   │   ├── mechanics/
│   │   └── service_tickets/
│   │
│   ├── extensions.py
│   ├── models.py
│   └── __init__.py
│
├── config.py
├── app.py
├── README.md
└── mechanic_shop_postman_collection.json
```

---

## Usage

Use Postman or another API testing tool to interact with the API.

Typical workflow:

1. Create a customer.

2. Create one or more mechanics.

3. Create a service ticket for a customer.

4. Assign one or more mechanics to the service ticket.

5. Remove mechanics from the service ticket when necessary.

6. Retrieve service tickets to view assigned mechanics.

---

## Roadmap

Potential future improvements include:

- Authentication and authorization

- Pagination for large datasets

- Search and filtering endpoints

- Service ticket status tracking

- Service history for customers

- Automatic timestamps

- Unit and integration testing

- API documentation with Swagger/OpenAPI

---

## Collaborators

Currently this project was developed independently as part of a backend software engineering curriculum.

Future collaborators can be listed here:

### Credits

- Classmates and mentors at Coding Temple
