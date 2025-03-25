from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import TIMESTAMP
from sqlalchemy.sql.functions import current_timestamp
from sqlalchemy.orm import Session

from app.schemas.usuario import UsuarioLogin, UsuarioCreate
from app.models.usuario import Usuario
from app.core.security import criar_token_jwt, verificar_senha, hash_senha
from app.database import get_db

router = APIRouter(prefix="/auth", tags=["Autenticação"])

@router.post("/login", response_model=dict)
async def login(credenciais, UsuarioLogin, db: Session = Depends(get_db)):
    usuario = db.query(Usuario).filter(Usuario.email == credenciais.email).first()

    if not usuario or not verificar_senha(credenciais.senha, usuario.senha):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Email ou senha incorretos",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    token = criar_token_jwt({"sub": usuario.email, "tipo": usuario.tipo})

    return {"access_token": token, "token_type": "bearer"}

@router.post("/cadastrar", status_code=status.HTTP_201_CREATED)
async def cadastrar(usuario, UsuarioCreate, db: Session = Depends(get_db)):
    if db.query(Usuario).filter(Usuario.email == usuario.email).first():
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email já cadastrado.",
        )
    
    db_usuario = Usuario (
        nome=usuario.nome,
        email=usuario.email,
        senha=hash_senha(usuario.senha),
        tipo=usuario.tipo,
        telefone=usuario.telefone,
        data_cadastro=current_timestamp()
    )

    db.add(db_usuario)
    db.commit()
    db.refresh(db_usuario)

    return {"mensagem": "Usuário criado com sucesso", "id": db_usuario.id}
