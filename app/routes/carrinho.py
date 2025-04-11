from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.models import CarrinhoPedido, CarrinhoProduto, Produto, Usuario
from app.schemas.carrinho import ItemCarrinhoCreate, CarrinhoResponse
from app.database import get_db
from app.core.current_user import get_current_user

router = APIRouter(prefix="/carrinho", tags=["Carrinho"])

@router.post("/adicionar", response_model=CarrinhoResponse)
async def adicionar_item_carrinho(item: ItemCarrinhoCreate, db: Session = Depends(get_db), current_user: Usuario = Depends(get_current_user)):
    produto = db.query(Produto).filter(Produto.id == item.produto_id).first()
    if not produto:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Produto não encontrado."
        )
    
    if produto.qntd_estoque < item.quantidade:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Estoque insuficiente. Disponível: {produto.qntd_estoque}"
        )
    
    carrinho = db.query(CarrinhoPedido).filter(
        CarrinhoPedido.fk_carrinho_usuario_id == current_user.id,
        CarrinhoPedido.status == "pendente"
    ).first()

    if not carrinho:
        carrinho = CarrinhoPedido(
            fk_carrinho_usuario_id=current_user.id,
            status="pendente"
        )

        db.add(carrinho)
        db.commit()
        db.refresh(carrinho)

    item_existente = db.query(CarrinhoProduto).filter(
        CarrinhoProduto.fk_cp_carrinho_id == carrinho.id,
        CarrinhoProduto.fk_cp_produto_id == item.produto_id
    ).first()

    if item_existente:
        item_existente.quantidade += item.quantidade
    else:
        novo_item = CarrinhoProduto(
            fk_cp_carrinho_id=carrinho.id,
            fk_cp_produto_id=item.produto_id,
            quantidade=item.quantidade
        )

        db.add(novo_item)

    db.commit()

    itens = db.query(
        CarrinhoProduto,
        Produto.nome,
        Produto.preco
    ).join(
        Produto, CarrinhoProduto.fk_cp_produto_id == Produto.id
    ).filter(
        CarrinhoProduto.fk_cp_carrinho_id == carrinho.id
    ).all()

    itens_response = []
    total = 0.0

    for item, nome, preco in itens:
        subtotal = float(preco) * item.quantidade
        total += subtotal

        itens_response.append({
            "id": item.fk_cp_produto_id,
            "produto_id": item.fk_cp_produto_id,
            "produto_nome": nome,
            "produto_preco": float(preco),
            "quantidade": item.quantidade,
            "subtotal": subtotal
        })

    return {
        "id": carrinho.id,
        "itens": itens_response,
        "total": total,
        "status": carrinho.status
    }


@router.get("/exibir", response_model=CarrinhoResponse)
async def ver_carrinho(db: Session = Depends(get_db), current_user: Usuario = Depends(get_current_user)):
    carrinho = db.query(CarrinhoPedido).filter(
        CarrinhoPedido.fk_carrinho_usuario_id == current_user.id,
        CarrinhoPedido.status == "pendente"
    ).first()

    if not carrinho:
        return {
            "id": 0,
            "itens": [],
            "total": 0.0,
            "status": "vazio"
        }
    
    itens = db.query(
        CarrinhoProduto,
        Produto.nome,
        Produto.preco
    ).join(
        Produto, CarrinhoProduto.fk_cp_produto_id == Produto.id
    ).filter(
        CarrinhoProduto.fk_cp_carrinho_id == carrinho.id
    ).all()

    itens_response = []
    total = 0.0

    for item, nome, preco in itens:
        subtotal = float(preco) * item.quantidade
        total += subtotal

        itens_response.append({
            "id": item.fk_cp_produto_id,
            "produto_id": item.fk_cp_produto_id,
            "produto_nome": nome,
            "produto_preco": float(preco),
            "quantidade": item.quantidade,
            "subtotal": subtotal
        })

    return {
        "id": carrinho.id,
        "itens": itens_response,
        "total": total,
        "status": carrinho.status
    }





