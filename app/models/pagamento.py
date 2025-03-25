from sqlalchemy import Column, Integer, Enum, Numeric, TIMESTAMP, ForeignKey
from sqlalchemy.sql.functions import current_timestamp
from sqlalchemy.orm import relationship
from app.database import Base

class Pagamento (Base):
    __tablename__ = "pagamentos"

    id = Column(Integer, primary_key=True, autoincrement=True)
    forma_pagamento = Column(Enum('credito', 'debito', 'pix', name='forma_pagamento'), nullable=False)
    valor = Column(Numeric(10, 2), nullable=False)
    status = Column(Enum('pendente', 'pago', 'cancelado', name='status_pagamento'), default='pendente')
    data_pagamento = Column(TIMESTAMP, server_default=current_timestamp())

    fk_pag_carrinho_id = Column(Integer, ForeignKey('carrinho_pedido.id', ondelete="CASCADE"), nullable=False)

    pedido = relationship("CarrinhoProduto", back_populates="pagamento")
