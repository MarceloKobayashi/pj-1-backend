from sqlalchemy import Column, Integer, Text, TIMESTAMP, ForeignKey
from sqlalchemy.sql.functions import current_timestamp
from sqlalchemy.orm import relationship
from app.database import Base

class Avalicao(Base):
    __tablename__ = "avaliacoes"

    id = Column(Integer, primary_key=True, autoincrement=True)
    nota = Column(Integer, nullable=False)  # Pydantic???
    comentario = Column(Text)
    data_avaliacao = Column(TIMESTAMP, server_default=current_timestamp())

    fk_ava_produto_id = Column(Integer, ForeignKey('produtos.id', ondelete="CASCADE"), nullable=False)
    fk_ava_usuario_id = Column(Integer, ForeignKey('usuarios.id', ondelete="CASCADE"), nullable=False)

    produto = relationship("Produto", back_populates="avaliacoes")
    usuario = relationship("Usuario", back_populates="avaliacoes")
