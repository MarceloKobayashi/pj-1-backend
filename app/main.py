from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.routes import auth, produto
from app.database import engine, Base

app = FastAPI(
    title="API",
    description="API para sistema de e-commerce",
    version="0.1.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)

Base.metadata.create_all(bind=engine)

app.include_router(auth.router)
app.include_router(produto.router)

@app.get("/")
def home():
    return{"status": "online", "mensagem": "Bem vindo a API"}

