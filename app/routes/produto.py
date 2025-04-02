from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List

from app.schemas.produto import ProdutoCreate, ProdutoResponse
from app.schemas.categoria import CategoriaResponse
from app.models.produto import Produto
from app.models.usuario import Usuario
from app.models.categoria import Categoria
from app.database import get_db
from app.core.current_user import get_current_user

router = APIRouter(prefix="/produtos", tags=["Produtos"])

@router.post("/criar", response_model=ProdutoResponse, status_code=status.HTTP_201_CREATED)
async def criar_produto(produto: ProdutoCreate, db: Session = Depends(get_db), current_user: Usuario = Depends(get_current_user)):
    if current_user.tipo != "vendedor":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Apenas vendedores podem criar produtos."
        )
    
    categoria = db.query(Categoria).filter(Categoria.id == produto.fk_produtos_categoria_id).first()
    if not categoria:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Categoria não encontrada."
        )
    
    db_produto = Produto(
        **produto.model_dump(),
        fk_produtos_vendedor_id=current_user.id
    )

    db.add(db_produto)
    db.commit()
    db.refresh(db_produto)

    return db_produto


@router.get("/categorias", response_model=List[CategoriaResponse])
async def listar_categorias(db: Session = Depends(get_db)):
    categorias = db.query(Categoria).all()
    return categorias

