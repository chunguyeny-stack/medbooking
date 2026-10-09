from datetime import datetime, timezone
from sqlalchemy import Column, Integer, String, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from datadase.database import Base


def utc_now():
    return datetime.now(timezone.utc)


class LeTan(Base):
    __tablename__ = "le_tan"

    ma_le_tan = Column(
        Integer,
        ForeignKey("nguoi_dung.user_id", ondelete="CASCADE"),
        primary_key=True
    )
    quay_lam_viec = Column(String(50), nullable=True)
    ca_truc = Column(String(50), nullable=True)  # Sang, Chieu, Toi
    ngay_vao_lam = Column(DateTime(timezone=True), default=utc_now)

    # Dùng dạng chuỗi "[LeTan.ma_le_tan]" để PyCharm nhận diện đúng kiểu tham chiếu
    user = relationship(
        "NguoiDung",
        foreign_keys="[LeTan.ma_le_tan]"
    )
