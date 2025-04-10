from pydantic import BaseModel, ConfigDict

class EnderecoBase(BaseModel):
    cep: str
    logradouro: str
    numero: str
    complemento: str | None = None
    cidade: str
    estado: str


class EnderecoCreate(EnderecoBase):
    pass


class EnderecoResponse(EnderecoBase):
    id: int
    fk_endereco_usuario_id: int

    model_config = ConfigDict(from_attributes=True)

