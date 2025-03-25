from fastapi import FastAPI

from app.routes import auth
from app.database import engine, Base

app = FastAPI(
    title="API",
    description="API para sistema de e-commerce",
    version="0.1.0"
)

Base.metadata.create_all(bind=engine)

app.include_router(auth.router)

@app.get("/")
def home():
    return{"status": "online", "mensagem": "Bem vindo a API"}

