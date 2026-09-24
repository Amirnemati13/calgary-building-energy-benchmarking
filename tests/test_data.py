import unittest
from benchmarkyyc.data import flatten_cycle, quantity


class SourceParsingTests(unittest.TestCase):
    def setUp(self):
        self.cycle = {"cycle-id": "c1", "cycle-year": 2024}
        self.payload = {"viz.properties/cycle-id": "c1", "viz.properties/properties": {
            "p1": {"property-id": "p1", "gross-floor-area": [100, "m**2"],
                   "year-built": [1990, "year"], "cycles": {
                       "c1": {"property-type": "Office", "eui-site": [0, "kWh/m**2/year"],
                              "ghg-intensity": [20, "kgCO_2e/m**2/year"]},
                       "c2": {"eui-site": [999, "kWh/m**2/year"]}}},
            "p2": {"cycles": {"c2": {}}}}}

    def test_selects_only_requested_cycle_and_preserves_zero(self):
        rows = flatten_cycle(self.payload, self.cycle)
        self.assertEqual(len(rows), 1)
        self.assertEqual(rows[0]["site_eui"], 0)
        self.assertIsNone(rows[0]["source_eui"])
        self.assertEqual(rows[0]["report_year"], 2024)

    def test_rejects_wrong_cycle(self):
        self.payload["viz.properties/cycle-id"] = "wrong"
        with self.assertRaises(ValueError):
            flatten_cycle(self.payload, self.cycle)

    def test_rejects_silent_unit_change(self):
        with self.assertRaises(ValueError):
            quantity([100, "GJ/m**2/year"], "kWh/m**2/year")

    def test_rejects_conflicting_identity(self):
        self.payload["viz.properties/properties"]["p1"]["property-id"] = "p2"
        with self.assertRaises(ValueError):
            flatten_cycle(self.payload, self.cycle)
