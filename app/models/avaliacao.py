from sqlalchemy import Column, Integer, TIMESTAMP, Text, ForeignKey
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from sqlalchemy import CheckConstraint
from app.database import Base

class Avaliacao(Base):
    __tablename__ = "avaliacoes"

    id = Column(Integer, primary_key=True, index=True)
    nota = Column(Integer, nullable=False)
    comentario = Column(Text)
    data_avaliacao = Column(TIMESTAMP, server_default=func.now())
    fk_ava_produto_id = Column(Integer, ForeignKey('produtos.id'))
    fk_ava_usuario_id = Column(Integer, ForeignKey('usuarios.id'))

    produto = relationship("Produto", back_populates="avaliacoes")
    usuario = relationship("Usuario", back_populates="avaliacoes")

    __table_args__ = (
        CheckConstraint('nota >= 1 AND nota <= 5', name='check_nota_range'),
    )
