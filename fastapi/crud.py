from sqlalchemy.orm import Session, session

import model
import schemas

def get_user(db:session,user_id=int):
    return db.query(model.User).filter(model.User.id == user_id).first()

def get_user_by_email(db:session,email:str):
    return db.query(model.User).filter(model.User.email == email).first()

def get_users(db:session,skip:int = 0,limit: int = 100):
    return db.query(model.User).offset(skip).limit(limit).all()

def create_user(db: Session, user: schemas.UserCreate):
    db_user = model.User(name=user.name, email=user.email)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

