"""
Entradas-Salidas v3, esquemas de pydantic
"""
from datetime import datetime

from pydantic import BaseModel, ConfigDict

from lib.schemas_base import OneBaseOut


class EntradaSalidaOut(BaseModel):
    """Esquema para entregar entradas-salidas"""

    id: int | None
    usuario_id: int | None
    usuario_email: str | None
    usuario_nombre: str | None
    tipo: str | None
    direccion_ip: str | None
    creado: datetime | None
    model_config = ConfigDict(from_attributes=True)


class OneEntradaSalidaOut(EntradaSalidaOut, OneBaseOut):
    """Esquema para entregar una entrada-salida"""
