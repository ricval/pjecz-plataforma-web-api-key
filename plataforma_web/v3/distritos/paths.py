"""
Distritos v3, rutas (paths)
"""
from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi_pagination.ext.sqlalchemy import paginate

from lib.database import Session, get_db
from lib.exceptions import MyAnyError
from lib.fastapi_pagination_custom_page import CustomPage

from ...core.permisos.models import Permiso
from ..usuarios.authentications import UsuarioInDB, get_current_active_user
from .crud import get_distrito_with_clave, get_distritos
from .schemas import DistritoOut, OneDistritoOut

distritos = APIRouter(prefix="/v3/distritos", tags=["distritos"])


@distritos.get("", response_model=CustomPage[DistritoOut])
async def listado_distritos(
    current_user: Annotated[UsuarioInDB, Depends(get_current_active_user)],
    db: Annotated[Session, Depends(get_db)],
    es_distrito_judicial: bool = None,
    es_distrito: bool = None,
    es_jurisdiccional: bool = None,
):
    """Listado de distritos"""
    if current_user.permissions.get("DISTRITOS", 0) < Permiso.VER:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Forbidden")
    try:
        resultados = get_distritos(
            db=db,
            es_distrito_judicial=es_distrito_judicial,
            es_distrito=es_distrito,
            es_jurisdiccional=es_jurisdiccional,
        )
    except MyAnyError as error:
        return CustomPage(success=False, message=str(error))
    return paginate(resultados)


@distritos.get("/{distrito_clave}", response_model=OneDistritoOut)
async def detalle_distrito(
    current_user: Annotated[UsuarioInDB, Depends(get_current_active_user)],
    db: Annotated[Session, Depends(get_db)],
    distrito_clave: str,
):
    """Detalle de una distrito a partir de su clave"""
    if current_user.permissions.get("DISTRITOS", 0) < Permiso.VER:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Forbidden")
    try:
        distrito = get_distrito_with_clave(db, distrito_clave)
    except MyAnyError as error:
        return OneDistritoOut(success=False, message=str(error))
    return OneDistritoOut.from_orm(distrito)
