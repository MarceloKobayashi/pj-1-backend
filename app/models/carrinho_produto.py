from sqlalchemy import Column, Integer,  ForeignKey
from sqlalchemy.orm import relationship
from app.database import Base

class CarrinhoProduto(Base):
    __tablename__ = "carrinho_produto"

    quantidade = Column(Integer, nullable=False, default=1)

    fk_cp_carrinho_id = Column(Integer, ForeignKey('carrinho_pedido_id', ondelete="CASCADE"), primary_key=True)
    fk_cp_produto_id = Column(Integer, ForeignKey('produtos.id', ondelete="CASCADE"), primary_key=True)

    carrinho = relationship("CarrinhoProduto", back_populates="produtos")
    produto = relationship("Produto", back_populates="carrinhos")
