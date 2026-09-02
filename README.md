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

## Docker

Build the Docker image:

```bash
docker build -t car-service-api .

## Run the container:

docker run --env-file .env -p 8000:8000 car-service-api

## The API & Swagger documentation will be available at:

http://localhost:8000

http://localhost:8000/docs

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
