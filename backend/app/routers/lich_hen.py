from app.auth import get_current_user, require_role
from app.database import get_db
from fastapi import APIRouter, Depends, HTTPException, status
from app.models.lich_hen import LichHen
from app.schemas.lich_hen import LichHenCreate, LichHenUpdate
from sqlalchemy.orm import Session

router = APIRouter(prefix="/lich-hen", tags=["Lich Hen"])


@router.post("", status_code=status.HTTP_201_CREATED)
def create_appointment(payload: LichHenCreate, db: Session = Depends(get_db)):
  new_lh = LichHen(
      doctor_id=payload.doctor_id,
      patient_name=payload.patient_name,
      patient_phone=payload.patient_phone,
      appointment_date=payload.appointment_date,
      notes=payload.notes,
  )
  db.add(new_lh)
  db.commit()
  db.refresh(new_lh)
  return {"message": "Đặt lịch hẹn thành công", "appointment_id": new_lh.id}


@router.get("")
def get_appointments(
    db: Session = Depends(get_db),
    current_user=Depends(require_role(["admin", "bac_si"])),
):
  appointments = db.query(LichHen).all()
  return appointments