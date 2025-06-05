from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List

from app.schemas.produto import ProdutoCreate, ProdutoResponse, ProdutoUpdate
from app.schemas.categoria import CategoriaResponse
from app.models import Produto, Usuario, Categoria, ImagemProduto, CarrinhoProduto
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
async def listar_produtos_vendedor(db: Session = Depends(get_db), current_user: Usuario = Depends(get_current_user), categoria_id: int = None, nome: str = None):
    if current_user.tipo != "vendedor":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Apenas vendedores podem listar seus produtos."
        )
    
    query = db.query(Produto).filter(Produto.fk_produtos_vendedor_id == current_user.id)

    if categoria_id:
        query = query.filter(Produto.fk_produtos_categoria_id == categoria_id)

    if nome:
        query = query.filter(Produto.nome.ilike(f"%{nome}%"))
    
    produtos = query.order_by(Produto.data_cadastro.desc()).all()
    
    return produtos

@router.put("/editar/{produto_id}", response_model=ProdutoResponse)
async def editar_produto(produto_id: int, produto: ProdutoUpdate, db: Session = Depends(get_db), current_user: Usuario = Depends(get_current_user)):
    if current_user.tipo != "vendedor":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Apenas vendedores podem editar produtos."
        )
    
    db_produto = db.query(Produto).filter(
        Produto.id == produto_id,
        Produto.fk_produtos_vendedor_id == current_user.id
    ).first()

    if not db_produto:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Produto não encontrado ou você não tem permissão para editá-lo."
        )
    
    categoria = db.query(Categoria).filter(
        Categoria.id == produto.fk_produtos_categoria_id
    ).first()

    if not categoria:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Categoria não identificada."
        )
    
    for field, value in produto.model_dump(exclude={"imagens"}).items():
        setattr(db_produto, field, value)

    db.query(ImagemProduto).filter(
        ImagemProduto.fk_imag_produto_id == produto_id
    ).delete()

    if produto.imagens:
        for img in produto.imagens:
            db_imagem = ImagemProduto(
                url_img = img.url_img,
                ordem=img.ordem,
                fk_imag_produto_id=produto_id
            )
            db.add(db_imagem)

    db.commit()
    db.refresh(db_produto)

    return db_produto

@router.delete("/deletar/{produto_id}", status_code=status.HTTP_204_NO_CONTENT)
async def deletar_produto(produto_id: int, db: Session = Depends(get_db), current_user: Usuario = Depends(get_current_user)):
    if current_user.tipo != "vendedor":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Apenas vendedores podem deletar produtos."
        )
    
    db_produto = db.query(Produto).filter(
        Produto.id == produto_id,
        Produto.fk_produtos_vendedor_id == current_user.id
    ).first()

    if not db_produto:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Produto não encontrado ou você não tem permissão para deletá-lo."
        )
    
    try:
        db.query(CarrinhoProduto).filter(
            CarrinhoProduto.fk_cp_produto_id == produto_id
        ).delete()

        db.query(ImagemProduto).filter(
            ImagemProduto.fk_imag_produto_id == produto_id
        ).delete()

        db.delete(db_produto)
        db.commit()

        return None
    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Erro ao deletar produto: {str(e)}"
        )


@router.get("/categorias", response_model=List[CategoriaResponse])
async def listar_categorias(db: Session = Depends(get_db)):
    categorias = db.query(Categoria).all()
    return categorias


@router.get("/produto/{produto_id}", response_model=ProdutoResponse)
async def get_produto(produto_id: int, db: Session = Depends(get_db)):
    produto = db.query(Produto).filter(Produto.id == produto_id).first()
    if not produto:
        raise HTTPException(status_code=404, detail="Produto não encontrado")
    return produto
