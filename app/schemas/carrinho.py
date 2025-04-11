from pydantic import BaseModel
from typing import Optional

class ItemCarrinhoCreate(BaseModel):
    produto_id: int
    quantidade: int = 1


class ItemCarrinhoResponse(BaseModel):
    id: int
    produto_id: int
    produto_nome: str
    produto_preco: float
    quantidade: int
    subtotal: float


class CarrinhoResponse(BaseModel):
    id: int
    itens: list[ItemCarrinhoResponse]
    total: float
    status: str

