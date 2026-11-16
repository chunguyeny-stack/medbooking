from datetime import datetime, date
from typing import Optional, List
from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from pydantic import BaseModel
from passlib.context import CryptContext
from sqlalchemy import func
import json

from database.database import get_db
from models.models import NguoiDung, BenhNhan, DichVu
from models.lich_hen import LichHen, LichLamViec
from models.bac_si import BacSi
from routers import auth_router as root_auth

router = APIRouter(prefix="/appointments", tags=["Quản lý Lịch hẹn"])
tai_khoan_router = APIRouter(tags=["Tài khoản"])


class DoiMatKhauRequest(BaseModel):
    current_password: str
    new_password: str


class BookingRequest(BaseModel):
    dich_vu_id: int
    ngay_kham: str
    khung_gio: str
    ghi_chu: Optional[str] = None
    bac_si_id: Optional[int] = None


@router.post("/dat-lich", status_code=status.HTTP_201_CREATED, summary="Bệnh nhân đặt lịch khám mới")
def create_appointment(
        payload: BookingRequest,
        db: Session = Depends(get_db),
        current_user: NguoiDung = Depends(root_auth.get_current_user)
):
    benh_nhan = db.query(BenhNhan).filter(BenhNhan.nguoi_dung_id == current_user.id).first()
    if not benh_nhan:
        benh_nhan = BenhNhan(nguoi_dung_id=current_user.id)
        db.add(benh_nhan)
        db.commit()
        db.refresh(benh_nhan)

    doctor = None
    if payload.bac_si_id:
        doctor = db.query(BacSi).filter(BacSi.id == payload.bac_si_id).first()
        if not doctor:
            doctor = db.query(BacSi).filter(BacSi.nguoi_dung_id == payload.bac_si_id).first()

    if not doctor:
        doctor = db.query(BacSi).first()
        if not doctor:
            raise HTTPException(status_code=404, detail="Hệ thống chưa có thông tin bác sĩ.")

    real_bac_si_id = doctor.id

    ngay_kham_parsed = None
    if payload.ngay_kham:
        try:
            ngay_kham_parsed = datetime.strptime(payload.ngay_kham[:10], "%Y-%m-%d").date()
        except ValueError:
            ngay_kham_parsed = date.today()

    khung_gio_sach = payload.khung_gio.replace(" ", "")
    lich_truc = db.query(LichLamViec).filter(
        LichLamViec.bac_si_id == real_bac_si_id,
        LichLamViec.ngay_kham == ngay_kham_parsed
    ).filter(
        func.replace(LichLamViec.khung_gio, ' ', '') == khung_gio_sach
    ).first()

    if not lich_truc:
        lich_truc = LichLamViec(
            bac_si_id=real_bac_si_id,
            ngay_kham=ngay_kham_parsed,
            khung_gio=payload.khung_gio,
            con_trong=True
        )
        db.add(lich_truc)
        db.commit()
        db.refresh(lich_truc)

    lich_truc.con_trong = False

    appt = LichHen(
        benh_nhan_id=benh_nhan.id,
        bac_si_id=real_bac_si_id,
        dich_vu_id=payload.dich_vu_id,
        ngay_kham=ngay_kham_parsed,
        khung_gio=payload.khung_gio,
        trang_thai="Chờ xác nhận",
        ghi_chu=payload.ghi_chu or ""
    )

    db.add(appt)
    db.commit()
    db.refresh(appt)

    return {
        "success": True,
        "message": "Đặt lịch khám thành công!",
        "id_lich_hen": appt.id
    }


# ⭐ API TRẢ VỀ DANH SÁCH GIỜ BẬN (ĐÃ TÁCH BIỆT RẠCH RÒI CA CHIỀU VÀ CA TỐI)
@router.get("/bac-si/{bac_si_id}/gio-ban", summary="Lấy danh sách khung giờ bận của bác sĩ theo ngày")
def get_bac_si_gio_ban(bac_si_id: int, ngay_kham: str, db: Session = Depends(get_db)):
    try:
        gio_ban = []
        search_dates = [ngay_kham]
        if "/" in ngay_kham:
            parts = ngay_kham.split("/")
            if len(parts) == 3:
                search_dates.append(f"{parts[2]}-{parts[0].zfill(2)}-{parts[1].zfill(2)}")
                search_dates.append(f"{parts[2]}-{parts[1].zfill(2)}-{parts[0].zfill(2)}")
        elif "-" in ngay_kham and len(ngay_kham.split("-")[0]) == 2:
            parts = ngay_kham.split("-")
            search_dates.append(f"{parts[2]}-{parts[0].zfill(2)}-{parts[1].zfill(2)}")

        lich_hens = db.query(LichHen).filter(
            LichHen.bac_si_id == bac_si_id,
            LichHen.ngay_kham.in_(search_dates),
            LichHen.trang_thai.notin_(["Cancelled", "Đã hủy", "cancelled", "reschedule"])
        ).all()
        for lh in lich_hens:
            if lh.khung_gio:
                gio_ban.append(lh.khung_gio.strip())

        lich_trucs = db.query(LichLamViec).filter(
            LichLamViec.bac_si_id == bac_si_id,
            LichLamViec.ngay_kham.in_(search_dates)
        ).all()

        all_slots = [
            "07:30 - 08:00", "08:00 - 08:30", "08:30 - 09:00", "09:00 - 09:30", "09:30 - 10:00", "10:00 - 10:30",
            "10:30 - 11:00", "11:00 - 11:30",
            "13:30 - 14:00", "14:00 - 14:30", "14:30 - 15:00", "15:00 - 15:30", "15:30 - 16:00", "16:00 - 16:30",
            "16:30 - 17:00",
            "17:00 - 17:30", "17:30 - 18:00", "18:00 - 18:30", "18:30 - 19:00", "19:00 - 19:30", "19:30 - 20:00",
            "20:00 - 20:30",
            "20:30 - 21:00", "21:00 - 21:30", "21:30 - 22:00", "22:00 - 22:30"
        ]

        for lt in lich_trucs:
            ly_do = str(getattr(lt, 'ly_do_ban', '') or '').strip()
            trang_thai = str(getattr(lt, 'trang_thai_chi_tiet', '')).upper()
            if ly_do != "" or "HUY" in trang_thai or "BAC_SI_HUY" in trang_thai:
                shift_str = str(getattr(lt, 'khung_gio', '') or '').upper()

                # Lấy mốc thời gian bắt đầu để phân loại tuyệt đối không bị dính chuỗi
                start_p = shift_str.split("-")[0].strip() if "-" in shift_str else shift_str

                # Ca sáng: bắt đầu trước 12:00 hoặc chứa chữ SÁNG
                if "SÁNG" in shift_str or start_p < "12:00":
                    for s in all_slots[:8]:
                        if s not in gio_ban: gio_ban.append(s)

                # Ca tối: bắt đầu từ 18:30 trở đi hoặc chứa chữ TỐI
                elif "TỐI" in shift_str or start_p >= "18:30":
                    for s in all_slots[18:]:
                        if s not in gio_ban: gio_ban.append(s)

                # Ca chiều: từ 13:30 đến 18:30 (tương ứng các slot từ index 8 đến 17)
                elif "CHIỀU" in shift_str or ("13:30" in shift_str and start_p < "18:30"):
                    for s in all_slots[8:18]:
                        if s not in gio_ban: gio_ban.append(s)
                else:
                    if lt.khung_gio and lt.khung_gio.strip() not in gio_ban:
                        gio_ban.append(lt.khung_gio.strip())

        return {"success": True, "gio_ban": list(set(gio_ban))}
    except Exception as e:
        return {"success": False, "gio_ban": [], "detail": str(e)}


# ⭐ API CHUYÊN BIỆT LẤY CA TRỐNG VÀ CA BẬN CỦA BÁC SĨ
@router.get("/bac-si/{bac_si_id}/ca-lam-viec", summary="Lấy danh sách ca làm việc và ca trống của bác sĩ theo ngày")
def get_bac_si_ca_lam_viec(bac_si_id: int, ngay_kham: str, db: Session = Depends(get_db)):
    try:
        search_dates = [ngay_kham]
        parsed_date = None

        if "/" in ngay_kham:
            parts = ngay_kham.split("/")
            if len(parts) == 3:
                try:
                    parsed_date = datetime.strptime(ngay_kham, "%m/%d/%Y").date()
                except ValueError:
                    try:
                        parsed_date = datetime.strptime(ngay_kham, "%d/%m/%Y").date()
                    except ValueError:
                        pass
                search_dates.append(f"{parts[2]}-{parts[0].zfill(2)}-{parts[1].zfill(2)}")
                search_dates.append(f"{parts[2]}-{parts[1].zfill(2)}-{parts[0].zfill(2)}")
        elif "-" in ngay_kham:
            parts = ngay_kham.split("-")
            if len(parts[0]) == 4:
                try:
                    parsed_date = datetime.strptime(ngay_kham[:10], "%Y-%m-%d").date()
                except ValueError:
                    pass
            elif len(parts[0]) == 2:
                search_dates.append(f"{parts[2]}-{parts[0].zfill(2)}-{parts[1].zfill(2)}")

        if not parsed_date and search_dates:
            for sd in search_dates:
                try:
                    parsed_date = datetime.strptime(sd[:10], "%Y-%m-%d").date()
                    break
                except ValueError:
                    continue

        if not parsed_date:
            parsed_date = date.today()

        lich_trucs = db.query(LichLamViec).filter(
            LichLamViec.bac_si_id == bac_si_id,
            LichLamViec.ngay_kham == parsed_date
        ).all()

        ca_trong_raw = []
        ca_ban = []

        for lt in lich_trucs:
            ly_do = str(getattr(lt, 'ly_do_ban', '') or '').strip()
            trang_thai = str(getattr(lt, 'trang_thai_chi_tiet', '')).upper()

            start_t = getattr(lt, 'gio_bat_dau', '07:30') or '07:30'
            end_t = getattr(lt, 'gio_ket_thuc', '11:30') or '11:30'
            shift_name = getattr(lt, 'ca_lam_viec', 'Ca khám') or 'Ca khám'

            shift_info = {
                "id": lt.id,
                "ca_lam_viec": shift_name,
                "gio_bat_dau": start_t,
                "gio_ket_thuc": end_t,
                "khung_gio": f"{start_t} - {end_t}",  # ⭐ Đã sửa lỗi ngắt dòng
                "ly_do_ban": ly_do
            }

            if ly_do != "" or "HUY" in trang_thai or "BAC_SI_HUY" in trang_thai:
                ca_ban.append(shift_info)
            else:
                ca_trong_raw.append(shift_info)

        seen_slots = set()
        ca_trong = []
        for s in ca_trong_raw:
            key = (s["gio_bat_dau"], s["gio_ket_thuc"], s["ca_lam_viec"])
            if key not in seen_slots:
                seen_slots.add(key)
                ca_trong.append(s)

        if not lich_trucs:
            ca_trong = [
                {"ca_lam_viec": "Ca sáng", "gio_bat_dau": "07:30", "gio_ket_thuc": "11:30", "khung_gio": "07:30 - 11:30"},
                {"ca_lam_viec": "Ca chiều", "gio_bat_dau": "13:30", "gio_ket_thuc": "18:30", "khung_gio": "13:30 - 18:30"},
                {"ca_lam_viec": "Ca tối", "gio_bat_dau": "18:30", "gio_ket_thuc": "22:30", "khung_gio": "18:30 - 22:30"}
            ]

        return {
            "success": True,
            "ngay_kham": str(parsed_date),
            "ca_trong": ca_trong,
            "ca_ban": ca_ban
        }
    except Exception as e:
        print(f"Lỗi lấy ca làm việc bác sĩ: {e}")
        return {"success": False, "ca_trong": [], "ca_ban": [], "detail": str(e)}


@router.put("/doi-lich-hen/{lich_hen_id}", summary="Cập nhật ngày và giờ khám mới cho lịch hẹn")
def doi_lich_hen_benh_nhan(
        lich_hen_id: int,
        payload: dict,
        db: Session = Depends(get_db),
        current_user: NguoiDung = Depends(root_auth.get_current_user)
):
    try:
        ngay_moi = payload.get("ngay_kham_moi") or payload.get("ngay_moi")
        gio_moi = payload.get("khung_gio_moi") or payload.get("gio_moi")

        if not ngay_moi or not gio_moi:
            raise HTTPException(status_code=400, detail="Vui lòng cung cấp đầy đủ ngày và giờ khám mới!")

        lich_hen = db.query(LichHen).filter(LichHen.id == lich_hen_id).first()
        if not lich_hen:
            raise HTTPException(status_code=404, detail="Không tìm thấy lịch hẹn.")

        ngay_parsed = datetime.strptime(str(ngay_moi)[:10], "%Y-%m-%d").date()

        lich_hen.ngay_kham = ngay_parsed
        lich_hen.khung_gio = str(gio_moi).strip()
        lich_hen.trang_thai = "Chờ bệnh nhân xác nhận"

        db.add(lich_hen)
        db.commit()
        db.refresh(lich_hen)

        return {"success": True, "message": "Đã đổi lịch khám và chuyển trạng thái thành chờ bệnh nhân xác nhận thành công!"}
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/bac-si/cua-toi", summary="Lấy danh sách ca khám của bác sĩ hiện tại")
@router.get("/bac-si", summary="Lấy danh sách ca khám của bác sĩ hiện tại (Alias)")
@router.get("/doctor/cua-toi", summary="Lấy danh sách ca khám của bác sĩ hiện tại (Alias 2)")
def get_lich_hen_cua_bac_si_hien_tai(
        db: Session = Depends(get_db),
        current_user: NguoiDung = Depends(root_auth.get_current_user)
):
    role = (current_user.vai_tro or "").lower().strip()
    allowed_roles = ["bac_si", "bác_si", "doctor", "bác sĩ"]

    if role not in allowed_roles:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail=f"Bạn không có quyền truy cập! Vai trò hiện tại trong DB là: '{current_user.vai_tro}'"
        )

    bac_si_profile = db.query(BacSi).filter(BacSi.nguoi_dung_id == current_user.id).first()
    if not bac_si_profile:
        bac_si_profile = BacSi(nguoi_dung_id=current_user.id, chuyen_khoa_id=1, gia_kham=150000)
        db.add(bac_si_profile)
        db.commit()
        db.refresh(bac_si_profile)

    lich_hens = db.query(LichHen).filter(LichHen.bac_si_id == bac_si_profile.id).order_by(
        LichHen.ngay_kham.desc()).all()

    formatted_data = []
    for a in lich_hens:
        appt_id = getattr(a, "id", None) or getattr(a, "ma_lich_hen", None)

        patient_name = "Bệnh nhân chưa rõ"
        patient_phone = "Chưa có SĐT"
        patient_email = ""
        patient_gender = "Chưa cập nhật"
        patient_dob = ""

        if a.benh_nhan_id:
            bn_record = db.query(BenhNhan).filter(BenhNhan.id == a.benh_nhan_id).first()
            if bn_record:
                patient_dob = str(
                    getattr(bn_record, "ngay_sinh", None) or getattr(bn_record, "date_of_birth", "") or "")
                for field in ["gioitinh", "gioi_tinh", "gender"]:
                    val = getattr(bn_record, field, None)
                    if val and str(val).strip() not in ["", "None", "null"]:
                        patient_gender = str(val).strip()
                        break

                if bn_record.nguoi_dung_id:
                    u_record = db.query(NguoiDung).filter(NguoiDung.id == bn_record.nguoi_dung_id).first()
                    if u_record:
                        patient_name = getattr(u_record, "ho_ten", None) or getattr(u_record, "fullname",
                                                                                    None) or "Bệnh nhân"
                        patient_phone = getattr(u_record, "so_dien_thoai", None) or getattr(u_record, "phone",
                                                                                            None) or "Chưa có SĐT"
                        patient_email = getattr(u_record, "email", None) or ""

                        if not patient_dob:
                            patient_dob = str(
                                getattr(u_record, "ngay_sinh", None) or getattr(u_record, "date_of_birth", "") or "")

                        if patient_gender == "Chưa cập nhật":
                            for field in ["gioitinh", "gioi_tinh", "gender"]:
                                val = getattr(u_record, field, None)
                                if val and str(val).strip() not in ["", "None", "null"]:
                                    patient_gender = str(val).strip()
                                    break

        calculated_age = "28"
        if patient_dob:
            try:
                dob_str = patient_dob[:10]
                birth_date = datetime.strptime(dob_str, "%Y-%m-%d").date()
                today = date.today()
                age = today.year - birth_date.year
                if (today.month, today.day) < (birth_date.month, birth_date.day):
                    age -= 1
                calculated_age = str(age if age >= 0 else 0)
            except Exception:
                pass

        doctor_name = getattr(current_user, "ho_ten", None) or getattr(current_user, "fullname",
                                                                       None) or "Bác sĩ chuyên khoa"
        if not doctor_name.startswith("BS.") and not doctor_name.startswith("ThS") and not doctor_name.startswith(
                "PGS") and not doctor_name.startswith("TS"):
            doctor_name = f"BS. {doctor_name}"

        service_name = "Khám tổng quát"
        if hasattr(a, "dich_vu") and a.dich_vu:
            service_name = getattr(a.dich_vu, "ten_dich_vu", "Khám tổng quát")

        don_thuoc_data = []
        raw_don_thuoc = getattr(a, "don_thuoc", None)
        if raw_don_thuoc:
            try:
                don_thuoc_data = json.loads(raw_don_thuoc)
            except Exception:
                don_thuoc_data = []

        formatted_data.append({
            "id": appt_id,
            "ma_lich_hen": appt_id,
            "ngay_kham": str(a.ngay_kham) if a.ngay_kham else "",
            "khung_gio": str(getattr(a, "khung_gio", "") or "08:00 - 09:00"),
            "benh_nhan": patient_name,
            "ho_ten": patient_name,
            "so_dien_thoai": patient_phone,
            "phone": patient_phone,
            "email": patient_email,
            "bac_si_name": doctor_name,
            "bac_si": doctor_name,
            "gioi_tinh": patient_gender,
            "ngay_sinh": patient_dob[:10] if patient_dob else "",
            "tuoi": calculated_age,
            "chuyen_khoa": service_name,
            "dich_vu": service_name,
            "trang_thai": getattr(a, "trang_thai", "Chờ xác nhận"),
            "ghi_chu": getattr(a, "ghi_chu", ""),
            "trieu_chung": getattr(a, "ghi_chu", ""),
            "clinical_notes": getattr(a, "trieu_chung_thuc_the", "") or "",
            "diagnosis": getattr(a, "chan_doan", "") or "",
            "advice": getattr(a, "loi_dan", "") or "",
            "don_thuoc": don_thuoc_data
        })

    return {
        "success": True,
        "total": len(formatted_data),
        "data": formatted_data
    }


@router.get("/cua-toi", summary="Lấy danh sách lịch hẹn cá nhân của bệnh nhân hiện tại")
def get_lich_hen_cua_toi(
        db: Session = Depends(get_db),
        current_user: NguoiDung = Depends(root_auth.get_current_user)
):
    try:
        benh_nhan = db.query(BenhNhan).filter(BenhNhan.nguoi_dung_id == current_user.id).first()
        if not benh_nhan:
            return {"success": True, "total": 0, "data": []}

        lich_hens = db.query(LichHen).filter(LichHen.benh_nhan_id == benh_nhan.id).order_by(
            LichHen.ngay_kham.desc()).all()

        default_doctor = db.query(BacSi).first()
        default_doc_id = default_doctor.id if default_doctor else 1

        data = []
        for l in lich_hens:
            doc_id_val = getattr(l, "bac_si_id", None)
            if not doc_id_val:
                doc_id_val = default_doc_id

            doc_name = "BS. Chuyên khoa"
            doc_record = db.query(BacSi).filter(BacSi.id == doc_id_val).first()
            if doc_record:
                raw_doc_name = getattr(doc_record, "ho_ten", None) or getattr(doc_record, "fullname", None)
                if not raw_doc_name and doc_record.nguoi_dung_id:
                    user_doc = db.query(NguoiDung).filter(NguoiDung.id == doc_record.nguoi_dung_id).first()
                    if user_doc:
                        raw_doc_name = getattr(user_doc, "ho_ten", None) or getattr(user_doc, "fullname", None)

                if raw_doc_name:
                    doc_name = str(raw_doc_name).strip()
                    if not doc_name.startswith("BS.") and not doc_name.startswith("PGS") and not doc_name.startswith("TS") and not doc_name.startswith("ThS"):
                        doc_name = f"BS. {doc_name}"

            patient_name = getattr(current_user, "ho_ten", None) or getattr(current_user, "fullname", None) or "Bệnh nhân"

            service_name = "Khám tổng quát"
            if hasattr(l, "dich_vu_id") and l.dich_vu_id:
                dv_record = db.query(DichVu).filter(DichVu.id == l.dich_vu_id).first()
                if dv_record:
                    service_name = getattr(dv_record, "ten_dich_vu", "Khám tổng quát")

            data.append({
                "id": l.id,
                "ma_lich_hen": l.id,
                "ngay_kham": str(l.ngay_kham) if l.ngay_kham else "",
                "khung_gio": l.khung_gio or "08:00 - 09:00",
                "trang_thai": l.trang_thai or "Chờ xác nhận",
                "bac_si_name": doc_name,
                "bac_si": doc_name,
                "bac_si_id": doc_id_val,
                "benh_nhan": patient_name,
                "ho_ten": patient_name,
                "chuyen_khoa": service_name,
                "ghi_chu": getattr(l, "ghi_chu", ""),
                "trieu_chung_thuc_the": getattr(l, "trieu_chung_thuc_the", None) or "",
                "chan_doan": getattr(l, "chan_doan", "") or "Chưa có chẩn đoán",
                "loi_dan": getattr(l, "loi_dan", "") or "Không có lời dặn",
                "don_thuoc": getattr(l, "don_thuoc", None),
                "thiet_bi_y_te": getattr(l, "thiet_bi_y_te", None)
            })

        return {"success": True, "total": len(data), "data": data}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/tat-ca", summary="Lấy toàn bộ danh sách lịch hẹn cho Lễ tân")
def lay_tat_ca_lich_hen(
        limit: int = Query(100, description="Giới hạn số lượng bản ghi tối đa"),
        db: Session = Depends(get_db),
        current_user=Depends(root_auth.get_current_user)
):
    try:
        # ⭐ CHỈ LẤY 100 LỊCH HẸN MỚI NHẤT TỪ CƠ SỞ DỮ LIỆU ĐỂ TẢI SIÊU TỐC
        lich_hens = db.query(LichHen).order_by(LichHen.ngay_kham.desc()).limit(100).all()
        if not lich_hens:
            return {"success": True, "data": []}

        # Thu thập toàn bộ ID để query hàng loạt (Bulk Query) chống N+1 query
        benh_nhan_ids = [l.benh_nhan_id for l in lich_hens if getattr(l, 'benh_nhan_id', None)]
        bac_si_ids = [l.bac_si_id for l in lich_hens if getattr(l, 'bac_si_id', None)]
        dich_vu_ids = [l.dich_vu_id for l in lich_hens if getattr(l, 'dich_vu_id', None)]

        bn_records = db.query(BenhNhan).filter(BenhNhan.id.in_(benh_nhan_ids)).all() if benh_nhan_ids else []
        bn_map = {bn.id: bn for bn in bn_records}
        nguoi_dung_ids = [bn.nguoi_dung_id for bn in bn_records if getattr(bn, 'nguoi_dung_id', None)]

        doc_records = db.query(BacSi).filter(BacSi.id.in_(bac_si_ids)).all() if bac_si_ids else []
        doc_map = {doc.id: doc for doc in doc_records}
        for doc in doc_records:
            if getattr(doc, 'nguoi_dung_id', None):
                nguoi_dung_ids.append(doc.nguoi_dung_id)

        nguoi_dung_ids = list(set(nguoi_dung_ids))
        nd_records = db.query(NguoiDung).filter(NguoiDung.id.in_(nguoi_dung_ids)).all() if nguoi_dung_ids else []
        nd_map = {nd.id: nd for nd in nd_records}

        dv_records = db.query(DichVu).filter(DichVu.id.in_(dich_vu_ids)).all() if dich_vu_ids else []
        dv_map = {dv.id: dv for dv in dv_records}

        data = []
        for l in lich_hens:
            ten_bn = "Bệnh nhân"
            sdt_bn = ""
            email_val = ""

            if getattr(l, 'benh_nhan_id', None) and l.benh_nhan_id in bn_map:
                bn_record = bn_map[l.benh_nhan_id]
                if bn_record.nguoi_dung_id and bn_record.nguoi_dung_id in nd_map:
                    nd_record = nd_map[bn_record.nguoi_dung_id]
                    ten_bn = getattr(nd_record, 'ho_ten', None) or getattr(nd_record, 'fullname', None) or ten_bn
                    sdt_bn = getattr(nd_record, 'so_dien_thoai', None) or getattr(nd_record, 'phone', None) or sdt_bn
                    email_val = getattr(nd_record, 'email', None) or getattr(nd_record, 'thu_dien_tu', None) or ""

            doc_name = "BS. Chuyên khoa"
            if getattr(l, 'bac_si_id', None) and l.bac_si_id in doc_map:
                doc_record = doc_map[l.bac_si_id]
                if doc_record.nguoi_dung_id and doc_record.nguoi_dung_id in nd_map:
                    user_doc = nd_map[doc_record.nguoi_dung_id]
                    if user_doc and getattr(user_doc, 'ho_ten', None):
                        doc_name = user_doc.ho_ten
                        if not doc_name.startswith("BS.") and not doc_name.startswith("PGS") and not doc_name.startswith("TS"):
                            doc_name = f"BS. {doc_name}"

            service_name = "Khám tổng quát"
            if getattr(l, "dich_vu_id", None) and l.dich_vu_id in dv_map:
                dv_record = dv_map[l.dich_vu_id]
                service_name = getattr(dv_record, "ten_dich_vu", "Khám tổng quát")

            data.append({
                "id": l.id,
                "ma_lich_hen": l.id,
                "benh_nhan": ten_bn,
                "ho_ten": ten_bn,
                "so_dien_thoai": sdt_bn if sdt_bn else "Chưa có SĐT",
                "phone": sdt_bn,
                "email": email_val,
                "ngay_kham": str(l.ngay_kham) if l.ngay_kham else "",
                "khung_gio": l.khung_gio or "08:00 - 09:00",
                "trang_thai": l.trang_thai or "Chờ xác nhận",
                "bac_si_name": doc_name,
                "bac_si": doc_name,
                "bac_si_id": getattr(l, "bac_si_id", None),
                "chuyen_khoa": service_name,
                "ghi_chu": getattr(l, "ghi_chu", "Khám tổng quát định kỳ"),
                "trieu_chung": getattr(l, "trieu_chung", "Khám tổng quát"),
                "trieu_chung_thuc_the": getattr(l, "trieu_chung_thuc_the", None) or "",
                "chan_doan": getattr(l, "chan_doan", None) or "",
                "loi_dan": getattr(l, "loi_dan", None) or "",
                "don_thuoc": getattr(l, "don_thuoc", None),
                "thiet_bi_y_te": getattr(l, "thiet_bi_y_te", None)
            })

        return {"success": True, "data": data}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.put("/cap-nhap-trang-thai/{lich_hen_id}", summary="Cập nhật trạng thái lịch hẹn của bệnh nhân")
def cap_nhat_trang_thai_lich_hen(
        lich_hen_id: int,
        trang_thai_moi: str = Query(..., description="Trạng thái mới của lịch hẹn"),
        db: Session = Depends(get_db),
        current_user: NguoiDung = Depends(root_auth.get_current_user)
):
    try:
        lich_hen = db.query(LichHen).filter(LichHen.id == lich_hen_id).first()
        if not lich_hen:
            raise HTTPException(status_code=404, detail="Không tìm thấy lịch hẹn.")

        lich_hen.trang_thai = trang_thai_moi
        db.add(lich_hen)
        db.commit()
        db.refresh(lich_hen)

        return {"success": True, "message": "Cập nhật trạng thái lịch hẹn thành công!"}
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=str(e))


@router.put("/patient-confirm-reschedule/{lich_hen_id}", summary="Bệnh nhân xác nhận lịch khám bù")
def patient_confirm_reschedule(
        lich_hen_id: int,
        db: Session = Depends(get_db),
        current_user: NguoiDung = Depends(root_auth.get_current_user)
):
    try:
        lich_hen = db.query(LichHen).filter(LichHen.id == lich_hen_id).first()
        if not lich_hen:
            raise HTTPException(status_code=404, detail="Không tìm thấy lịch hẹn.")

        # Cập nhật trạng thái thành bệnh nhân đã xác nhận lịch khám bù, chờ lễ tân duyệt cuối
        lich_hen.trang_thai = "Bệnh nhân đã xác nhận lịch khám bù"
        db.add(lich_hen)
        db.commit()
        db.refresh(lich_hen)

        return {"success": True, "message": "Đã xác nhận lịch khám bù thành công! Vui lòng chờ lễ tân duyệt lại."}
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=str(e))