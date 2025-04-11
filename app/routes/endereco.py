from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List

from app.schemas.endereco import EnderecoCreate, EnderecoResponse
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

