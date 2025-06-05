from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class ItemCarrinhoCreate(BaseModel):
    produto_id: int
    quantidade: int = 1


class ItemCarrinhoRemove(BaseModel):
    produto_id: int


class ItemCarrinhoResponse(BaseModel):
    id: int
    produto_id: int
    produto_nome: str
    produto_preco: float
    quantidade: int
    subtotal: float
    imagem_url: Optional[str] = None


class CarrinhoResponse(BaseModel):
    id: int
    itens: list[ItemCarrinhoResponse]
    total: float
    status: str

class CarrinhoPedidoResponse(BaseModel):
    id: int
    itens: list[ItemCarrinhoResponse]
    total: float
    status: str
    data_adicao: datetime
