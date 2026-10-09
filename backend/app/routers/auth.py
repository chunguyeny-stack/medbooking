from app.auth import (
    create_access_token,
    get_current_user,
    get_password_hash,
    verify_password,
)
from app.database import get_db
from fastapi import APIRouter, Depends, HTTPException, status
from app.models import NguoiDung
from app.schemas import Token, UserCreate, UserLogin
from sqlalchemy.orm import Session

router = APIRouter(prefix="/auth", tags=["Authentication"])


@router.post("/register", status_code=status.HTTP_201_CREATED)
def register(user_data: UserCreate, db: Session = Depends(get_db)):
  existing = (
      db.query(NguoiDung)
      .filter(
          (NguoiDung.username == user_data.username)
          | (NguoiDung.email == user_data.email)
      )
      .first()
  )
  if existing:
    raise HTTPException(status_code=400, detail="Username hoặc email đã tồn tại")

  new_user = NguoiDung(
      username=user_data.username,
      email=user_data.email,
      hashed_password=get_password_hash(user_data.password),
      role=user_data.role,
  )
  db.add(new_user)
  db.commit()
  db.refresh(new_user)
  return {"message": "Đăng ký thành công", "user_id": new_user.id}


@router.post("/login", response_model=Token)
def login(form_data: UserLogin, db: Session = Depends(get_db)):
  user = (
      db.query(NguoiDung)
      .filter(NguoiDung.username == form_data.username)
      .first()
  )
  if not user or not verify_password(form_data.password, user.hashed_password):
    raise HTTPException(status_code=401, detail="Sai username hoặc password")

  token = create_access_token(data={"sub": user.username, "role": user.role})
  return {"access_token": token, "token_type": "bearer"}


@router.get("/me")
def get_me(current_user: NguoiDung = Depends(get_current_user)):
  return {
      "id": current_user.id,
      "username": current_user.username,
      "email": current_user.email,
      "role": current_user.role,
  }