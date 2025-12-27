from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from typing import List
from jose import JWTError, jwt
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm

# Importações internas
from . import models, schemas, database, auth, crud
from .database import engine, SessionLocal

# Inicializa as tabelas
models.Base.metadata.create_all(bind=engine)

app = FastAPI(title="MeuDinheiro API")

# --- CONFIGURAÇÃO DE CORS ---
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "http://127.0.0.1:5173","https://controlacustosf.onrender.com"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

# --- DEPENDÊNCIAS ---

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def get_current_user(db: Session = Depends(get_db), token: str = Depends(oauth2_scheme)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Token inválido ou sessão expirada",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, auth.SECRET_KEY, algorithms=[auth.ALGORITHM])
        email: str = payload.get("sub")
        if email is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception
    
    user = crud.get_user_by_email(db, email=email)
    if user is None:
        raise credentials_exception
    return user

# --- ROTAS DE AUTENTICAÇÃO ---

@app.post("/register", response_model=schemas.User, status_code=status.HTTP_201_CREATED)
def register(user: schemas.UserCreate, db: Session = Depends(get_db)):
    db_user = crud.get_user_by_email(db, email=user.email)
    if db_user:
        raise HTTPException(status_code=400, detail="Este e-mail já está cadastrado.")
    return crud.create_user(db=db, user=user)

@app.post("/token", response_model=schemas.Token)
def login(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    user = crud.get_user_by_email(db, email=form_data.username)
    if not user or not auth.verify_password(form_data.password, user.hashed_password):
        raise HTTPException(status_code=401, detail="E-mail ou senha incorretos.")
    
    access_token = auth.create_access_token(data={"sub": user.email})
    return {"access_token": access_token, "token_type": "bearer"}

# --- ROTAS DE CATEGORIAS ---

@app.get("/categories/", response_model=List[schemas.Category])
def read_categories(db: Session = Depends(get_db), current_user: models.User = Depends(get_current_user)):
    return crud.get_categories(db, user_id=current_user.id)

@app.post("/categories/", response_model=schemas.Category)
def create_category(category: schemas.CategoryCreate, db: Session = Depends(get_db), current_user: models.User = Depends(get_current_user)):
    return crud.create_category(db=db, category=category, user_id=current_user.id)

@app.put("/categories/{category_id}", response_model=schemas.Category)
def update_category(category_id: int, category: schemas.CategoryCreate, db: Session = Depends(get_db), current_user: models.User = Depends(get_current_user)):
    db_category = crud.update_category(db, category_id, category, current_user.id)
    if not db_category:
        raise HTTPException(status_code=404, detail="Categoria não encontrada")
    return db_category

@app.delete("/categories/{category_id}")
def delete_category(category_id: int, db: Session = Depends(get_db), current_user: models.User = Depends(get_current_user)):
    success = crud.delete_category(db, category_id, current_user.id)
    if not success:
        raise HTTPException(status_code=404, detail="Categoria não encontrada")
    return {"message": "Categoria removida com sucesso"}

# --- ROTAS DE TRANSAÇÕES ---

@app.get("/transactions/", response_model=List[schemas.Transaction])
def read_transactions(db: Session = Depends(get_db), current_user: models.User = Depends(get_current_user)):
    return crud.get_transactions(db, user_id=current_user.id)

@app.post("/transactions/", response_model=schemas.Transaction)
def create_transaction(transaction: schemas.TransactionCreate, db: Session = Depends(get_db), current_user: models.User = Depends(get_current_user)):
    return crud.create_transaction(db, transaction, current_user.id)

@app.delete("/transactions/{transaction_id}")
def delete_transaction(transaction_id: int, db: Session = Depends(get_db), current_user: models.User = Depends(get_current_user)):
    db_trans = crud.delete_transaction(db, transaction_id, current_user.id)
    if not db_trans:
        raise HTTPException(status_code=404, detail="Transação não encontrada")
    return {"message": "Transação removida com sucesso"}

# --- RESUMO FINANCEIRO ---

@app.get("/summary/")
def get_summary(db: Session = Depends(get_db), current_user: models.User = Depends(get_current_user)):
    transactions = crud.get_transactions(db, user_id=current_user.id)
    income = sum(t.amount for t in transactions if t.type == "income")
    expense = sum(t.amount for t in transactions if t.type == "expense")
    return {
        "balance": round(income - expense, 2),
        "income": round(income, 2),
        "expense": round(expense, 2)
    }

# --- ROTAS DE PESSOAS (ABAS) ---

@app.get("/people/", response_model=List[schemas.Person])
def read_people(db: Session = Depends(get_db), current_user: models.User = Depends(get_current_user)):
    return crud.get_people(db, user_id=current_user.id)

@app.post("/people/", response_model=schemas.Person)
def create_person(person: schemas.PersonCreate, db: Session = Depends(get_db), current_user: models.User = Depends(get_current_user)):
    return crud.create_person(db, person, user_id=current_user.id)

@app.delete("/people/{person_id}")
def delete_person(person_id: int, db: Session = Depends(get_db), current_user: models.User = Depends(get_current_user)):
    if not crud.delete_person(db, person_id, current_user.id):
        raise HTTPException(status_code=404, detail="Pessoa não encontrada")
    return {"message": "Pessoa e histórico removidos"}

# --- ROTAS DE COMPRAS ---

@app.post("/people/{person_id}/purchases/", response_model=schemas.CardPurchase)
def add_purchase_to_person(person_id: int, purchase: schemas.CardPurchaseCreate, db: Session = Depends(get_db), current_user: models.User = Depends(get_current_user)):
    # Verifica se a pessoa pertence ao usuário logado
    person = db.query(models.Person).filter(models.Person.id == person_id, models.Person.user_id == current_user.id).first()
    if not person:
        raise HTTPException(status_code=404, detail="Pessoa não encontrada")
    return crud.create_card_purchase(db, purchase, person_id=person_id)

@app.delete("/purchases/{purchase_id}")
def delete_card_purchase(purchase_id: int, db: Session = Depends(get_db), current_user: models.User = Depends(get_current_user)):
    if not crud.delete_card_purchase(db, purchase_id):
        raise HTTPException(status_code=404, detail="Compra não encontrada")
    return {"message": "Lançamento removido"}

@app.put("/people/{person_id}", response_model=schemas.Person)
def update_person(person_id: int, person: schemas.PersonCreate, db: Session = Depends(get_db)):
    db_person = db.query(models.Person).filter(models.Person.id == person_id).first()
    if not db_person:
        raise HTTPException(status_code=404, detail="Pessoa não encontrada")
    db_person.name = person.name
    db.commit()
    db.refresh(db_person)
    return db_person


# No main.py, adicione esta rota:
@app.get("/people/{person_id}/purchases/", response_model=List[schemas.CardPurchase])
def read_person_purchases(person_id: int, db: Session = Depends(get_db), current_user: models.User = Depends(get_current_user)):
    # Verifica se a pessoa pertence ao usuário logado para segurança
    person = db.query(models.Person).filter(models.Person.id == person_id, models.Person.user_id == current_user.id).first()
    if not person:
        raise HTTPException(status_code=404, detail="Pessoa não encontrada")
    
    # Retorna as compras vinculadas a essa pessoa
    return db.query(models.CardPurchase).filter(models.CardPurchase.person_id == person_id).all()