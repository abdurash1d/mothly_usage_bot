from datetime import date, datetime
from typing import Optional

from sqlalchemy import Date, DateTime, ForeignKey, Index, Integer, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base import Base


class Income(Base):
    __tablename__ = "incomes"

    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"), nullable=False, index=True)
    income_type: Mapped[str] = mapped_column(String(32), nullable=False)
    amount_uzs: Mapped[int] = mapped_column(Integer, nullable=False)
    income_date: Mapped[date] = mapped_column(Date, nullable=False, index=True)
    note: Mapped[Optional[str]] = mapped_column(String(1024), nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)

    user = relationship("User")


Index("ix_incomes_user_date", Income.user_id, Income.income_date)
Index("ix_incomes_user_type_date", Income.user_id, Income.income_type, Income.income_date)
