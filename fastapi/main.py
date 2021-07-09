from fastapi import Depends, FastAPI, HTTPException
from sqlalchemy.orm import Session, session
from starlette.middleware.cors import CORSMiddleware
from typing import List
from db import SessionLocal

import crud
import schemas

app = FastAPI()

#: Configure CORS
origins = [
    "http://localhost:8080",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.get("/users/",response_model=List[schemas.User])
def read_users(skip:int = 0, limit:int = 100,db:session = Depends(get_db)):
    users = crud.get_users(db,skip=skip,limit=limit)
    return users

@app.get("/users/{user_id}",response_model=schemas.User)
def read_user(user_id:int,db: session = Depends(get_db)):
    db_user = crud.get_user(db,user_id=user_id)
    if db_user is None:
        raise HTTPException(status_code=404,detail="user not found")
    return db_user

@app.post("/users/",response_model=schemas.User)
def create_user(user:schemas.UserCreate,db:session=Depends(get_db)):
    db_user = crud.get_user_by_email(db,email=user.email)
    if db_user:
        raise HTTPException(status_code=400,detail="email already")
    return crud.create_user(db=db,user=user)

@app.put("/users/{user_id}",response_model=schemas.User)
def create_user(user_id:int,user:schemas.UserCreate,db:session=Depends(get_db)):
    db_user = crud.get_user(db,user_id=user_id)
    db_user.name = user.name
    db_user.email = user.email
    db.commit()
    db_user = crud.get_user(db,user_id=user_id)
    return db_user

@app.delete("/users/{user_id}",response_model=schemas.User)
def create_user(user_id:int,user:schemas.UserCreate,db:session=Depends(get_db)):
    db_user = crud.get_user(db,user_id=user_id)
    db.delete(db_user)
    db.commit()
    return db_user
