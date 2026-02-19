from sqlalchemy import Column, Integer, String, DateTime
from datetime import datetime
from .database import Base  # <--- Esta línea es la que falta o tiene error

class SecurityAsset(Base):
    __tablename__ = "assets"

    id = Column(Integer, primary_key=True, index=True)
    hostname = Column(String, index=True)
    ip_address = Column(String, unique=True)
    os_type = Column(String)
    risk_level = Column(String)
    last_scan = Column(DateTime, default=datetime.utcnow)