from fastapi import Response, status, HTTPException, Depends, APIRouter
from .. import models, schema, utils
from sqlalchemy.orm import Session
from typing import List
from ..database import get_db

router = APIRouter(
    prefix="/users",
    tags=["Users"]
)


# ----------------CREATE A USER------------------------

@router.post("/new-user", status_code=status.HTTP_201_CREATED, response_model=schema.UserResponse)
def create_user(user: schema.UserCreate, db: Session = Depends(get_db)):
    # Hash the password
    hashed_password = utils.hashed(user.password)
    user.password = hashed_password

    new_user = models.User(**user.dict())

    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user


# --------------------GET USER BY ID------------------------------------------
@router.get('/{user_id}', response_model=schema.UserResponse)
def get_user(user_id: int, db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.id == user_id).first()

    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"User with id: {user_id} does not exist")

    return user
