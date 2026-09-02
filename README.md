# Car Service API

A REST API for managing cars, details and users,
built with FastAPI.

## Features

- User registration and authentication
- CRUD operations for cars
- Car ownership
- Details management
- Permissions and authorisation
- API validation

## Technologies

- Python
- FastAPI
- SQLite / SQLAlchemy
- JWT
- Docker
- Git

## API Endpoints

Authentication
POST /api/register/
POST /api/login/
POST /api/update/

Cars
GET    /api/cars/
GET    /api/mycars/
POST   /api/cars/
GET    /api/cars/{id}/
PUT    /api/cars/{id}/
DELETE /api/cars/{id}/

Cars
GET    /api/details/
GET    /api/mydetails/
POST   /api/details/
POST   /api/simmilar_details/
GET    /api/details/{id}/
DELETE /api/cars/{id}/

## Installation

git clone ...
cd car-service-api

python -m venv .venv
source .venv/bin/activate

pip install -r requirements.txt

python manage.py migrate
python manage.py runserver

## Authentication

registration & authentication using JWT
authenticated users can create cars, details
only the owner can modify/delete their cars, details
read-only access for unauthenticated users, details

## Project Structure

main.py - management commands
routers - api routers / business logics
schemas - pydantic models / data validation
dependencies - ownership / permissions control
core -  authentication & authorisation / jwt & hash
models - database models / relationships
alembic - database management / migrations

## Future Improvements

- PostgreSQL
- Automated tests
