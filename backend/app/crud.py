from sqlalchemy.orm import Session
from . import models, schemas, auth

# --- USUÁRIOS ---

def get_user_by_email(db: Session, email: str):
    return db.query(models.User).filter(models.User.email == email).first()

def create_user(db: Session, user: schemas.UserCreate):
    hashed_password = auth.get_password_hash(user.password)
    db_user = models.User(email=user.email, hashed_password=hashed_password)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

# --- TRANSAÇÕES (FILTRADAS POR USUÁRIO) ---

def get_transactions(db: Session, user_id: int, skip: int = 0, limit: int = 100):
    return db.query(models.Transaction)\
             .filter(models.Transaction.owner_id == user_id)\
             .order_by(models.Transaction.date.desc())\
             .offset(skip).limit(limit).all()

def create_transaction(db: Session, transaction: schemas.TransactionCreate, user_id: int):
    # model_dump() substitui o antigo .dict() no Pydantic V2
    db_transaction = models.Transaction(**transaction.model_dump(), owner_id=user_id)
    db.add(db_transaction)
    db.commit()
    db.refresh(db_transaction)
    return db_transaction

def delete_transaction(db: Session, transaction_id: int, user_id: int):
    db_item = db.query(models.Transaction).filter(
        models.Transaction.id == transaction_id, 
        models.Transaction.owner_id == user_id
    ).first()
    if db_item:
        db.delete(db_item)
        db.commit()
    return db_item

# --- CATEGORIAS (FILTRADAS POR USUÁRIO) ---

def get_categories(db: Session, user_id: int):
    return db.query(models.Category).filter(models.Category.user_id == user_id).all()

def create_category(db: Session, category: schemas.CategoryCreate, user_id: int):
    db_category = models.Category(
        name=category.name, 
        color=category.color, 
        user_id=user_id
    )
    db.add(db_category)
    db.commit()
    db.refresh(db_category)
    return db_category

def update_category(db: Session, category_id: int, category_update: schemas.CategoryCreate, user_id: int):
    db_category = db.query(models.Category).filter(
        models.Category.id == category_id, 
        models.Category.user_id == user_id
    ).first()
    
    if db_category:
        db_category.name = category_update.name
        db_category.color = category_update.color
        db.commit()
        db.refresh(db_category)
    return db_category

def delete_category(db: Session, category_id: int, user_id: int):
    db_category = db.query(models.Category).filter(
        models.Category.id == category_id, 
        models.Category.user_id == user_id
    ).first()
    if db_category:
        db.delete(db_category)
        db.commit()
        return True
    return False

# --- PESSOAS ---
def get_people(db: Session, user_id: int):
    return db.query(models.Person).filter(models.Person.user_id == user_id).all()

def create_person(db: Session, person: schemas.PersonCreate, user_id: int):
    db_person = models.Person(**person.dict(), user_id=user_id)
    db.add(db_person)
    db.commit()
    db.refresh(db_person)
    return db_person

def delete_person(db: Session, person_id: int, user_id: int):
    db_person = db.query(models.Person).filter(models.Person.id == person_id, models.Person.user_id == user_id).first()
    if db_person:
        db.delete(db_person)
        db.commit()
        return True
    return False

# --- COMPRAS NO CARTÃO ---
def create_card_purchase(db: Session, purchase: schemas.CardPurchaseCreate, person_id: int):
    db_purchase = models.CardPurchase(**purchase.dict(), person_id=person_id)
    db.add(db_purchase)
    db.commit()
    db.refresh(db_purchase)
    return db_purchase

def delete_card_purchase(db: Session, purchase_id: int):
    db_purchase = db.query(models.CardPurchase).filter(models.CardPurchase.id == purchase_id).first()
    if db_purchase:
        db.delete(db_purchase)
        db.commit()
        return True
    return False

# Adicione ao seu crud.py
def get_person_purchases(db: Session, person_id: int):
    return db.query(models.CardPurchase).filter(models.CardPurchase.person_id == person_id).all()