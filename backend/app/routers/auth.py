from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from fastapi.security import OAuth2PasswordRequestForm
from app.database.database import get_db
from app.models.models import NguoiDung, BenhNhan, BacSi
from app.schemas.schemas import UserRegister, Token, UserResponse
from app.auth import get_password_hash, verify_password, create_access_token, get_current_user

router = APIRouter(prefix="/api/auth", tags=["Auth"])

@router.post("/register", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
def register(user_data: UserRegister, db: Session = Depends(get_db)):
    existing_user = db.query(NguoiDung).filter(NguoiDung.email == user_data.email).first()
    if existing_user:
        raise HTTPException(status_code=400, detail="Email đã được đăng ký hệ thống")
    
    hashed_password = get_password_hash(user_data.mat_khau)
    new_user = NguoiDung(
        email=user_data.email,
        mat_khau=hashed_password,
        ho_ten=user_data.ho_ten,
        so_dien_thoai=user_data.so_dien_thoai,
        vai_tro=user_data.vai_tro
    )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    if user_data.vai_tro == "benh_nhan":
        benh_nhan = BenhNhan(
            nguoi_dung_id=new_user.id,
            ngay_sinh=user_data.ngay_sinh,
            gioi_tinh=user_data.gioi_tinh,
            dia_chi=user_data.dia_chi
        )
        db.add(benh_nhan)
        db.commit()
    elif user_data.vai_tro == "bac_si":
        bac_si = BacSi(nguoi_dung_id=new_user.id, mo_ta="Bác sĩ chuyên khoa")
        db.add(bac_si)
        db.commit()

    return new_user

@router.post("/login", response_model=Token)
def login(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    user = db.query(NguoiDung).filter(NguoiDung.email == form_data.username).first()
    if not user or not verify_password(form_data.password, user.mat_khau):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Email hoặc mật khẩu không chính xác",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    access_token = create_access_token(data={"sub": user.email, "vai_tro": user.vai_tro})
    return {"access_token": access_token, "token_type": "bearer"}

@router.get("/me", response_model=UserResponse)
def get_me(current_user: NguoiDung = Depends(get_current_user)):
    return current_user