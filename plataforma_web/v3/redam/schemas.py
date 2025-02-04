"""
REDAM (Registro Estatal de Deudores Alimentarios Morosos) v3, esquemas de pydantic
"""
from datetime import date

from pydantic import BaseModel, ConfigDict

from lib.schemas_base import OneBaseOut


class RedamOut(BaseModel):
    """Esquema para entregar deudores alimentarios morosos"""

    id: int | None
    distrito_id: int | None
    distrito_clave: str | None
    distrito_nombre: str | None
    distrito_nombre_corto: str | None
    autoridad_id: int | None
    autoridad_clave: str | None
    autoridad_descripcion: str | None
    autoridad_descripcion_corta: str | None
    nombre: str | None
    expediente: str | None
    fecha: date | None
    observaciones: str | None
    model_config = ConfigDict(from_attributes=True)


class OneRedamOut(RedamOut, OneBaseOut):
    """Esquema para entregar un deudor alimentario moroso"""
