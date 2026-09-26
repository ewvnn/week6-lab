import unittest

from duckfine import DuckFine


class TestDuckFine(unittest.TestCase):
    def setUp(self):
        self.fine = DuckFine("M001")

    def test_init_stores_member_id(self):
        self.assertEqual(self.fine.member_id, "M001")

    def test_init_total_owed_starts_at_zero(self):
        self.assertEqual(self.fine.total_owed, 0.0)

    def test_negative_days_raises_value_error(self):
        with self.assertRaises(ValueError):
            self.fine.charge(-1)

    def test_negative_days_does_not_change_total(self):
        with self.assertRaises(ValueError):
            self.fine.charge(-1)
        self.assertEqual(self.fine.total_owed, 0.0)

    def test_zero_days_late_is_free(self):
        self.assertEqual(self.fine.charge(0), 0.0)

    def test_days_within_grace_period_are_free(self):
        self.assertEqual(self.fine.charge(2), 0.0)

    def test_first_day_after_grace_is_charged(self):
        self.assertAlmostEqual(self.fine.charge(3), 0.50)

    def test_fee_is_daily_rate_times_chargeable_days(self):
        self.assertAlmostEqual(self.fine.charge(6), 2.00)

    def test_fee_just_reaching_cap(self):
        self.assertAlmostEqual(self.fine.charge(12), 5.00)

    def test_fee_is_capped_at_max(self):
        self.assertAlmostEqual(self.fine.charge(100), 5.00)

    def test_deluxe_doubles_fee(self):
        self.assertAlmostEqual(self.fine.charge(4, deluxe=True), 2.00)

    def test_deluxe_within_grace_period_is_free(self):
        self.assertEqual(self.fine.charge(2, deluxe=True), 0.0)

    def test_deluxe_fee_is_capped_at_max(self):
        self.assertAlmostEqual(self.fine.charge(10, deluxe=True), 5.00)

    def test_charge_adds_fee_to_total_owed(self):
        self.fine.charge(4)
        self.assertAlmostEqual(self.fine.total_owed, 1.00)

    def test_total_owed_accumulates_across_charges(self):
        self.fine.charge(4)
        self.fine.charge(100)
        self.assertAlmostEqual(self.fine.total_owed, 6.00)

    def test_free_charge_does_not_change_total(self):
        self.fine.charge(1)
        self.assertEqual(self.fine.total_owed, 0.0)

    def test_cap_applies_per_charge_not_to_total(self):
        self.fine.charge(100)
        self.fine.charge(100)
        self.assertAlmostEqual(self.fine.total_owed, 10.00)


if __name__ == "__main__":
    unittest.main()
