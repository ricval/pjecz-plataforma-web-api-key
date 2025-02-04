"""
Materias-Tipos de Juicios v3, esquemas de pydantic
"""
from pydantic import BaseModel, ConfigDict

from lib.schemas_base import OneBaseOut


class MateriaTipoJuicioOut(BaseModel):
    """Esquema para entregar materias-tipos de juicios"""

    id: int | None
    materia_id: int | None
    materia_clave: str | None
    materia_nombre: str | None
    descripcion: str | None
    model_config = ConfigDict(from_attributes=True)


class OneMateriaTipoJuicioOut(MateriaTipoJuicioOut, OneBaseOut):
    """Esquema para entregar un materia-tipo de juicio"""
