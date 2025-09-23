from pydantic import BaseModel, Field
from typing import Optional


class EstateBase(BaseModel):
    nombre_finca: str = Field(min_length=3, max_length=70)
    longitud: float
    latitud: float
    id_usuario: int
    estado_finca: bool

class EstateCreate(EstateBase):
    pass

class EstateUpdate(BaseModel):
    nombre_finca: Optional[str] = Field(default=None, min_length=3, max_length=70)
    longitud: Optional[float] = None
    latitud: Optional[float] = None

class EstateEstado(BaseModel):
    estado_finca: Optional[bool] = None

class EstateOut(EstateBase):
    id_finca: int
    nombre: str

