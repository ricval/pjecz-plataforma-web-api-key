"""
Roles v3, esquemas de pydantic
"""
from pydantic import BaseModel, ConfigDict

from lib.schemas_base import OneBaseOut


class RolOut(BaseModel):
    """Esquema para entregar roles"""

    id: int | None
    nombre: str | None
    model_config = ConfigDict(from_attributes=True)


class OneRolOut(RolOut, OneBaseOut):
    """Esquema para entregar un rol"""
