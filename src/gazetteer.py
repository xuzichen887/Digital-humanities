"""Convert an attributed sacred-site gazetteer CSV to GeoJSON.

The module intentionally ships no real site locations or third-party datasets.
"""

import argparse
import csv
import io
import json
import math
from pathlib import Path
from urllib.parse import urlsplit

REQUIRED = ("site_id", "name", "latitude", "longitude", "source_url", "license")
OPTIONAL = ("tradition", "period", "notes")


def csv_to_geojson(csv_text: str) -> dict:
    """Validate a UTF-8 CSV and produce a GeoJSON FeatureCollection.

    Raises ValueError with a row number for malformed or unattributed records.
    Coordinates follow GeoJSON's [longitude, latitude] order (WGS84 degrees).
    """
    reader = csv.DictReader(io.StringIO(csv_text.lstrip("\ufeff")))
    if not reader.fieldnames:
        raise ValueError("CSV must contain a header row")
    missing = [field for field in REQUIRED if field not in reader.fieldnames]
    if missing:
        raise ValueError("Missing required CSV columns: " + ", ".join(missing))

    seen_ids = set()
    features = []
    for row_number, row in enumerate(reader, start=2):
        if None in row:
            raise ValueError(f"Row {row_number}: too many CSV fields")
        values = {key: (row.get(key) or "").strip() for key in reader.fieldnames}
        for field in REQUIRED:
            if not values[field]:
                raise ValueError(f"Row {row_number}: missing {field}")

        site_id = values["site_id"]
        if site_id in seen_ids:
            raise ValueError(f"Row {row_number}: duplicate site_id {site_id!r}")
        seen_ids.add(site_id)

        try:
            lat = float(values["latitude"])
            lon = float(values["longitude"])
        except ValueError as exc:
            raise ValueError(f"Row {row_number}: coordinates must be numeric") from exc
        if not math.isfinite(lat) or not math.isfinite(lon) or not (-90 <= lat <= 90) or not (-180 <= lon <= 180):
            raise ValueError(f"Row {row_number}: coordinates out of range or non-finite")

        parsed = urlsplit(values["source_url"])
        if parsed.scheme not in ("http", "https") or not parsed.netloc:
            raise ValueError(f"Row {row_number}: source_url must be an absolute HTTP(S) URL")

        properties = {field: values[field] for field in ("site_id", "name", "source_url", "license")}
        properties.update({field: values[field] for field in OPTIONAL if values.get(field)})
        features.append({
            "type": "Feature",
            "geometry": {"type": "Point", "coordinates": [lon, lat]},
            "properties": properties,
        })

    return {"type": "FeatureCollection", "features": features}


def main() -> None:
    parser = argparse.ArgumentParser(description="Validate an attributed sacred-site CSV and export GeoJSON")
    parser.add_argument("input", type=Path, help="CSV with UTF-8 encoding")
    parser.add_argument("-o", "--output", type=Path, help="GeoJSON output path (default: stdout)")
    args = parser.parse_args()
    try:
        data = csv_to_geojson(args.input.read_text(encoding="utf-8-sig"))
        output = json.dumps(data, ensure_ascii=False, indent=2) + "\n"
        if args.output:
            args.output.write_text(output, encoding="utf-8")
        else:
            print(output, end="")
    except (OSError, UnicodeError, ValueError, csv.Error) as exc:
        parser.error(str(exc))


if __name__ == "__main__":
    main()
