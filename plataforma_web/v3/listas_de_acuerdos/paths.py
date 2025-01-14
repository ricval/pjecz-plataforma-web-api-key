"""
Listas de Acuerdos v3, rutas (paths)
"""
from datetime import date
from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi_pagination.ext.sqlalchemy import paginate

from lib.database import Session, get_db
from lib.exceptions import MyAnyError
from lib.fastapi_pagination_custom_page import CustomPage

from ...core.listas_de_acuerdos.models import ListaDeAcuerdo
from ...core.permisos.models import Permiso
from ..usuarios.authentications import UsuarioInDB, get_current_active_user
from .crud import create_lista_de_acuerdo, delete_lista_de_acuerdo, get_lista_de_acuerdo, get_listas_de_acuerdos, update_lista_de_acuerdo
from .schemas import ListaDeAcuerdoIn, ListaDeAcuerdoOut, OneListaDeAcuerdoOut

listas_de_acuerdos = APIRouter(prefix="/v3/listas_de_acuerdos", tags=["listas de acuerdos"])


@listas_de_acuerdos.get("", response_model=CustomPage[ListaDeAcuerdoOut])
async def listado_listas_de_acuerdos(
    current_user: Annotated[UsuarioInDB, Depends(get_current_active_user)],
    db: Annotated[Session, Depends(get_db)],
    autoridad_id: int = None,
    autoridad_clave: str = None,
    distrito_id: int = None,
    distrito_clave: str = None,
    anio: int = None,
    fecha: date = None,
    fecha_desde: date = None,
    fecha_hasta: date = None,
):
    """Listado de listas de acuerdos"""
    if current_user.permissions.get("LISTAS DE ACUERDOS", 0) < Permiso.VER:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Forbidden")
    try:
        resultados = get_listas_de_acuerdos(
            db=db,
            autoridad_id=autoridad_id,
            autoridad_clave=autoridad_clave,
            distrito_id=distrito_id,
            distrito_clave=distrito_clave,
            anio=anio,
            fecha=fecha,
            fecha_desde=fecha_desde,
            fecha_hasta=fecha_hasta,
        )
    except MyAnyError as error:
        return CustomPage(success=False, message=str(error))
    return paginate(resultados)


@listas_de_acuerdos.get("/{lista_de_acuerdo_id}", response_model=OneListaDeAcuerdoOut)
async def detalle_lista_de_acuerdo(
    current_user: Annotated[UsuarioInDB, Depends(get_current_active_user)],
    db: Annotated[Session, Depends(get_db)],
    lista_de_acuerdo_id: int,
):
    """Detalle de una lista de acuerdo a partir de su id"""
    if current_user.permissions.get("LISTAS DE ACUERDOS", 0) < Permiso.VER:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Forbidden")
    try:
        lista_de_acuerdo = get_lista_de_acuerdo(db, lista_de_acuerdo_id)
    except MyAnyError as error:
        return OneListaDeAcuerdoOut(success=False, message=str(error))
    return OneListaDeAcuerdoOut.from_orm(lista_de_acuerdo)


@listas_de_acuerdos.post("", response_model=OneListaDeAcuerdoOut)
async def crear_lista_de_acuerdo(
    current_user: Annotated[UsuarioInDB, Depends(get_current_active_user)],
    db: Annotated[Session, Depends(get_db)],
    lista_de_acuerdo_in: ListaDeAcuerdoIn,
):
    """Crear una lista de acuerdo"""
    if current_user.permissions.get("LISTAS DE ACUERDOS", 0) < Permiso.CREAR:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Forbidden")
    try:
        lista_de_acuerdo = create_lista_de_acuerdo(db, ListaDeAcuerdo(**lista_de_acuerdo_in.dict()))
    except MyAnyError as error:
        return OneListaDeAcuerdoOut(success=False, message=str(error))
    respuesta = OneListaDeAcuerdoOut.from_orm(lista_de_acuerdo)
    respuesta.message = "Lista de acuerdo creada correctamente"
    return respuesta


@listas_de_acuerdos.put("/{lista_de_acuerdo_id}", response_model=OneListaDeAcuerdoOut)
async def modificar_lista_de_acuerdo(
    current_user: Annotated[UsuarioInDB, Depends(get_current_active_user)],
    db: Annotated[Session, Depends(get_db)],
    lista_de_acuerdo_id: int,
    lista_de_acuerdo_in: ListaDeAcuerdoIn,
):
    """Modificar una lista de acuerdo"""
    if current_user.permissions.get("LISTAS DE ACUERDOS", 0) < Permiso.MODIFICAR:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Forbidden")
    try:
        lista_de_acuerdo = update_lista_de_acuerdo(db, lista_de_acuerdo_id, ListaDeAcuerdo(**lista_de_acuerdo_in.dict()))
    except MyAnyError as error:
        return OneListaDeAcuerdoOut(success=False, message=str(error))
    respuesta = OneListaDeAcuerdoOut.from_orm(lista_de_acuerdo)
    respuesta.message = "Lista de acuerdo modificada correctamente"
    return respuesta


@listas_de_acuerdos.delete("/{lista_de_acuerdo_id}", response_model=OneListaDeAcuerdoOut)
async def borrar_lista_de_acuerdo(
    current_user: Annotated[UsuarioInDB, Depends(get_current_active_user)],
    db: Annotated[Session, Depends(get_db)],
    lista_de_acuerdo_id: int,
):
    """Borrar una lista de acuerdo"""
    if current_user.permissions.get("LISTAS DE ACUERDOS", 0) < Permiso.BORRAR:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Forbidden")
    try:
        lista_de_acuerdo = delete_lista_de_acuerdo(db, lista_de_acuerdo_id)
    except MyAnyError as error:
        return OneListaDeAcuerdoOut(success=False, message=str(error))
    respuesta = OneListaDeAcuerdoOut.from_orm(lista_de_acuerdo)
    respuesta.message = "Lista de Acuerdo borrada correctamente"
    return respuesta
