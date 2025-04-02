from pydantic import BaseModel, ConfigDict

class CategoriaBase(BaseModel):
    nome: str


class CategoriaResponse(CategoriaBase):
    id: int

    model_config = ConfigDict(from_attributes=True)