"""
Inventarios Equipos v3, rutas (paths)
"""
from datetime import date
from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi_pagination.ext.sqlalchemy import paginate

from lib.database import Session, get_db
from lib.exceptions import MyAnyError
from lib.fastapi_pagination_custom_page import CustomPage

from ...core.permisos.models import Permiso
from ..usuarios.authentications import UsuarioInDB, get_current_active_user
from .crud import get_inv_equipo, get_inv_equipos
from .schemas import InvEquipoOut, OneInvEquipoOut

inv_equipos = APIRouter(prefix="/v3/inv_equipos", tags=["inventarios"])


@inv_equipos.get("", response_model=CustomPage[InvEquipoOut])
async def listado_inv_equipos(
    current_user: Annotated[UsuarioInDB, Depends(get_current_active_user)],
    db: Annotated[Session, Depends(get_db)],
    creado: date = None,
    creado_desde: date = None,
    creado_hasta: date = None,
    distrito_id: int = None,
    distrito_clave: str = None,
    fecha_fabricacion_desde: date = None,
    fecha_fabricacion_hasta: date = None,
    inv_custodia_id: int = None,
    inv_modelo_id: int = None,
    inv_red_id: int = None,
    oficina_id: int = None,
    oficina_clave: str = None,
    tipo: str = None,
):
    """Listado de equipos"""
    if current_user.permissions.get("INV EQUIPOS", 0) < Permiso.VER:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Forbidden")
    try:
        resultados = get_inv_equipos(
            db=db,
            creado=creado,
            creado_desde=creado_desde,
            creado_hasta=creado_hasta,
            distrito_id=distrito_id,
            distrito_clave=distrito_clave,
            fecha_fabricacion_desde=fecha_fabricacion_desde,
            fecha_fabricacion_hasta=fecha_fabricacion_hasta,
            inv_custodia_id=inv_custodia_id,
            inv_modelo_id=inv_modelo_id,
            inv_red_id=inv_red_id,
            oficina_id=oficina_id,
            oficina_clave=oficina_clave,
            tipo=tipo,
        )
    except MyAnyError as error:
        return CustomPage(success=False, message=str(error))
    return paginate(resultados)


@inv_equipos.get("/{inv_equipo_id}", response_model=OneInvEquipoOut)
async def detalle_inv_equipo(
    current_user: Annotated[UsuarioInDB, Depends(get_current_active_user)],
    db: Annotated[Session, Depends(get_db)],
    inv_equipo_id: int,
):
    """Detalle de una equipo a partir de su id"""
    if current_user.permissions.get("INV EQUIPOS", 0) < Permiso.VER:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Forbidden")
    try:
        inv_equipo = get_inv_equipo(db, inv_equipo_id)
    except MyAnyError as error:
        return OneInvEquipoOut(success=False, message=str(error))
    return OneInvEquipoOut.from_orm(inv_equipo)
