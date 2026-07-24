from sqlalchemy import Column, String, DateTime, BigInteger, Text
from sqlalchemy.orm import Mapped, mapped_column
from ..db.database import Base


class Urls(Base):
    """URL адреса"""
    __tablename__ = "urls"

    url_id: Mapped[int] = mapped_column(BigInteger, primary_key=True)
    long_url: Mapped[str] = mapped_column(Text, nullable=False)
    short_code: Mapped[str] = mapped_column(
        String(15), 
        nullable=False, 
        unique=True, 
        index=True
    )