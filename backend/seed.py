from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app import models
import os

# Caminho absoluto para garantir que o banco seja encontrado dentro da pasta app
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(BASE_DIR, "app", "gastos.db")
SQLALCHEMY_DATABASE_URL = f"sqlite:///{DB_PATH}"

engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def seed():
    db = SessionLocal()
    print(f"Conectando ao banco em: {DB_PATH}")
    
    # Cria as tabelas se não existirem
    models.Base.metadata.create_all(bind=engine)

    categories = [
        {"name": "Salário", "color": "#2609b7"},
        {"name": "Alimentação", "color": "#e67e22"},
        {"name": "Transporte", "color": "#3498db"},
        {"name": "Lazer", "color": "#f1c40f"},
        {"name": "Saúde", "color": "#e74c3c"},
        {"name": "Moradia", "color": "#9b59b6"}
    ]

    for cat in categories:
        # Busca se a categoria já existe para não duplicar
        exists = db.query(models.Category).filter(models.Category.name == cat["name"]).first()
        if not exists:
            new_cat = models.Category(name=cat["name"], color=cat["color"])
            db.add(new_cat)
    
    db.commit()
    db.close()
    print("✅ Categorias iniciais sincronizadas com sucesso!")

if __name__ == "__main__":
    seed()