import importlib
from datetime import date, datetime, timezone
from typing import Optional, List
from fastapi import APIRouter, Depends, HTTPException, Query, status
from pydantic import BaseModel
from sqlalchemy.orm import Session
from sqlalchemy import func, text

from app.database.database import get_db
from app.models.models import NguoiDung, BenhNhan, DichVu, ChuyenKhoa
from app.models.lich_hen import LichHen, LogTrangThai, LichLamViec
from app.models.bac_si import BacSi

from app import auth as root_auth

router = APIRouter(prefix="/appointments", tags=["Quản lý Lịch hẹn"])
tai_khoan_router = APIRouter(tags=["Tài khoản"])


class BookingRequest(BaseModel):
    bac_si_id: int
    dich_vu_id: int
    ngay_kham: date
    khung_gio: str
    ghi_chu: Optional[str] = None


class UpdateStatusRequest(BaseModel):
    trang_thai_moi: str
    ghi_chu: Optional[str] = None


@router.post("", status_code=status.HTTP_201_CREATED, summary="Bệnh nhân đặt lịch khám mới")
def create_appointment(
        payload: BookingRequest,
        db: Session = Depends(get_db),
        current_user: NguoiDung = Depends(root_auth.get_current_user)
):
    benh_nhan = current_user.benh_nhan_profile
    if not benh_nhan:
        raise HTTPException(status_code=400, detail="Tài khoản hiện tại chưa có hồ sơ bệnh nhân.")

    doctor = db.query(BacSi).filter(BacSi.id == payload.bac_si_id).first()
    if not doctor:
        raise HTTPException(status_code=404, detail="Bác sĩ không tồn tại.")

    lich_truc = db.query(LichLamViec).filter(
        LichLamViec.bac_si_id == payload.bac_si_id,
        LichLamViec.ngay_kham == payload.ngay_kham,
        LichLamViec.khung_gio == payload.khung_gio,
        LichLamViec.con_trong == True
    ).first()

    if not lich_truc:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Bác sĩ không có lịch làm việc, đã nghỉ, hoặc khung giờ này đã đóng."
        )

    bs_trung_lich = db.query(LichHen).filter(
        LichHen.bac_si_id == payload.bac_si_id,
        LichHen.ngay_kham == payload.ngay_kham,
        LichHen.khung_gio == payload.khung_gio,
        LichHen.trang_thai.notin_(["Cancelled", "Đã hủy"])
    ).first()

    if bs_trung_lich:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Bác sĩ đã có lịch hẹn khác vào khung giờ này."
        )

    bn_trung_lich = db.query(LichHen).filter(
        LichHen.benh_nhan_id == benh_nhan.id,
        LichHen.ngay_kham == payload.ngay_kham,
        LichHen.khung_gio == payload.khung_gio,
        LichHen.trang_thai.notin_(["Cancelled", "Đã hủy"])
    ).first()

    if bn_trung_lich:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Bạn đã có một lịch hẹn khác trùng vào ngày và khung giờ này."
        )

    appt = LichHen(
        benh_nhan_id=benh_nhan.id,
        bac_si_id=payload.bac_si_id,
        dich_vu_id=payload.dich_vu_id,
        ngay_kham=payload.ngay_kham,
        khung_gio=payload.khung_gio,
        trang_thai="Chờ xác nhận",
        ghi_chu=payload.ghi_chu or ""
    )

    db.add(appt)
    db.flush()

    lich_truc.con_trong = False

    log = LogTrangThai(
        lich_hen_id=appt.id,
        trang_thai_cu="",
        trang_thai_moi="Chờ xác nhận",
        thoi_gian=datetime.now(timezone.utc),
        nguoi_thuc_hien=current_user.ho_ten
    )
    db.add(log)
    db.commit()
    db.refresh(appt)

    return {"message": "Đặt lịch khám thành công.", "ma_lich_hen": appt.id}


@router.get("/tat-ca", summary="Lấy toàn bộ danh sách lịch hẹn chuẩn xác")
def get_tat_ca_lich_hen(
        db: Session = Depends(get_db),
        current_user: NguoiDung = Depends(root_auth.get_current_user)
):
    try:
        appointments = db.query(LichHen).order_by(LichHen.ngay_kham.desc()).all()
        if not appointments:
            return {"success": True, "total": 0, "data": []}

        benh_nhan_ids = [a.benh_nhan_id for a in appointments if a.benh_nhan_id]
        bac_si_ids = [a.bac_si_id for a in appointments if a.bac_si_id]

        bn_records = db.query(BenhNhan).filter(BenhNhan.id.in_(benh_nhan_ids)).all() if benh_nhan_ids else []
        bn_map = {bn.id: bn for bn in bn_records}
        nguoi_dung_ids = [bn.nguoi_dung_id for bn in bn_records if bn.nguoi_dung_id]

        doc_records = db.query(BacSi).filter(BacSi.id.in_(bac_si_ids)).all() if bac_si_ids else []
        doc_map = {doc.id: doc for doc in doc_records}
        for doc in doc_records:
            if doc.nguoi_dung_id:
                nguoi_dung_ids.append(doc.nguoi_dung_id)

        nguoi_dung_ids = list(set(nguoi_dung_ids))
        nd_records = db.query(NguoiDung).filter(NguoiDung.id.in_(nguoi_dung_ids)).all() if nguoi_dung_ids else []
        nd_map = {nd.id: nd for nd in nd_records}

        chuyen_khoa_ids = [doc.chuyen_khoa_id for doc in doc_records if getattr(doc, 'chuyen_khoa_id', None)]
        ck_records = db.query(ChuyenKhoa).filter(ChuyenKhoa.id.in_(chuyen_khoa_ids)).all() if chuyen_khoa_ids else []
        ck_map = {ck.id: ck for ck in ck_records}

        data = []
        for a in appointments:
            bn_name = "Bệnh nhân chưa rõ"
            bn_phone = "Chưa có SĐT"
            email_val = ""

            if a.benh_nhan_id and a.benh_nhan_id in bn_map:
                bn_record = bn_map[a.benh_nhan_id]
                if bn_record.nguoi_dung_id and bn_record.nguoi_dung_id in nd_map:
                    u_bn = nd_map[bn_record.nguoi_dung_id]
                    bn_name = getattr(u_bn, 'ho_ten', None) or getattr(u_bn, 'fullname', None) or "Bệnh nhân"
                    bn_phone = getattr(u_bn, 'so_dien_thoai', None) or getattr(u_bn, 'phone', None) or "Chưa có SĐT"
                    email_val = getattr(u_bn, 'email', None) or getattr(u_bn, 'thu_dien_tu', None) or ""

            bs_name = "BS. Chuyên khoa"
            chuyen_khoa_name = "Khám tổng quát"

            if a.bac_si_id and a.bac_si_id in doc_map:
                bs_record = doc_map[a.bac_si_id]
                if bs_record.nguoi_dung_id and bs_record.nguoi_dung_id in nd_map:
                    u_bs = nd_map[bs_record.nguoi_dung_id]
                    if u_bs and getattr(u_bs, 'ho_ten', None):
                        bs_name = u_bs.ho_ten
                        if not bs_name.startswith("BS."):
                            bs_name = f"BS. {bs_name}"

                if getattr(bs_record, 'chuyen_khoa_id', None) and bs_record.chuyen_khoa_id in ck_map:
                    ck_record = ck_map[bs_record.chuyen_khoa_id]
                    chuyen_khoa_name = getattr(ck_record, 'ten_chuyen_khoa', None) or getattr(ck_record, 'name',
                                                                                              None) or chuyen_khoa_name

            data.append({
                "ma_lich_hen": a.id,
                "ngay_kham": str(a.ngay_kham) if a.ngay_kham else "",
                "khung_gio": getattr(a, 'khung_gio', "08:00 - 09:00"),
                "benh_nhan": bn_name,
                "so_dien_thoai": bn_phone,
                "bac_si_name": bs_name,
                "bac_si_id": a.bac_si_id,
                "ghi_chu": getattr(a, 'ghi_chu', "Khám tổng quát"),
                "trang_thai": getattr(a, 'trang_thai', "Chờ khám"),
                "chuyen_khoa": chuyen_khoa_name,
                "email": email_val
            })

        return {"success": True, "total": len(data), "data": data}
    except Exception as e:
        print(f"Lỗi API /tat-ca: {e}")
        return {"success": False, "total": 0, "data": [], "detail": str(e)}


# ==========================================
# CÁC API QUẢN LÝ LỊCH LÀM VIỆC BÁC SĨ (CA TRỰC)
# ==========================================

class LichLamViecRequest(BaseModel):
    bac_si_id: int
    ngay_lam_viec: date
    ca_lam_viec: str
    gio_bat_dau: str
    gio_ket_thuc: str
    trang_thai: str


@router.get("/admin/lich-lam-viec", summary="Lấy danh sách lịch làm việc bác sĩ cho Lễ tân")
def get_danh_sach_lich_lam_viec(
        db: Session = Depends(get_db),
        current_user: NguoiDung = Depends(root_auth.get_current_user)
):
    try:
        schedules = db.query(LichLamViec).order_by(LichLamViec.ngay_kham.desc()).all()
        if not schedules:
            return []

        bac_si_ids = [s.bac_si_id for s in schedules if s.bac_si_id]
        doc_records = db.query(BacSi).filter(BacSi.id.in_(bac_si_ids)).all() if bac_si_ids else []
        doc_map = {doc.id: doc for doc in doc_records}

        nguoi_dung_ids = [doc.nguoi_dung_id for doc in doc_records if doc.nguoi_dung_id]
        nd_records = db.query(NguoiDung).filter(NguoiDung.id.in_(nguoi_dung_ids)).all() if nguoi_dung_ids else []
        nd_map = {nd.id: nd for nd in nd_records}

        data = []
        for s in schedules:
            doc_name = "Bác sĩ chuyên khoa"
            if s.bac_si_id and s.bac_si_id in doc_map:
                doc_record = doc_map[s.bac_si_id]
                if doc_record.nguoi_dung_id and doc_record.nguoi_dung_id in nd_map:
                    u_doc = nd_map[doc_record.nguoi_dung_id]
                    if u_doc and getattr(u_doc, 'ho_ten', None):
                        doc_name = u_doc.ho_ten
                        if not doc_name.startswith("BS."):
                            doc_name = f"BS. {doc_name}"

            gio_bd = "07:30"
            gio_kt = "11:30"
            ca_text = getattr(s, 'ca_lam_viec', 'Ca sáng')

            if s.khung_gio and " - " in s.khung_gio:
                parts = s.khung_gio.split(" - ")
                gio_bd = parts[0].strip()
                gio_kt = parts[1].strip()

                if gio_bd >= "18:30":
                    ca_text = "Ca tối"
                elif gio_bd >= "13:30":
                    ca_text = "Ca chiều"
                else:
                    ca_text = "Ca sáng"

            raw_status = str(getattr(s, 'trang_thai_chi_tiet', '') or '').lower().strip()
            if not raw_status or raw_status == 'none' or raw_status == 'nhap':
                raw_status = 'da_xac_nhan'

            data.append({
                "id": s.id,
                "bac_si_id": s.bac_si_id,
                "doctorName": doc_name,
                "ngay_lam_viec": str(s.ngay_kham) if hasattr(s, 'ngay_kham') and s.ngay_kham else "",
                "ca_lam_viec": ca_text,
                "gio_bat_dau": gio_bd,
                "gio_ket_thuc": gio_kt,
                "status": raw_status,
                "ly_do_ban": getattr(s, 'ly_do_ban', '') or ''
            })

        return data
    except Exception as e:
        print(f"Lỗi lấy lịch làm việc: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/admin/lich-lam-viec", status_code=status.HTTP_201_CREATED, summary="Lễ tân tạo lịch làm việc mới")
def create_lich_lam_viec(
        payload: LichLamViecRequest,
        db: Session = Depends(get_db),
        current_user: NguoiDung = Depends(root_auth.get_current_user)
):
    try:
        # ⭐ Đã sửa lỗi ngắt dòng thành dấu gạch ngang chuẩn
        chuoi_khung_gio = f"{payload.gio_bat_dau} - {payload.gio_ket_thuc}"

        new_sched = LichLamViec(
            bac_si_id=payload.bac_si_id,
            ngay_kham=payload.ngay_lam_viec,
            khung_gio=chuoi_khung_gio,
            con_trong=True
        )

        if hasattr(LichLamViec, 'trang_thai_chi_tiet'):
            new_sched.trang_thai_chi_tiet = payload.trang_thai
        if hasattr(LichLamViec, 'ca_lam_viec'):
            new_sched.ca_lam_viec = payload.ca_lam_viec
        if hasattr(LichLamViec, 'gio_bat_dau'):
            new_sched.gio_bat_dau = payload.gio_bat_dau
        if hasattr(LichLamViec, 'gio_ket_thuc'):
            new_sched.gio_ket_thuc = payload.gio_ket_thuc

        db.add(new_sched)
        db.commit()
        db.refresh(new_sched)

        return {"success": True, "message": "Tạo lịch làm việc thành công!", "id": new_sched.id}
    except Exception as e:
        db.rollback()
        print(f"Lỗi chi tiết khi tạo lịch làm việc: {e}")
        raise HTTPException(status_code=500, detail=f"Lỗi cơ sở dữ liệu: {str(e)}")


@router.put("/admin/lich-lam-viec/{lich_id}", summary="Cập nhật hoặc phê duyệt lịch làm việc")
def update_lich_lam_viec(
        lich_id: int,
        payload: LichLamViecRequest,
        db: Session = Depends(get_db),
        current_user: NguoiDung = Depends(root_auth.get_current_user)
):
    try:
        sched = db.query(LichLamViec).filter(LichLamViec.id == lich_id).first()
        if not sched:
            raise HTTPException(status_code=404, detail="Không tìm thấy lịch làm việc.")

        sched.bac_si_id = payload.bac_si_id
        sched.ngay_kham = payload.ngay_lam_viec
        # ⭐ Đã sửa lỗi ngắt dòng thành dấu gạch ngang chuẩn
        sched.khung_gio = f"{payload.gio_bat_dau} - {payload.gio_ket_thuc}"

        if hasattr(LichLamViec, 'trang_thai_chi_tiet'):
            sched.trang_thai_chi_tiet = payload.trang_thai
        if hasattr(LichLamViec, 'ca_lam_viec'):
            sched.ca_lam_viec = payload.ca_lam_viec
        if hasattr(LichLamViec, 'gio_bat_dau'):
            sched.gio_bat_dau = payload.gio_bat_dau
        if hasattr(LichLamViec, 'gio_ket_thuc'):
            sched.gio_ket_thuc = payload.gio_ket_thuc

        db.commit()
        return {"success": True, "message": "Cập nhật lịch làm việc thành công!"}
    except Exception as e:
        db.rollback()
        print(f"Lỗi chi tiết khi cập nhật lịch làm việc: {e}")
        raise HTTPException(status_code=500, detail=f"Lỗi: {str(e)}")


# ⭐ NÂNG CẤP HÀM XÓA: Xóa sạch toàn bộ bản ghi trùng lặp của ca trực đó trong database
@router.delete("/admin/lich-lam-viec/{lich_id}", summary="Xóa lịch làm việc")
def delete_lich_lam_viec(
        lich_id: int,
        db: Session = Depends(get_db),
        current_user: NguoiDung = Depends(root_auth.get_current_user)
):
    try:
        sched = db.query(LichLamViec).filter(LichLamViec.id == lich_id).first()
        if not sched:
            raise HTTPException(status_code=404, detail="Không tìm thấy lịch làm việc.")

        # ⭐ Dùng khung_gio thay cho gio_bat_dau để gom xóa các bản ghi trùng lặp
        db.query(LichLamViec).filter(
            LichLamViec.bac_si_id == sched.bac_si_id,
            LichLamViec.ngay_kham == sched.ngay_kham,
            LichLamViec.khung_gio == sched.khung_gio
        ).delete(synchronize_session=False)

        db.commit()
        return {"success": True, "message": "Đã xóa hoàn toàn lịch làm việc thành công!"}
    except Exception as e:
        db.rollback()
        print(f"🔥 LỖI CHI TIẾT KHI XÓA LỊCH LÀM VIỆC (ID: {lich_id}): {str(e)}")
        raise HTTPException(status_code=500, detail=f"Không thể xóa lịch do vướng dữ liệu liên quan: {str(e)}")

@router.get("/admin/bac-si", summary="Lấy danh sách toàn bộ bác sĩ cho Lễ tân")
def get_danh_sach_bac_si_cho_le_tan(
        db: Session = Depends(get_db),
        current_user: NguoiDung = Depends(root_auth.get_current_user)
):
    try:
        doctors = db.query(BacSi).all()
        if not doctors:
            return []

        nguoi_dung_ids = [doc.nguoi_dung_id for doc in doctors if doc.nguoi_dung_id]
        nd_records = db.query(NguoiDung).filter(NguoiDung.id.in_(nguoi_dung_ids)).all() if nguoi_dung_ids else []
        nd_map = {nd.id: nd for nd in nd_records}

        result = []
        for doc in doctors:
            doc_name = "Bác sĩ"
            if doc.nguoi_dung_id and doc.nguoi_dung_id in nd_map:
                u = nd_map[doc.nguoi_dung_id]
                if u and getattr(u, 'ho_ten', None):
                    doc_name = u.ho_ten
                    if not doc_name.startswith("BS."):
                        doc_name = f"BS. {doc_name}"
            result.append({
                "id": doc.id,
                "name": doc_name
            })
        return result
    except Exception as e:
        print(f"Lỗi lấy danh sách bác sĩ: {e}")
        return []


@router.put("/appointments/xac-nhan-kham-bu/{lich_id}", summary="Bệnh nhân xác nhận lịch khám bù")
def xac_nhan_kham_bu(
        lich_id: int,
        db: Session = Depends(get_db),
        current_user: NguoiDung = Depends(root_auth.get_current_user)
):
    appt = db.query(LichHen).filter(LichHen.id == lich_id).first()
    if not appt:
        raise HTTPException(status_code=404, detail="Không tìm thấy lịch hẹn.")

    # Cập nhật trạng thái rõ ràng để lễ tân nhận biết
    appt.trang_thai = "Đã xác nhận lịch khám bù"
    db.commit()
    return {"success": True, "message": "Xác nhận lịch khám bù thành công."}