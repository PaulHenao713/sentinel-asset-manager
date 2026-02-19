from pydantic import BaseModel
from typing import Optional
from datetime import datetime

#1. base: lo que tendran en común al crear y al leer

class AssetBase(BaseModel):
    hostname: str
    ip_address: str
    os_type: str
    risk_level: str 

#2. aqui se utiliza create para poder crear lo necesario:
class AssetCreate(AssetBase):
    pass

#3. response lo que vamos a devolverle al usuiario que incluira fecha y ID 
class AssetResponse(AssetBase):
    id : int
    last_scan: Optional[datetime] = None

    class Config:
    #esto permitira a pydantic leer datos de SQLAlchemy (modo ORM)
        from_attributes: True