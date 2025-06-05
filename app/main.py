from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.middleware import Middleware

from app.routes import index, auth, produto, endereco, carrinho, avaliacao
from app.database import engine, Base

middleware = [
    Middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
        expose_headers=["*"]
    )
]

app = FastAPI(
    title="API",
    description="API para sistema de e-commerce",
    version="0.1.0",
    middleware=middleware
)

Base.metadata.create_all(bind=engine)

app.include_router(index.router)
app.include_router(auth.router)
app.include_router(produto.router)
app.include_router(endereco.router)
app.include_router(carrinho.router)
app.include_router(avaliacao.router)

@app.get("/")
def home():
    return{"status": "online", "mensagem": "Bem vindo a API"}

