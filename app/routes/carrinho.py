from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from sqlalchemy import and_
from datetime import datetime, timedelta

from app.models import CarrinhoPedido, CarrinhoProduto, Produto, Usuario, ImagemProduto
from app.schemas.carrinho import ItemCarrinhoCreate, CarrinhoResponse, ItemCarrinhoResponse, ItemCarrinhoRemove, CarrinhoPedidoResponse
from app.database import get_db
from app.core.current_user import get_current_user

router = APIRouter(prefix="/carrinho", tags=["Carrinho"])

removed_itens_cache = {}

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
        item_existente.quantidade = item.quantidade
    else:
        novo_item = CarrinhoProduto(
            fk_cp_carrinho_id=carrinho.id,
            fk_cp_produto_id=item.produto_id,
            quantidade=item.quantidade
        )

        db.add(novo_item)

    db.commit()

    carrinho_itens = db.query(CarrinhoProduto).filter(
        CarrinhoProduto.fk_cp_carrinho_id == carrinho.id
    ).all()

    itens_response = []
    total = 0.0

    for item_carrinho in carrinho_itens:
        produto = db.query(Produto).filter(Produto.id == item_carrinho.fk_cp_produto_id).first()

        imagem = db.query(ImagemProduto).filter(
            and_(
                ImagemProduto.fk_imag_produto_id == item_carrinho.fk_cp_produto_id,
                ImagemProduto.ordem == 1
            )
        ).first()

        subtotal = round(float(produto.preco) * item_carrinho.quantidade, 2)
        total += subtotal

        itens_response.append(ItemCarrinhoResponse(
            id=item_carrinho.fk_cp_produto_id,
            produto_id=item_carrinho.fk_cp_produto_id,
            produto_nome=produto.nome,
            produto_preco=float(produto.preco),
            quantidade=item_carrinho.quantidade,
            subtotal=subtotal,
            imagem_url=imagem.url_img if imagem else None
        ))

    total = round(total, 2)

    return CarrinhoResponse(
        id=carrinho.id,
        itens=itens_response,
        total=total,
        status=carrinho.status
    )


@router.get("/exibir", response_model=CarrinhoResponse)
async def ver_carrinho(db: Session = Depends(get_db), current_user: Usuario = Depends(get_current_user)):
    if current_user.tipo != "comprador":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Apenas compradores podem acessar o carrinho."
        )

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
    
    carrinho_itens = db.query(CarrinhoProduto).filter(
        CarrinhoProduto.fk_cp_carrinho_id == carrinho.id
    ).all()

    itens_response = []
    total = 0.0

    for item in carrinho_itens:
        produto = db.query(Produto).filter(Produto.id == item.fk_cp_produto_id).first()

        imagem = db.query(ImagemProduto).filter(
            ImagemProduto.fk_imag_produto_id == item.fk_cp_produto_id,
            ImagemProduto.ordem == 1
        ).first()

        subtotal = round(float(produto.preco) * item.quantidade, 2)
        total += subtotal

        itens_response.append({
            "id": item.fk_cp_produto_id,
            "produto_id": item.fk_cp_produto_id,
            "produto_nome": produto.nome,
            "produto_preco": float(produto.preco),
            "quantidade": item.quantidade,
            "subtotal": subtotal,
            "imagem_url": imagem.url_img if imagem else None
        })

    return CarrinhoResponse(
        id=carrinho.id,
        itens=itens_response,
        total=round(total, 2),
        status=carrinho.status
    )

@router.delete("/remover", status_code=status.HTTP_200_OK)
async def remover_item_carrinho(item: ItemCarrinhoRemove, db: Session = Depends(get_db), current_user: Usuario = Depends(get_current_user)):
    if current_user.tipo != "comprador":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Apenas compradores podem modificar o carrinho."
        )
    
    carrinho = db.query(CarrinhoPedido).filter(
        CarrinhoPedido.fk_carrinho_usuario_id == current_user.id,
        CarrinhoPedido.status == "pendente"
    ).first()

    if not carrinho:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Carrinho não encontrado"
        )
    
    item_carrinho = db.query(CarrinhoProduto).filter(
        CarrinhoProduto.fk_cp_carrinho_id == carrinho.id,
        CarrinhoProduto.fk_cp_produto_id == item.produto_id
    ).first()

    if not item_carrinho:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Item não encontrado no carrinho."
        )
    
    db.delete(item_carrinho)
    db.commit()

    return {"message": "Item removido do carrinho com sucesso."}

@router.post("/remover-desfazer", status_code=status.HTTP_200_OK)
async def remover_itens_desfazer(item: ItemCarrinhoRemove, db: Session = Depends(get_db), current_user: Usuario = Depends(get_current_user)):
    if current_user.tipo != "comprador":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Apenas compradores podem modificar o carrinho."
        )
    
    carrinho = db.query(CarrinhoPedido).filter(
        CarrinhoPedido.fk_carrinho_usuario_id == current_user.id,
        CarrinhoPedido.status == "pendente"
    ).first()

    if not carrinho:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Carrinho não encontrado"
        )
    
    item_carrinho = db.query(CarrinhoProduto).filter(
        CarrinhoProduto.fk_cp_carrinho_id == carrinho.id,
        CarrinhoProduto.fk_cp_produto_id == item.produto_id
    ).first()

    if not item_carrinho:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Item não encontrado no carrinho."
        )
    
    removed_itens_cache[f"{current_user.id}_{item.produto_id}"] = {
        "data": {
            "carrinho_id": carrinho.id,
            "produto_id": item_carrinho.fk_cp_produto_id,
            "quantidade": item_carrinho.quantidade
        },
        "expires_at": datetime.now() + timedelta(seconds=30)
    }

    db.delete(item_carrinho)
    db.commit()

    return {"message": "Item removido do carrinho. Você pode desfazer essa remoção em 30 segundos."}

@router.post("/desfazer-remocao", status_code=status.HTTP_200_OK)
async def desfazer_remocao(item: ItemCarrinhoRemove, db: Session = Depends(get_db), current_user: Usuario = Depends(get_current_user)):
    cache_key = f"{current_user.id}_{item.produto_id}"
    cached_item = removed_itens_cache.get(cache_key)

    if not cached_item or cached_item["expires_at"] < datetime.now():
        raise HTTPException(
            status_code=status.HTTP_410_GONE,
            detail="Tempo para desfazer expirado."
        )
    
    item_data = cached_item["data"]

    carrinho = db.query(CarrinhoPedido).get(item_data["carrinho_id"])
    if not carrinho:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Carrinho não encontrado."
        )
    
    novo_item = CarrinhoProduto(
        fk_cp_carrinho_id=carrinho.id,
        fk_cp_produto_id=item_data["produto_id"],
        quantidade=item_data["quantidade"]
    )

    db.add(novo_item)
    db.commit()

    del removed_itens_cache[cache_key]

    return {"message": "Remoção desfeita com sucesso."}

# Rota para finalizar
@router.put("/finalizar")
async def finalizar_compra(db: Session = Depends(get_db), current_user: Usuario = Depends(get_current_user)):
    carrinho = db.query(CarrinhoPedido).filter(
        CarrinhoPedido.fk_carrinho_usuario_id == current_user.id,
        CarrinhoPedido.status == "pendente"
    ).first()

    if not carrinho:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Nenhum carrinho pendente encontrado."
        )
    
    itens_carrinho = db.query(CarrinhoProduto).filter(CarrinhoProduto.fk_cp_carrinho_id == carrinho.id).all()
    if not itens_carrinho:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="O carrinho está vazio."
        )
    
    for item in itens_carrinho:
        produto = db.query(Produto).filter(Produto.id == item.fk_cp_produto_id).first()
        if produto.qntd_estoque < item.quantidade:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Estoque insuficiente para o produto {produto.name}. Disponível: {produto.qntd_estoque}"
            )

    carrinho.status = "finalizado"
    db.commit()

    for item in itens_carrinho:
        produto = db.query(Produto).filter(Produto.id == item.fk_cp_produto_id).first()
        produto.qntd_estoque -= item.quantidade
        db.commit()
    
    return {"detail": "Compra finalizada com sucesso."}

@router.get("/pedidos", response_model=list[CarrinhoPedidoResponse])
async def listar_pedidos_finalizados(db: Session = Depends(get_db), current_user: Usuario = Depends(get_current_user)):
    pedidos = db.query(CarrinhoPedido).filter(
        CarrinhoPedido.fk_carrinho_usuario_id == current_user.id,
        CarrinhoPedido.status == "finalizado"
    ).order_by(CarrinhoPedido.data_adicao.desc()).all()

    resposta = []

    for pedido in pedidos:
        itens_carrinho = db.query(CarrinhoProduto).filter(
            CarrinhoProduto.fk_cp_carrinho_id == pedido.id
        ).all()

        itens_response = []
        total = 0.0

        for item in itens_carrinho:
            produto = db.query(Produto).filter(Produto.id == item.fk_cp_produto_id).first()
            if not produto:
                continue
            
            imagem = db.query(ImagemProduto).filter(
                ImagemProduto.fk_imag_produto_id == item.fk_cp_produto_id,
                ImagemProduto.ordem == 1
            ).first()

            subtotal = round(float(produto.preco) * item.quantidade, 2)
            total += subtotal

            itens_response.append(ItemCarrinhoResponse(
                id=item.fk_cp_produto_id,
                produto_id=item.fk_cp_produto_id,
                produto_nome=produto.nome,
                produto_preco=float(produto.preco),
                quantidade=item.quantidade,
                subtotal=subtotal,
                imagem_url=imagem.url_img if imagem else None
            ))
        
        resposta.append(CarrinhoPedidoResponse(
            id=pedido.id,
            itens=itens_response,
            total=round(total, 2),
            status=pedido.status,
            data_adicao=pedido.data_adicao
        ))

    return resposta