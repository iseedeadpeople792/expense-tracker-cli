"""Трекер расходов в консоли: SQLite, без зависимостей.
Примеры:
  python expense.py add 450 еда --note "обед"
  python expense.py list --month 2026-10
  python expense.py report --month 2026-10
"""
import argparse
import datetime
import os
import sqlite3

DB = os.environ.get("EXPENSE_DB", "expenses.db")


def connect(path=None):
    con = sqlite3.connect(path or DB)
    con.execute(
        "CREATE TABLE IF NOT EXISTS expenses (id INTEGER PRIMARY KEY, day TEXT NOT NULL, amount REAL NOT NULL,"
        " category TEXT NOT NULL, note TEXT NOT NULL DEFAULT '')"
    )
    return con


def add(con, amount, category, note="", day=None):
    if amount <= 0:
        raise ValueError("сумма должна быть больше нуля")
    day = day or datetime.date.today().isoformat()
    con.execute("INSERT INTO expenses (day, amount, category, note) VALUES (?, ?, ?, ?)", (day, amount, category.lower(), note))
    con.commit()


def rows(con, month=None):
    sql, args = "SELECT day, amount, category, note FROM expenses", ()
    if month:
        sql, args = sql + " WHERE day LIKE ?", (month + "%",)
    return con.execute(sql + " ORDER BY day, id", args).fetchall()


def report(con, month=None):
    """Возвращает (итого, список (категория, сумма, доля %)) по убыванию суммы."""
    by_cat = {}
    for _, amount, category, _ in rows(con, month):
        by_cat[category] = by_cat.get(category, 0) + amount
    total = sum(by_cat.values())
    return total, [(c, s, round(100 * s / total, 1)) for c, s in sorted(by_cat.items(), key=lambda x: -x[1])]


def main(argv=None):
    p = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = p.add_subparsers(dest="cmd", required=True)
    a = sub.add_parser("add")
    a.add_argument("amount", type=float)
    a.add_argument("category")
    a.add_argument("--note", default="")
    for name in ("list", "report"):
        sub.add_parser(name).add_argument("--month", help="ГГГГ-ММ")
    args = p.parse_args(argv)
    con = connect()
    if args.cmd == "add":
        add(con, args.amount, args.category, args.note)
        print("Добавлено")
    elif args.cmd == "list":
        for day, amount, cat, note in rows(con, args.month):
            print(f"{day}  {amount:>9.2f}  {cat:<12} {note}")
    else:
        total, items = report(con, args.month)
        print(f"Итого: {total:.2f}")
        for cat, s, pct in items:
            print(f"  {cat:<12} {s:>9.2f}  {pct}%")


if __name__ == "__main__":
    main()
