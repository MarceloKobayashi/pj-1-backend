from sqlalchemy import Column, Integer, String, Text, DECIMAL, ForeignKey, TIMESTAMP
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from app.database import Base

class Produto(Base):
    __tablename__ = "produtos"

    id = Column(Integer, primary_key=True, index=True)
    nome = Column(String(100), nullable=False)
    descricao = Column(Text)
    preco = Column(DECIMAL(10, 2), nullable=False)
    qntd_estoque = Column(Integer, nullable=False)
    data_cadastro = Column(TIMESTAMP, server_default=func.now())
    fk_produtos_vendedor_id = Column(Integer, ForeignKey('usuarios.id'))
    fk_produtos_categoria_id = Column(Integer, ForeignKey('categorias.id'))

    # Relacionamentos
    vendedor = relationship("Usuario", back_populates="produtos")
    categoria = relationship("Categoria", back_populates="produtos")
    carrinhos = relationship("CarrinhoProduto", back_populates="produto")
    imagens = relationship("ImagemProduto", back_populates="produto", cascade="all, delete-orphan")
    avaliacoes = relationship("Avaliacao", back_populates="produto")