from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.routes import index, auth, produto, endereco, carrinho
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

app.include_router(index.router)
app.include_router(auth.router)
app.include_router(produto.router)
app.include_router(endereco.router)
app.include_router(carrinho.router)

@app.get("/")
def home():
    return{"status": "online", "mensagem": "Bem vindo a API"}

