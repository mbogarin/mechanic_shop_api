# Mechanic Shop API

[![Mechanic Shop API CI/CD](https://github.com/mbogarin/mechanic_shop_api/actions/workflows/main.yaml/badge.svg?branch=deployment-cicd-pipeline)](https://github.com/mbogarin/mechanic_shop_api/actions/workflows/main.yaml)

A RESTful Flask API for managing customers, mechanics, service tickets, and inventory for a mechanic shop.

## Live Project

- **Deployed API:** [mechanic-shop-api-06j7.onrender.com](https://mechanic-shop-api-06j7.onrender.com)
- **Swagger UI:** [Interactive API Documentation](https://mechanic-shop-api-06j7.onrender.com/api/docs/)
- **Swagger JSON:** [API Specification](https://mechanic-shop-api-06j7.onrender.com/api/swagger.json)
- **GitHub Repository:** [github.com/mbogarin/mechanic_shop_api](https://github.com/mbogarin/mechanic_shop_api)

## Author

**Magali Bogarin**

- GitHub: [@mbogarin](https://github.com/mbogarin)

## Table of Contents

- [Project Overview](#project-overview)
- [Features](#features)
- [Technology Stack](#technology-stack)
- [Project Structure](#project-structure)
- [API Endpoints](#api-endpoints)
- [Authentication](#authentication)
- [Local Installation](#local-installation)
- [Testing](#testing)
- [CI/CD Pipeline](#cicd-pipeline)
- [API Documentation](#api-documentation)
- [Future Improvements](#future-improvements)
- [Educational Scope](#educational-scope)
- [Acknowledgments](#acknowledgments)

## Project Overview

The Mechanic Shop API is an educational backend project built with Flask. It provides endpoints for managing customers, mechanics, service tickets, and inventory parts.

The application follows the Application Factory Pattern and uses Flask Blueprints to separate API resources into maintainable modules. SQLAlchemy manages database operations, while Marshmallow handles request validation and response serialization.

The deployed application uses PostgreSQL on Render. SQLite provides an isolated database for automated testing and can also be used as a local development fallback.

## Features

### Customer Management

- Create customer accounts
- Retrieve paginated customer records
- Retrieve an individual customer
- Authenticate customers and issue JWTs
- Update the authenticated customer
- Delete the authenticated customer
- Retrieve tickets belonging to the authenticated customer

### Mechanic Management

- Create mechanics
- Retrieve all mechanics
- Update mechanic information
- Delete mechanics
- Rank mechanics by assigned service-ticket count

### Service-Ticket Management

- Create service tickets for existing customers
- Retrieve all service tickets
- Assign mechanics to tickets
- Remove mechanics from tickets
- Add and remove multiple mechanics in one request
- Add inventory parts to tickets

### Inventory Management

- Create inventory parts
- Retrieve all inventory parts
- Retrieve an individual part
- Partially update inventory records
- Delete inventory parts

### Authentication and Performance

- JWT customer authentication
- Token-protected customer routes
- Rate limiting on mechanic assignments
- Response caching for service-ticket retrieval
- Customer pagination

### Documentation and Testing

- Interactive Swagger UI
- Swagger 2.0 JSON specification
- Request and response definitions
- Authentication documentation
- Request and response examples
- 34 automated unit tests
- Positive and negative test cases
- Separate test module for each blueprint

### Deployment and CI/CD

- PostgreSQL database hosted on Render
- Flask API deployed as a Render web service
- Gunicorn production server
- Environment-based production configuration
- GitHub Actions build, test, and deploy jobs
- Deployment runs only after the build and tests pass

## Technology Stack

- Python 3.14
- Flask
- Flask-SQLAlchemy
- SQLAlchemy
- Flask-Marshmallow
- Marshmallow
- PostgreSQL
- SQLite
- Flask-Swagger
- Flask-Swagger-UI
- JSON Web Tokens with python-jose
- Flask-Limiter
- Flask-Caching
- Gunicorn
- Render
- GitHub Actions
- unittest
- Postman

---

## Project Structure

```text
mechanic_shop_api/
├── .github/
│   └── workflows/
│       └── main.yaml
├── app/
│   ├── blueprints/
│   │   ├── customers/
│   │   │   ├── __init__.py
│   │   │   ├── routes.py
│   │   │   └── schemas.py
│   │   ├── inventory/
│   │   │   ├── __init__.py
│   │   │   ├── routes.py
│   │   │   └── schemas.py
│   │   ├── mechanics/
│   │   │   ├── __init__.py
│   │   │   ├── routes.py
│   │   │   └── schemas.py
│   │   └── service_tickets/
│   │       ├── __init__.py
│   │       ├── routes.py
│   │       └── schemas.py
│   ├── static/
│   │   └── swagger.yaml
│   ├── utils/
│   │   └── util.py
│   ├── __init__.py
│   ├── extensions.py
│   └── models.py
├── tests/
│   ├── test_customers.py
│   ├── test_inventory.py
│   ├── test_mechanics.py
│   └── test_service_tickets.py
├── .gitignore
├── config.py
├── flask_app.py
├── mechanic_shop.postman_collection.json
├── README.md
└── requirements.txt
```

## API Endpoints

### Customers

| Method | Endpoint                   | Description                                   | Authentication |
| ------ | -------------------------- | --------------------------------------------- | -------------- |
| POST   | `/customers/`              | Create a customer                             | No             |
| GET    | `/customers/`              | Retrieve paginated customers                  | No             |
| GET    | `/customers/{customer_id}` | Retrieve a customer by ID                     | No             |
| POST   | `/customers/login`         | Log in and receive a JWT                      | No             |
| PUT    | `/customers/`              | Update the authenticated customer             | JWT            |
| DELETE | `/customers/`              | Delete the authenticated customer             | JWT            |
| GET    | `/customers/my-tickets`    | Retrieve the authenticated customer’s tickets | JWT            |

### Mechanics

| Method | Endpoint                   | Description                             |
| ------ | -------------------------- | --------------------------------------- |
| POST   | `/mechanics/`              | Create a mechanic                       |
| GET    | `/mechanics/`              | Retrieve all mechanics                  |
| PUT    | `/mechanics/{mechanic_id}` | Update a mechanic                       |
| DELETE | `/mechanics/{mechanic_id}` | Delete a mechanic                       |
| GET    | `/mechanics/most-tickets`  | Rank mechanics by assigned ticket count |

### Service Tickets

| Method | Endpoint                                                     | Description                      |
| ------ | ------------------------------------------------------------ | -------------------------------- |
| POST   | `/service-tickets/`                                          | Create a service ticket          |
| GET    | `/service-tickets/`                                          | Retrieve all service tickets     |
| PUT    | `/service-tickets/{ticket_id}/assign-mechanic/{mechanic_id}` | Assign a mechanic                |
| PUT    | `/service-tickets/{ticket_id}/remove-mechanic/{mechanic_id}` | Remove a mechanic                |
| PUT    | `/service-tickets/{ticket_id}/edit`                          | Add or remove multiple mechanics |
| PUT    | `/service-tickets/{ticket_id}/add-part/{part_id}`            | Add an inventory part            |

### Inventory

| Method | Endpoint               | Description                        |
| ------ | ---------------------- | ---------------------------------- |
| POST   | `/inventory/`          | Create an inventory part           |
| GET    | `/inventory/`          | Retrieve all inventory parts       |
| GET    | `/inventory/{part_id}` | Retrieve an inventory part         |
| PUT    | `/inventory/{part_id}` | Partially update an inventory part |
| DELETE | `/inventory/{part_id}` | Delete an inventory part           |

For complete request schemas, response definitions, examples, and error responses, visit the [Swagger UI](https://mechanic-shop-api-06j7.onrender.com/api/docs/).

## Authentication

Customer update, deletion, and ticket-history routes require a JWT.

### Obtain a token

Send customer credentials to:

```http
POST /customers/login
```

Example request:

```json
{
	"email": "customer@example.com",
	"password": "password123"
}
```

A successful response includes a token:

```json
{
	"status": "success",
	"message": "Customer successfully logged in!",
	"token": "your.jwt.token"
}
```

### Use the token

Clients may send either of these authorization-header formats:

```http
Authorization: Bearer your.jwt.token
```

```http
Authorization: your.jwt.token
```

When using Swagger UI, click **Authorize** and paste only the token. The `Bearer` prefix is not required there.

## Local Installation

### 1. Clone the Repository

```bash
git clone https://github.com/mbogarin/mechanic_shop_api.git
cd mechanic_shop_api
```

Until the deployment branch is merged into `main`, switch to it with:

```bash
git checkout deployment-cicd-pipeline
```

### 2. Create a Virtual Environment

```bash
python -m venv venv
```

### 3. Activate the Virtual Environment

macOS or Linux:

```bash
source venv/bin/activate
```

Windows PowerShell:

```powershell
venv\Scripts\Activate.ps1
```

### 4. Install Dependencies

```bash
python -m pip install -r requirements.txt
```

### 5. Configure Environment Variables

Set a database URI and JWT secret before starting the application.

macOS or Linux:

```bash
export SQLALCHEMY_DATABASE_URI="sqlite:///development.db"
export SECRET_KEY="$(python -c 'import secrets; print(secrets.token_urlsafe(64))')"
```

Windows PowerShell:

```powershell
$env:SQLALCHEMY_DATABASE_URI = "sqlite:///development.db"
$env:SECRET_KEY = python -c "import secrets; print(secrets.token_urlsafe(64))"
```

Never commit real database credentials or secret keys.

### 6. Start the Application

```bash
flask --app flask_app run --debug
```

The local API will be available at:

```text
http://127.0.0.1:5000
```

The Swagger file is configured for the deployed HTTPS service. Use the live Swagger UI when testing the hosted API.

## Testing

The test suite uses Python’s built-in `unittest` library and an isolated SQLite database.

Run all tests:

```bash
python -m unittest discover -s tests -p "test_*.py"
```

Current result:

```text
Ran 34 tests
OK
```

Test modules:

- `test_customers.py`
- `test_mechanics.py`
- `test_service_tickets.py`
- `test_inventory.py`

## CI/CD Pipeline

The workflow is defined in:

```text
.github/workflows/main.yaml
```

It runs when changes are pushed to `deployment-cicd-pipeline`.

The jobs execute in this order:

```text
build → test → deploy
```

1. **Build** checks out the repository, installs dependencies, and checks Python syntax.
2. **Test** installs dependencies in a clean runner and executes all unit tests.
3. **Deploy** triggers a Render deployment only after the test job succeeds.

The deployment job uses GitHub repository secrets for the Render service ID and API key. Database credentials and the JWT secret are stored as environment variables in Render rather than in source control.

## API Documentation

The documentation is available in two forms:

- [Interactive Swagger UI](https://mechanic-shop-api-06j7.onrender.com/api/docs/)
- [Swagger JSON specification](https://mechanic-shop-api-06j7.onrender.com/api/swagger.json)

The documentation covers:

- All 23 API operations
- Path and request methods
- Route categories and summaries
- Request parameters
- Payload definitions
- Response definitions
- Example values
- JWT authentication requirements
- Validation and error responses

## Future Improvements

Potential improvements beyond the assignment requirements include:

- Password hashing
- Role-based authorization for staff operations
- Database migrations with Alembic or Flask-Migrate
- Automated coverage reporting
- Docker support
- OpenAPI 3 migration
- Additional service-ticket CRUD operations
- Production-grade rate-limit storage

## Educational Scope

This project was developed independently as part of the Coding Temple Software Engineering curriculum. It demonstrates backend API development, relational data modeling, authentication, documentation, automated testing, cloud deployment, and continuous integration and deployment.

## Acknowledgments

- Coding Temple instructors
- Coding Temple mentors
- Coding Temple classmates
