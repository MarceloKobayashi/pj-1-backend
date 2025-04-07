from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List

from app.models import Produto, Usuario
from app.schemas.produto import ProdutoVendedorResponse
from app.database import get_db

router = APIRouter(prefix="/index", tags=["Index"])

@router.get("/listar", response_model=List[ProdutoVendedorResponse])
async def listar_produtos(db: Session = Depends(get_db), categoria_id: int = None, pagina: int = 1, limite: int = 12):
    try:
        query = db.query(Produto, Usuario.nome.label('vendedor_nome')).join(Usuario, Produto.fk_produtos_vendedor_id == Usuario.id)

        if categoria_id:
            query = query.filter(Produto.fk_produtos_categoria_id == categoria_id)

        offset = (pagina - 1) * limite
        produtos = query.order_by(Produto.data_cadastro.desc())\
                        .offset(offset)\
                        .limit(limite)\
                        .all()
        
        return [
            {
                **produto.__dict__,
                "vendedor_nome": vendedor_nome
            }
            for produto, vendedor_nome in produtos
        ]
    
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Erro ao listar produtos: {str(e)}"
        )

