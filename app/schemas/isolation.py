import datetime
from pydantic import BaseModel, Field
from typing import Optional

class IsolationBase(BaseModel):
    id_incidente_gallina : int
    fecha_hora: datetime.datetime
    id_galpon: int

class IsolationCreate(IsolationBase):
    pass

class IsolationUpdate(BaseModel):
    id_incidente_gallina: Optional[int] = None
    fecha_hora: Optional[datetime.datetime] = None
    id_galpon: Optional[int] = None
    

class IsolationEstado(BaseModel):
    pass

class IsolationOut(IsolationBase):
    id_aislamiento: int
    nombre: str
