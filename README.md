# library-app

[![Build Status](https://travis-ci.org/soldatov-ss/library-app.svg?branch=master)](https://travis-ci.org/soldatov-ss/library-app)
[![Built with](https://img.shields.io/badge/Built_with-Cookiecutter_Django_Rest-F7B633.svg)](https://github.com/agconti/cookiecutter-django-rest)

Library application for managing books and authors.

# Prerequisites

- [Python 3.8 or higher](https://www.python.org/downloads/)
- [Docker](https://docs.docker.com/docker-for-mac/install/) (optional, for containerized setup)

# Environment Variables

Create a `.env` file in the project root directory and add variables from the `.env.example` file.


# Installation Using Docker (Recommended)

Start the dev server for local development:

```bash
docker-compose up
```

Run a command inside the docker container:

```bash
docker-compose run --rm web [command]
```

# Installation Without Docker

Create a virtual environment and activate it:
```bash
python3 -m venv venv
source venv/bin/activate  # On Windows use `venv\Scripts\activate`
```

Install dependencies:
```bash
pip install -r requirements.txt
```

Apply migrations:
```bash
python manage.py migrate
```

Run the server:
```bash
python manage.py runserver
```

You can now access the application in your browser at
```
http://localhost:8000
```

# Admin Panel

Create a superuser for the Django admin interface:
```bash
python manage.py createsuperuser
```

Access the admin panel in your browser at
```
http://localhost:8000/admin
```

# Running Tests

Run tests with:
```bash
python manage.py tests
```

# API Documentation

## MkDocs

MkDocs is used to create detailed API documentation. To view the documentation:
```bash
mkdocs serve
```

Access the documentation in your browser at
```
http://localhost:8001/
```

## Django-Spectacular

Django-Spectacular is used to generate OpenAPI schema. To visit one of the following URLs:
- OpenAPI schema: `http://localhost:8000/api/schema/`
- Swagger UI: `http://localhost:8000/api/schema/swagger-ui/`
- ReDoc: `http://localhost:8000/api/schema/redoc/`

# Installation Without Docker

Create a virtual environment and activate it:
```bash
python3 -m venv venv
source venv/bin/activate  # On Windows use `venv\Scripts\activate`
```

Install dependencies:
```bash
pip install -r requirements.txt
```

Apply migrations:
```bash
python manage.py migrate
```

Run the server:
```bash
python manage.py runserver
```

You can now access the application in your browser at
```
http://localhost:8000
```

# Admin Panel

Create a superuser for the Django admin interface:
```bash
python manage.py createsuperuser
```

Access the admin panel in your browser at
```
http://localhost:8000/admin
```

# Running Tests

Run tests with:
```bash
python manage.py test
```

# API Documentation

## MkDocs

MkDocs is used to create detailed API documentation. To view the documentation:
```bash
mkdocs serve
```

Access the documentation in your browser at
```
http://localhost:8001/
```

## Django-Spectacular

Django-Spectacular is used to generate OpenAPI schema. To visit one of the following URLs:
- OpenAPI schema: `http://localhost:8000/api/schema/`
- Swagger UI: `http://localhost:8000/api/schema/swagger-ui/`
- ReDoc: `http://localhost:8000/api/schema/redoc/`
