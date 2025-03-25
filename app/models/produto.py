from sqlalchemy import Column, Integer, String, Text, Numeric, ForeignKey, TIMESTAMP
from sqlalchemy.sql.functions import current_timestamp
from sqlalchemy.orm import relationship
from app.database import Base

class Produto(Base):
    __tablename__ = "produtos"

    id = Column(Integer, primary_key=True, autoincrement=True)
    nome = Column(String(100), nullable=False)
    descricao = Column(Text)
    preco = Column(Numeric(10, 2), nullable=False)
    qntd_estoque = Column(Integer, nullable=False)
    data_cadastro = Column(TIMESTAMP, server_default=current_timestamp())

    fk_produtos_vendedor_id = Column(Integer, ForeignKey('usuarios.id', ondelete="CASCADE"), nullable=False)
    fk_produtos_categoria_id = Column(Integer, ForeignKey('categorias.id', ondelete="CASCADE"), nullable=False)

    vendedor = relationship("Usuario", back_populates="produtos")
    categoria = relationship("Categoria", back_populates="produtos")
    imagens = relationship("ImagemProduto", back_populates="produtos", cascade="all, delete")
    carrinhos = relationship("CarrinhoProduto", back_populates="produtos")
    avaliacao = relationship("Avaliacao", back_populates="produtos")
