"""
Distritos v3, esquemas de pydantic
"""
from pydantic import BaseModel, ConfigDict

from lib.schemas_base import OneBaseOut


class DistritoOut(BaseModel):
    """Esquema para entregar distritos"""

    id: int | None
    clave: str | None
    nombre: str | None
    nombre_corto: str | None
    es_distrito_judicial: bool | None
    es_distrito: bool | None
    es_jurisdiccional: bool | None
    model_config = ConfigDict(from_attributes=True)


class OneDistritoOut(DistritoOut, OneBaseOut):
    """Esquema para entregar un distrito"""
