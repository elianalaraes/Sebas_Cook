import os


class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'dev-key-sebas-cook'

    # 1. Obtener la URL de entorno o usar la base local SQLite
    db_url = os.environ.get('DATABASE_URL') or 'sqlite:///sebas_cook.db'

    # 2. Corregir prefijo para SQLAlchemy en caso de desplegar en Render / Heroku / Azure
    if db_url.startswith("postgres://"):
        db_url = db_url.replace("postgres://", "postgresql://", 1)

    SQLALCHEMY_DATABASE_URI = db_url
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # Se recomienda desactivar estos flags en producción por seguridad
    DEBUG = False
    TESTING = False

