"""
Glosas v3, rutas (paths)
"""
from datetime import date

from fastapi import APIRouter, HTTPException, status
from fastapi_pagination.ext.sqlalchemy import paginate

from lib.database import DatabaseSession
from lib.exceptions import MyAnyError
from lib.fastapi_pagination_custom_page import CustomPage, custom_page_success_false

from ...core.permisos.models import Permiso
from ..usuarios.authentications import CurrentUser

from .crud import get_glosas, get_glosa
from .schemas import GlosaOut, OneGlosaOut

glosas = APIRouter(prefix="/v3/glosas", tags=["glosas"])


@glosas.get("", response_model=CustomPage[GlosaOut])
async def listado_glosas(
    current_user: CurrentUser,
    db: DatabaseSession,
    autoridad_id: int = None,
    autoridad_clave: str = None,
    expediente: str = None,
    anio: int = None,
    fecha: date = None,
):
    """Listado de glosas"""
    if current_user.permissions.get("GLOSAS", 0) < Permiso.VER:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Forbidden")
    try:
        resultados = get_glosas(
            db=db,
            autoridad_id=autoridad_id,
            autoridad_clave=autoridad_clave,
            expediente=expediente,
            anio=anio,
            fecha=fecha,
        )
    except MyAnyError as error:
        return custom_page_success_false(error)
    return paginate(resultados)


@glosas.get("/{glosa_id}", response_model=OneGlosaOut)
async def detalle_glosa(
    current_user: CurrentUser,
    db: DatabaseSession,
    glosa_id: int,
):
    """Detalle de una glosa a partir de su id"""
    if current_user.permissions.get("GLOSAS", 0) < Permiso.VER:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Forbidden")
    try:
        glosa = get_glosa(db=db, glosa_id=glosa_id)
    except MyAnyError as error:
        return OneGlosaOut(success=False, message=str(error))
    return OneGlosaOut.from_orm(glosa)
