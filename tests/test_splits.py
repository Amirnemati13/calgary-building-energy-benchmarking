import unittest
import pandas as pd
from benchmarkyyc.splits import property_splits, spatial_splits, temporal_split


class SplitTests(unittest.TestCase):
    def setUp(self):
        self.frame = pd.DataFrame([
            {"property_id": f"p{i}", "report_year": year,
             "latitude": 50.9 + i * .06, "longitude": -114.1}
            for i in range(6) for year in [2022, 2023, 2024]])

    def test_grouped_split_keeps_all_years_of_a_property_together(self):
        for train, test in property_splits(self.frame, n_splits=3):
            self.assertTrue(set(self.frame.iloc[train].property_id).isdisjoint(self.frame.iloc[test].property_id))
            self.assertLessEqual(self.frame.iloc[test].report_year.max(), 2023)

    def test_spatial_split_keeps_repeated_properties_together(self):
        for train, test in spatial_splits(self.frame, n_splits=3):
            self.assertTrue(set(self.frame.iloc[train].property_id).isdisjoint(self.frame.iloc[test].property_id))

    def test_temporal_test_never_trains_on_present_or_future(self):
        train, test = temporal_split(self.frame, 2023)
        self.assertTrue((self.frame.iloc[train].report_year < 2023).all())
        self.assertTrue((self.frame.iloc[test].report_year == 2023).all())

    def test_invalid_block_size_fails(self):
        with self.assertRaises(ValueError):
            list(spatial_splits(self.frame, block_km=0))

    def test_nearby_properties_share_spatial_fold(self):
        paired = self.frame.copy()
        paired['property_id'] = paired.property_id + '_neighbor'
        combined = pd.concat([self.frame, paired], ignore_index=True)
        for train, test in spatial_splits(combined, n_splits=3):
            train_locations = set(zip(combined.iloc[train].latitude, combined.iloc[train].longitude))
            test_locations = set(zip(combined.iloc[test].latitude, combined.iloc[test].longitude))
            self.assertTrue(train_locations.isdisjoint(test_locations))
