from fastapi import FastAPI
from app.api.v1.endpoints import users, tests, results

app = FastAPI()

# Incluyendo los routers de los módulos creados
app.include_router(users.router, prefix="/api/v1/users", tags=["Users"])
app.include_router(tests.router, prefix="/api/v1/tests", tags=["Tests"])
app.include_router(results.router, prefix="/api/v1/results", tags=["Results"])
