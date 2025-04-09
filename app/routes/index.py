from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session, joinedload
from typing import List

from app.models import Produto, Usuario
from app.schemas.produto import ProdutoVendedorResponse
from app.database import get_db

router = APIRouter(prefix="/index", tags=["Index"])

@router.get("/listar", response_model=List[ProdutoVendedorResponse])
async def listar_produtos(db: Session = Depends(get_db), categoria_id: int = None, nome: str = None, pagina: int = 1, limite: int = 12):
    try:
        query = db.query(Produto).options(
            joinedload(Produto.imagens),
            joinedload(Produto.vendedor)
        )

        if categoria_id:
            query = query.filter(Produto.fk_produtos_categoria_id == categoria_id)

        if nome:
            query = query.filter(Produto.nome.ilike(f"%{nome}%"))

        offset = (pagina - 1) * limite
        produtos = query.order_by(Produto.data_cadastro.desc())\
                        .offset(offset)\
                        .limit(limite)\
                        .all()
        
        return [
            {
                "id": p.id,
                "nome": p.nome,
                "descricao": p.descricao,
                "preco": p.preco,
                "qntd_estoque": p.qntd_estoque,
                "fk_produtos_categoria_id": p.fk_produtos_categoria_id,
                "vendedor_nome": p.vendedor.nome,
                "imagens": [{"url_img": img.url_img} for img in p.imagens]
            }
            for p in produtos
        ]
    
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Erro ao listar produtos: {str(e)}"
        )

