from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List

from app.schemas.produto import ProdutoCreate, ProdutoResponse
from app.schemas.categoria import CategoriaResponse
from app.models.produto import Produto
from app.models.usuario import Usuario
from app.models.categoria import Categoria
from app.models.imagem_produto import ImagemProduto
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
    
    produto_data = produto.model_dump(exclude={"imagens"})
    db_produto = Produto(
        **produto_data,
        fk_produtos_vendedor_id=current_user.id
    )

    db.add(db_produto)
    db.commit()
    db.refresh(db_produto)

    if produto.imagens:
        for img in produto.imagens:
            db_imagem = ImagemProduto(
                url_img=img.url_img,
                ordem=img.ordem,
                fk_imag_produto_id=db_produto.id
            )
            db.add(db_imagem)
        db.commit()
        db.refresh(db_produto)

    return db_produto

@router.get("/listar-meus-produtos", response_model=List[ProdutoResponse])
async def listar_produtos_vendedor(db: Session = Depends(get_db), current_user: Usuario = Depends(get_current_user)):
    if current_user.tipo != "vendedor":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Apenas vendedores podem listar seus produtos."
        )
    
    produtos = db.query(Produto)\
        .filter(Produto.fk_produtos_vendedor_id == current_user.id)\
        .order_by(Produto.data_cadastro.desc())\
        .all()
    
    return produtos

@router.get("/categorias", response_model=List[CategoriaResponse])
async def listar_categorias(db: Session = Depends(get_db)):
    categorias = db.query(Categoria).all()
    return categorias

