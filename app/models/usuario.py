from enum import Enum as PyEnum
from sqlalchemy import Enum as SQLEnum
from sqlalchemy import Column, Integer, String, TIMESTAMP
from sqlalchemy.sql.functions import current_timestamp
from sqlalchemy.orm import relationship
from app.database import Base

class TipoUsuario(str, PyEnum):
    COMPRADOR ="comprador"
    VENDEDOR = "vendedor"
    ADMIN = "admin" 

class Usuario(Base):
    __tablename__ = "usuarios"

    id = Column(Integer, primary_key=True, autoincrement=True)
    nome = Column(String(100), nullable=False)
    email = Column(String(100), unique=True, nullable=False)
    senha = Column(String(255), nullable=False) # Hash gerado antes de salvar
    tipo = Column(SQLEnum(TipoUsuario), nullable=False)
    telefone = Column(String(20))
    data_cadastro = Column(TIMESTAMP, server_default=current_timestamp(), nullable=False)

    enderecos = relationship("Endereco", back_populates="usuario", cascade="all, delete")
    produtos = relationship("Produto", back_populates="vendedor")
    pedidos = relationship("CarrinhoPedido", back_populates="usuario")
    avaliacoes = relationship("Avaliacao", back_populates="usuario")
