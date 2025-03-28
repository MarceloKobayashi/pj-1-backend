from sqlalchemy import Column, Integer, String, Enum, TIMESTAMP
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from app.database import Base

class Usuario(Base):
    __tablename__ = "usuarios"

    id = Column(Integer, primary_key=True, index=True)
    nome = Column(String(100), nullable=False)
    email = Column(String(100), unique=True, nullable=False)
    senha = Column(String(255), nullable=False)
    tipo = Column(Enum('comprador', 'vendedor', 'admin', name='tipo_usuario'), nullable=False)
    telefone = Column(String(20))
    data_cadastro = Column(TIMESTAMP, server_default=func.now())

    # Relacionamentos
    enderecos = relationship("Endereco", back_populates="usuario", cascade="all, delete-orphan")
    produtos = relationship("Produto", back_populates="vendedor")
    carrinhos = relationship("CarrinhoPedido", back_populates="usuario")
    pagamentos = relationship("Pagamento", back_populates="usuario")
    avaliacoes = relationship("Avaliacao", back_populates="usuario")
    