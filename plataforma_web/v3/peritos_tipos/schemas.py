"""
Peritos - Tipos v3, esquemas de pydantic
"""
from pydantic import BaseModel, ConfigDict

from lib.schemas_base import OneBaseOut


class PeritoTipoOut(BaseModel):
    """Esquema para entregar tipos de peritos"""

    id: int | None
    nombre: str | None
    model_config = ConfigDict(from_attributes=True)


class OnePeritoTipoOut(PeritoTipoOut, OneBaseOut):
    """Esquema para entregar un tipo de perito"""
