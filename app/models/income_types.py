from enum import Enum


class IncomeType(str, Enum):
    SALARY = "salary"
    BONUS = "bonus"
    KPI = "kpi"


INCOME_LABELS_RU = {
    IncomeType.SALARY: "Зарплата",
    IncomeType.BONUS: "Бонус",
    IncomeType.KPI: "KPI",
}


INCOME_LABELS_UZ = {
    IncomeType.SALARY: "Maosh",
    IncomeType.BONUS: "Bonus",
    IncomeType.KPI: "KPI",
}


def income_type_options():
    return [
        {"key": key.value, "label_ru": INCOME_LABELS_RU[key], "label_uz": INCOME_LABELS_UZ[key]}
        for key in IncomeType
    ]
