"""Evaluation splits with explicit property and time boundaries."""

import numpy as np
from sklearn.model_selection import GroupKFold


def property_splits(frame, through_year=2023, n_splits=5):
    positions = np.flatnonzero(frame.report_year.to_numpy() <= through_year)
    for train, test in GroupKFold(n_splits).split(positions, groups=frame.iloc[positions].property_id):
        yield positions[train], positions[test]


def spatial_splits(frame, through_year=2023, n_splits=5, block_km=5):
    if block_km <= 0:
        raise ValueError("block_km must be positive")
    positions = np.flatnonzero(frame.report_year.to_numpy() <= through_year)
    subset = frame.iloc[positions]
    coordinates = subset.groupby("property_id")[["latitude", "longitude"]].median()
    if coordinates.isna().any().any():
        raise ValueError("Spatial validation requires coordinates for each property")
    east = (coordinates.longitude + 114.3) * 111.32 * np.cos(np.deg2rad(51.05))
    north = (coordinates.latitude - 50.8) * 111.32
    blocks = np.floor(east / block_km).astype(int).astype(str) + "_" + np.floor(north / block_km).astype(int).astype(str)
    groups = subset.property_id.map(blocks).to_numpy()
    for train, test in GroupKFold(n_splits).split(positions, groups=groups):
        yield positions[train], positions[test]


def temporal_split(frame, test_year):
    years = frame.report_year.to_numpy()
    train, test = np.flatnonzero(years < test_year), np.flatnonzero(years == test_year)
    if not len(train) or not len(test):
        raise ValueError(f"Insufficient observations for temporal test {test_year}")
    return train, test
