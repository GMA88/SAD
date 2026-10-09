from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# Archivo de base de datos local SQLite
SQLALCHEMY_DATABASE_URL = "sqlite:///./erp_database.db"

# Para PostgreSQL (que usaríamos en producción) sería algo así:
# SQLALCHEMY_DATABASE_URL = "postgresql://usuario:password@localhost/erp_db"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL, 
    connect_args={"check_same_thread": False} # Solo necesario para SQLite
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
