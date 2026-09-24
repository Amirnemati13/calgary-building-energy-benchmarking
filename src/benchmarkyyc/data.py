"""Download dated public snapshots and retain source-level provenance."""

import argparse
from datetime import datetime, timezone
import hashlib
import json
from pathlib import Path
import time
from urllib.parse import urlencode
from urllib.request import Request, urlopen

import pandas as pd

BASE_URL = "https://grid.opentech.eco/orgs/calgary/api/public/v2/viz/"
PROGRAM_URL = "https://www.calgary.ca/environment/programs/building-energy-benchmarking-program.html"
FIELDS = {
    "eui-site": "site_eui", "eui-source": "source_eui",
    "ghg-intensity": "ghg_intensity", "ghg-total": "total_ghg_t",
    "energy-star-score": "energy_star_score", "water-use-intensity": "water_intensity",
}
EXPECTED_UNITS = {
    "eui-site": "kWh/m**2/year", "eui-source": "kWh/m**2/year",
    "gross-floor-area": "m**2", "year-built": "year",
    "ghg-intensity": "kgCO2e/m**2/year", "ghg-total": "tCO2e/year",
    "energy-star-score": "energystar", "water-use-intensity": "m**3/m**2/year",
}


def download(url):
    """Read public resources with a timeout and bounded retries."""
    for attempt in range(3):
        try:
            request = Request(url, headers={"User-Agent": "CalgaryBuildingEnergyResearch/0.1"})
            with urlopen(request, timeout=60) as response:
                return response.read()
        except OSError:
            if attempt == 2:
                raise
            time.sleep(1 + attempt)


def quantity(value, unit):
    if value is None:
        return None
    if not isinstance(value, list) or len(value) != 2:
        raise ValueError(f"Expected [value, unit], received {value!r}")
    if str(value[1]).replace("CO_2", "CO2") != unit:
        raise ValueError(f"Unexpected unit: {value[1]!r}; expected {unit!r}")
    return value[0]


def flatten_cycle(payload, cycle):
    """Keep one record per disclosed property in the requested reporting cycle."""
    cycle_id = cycle["cycle-id"]
    if payload.get("viz.properties/cycle-id") != cycle_id:
        raise ValueError("Response cycle does not match the requested cycle")
    rows = []
    for property_id, prop in payload["viz.properties/properties"].items():
        values = prop.get("cycles", {}).get(cycle_id)
        if values is None:
            continue
        if prop.get("property-id", property_id) != property_id:
            raise ValueError("Property key and disclosed identifier disagree")
        coord = prop.get("coord") or {}
        row = {
            "property_id": property_id, "report_year": cycle["cycle-year"],
            "organization": prop.get("organization"), "city": prop.get("city"),
            "latitude": coord.get("lat"), "longitude": coord.get("lng"),
            "floor_area_m2": quantity(prop.get("gross-floor-area"), "m**2"),
            "year_built": quantity(prop.get("year-built"), "year"),
            "property_type": values.get("property-type"),
        }
        for source, column in FIELDS.items():
            row[column] = quantity(values.get(source), EXPECTED_UNITS[source])
        rows.append(row)
    return rows


def fetch_snapshot(destination):
    """Create a new snapshot; never overwrite a previous download."""
    destination = Path(destination)
    destination.mkdir(parents=True, exist_ok=False)
    config_bytes = download(BASE_URL + "config")
    config = json.loads(config_bytes)
    attributes = config["viz.attributes/attributes-config"]["attributes-table"]
    for key, expected in EXPECTED_UNITS.items():
        if attributes[key]["unit"] != expected:
            raise ValueError(f"Source unit changed for {key}")
    cycles = sorted(config["viz.cycles/all-cycles"], key=lambda c: c["cycle-year"])
    # Retain analytical metadata only; omit unrelated map-provider configuration.
    metadata = {"cycles": cycles, "units": EXPECTED_UNITS}
    (destination / "source_metadata.json").write_text(json.dumps(metadata, indent=2), encoding="utf-8")
    rows, endpoints = [], []
    for cycle in cycles:
        url = BASE_URL + "properties?" + urlencode({"cycle-id": cycle["cycle-id"]})
        content = download(url)
        year_rows = flatten_cycle(json.loads(content), cycle)
        (destination / f"properties_{cycle['cycle-year']}.json").write_bytes(content)
        rows.extend(year_rows)
        endpoints.append({"year": cycle["cycle-year"], "url": url,
                          "rows": len(year_rows), "sha256": hashlib.sha256(content).hexdigest()})
    panel = pd.DataFrame(rows)
    if panel.empty or panel.duplicated(["property_id", "report_year"]).any():
        raise ValueError("Empty panel or duplicate property-year keys")
    panel_path = destination / "panel.csv"
    panel.to_csv(panel_path, index=False, encoding="utf-8")
    provenance = {
        "downloaded_utc": datetime.now(timezone.utc).isoformat(),
        "program_url": PROGRAM_URL, "map_url": "https://grid.opentech.eco/orgs/calgary/viz",
        "config_url": BASE_URL + "config", "config_sha256": hashlib.sha256(config_bytes).hexdigest(),
        "endpoints": endpoints, "units": EXPECTED_UNITS,
        "records": len(panel), "unique_properties": int(panel.property_id.nunique()),
        "panel_sha256": hashlib.sha256(panel_path.read_bytes()).hexdigest(),
    }
    (destination / "provenance.json").write_text(json.dumps(provenance, indent=2), encoding="utf-8")
    return provenance


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", type=Path, required=True, help="A new snapshot directory")
    args = parser.parse_args()
    info = fetch_snapshot(args.output)
    print(f"Downloaded {info['records']} records for {info['unique_properties']} properties.")
    print(f"Snapshot: {args.output}")


if __name__ == "__main__":
    main()
