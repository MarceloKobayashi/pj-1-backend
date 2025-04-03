from sqlalchemy import Column, Integer, Enum, TIMESTAMP, ForeignKey
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from app.database import Base

class CarrinhoPedido(Base):
    __tablename__ = "carrinho_pedido"

    id = Column(Integer, primary_key=True, index=True)
    status = Column(Enum('pendente', 'processando', 'finalizado', 'cancelado', name='status_pedido'))
    data_adicao = Column(TIMESTAMP, server_default=func.now())
    fk_carrinho_usuario_id = Column(Integer, ForeignKey('usuarios.id'))

    usuario = relationship("Usuario", back_populates="carrinhos")
    produtos = relationship("CarrinhoProduto", back_populates="carrinho")
    pagamento = relationship("Pagamento", back_populates="carrinho", uselist=False)


class CarrinhoProduto(Base):
    __tablename__ = "carrinho_produto"

    quantidade = Column(Integer, nullable=False, default=1)
    fk_cp_carrinho_id = Column(Integer, ForeignKey('carrinho_pedido.id'), primary_key=True)
    fk_cp_produto_id = Column(Integer, ForeignKey('produtos.id'), primary_key=True)

    carrinho = relationship("CarrinhoPedido", back_populates="produtos")
    produto = relationship("Produto")

