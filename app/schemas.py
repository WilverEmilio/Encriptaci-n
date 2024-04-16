from pydantic import BaseModel
from typing import Optional

class Datos(BaseModel):
    idingreso: Optional[int]
    usuario: str
    contrasena: str
    correo_electronico: str
    
    class Config:
        orm_mode = True
        
class Crear_Usuario(BaseModel):
    usuario: str
    contrasena: str
    correo_electronico: str

    class Config:
        orm_mode = True
        
class Ingreso(BaseModel):
    usuario: str
    contrasena: str

    class Config:
        orm_mode = True