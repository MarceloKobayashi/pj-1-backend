from sqlalchemy import Column, Integer, Enum, TIMESTAMP, ForeignKey
from sqlalchemy.sql.functions import current_timestamp
from sqlalchemy.orm import relationship
from app.database import Base

class CarrinhoPedido(Base):
    __tablename__ = "carrinho_pedido"

    id = Column(Integer, primary_key=True, autoincrement=True)
    status = Column(Enum('pendente', 'processando', 'finalizado', 'cancelado', name='status_pedido'))
    data_adicao = Column(TIMESTAMP, server_default=current_timestamp())

    fk_carrinho_usuario_id = Column(Integer, ForeignKey('usuarios.id', ondelete="CASCADE"), nullable=False)

    usuario = relationship("Usuario", back_populates="pedidos")
    produtos = relationship("CarrinhoProduto", back_populates="carrinho", cascade="all, delete")
    pagamento = relationship("Pagamento", back_populates="pedido", uselist=False, cascade="all, delete")
