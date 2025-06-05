from pydantic import BaseModel, conint
from datetime import datetime
from typing import Optional

class AvaliacaoBase(BaseModel):
    nota: conint(ge=1, le=5)
    comentario: Optional[str] = None
    


class AvaliacaoCreate(AvaliacaoBase):
    pass


class AvaliacaoResponse(AvaliacaoBase):
    id: int
    data_avaliacao: datetime
    fk_ava_produto_id: int
    fk_ava_usuario_id: int

    class Config:
        orm_model = True