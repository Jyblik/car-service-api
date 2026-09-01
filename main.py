from fastapi import FastAPI

from database import Base, engine
from car_app.routers.cars import router as cars_router
from car_app.routers.users import router as users_router
from car_app.routers.details import router as details_router

Base.metadata.create_all(bind=engine)

app = FastAPI()

# add router for cars' pages
app.include_router(cars_router)
app.include_router(users_router)
app.include_router(details_router)