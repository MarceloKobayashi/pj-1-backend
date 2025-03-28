from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from app.database import Base

class ImagemProduto(Base):
    __tablename__ = "imagens_produtos"

    id = Column(Integer, primary_key=True, index=True)
    url_img = Column(String(255), nullable=False)
    ordem = Column(Integer, default=1)
    produto_id = Column(Integer, ForeignKey('produtos.id'))

    produto = relationship("Produto", back_populates="imagens")
