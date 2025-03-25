from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from app.database import Base

class ImagemProduto(Base):
    __tablename__ = "imagens_produtos"

    id = Column(Integer, primary_key=True, autoincrement=True)
    url_img = Column(String(255), nullable=False)
    ordem = Column(Integer, default=1)
    
    fk_imag_produto_id = Column(Integer, ForeignKey('produtos.id', ondelete="CASCADE"), nullable=False)

    produto = relationship("Produto", back_populates="imagens")
