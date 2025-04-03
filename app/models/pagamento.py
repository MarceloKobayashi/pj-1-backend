from sqlalchemy import Column, Integer, Enum, DECIMAL, TIMESTAMP, ForeignKey
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from app.database import Base

class Pagamento(Base):
    __tablename__ = "pagamentos"

    id = Column(Integer, primary_key=True, index=True)
    forma_pagamento = Column(Enum('credito', 'debito', 'pix', name='forma_pagamento'), nullable=False)
    valor = Column(DECIMAL(10, 2), nullable=False)
    status = Column(Enum('pendente', 'pago', 'cancelado', name='status_pagamento'), default='pendente')
    data_pagamento = Column(TIMESTAMP)
    fk_pag_carrinho_id = Column(Integer, ForeignKey('carrinho_pedido.id'))

    carrinho = relationship("CarrinhoPedido", back_populates="pagamento")

