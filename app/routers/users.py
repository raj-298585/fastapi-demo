from fastapi import APIRouter, Depends, HTTPException
from ..database import schemas, database, crud
from sqlalchemy.orm import Session

router = APIRouter()

@router.post("/users/", response_model=schemas.User)
def create_user(user: schemas.UserCreate, db: Session = Depends(database.get_db)):
    db_user = crud.get_user_by_email(db, email=user.email)
    if db_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    return crud.create_user(db=db, user=user)

@router.get("/users/", tags=["users"], response_model=list[schemas.User])
async def read_users(skip: int = 0, limit: int = 100, db: Session = Depends(database.get_db)):
    # return [{"username": "Rick"}, {"username": "Morty"}]
    users = crud.get_users(db, skip=skip, limit=limit)
    return users


@router.get("/users/me", tags=["users"])
async def read_user_me():
    return {"username": "fakecurrentuser"}


@router.get("/users/{username}", tags=["users"])
async def read_user(username: str):
    return {"username": username}
