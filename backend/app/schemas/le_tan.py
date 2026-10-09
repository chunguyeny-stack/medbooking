from datetime import datetime
from typing import Optional
from pydantic import BaseModel, EmailStr


class UserCreate(BaseModel):
  username: str
  email: EmailStr
  password: str
  role: str = "le_tan"


class UserLogin(BaseModel):
  username: str
  password: str


class Token(BaseModel):
  access_token: str
  token_type: str


class LeTanResponse(BaseModel):
  id: int
  username: str
  email: str
  role: str
  status: int
  created_at: datetime

  class Config:
    from_attributes = True