"""
Audiencias v3, CRUD (create, read, update, and delete)
"""
from datetime import date, datetime
from typing import Any

from sqlalchemy.orm import Session

from lib.exceptions import MyIsDeletedError, MyNotExistsError, MyNotValidParamError

from ...core.audiencias.models import Audiencia
from ...core.autoridades.models import Autoridad
from ..autoridades.crud import get_autoridad, get_autoridad_with_clave
from ..distritos.crud import get_distrito, get_distrito_with_clave


def get_audiencias(
    db: Session,
    autoridad_id: int = None,
    autoridad_clave: str = None,
    distrito_id: int = None,
    distrito_clave: str = None,
    anio: int = None,
    fecha: date = None,
) -> Any:
    """Consultar las audiencias activas"""
    consulta = db.query(Audiencia)
    if autoridad_id is not None:
        autoridad = get_autoridad(db, autoridad_id)
        consulta = consulta.filter_by(autoridad_id=autoridad.id)
    elif autoridad_clave is not None:
        autoridad = get_autoridad_with_clave(db, autoridad_clave)
        consulta = consulta.filter_by(autoridad_id=autoridad.id)
    elif distrito_id is not None:
        distrito = get_distrito(db, distrito_id)
        consulta = consulta.join(Autoridad).filter(Autoridad.distrito_id == distrito.id)
    elif distrito_clave is not None:
        distrito = get_distrito_with_clave(db, distrito_clave)
        consulta = consulta.join(Autoridad).filter(Autoridad.distrito_id == distrito.id)
    if fecha is not None:
        desde = datetime(year=fecha.year, month=fecha.month, day=fecha.day, hour=0, minute=0, second=0)
        hasta = datetime(year=fecha.year, month=fecha.month, day=fecha.day, hour=23, minute=59, second=59)
        consulta = consulta.filter(Audiencia.tiempo >= desde).filter(Audiencia.tiempo <= hasta)
    elif anio is not None:
        desde = datetime(year=anio, month=1, day=1, hour=0, minute=0, second=0)
        hasta = datetime(year=anio, month=12, day=31, hour=23, minute=59, second=59)
        consulta = consulta.filter(Audiencia.tiempo >= desde).filter(Audiencia.tiempo <= hasta)
    return consulta.filter_by(estatus="A").order_by(Audiencia.id)


def get_audiencia(db: Session, audiencia_id: int) -> Audiencia:
    """Consultar una audiencia por su id"""
    audiencia = db.query(Audiencia).get(audiencia_id)
    if audiencia is None:
        raise MyNotExistsError("No existe esa audiencia")
    if audiencia.estatus != "A":
        raise MyIsDeletedError("No es activa ese audiencia, está eliminada")
    return audiencia


def create_audiencia(db: Session, audiencia: Audiencia) -> Audiencia:
    """Crear una audiencia"""

    # Validar autoridad
    get_autoridad(db, audiencia.autoridad_id)

    # Guardar
    db.add(audiencia)
    db.commit()
    db.refresh(audiencia)

    # Entregar
    return audiencia


def update_audiencia(db: Session, audiencia_id: int, audiencia_in: Audiencia) -> Audiencia:
    """Modificar una audiencia"""

    # Consultar audiencia
    audiencia = get_audiencia(db, audiencia_id)

    # Validar autoridad, si se especificó y se cambió
    if audiencia_in.autoridad_id is not None and audiencia.autoridad_id != audiencia_in.autoridad_id:
        autoridad = get_autoridad(db, audiencia_in.autoridad_id)
        audiencia.autoridad_id = autoridad.autoridad_id

    # Actualizar las columnas
    audiencia.tiempo = audiencia_in.tiempo
    audiencia.tipo_audiencia = audiencia_in.tipo_audiencia
    audiencia.expediente = audiencia_in.expediente
    audiencia.actores = audiencia_in.actores
    audiencia.demandados = audiencia_in.demandados
    audiencia.sala = audiencia_in.sala
    audiencia.caracter = audiencia_in.caracter
    audiencia.causa_penal = audiencia_in.causa_penal
    audiencia.delitos = audiencia_in.delitos
    audiencia.toca = audiencia_in.toca
    audiencia.expediente_origen = audiencia_in.expediente_origen
    audiencia.imputados = audiencia_in.imputados
    audiencia.origen = audiencia_in.origen

    # Guardar
    db.add(audiencia)
    db.commit()
    db.refresh(audiencia)

    # Entregar
    return audiencia


def delete_audiencia(db: Session, audiencia_id: int) -> Audiencia:
    """Borrar una audiencia"""
    audiencia = get_audiencia(db, audiencia_id)
    audiencia.estatus = "B"
    db.add(audiencia)
    db.commit()
    db.refresh(audiencia)
    return audiencia
