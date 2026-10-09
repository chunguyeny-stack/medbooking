from app.auth import require_role
from app.database import get_db
from fastapi import APIRouter, Depends, HTTPException, status
from app.models.le_tan import LeTan
from sqlalchemy.orm import Session

router = APIRouter(prefix="/le-tan", tags=["Le Tan"])


@router.get("")
def get_all_le_tan(
    db: Session = Depends(get_db),
    current_user=Depends(require_role(["admin"])),
):
  list_lt = db.query(LeTan).all()
  return list_lt