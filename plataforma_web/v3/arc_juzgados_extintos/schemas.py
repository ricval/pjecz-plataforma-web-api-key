"""
Archivo - Juzgados Extintos v3, esquemas de pydantic
"""
from pydantic import BaseModel, ConfigDict

from lib.schemas_base import OneBaseOut


class ArcJuzgadoExtintoOut(BaseModel):
    """Esquema para entregar juzgados extintos"""

    id: int | None
    clave: str | None
    descripcion: str | None
    descripcion_corta: str | None
    model_config = ConfigDict(from_attributes=True)


class OneArcJuzgadoExtintoOut(ArcJuzgadoExtintoOut, OneBaseOut):
    """Esquema para entregar un juzgado extinto"""
