"""
Archivo - Juzgados Extintos v3, rutas (paths)
"""
from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi_pagination.ext.sqlalchemy import paginate

from lib.database import Session, get_db
from lib.exceptions import MyAnyError
from lib.fastapi_pagination_custom_page import CustomPage

from ...core.permisos.models import Permiso
from ..usuarios.authentications import UsuarioInDB, get_current_active_user
from .crud import get_arc_juzgado_extinto, get_arc_juzgados_extintos
from .schemas import ArcJuzgadoExtintoOut, OneArcJuzgadoExtintoOut

arc_juzgados_extintos = APIRouter(prefix="/v3/arc_juzgados_extintos", tags=["archivo"])


@arc_juzgados_extintos.get("", response_model=CustomPage[ArcJuzgadoExtintoOut])
async def listado_arc_juzgados_extintos(
    current_user: Annotated[UsuarioInDB, Depends(get_current_active_user)],
    db: Annotated[Session, Depends(get_db)],
):
    """Listado de juzgados extintos"""
    if current_user.permissions.get("ARC DOCUMENTOS", 0) < Permiso.VER:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Forbidden")
    try:
        resultados = get_arc_juzgados_extintos(db)
    except MyAnyError as error:
        return CustomPage(success=False, message=str(error))
    return paginate(resultados)


@arc_juzgados_extintos.get("/{arc_juzgado_extinto_id}", response_model=OneArcJuzgadoExtintoOut)
async def detalle_arc_juzgado_extinto(
    current_user: Annotated[UsuarioInDB, Depends(get_current_active_user)],
    db: Annotated[Session, Depends(get_db)],
    arc_juzgado_extinto_id: int,
):
    """Detalle de una juzgado extinto a partir de su id"""
    if current_user.permissions.get("ARC DOCUMENTOS", 0) < Permiso.VER:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Forbidden")
    try:
        arc_juzgado_extinto = get_arc_juzgado_extinto(db, arc_juzgado_extinto_id)
    except MyAnyError as error:
        return OneArcJuzgadoExtintoOut(success=False, message=str(error))
    return OneArcJuzgadoExtintoOut.from_orm(arc_juzgado_extinto)
