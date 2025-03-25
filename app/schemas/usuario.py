# Arquivo para validar os dados recebidos apenas.

from pydantic import BaseModel, EmailStr, field_validator, ConfigDict
from sqlalchemy import Enum

class UsuarioBase(BaseModel):
    model_config = ConfigDict(arbitrary_types_allowed=True)

    email: EmailStr
    tipo: str


class UsuarioLogin(UsuarioBase):
    senha: str


class UsuarioCreate(UsuarioLogin):
    nome: str

    @field_validator('tipo')
    def validar_tipo(cls, v):
        tipos_validos = ['comprador', 'vendedor', 'admin']
        if v not in tipos_validos:
            raise ValueError(f'Tipo inválido. Use: {tipos_validos}')
        
        return v
