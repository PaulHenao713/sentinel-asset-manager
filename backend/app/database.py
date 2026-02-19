from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

#se crea el archivo de la base de datos en la raiz del backend

SQLALCHAMY_DATABASE_URL = "sqlite:///./database.db"


#El motor de la bse de datos
engine = create_engine(
    SQLALCHAMY_DATABASE_URL, connect_args={"check_same_thread": False}
    )
# sesion para interactuar con la DB 

SessionLocal = sessionmaker(autocommit=False, autoflush= False, bind=engine)

#clase base para los modelos 
Base = declarative_base()
