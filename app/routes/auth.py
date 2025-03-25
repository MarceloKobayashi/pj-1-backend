from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.schemas.usuario import UsuarioLogin, UsuarioCreate
from app.models.usuario import Usuario
from app.core.security import criar_token_jwt, verificar_senha, hash_senha
from app.database import get_db