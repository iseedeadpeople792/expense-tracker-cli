# expense-tracker-cli

Консольный трекер личных расходов на Python и SQLite. Без внешних зависимостей.

## Возможности
- добавление расхода с категорией и заметкой;
- список расходов за месяц;
- отчёт по категориям с долей в процентах.

## Запуск
```
python expense.py add 450 еда --note "обед"
python expense.py list --month 2026-10
python expense.py report --month 2026-10
```
База хранится в `expenses.db` (путь можно задать переменной `EXPENSE_DB`).

## Тесты
```
python -m unittest -v
```

Учебный проект для портфолио. Python 3.9+.
