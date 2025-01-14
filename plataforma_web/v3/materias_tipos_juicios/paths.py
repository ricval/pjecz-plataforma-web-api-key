"""
Materias-Tipos de Juicios v3, rutas (paths)
"""
from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi_pagination.ext.sqlalchemy import paginate

from lib.database import Session, get_db
from lib.exceptions import MyAnyError
from lib.fastapi_pagination_custom_page import CustomPage

from ...core.permisos.models import Permiso
from ..usuarios.authentications import UsuarioInDB, get_current_active_user
from .crud import get_materia_tipo_juicio, get_materias_tipos_juicios
from .schemas import MateriaTipoJuicioOut, OneMateriaTipoJuicioOut

materias_tipos_juicios = APIRouter(prefix="/v3/materias_tipos_juicios", tags=["materias"])


@materias_tipos_juicios.get("", response_model=CustomPage[MateriaTipoJuicioOut])
async def listado_materias_tipos_juicios(
    current_user: Annotated[UsuarioInDB, Depends(get_current_active_user)],
    db: Annotated[Session, Depends(get_db)],
    materia_id: int = None,
    materia_clave: str = None,
):
    """Listado de materias-tipos de juicios"""
    if current_user.permissions.get("MATERIAS TIPOS JUICIOS", 0) < Permiso.VER:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Forbidden")
    try:
        resultados = get_materias_tipos_juicios(
            db=db,
            materia_id=materia_id,
            materia_clave=materia_clave,
        )
    except MyAnyError as error:
        return CustomPage(success=False, message=str(error))
    return paginate(resultados)


@materias_tipos_juicios.get("/{materia_tipo_juicio_id}", response_model=OneMateriaTipoJuicioOut)
async def detalle_materia_tipo_juicio(
    current_user: Annotated[UsuarioInDB, Depends(get_current_active_user)],
    db: Annotated[Session, Depends(get_db)],
    materia_tipo_juicio_id: int,
):
    """Detalle de una materia-tipo de juicio a partir de su id"""
    if current_user.permissions.get("MATERIAS TIPOS JUICIOS", 0) < Permiso.VER:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Forbidden")
    try:
        materia_tipo_juicio = get_materia_tipo_juicio(db, materia_tipo_juicio_id)
    except MyAnyError as error:
        return OneMateriaTipoJuicioOut(success=False, message=str(error))
    return OneMateriaTipoJuicioOut.from_orm(materia_tipo_juicio)
