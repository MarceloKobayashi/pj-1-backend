from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List

from app.schemas.endereco import EnderecoCreate, EnderecoResponse, EnderecoUpdate
from app.models import Endereco, Usuario
from app.core.current_user import get_current_user
from app.database import get_db

router = APIRouter(prefix="/enderecos", tags=["Endereços"])

@router.post("/cadastrar", response_model=EnderecoResponse)
async def criar_endereco(endereco: EnderecoCreate, db: Session = Depends(get_db), current_user: Usuario = Depends(get_current_user)):
    if current_user.tipo != "comprador":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Apenas compradores podem cadastrar endereços"
        )
    
    db_endereco = Endereco(
        **endereco.model_dump(),
        fk_endereco_usuario_id = current_user.id
    )

    db.add(db_endereco)
    db.commit()
    db.refresh(db_endereco)

    return db_endereco

@router.get("/listar", response_model=List[EnderecoResponse])
async def listar_enderecos(db: Session = Depends(get_db), current_user: Usuario = Depends(get_current_user)):
    return db.query(Endereco)\
        .filter(Endereco.fk_endereco_usuario_id == current_user.id)\
        .all()

@router.delete("/deletar/{endereco_id}", status_code=status.HTTP_204_NO_CONTENT)
async def deletar_endereco(endereco_id: int, db: Session = Depends(get_db), current_user: Usuario = Depends(get_current_user)):
    endereco = db.query(Endereco).filter(Endereco.id == endereco_id, Endereco.fk_endereco_usuario_id == current_user.id).first()
    if not endereco:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Endereço não encontrado."
        )
    
    db.delete(endereco)
    db.commit()

    return None

@router.put("editar/{endereco_id}", response_model=EnderecoResponse)
async def editar_endereco(endereco_id: int, endereco_data: EnderecoUpdate, db: Session = Depends(get_db), current_user: Session = Depends(get_current_user)):
    endereco = db.query(Endereco).filter(Endereco.id == endereco_id, Endereco.fk_endereco_usuario_id == current_user.id).first()
    if not endereco:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Endereço não encontrado."
        )
    
    for key, value in endereco_data.model_dump().items():
        setattr(endereco, key, value)

    db.commit()
    db.refresh(endereco)

    return endereco

