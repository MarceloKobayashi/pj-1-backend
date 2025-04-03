from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from app.database import Base

class Endereco(Base):
    __tablename__ = "enderecos"

    id = Column(Integer, primary_key=True, index=True)
    cep = Column(String(10), nullable=False)
    logradouro = Column(String(255), nullable=False)
    numero = Column(String(10), nullable=False)
    complemento = Column(String(100))
    cidade = Column(String(100), nullable=False)
    estado = Column(String(50), nullable=False)
    fk_endereco_usuario_id = Column(Integer, ForeignKey('usuarios.id', ondelete="CASCADE"))

    usuario = relationship("Usuario", back_populates="enderecos")