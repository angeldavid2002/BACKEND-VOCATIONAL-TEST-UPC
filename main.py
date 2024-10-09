from fastapi import FastAPI
from app.api.v1.endpoints import users, tests

app = FastAPI()

# Rutas públicas
@app.get("/")
async def homepage():
    return {"message": "Página de Inicio"}

@app.get("/welcome")
async def welcome():
    return {"message": "Bienvenido al sistema de test vocacional"}

# Incluir rutas protegidas y públicas
app.include_router(users.router, prefix="/api/v1/users", tags=["Users"])
app.include_router(tests.router, prefix="/api/v1/tests", tags=["Tests"])
