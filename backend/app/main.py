from fastapi.middleware.cors import CORSMiddleware
from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from datetime import datetime

from . import models, schemas
from .database import engine, SessionLocal

#aqui se crea las trablas en la base de datos automaticamente si es que no existen

models.Base.metadata.create_all(bind=engine)
app = FastAPI(title="Sentinel Inventory API", version="0.1.0")


app.add_middleware(
    CORSMiddleware,
    allow_origins= ["*"], #aqui se visualiza a futuro para producción y cambiarlo por la url real
    allow_credentials=True,
    allow_methods=["*"], #aqui se permite get, post, put, delete
    allow_headers=["*"]

)

# Dependencias para obtener la DB 
#aqui se abre una conexion segura por cada petición que llegue y la cierra al terminar
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.get("/")
def read_root():
    return{"status":"Online","message":"Sentinel Inventory System is running"}

#1ra ruta: Crear un activo (POST)
@app.post("/assets/", response_model=schemas.AssetResponse)
def create_asset(asset: schemas.AssetCreate, db: Session = Depends(get_db)):
    # 1. Buscamos si ya existe
    existing_asset = db.query(models.SecurityAsset).filter(models.SecurityAsset.ip_address == asset.ip_address).first()
    
    if existing_asset:
        # LÓGICA DE ACTUALIZACIÓN (AUTOMATIZACIÓN)
        existing_asset.hostname = asset.hostname
        existing_asset.os_type = asset.os_type
        existing_asset.risk_level = asset.risk_level
        existing_asset.last_scan = datetime.utcnow() # Actualizamos la fecha
        
        db.commit()
        db.refresh(existing_asset)
        return existing_asset
    else:
        # LÓGICA DE CREACIÓN (COMO ANTES)
        new_asset = models.SecurityAsset(
            hostname=asset.hostname,
            ip_address=asset.ip_address,
            os_type=asset.os_type,
            risk_level=asset.risk_level,
            last_scan=datetime.utcnow()
        )
        db.add(new_asset)
        db.commit()
        db.refresh(new_asset)
        return new_asset

#2da ruta: listar los archivos (GET)
@app.get("/assets/", response_model=List[schemas.AssetResponse])
def read_assets(skip: int=0, limit: int =100, db:Session = Depends(get_db)):
    assets = db.query(models.SecurityAsset).offset(skip).limit(limit).all()
    return assets