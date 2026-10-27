import unittest

import expense


class ExpenseTest(unittest.TestCase):
    def setUp(self):
        self.con = expense.connect(":memory:")

    def test_report_groups_and_sorts(self):
        expense.add(self.con, 100, "Еда", day="2026-10-01")
        expense.add(self.con, 300, "транспорт", day="2026-10-02")
        expense.add(self.con, 100, "еда", day="2026-10-03")
        total, items = expense.report(self.con, "2026-10")
        self.assertEqual(total, 500)
        self.assertEqual(items[0], ("транспорт", 300, 60.0))
        self.assertEqual(items[1], ("еда", 200, 40.0))

    def test_month_filter(self):
        expense.add(self.con, 50, "еда", day="2026-09-30")
        expense.add(self.con, 70, "еда", day="2026-10-01")
        self.assertEqual(len(expense.rows(self.con, "2026-10")), 1)

    def test_rejects_non_positive(self):
        with self.assertRaises(ValueError):
            expense.add(self.con, 0, "еда")


if __name__ == "__main__":
    unittest.main()
