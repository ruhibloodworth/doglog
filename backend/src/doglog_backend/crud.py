from sqlalchemy.orm import Session
from argon2 import PasswordHasher

ph = PasswordHasher()

from . import models, schemas

def verify_pw(db: Session, password: str, user: models.User):
    try:
        ph.verify(user.hashed_password, password)
        
        if ph.check_needs_rehash(user.hashed_password):
            user.hashed_password = ph.hash(password)
            db.add(user)
            db.commit()
            db.refresh(user)
        return user
    except:
        return False

def get_user(db: Session, user_id: int):
    return db.query(models.User).filter(models.User.id == user_id).first()

def get_user_by_email(db: Session, email: str):
    return db.query(models.User).filter(models.User.email == email).first()

def get_users(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.User).offset(skip).limit(limit).all()

def create_user(db: Session, user: schemas.UserCreate):
    hashed_password = ph.hash(user.password)
    db_user = models.User(email=user.email, hashed_password=hashed_password)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user
