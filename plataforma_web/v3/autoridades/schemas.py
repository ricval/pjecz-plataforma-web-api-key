"""
Autoridades v3, esquemas de pydantic
"""
from pydantic import BaseModel, ConfigDict

from lib.schemas_base import OneBaseOut


class AutoridadOut(BaseModel):
    """Esquema para entregar autoridades"""

    id: int | None
    distrito_id: int | None
    distrito_clave: str | None
    distrito_nombre: str | None
    distrito_nombre_corto: str | None
    materia_id: int | None
    materia_clave: str | None
    materia_nombre: str | None
    clave: str | None
    descripcion: str | None
    descripcion_corta: str | None
    es_archivo_solicitante: bool | None
    es_cemasc: bool | None
    es_creador_glosas: bool | None
    es_defensoria: bool | None
    es_jurisdiccional: bool | None
    es_notaria: bool | None
    organo_jurisdiccional: str | None
    audiencia_categoria: str | None
    model_config = ConfigDict(from_attributes=True)


class OneAutoridadOut(AutoridadOut, OneBaseOut):
    """Esquema para entregar un autoridad"""
