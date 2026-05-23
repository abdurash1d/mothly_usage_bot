from datetime import date

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app.db.base import Base
from app.models.income_types import IncomeType
from app.models.user import User
from app.schemas import ExpenseCreate, ExpenseUpdate, IncomeCreate, IncomeUpdate
from app.services.expenses import (
    create_expense,
    create_income,
    delete_expense,
    delete_income,
    list_monthly_ledger,
    monthly_summary,
    update_expense,
    update_income,
)


def test_create_and_monthly_summary_flow():
    engine = create_engine("sqlite+pysqlite:///:memory:")
    TestingSession = sessionmaker(bind=engine)
    Base.metadata.create_all(bind=engine)

    db = TestingSession()
    user = User(telegram_user_id=1, username="owner")
    db.add(user)
    db.commit()
    db.refresh(user)

    create_expense(
        db,
        user.id,
        ExpenseCreate(
            category_key="transportation",
            amount_uzs=15000,
            expense_date=date(2026, 5, 10),
            note="taxi",
        ),
    )
    create_expense(
        db,
        user.id,
        ExpenseCreate(
            category_key="market",
            amount_uzs=45000,
            expense_date=date(2026, 5, 11),
            note=None,
        ),
    )
    create_income(
        db,
        user.id,
        IncomeCreate(
            income_type_key=IncomeType.SALARY.value,
            amount_uzs=1000000,
            income_date=date(2026, 5, 1),
            note="main salary",
        ),
    )
    create_income(
        db,
        user.id,
        IncomeCreate(
            income_type_key=IncomeType.BONUS.value,
            amount_uzs=250000,
            income_date=date(2026, 5, 20),
            note=None,
        ),
    )

    summary = monthly_summary(db, user.id, 2026, 5)
    assert summary.expense_total_uzs == 60000
    assert summary.income_total_uzs == 1250000
    assert summary.balance_uzs == 1190000
    assert summary.expense_entry_count == 2
    assert summary.income_entry_count == 2
    assert len(summary.by_category) == 2

    ledger = list_monthly_ledger(db, user.id, 2026, 5)
    assert len(ledger) == 4
    assert ledger[0].entry_type in {"income", "expense"}


def test_update_and_delete_entries_flow():
    engine = create_engine("sqlite+pysqlite:///:memory:")
    TestingSession = sessionmaker(bind=engine)
    Base.metadata.create_all(bind=engine)
    db = TestingSession()

    user = User(telegram_user_id=1, username="owner")
    db.add(user)
    db.commit()
    db.refresh(user)

    expense = create_expense(
        db,
        user.id,
        ExpenseCreate(
            category_key="market",
            amount_uzs=12000,
            expense_date=date(2026, 5, 10),
            note="wrong",
        ),
    )
    income = create_income(
        db,
        user.id,
        IncomeCreate(
            income_type_key=IncomeType.SALARY.value,
            amount_uzs=1000000,
            income_date=date(2026, 5, 1),
            note=None,
        ),
    )

    updated_expense = update_expense(
        db,
        user.id,
        expense.id,
        ExpenseUpdate(category_key="transportation", amount_uzs=15000, note="fixed"),
    )
    assert updated_expense.category == "transportation"
    assert updated_expense.amount_uzs == 15000

    updated_income = update_income(
        db,
        user.id,
        income.id,
        IncomeUpdate(income_type_key=IncomeType.KPI.value, amount_uzs=1100000),
    )
    assert updated_income.income_type == IncomeType.KPI.value
    assert updated_income.amount_uzs == 1100000

    summary = monthly_summary(db, user.id, 2026, 5)
    assert summary.expense_total_uzs == 15000
    assert summary.income_total_uzs == 1100000

    assert delete_expense(db, user.id, expense.id) is True
    assert delete_income(db, user.id, income.id) is True

    summary_after_delete = monthly_summary(db, user.id, 2026, 5)
    assert summary_after_delete.expense_total_uzs == 0
    assert summary_after_delete.income_total_uzs == 0
