from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from sqlalchemy import and_
from datetime import datetime, timedelta
from typing import List

from app.models import Avaliacao, Usuario, Produto
from app.schemas.avaliacao import AvaliacaoResponse, AvaliacaoCreate
from app.database import get_db
from app.core.current_user import get_current_user

router = APIRouter(prefix="/avaliacao", tags=["Avaliacao"])

@router.get("/listar/{produto_id}", response_model=List[AvaliacaoResponse])
async def listar_avaliacoes(produto_id: int, db: Session = Depends(get_db), current_user: Usuario = Depends(get_current_user)):
    avaliacoes = db.query(Avaliacao).filter(
        Avaliacao.fk_ava_produto_id == produto_id
    ).order_by(Avaliacao.data_avaliacao.desc()).all()
    
    return avaliacoes

@router.post("/registrar/{produto_id}", response_model=AvaliacaoResponse, status_code=201)
async def criar_avaliacao(produto_id: int, avaliacao: AvaliacaoCreate, db: Session = Depends(get_db), current_user: Usuario = Depends(get_current_user)):
    produto = db.query(Produto).filter(Produto.id == produto_id).first()
    if not produto:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Produto não encontrado."
        )

    nova_avaliacao = Avaliacao(
        nota=avaliacao.nota,
        comentario=avaliacao.comentario,
        data_avaliacao=datetime.utcnow(),
        fk_ava_usuario_id=current_user.id,
        fk_ava_produto_id=produto_id
    )

    db.add(nova_avaliacao)
    db.commit()
    db.refresh(nova_avaliacao)

    return nova_avaliacao

@router.get("/usuario", response_model=List[AvaliacaoResponse])
async def listar_avaliacoes_usuario(db: Session = Depends(get_db), current_user: Usuario = Depends(get_current_user)):
    avaliacoes = db.query(Avaliacao).filter(Avaliacao.fk_ava_usuario_id == current_user.id).order_by(Avaliacao.fk_ava_produto_id).all()

    return avaliacoes