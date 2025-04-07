# Arquivo para validar os dados recebidos apenas.

from pydantic import BaseModel, ConfigDict
from datetime import datetime
from typing import Optional, List

class ImagemProdutoBase(BaseModel):
    url_img: str
    ordem: Optional[int] = 1


class ProdutoBase(BaseModel):
    nome: str
    descricao: Optional[str] = None
    preco: float
    qntd_estoque: int
    fk_produtos_categoria_id: int
    imagens: Optional[List[ImagemProdutoBase]] = None


class ProdutoCreate(ProdutoBase):
    pass


class ProdutoUpdate(ProdutoBase):
    pass


class ProdutoResponse(ProdutoBase):
    id: int
    data_cadastro: datetime
    fk_produtos_vendedor_id: int

    model_config = ConfigDict(from_attributes=True)


class ProdutoVendedorResponse(ProdutoBase):
    id: int
    data_cadastro: datetime
    fk_produtos_vendedor_id: int
    vendedor_nome: str

    model_config = ConfigDict(from_attributes=True)
