import unittest

from src.gazetteer import csv_to_geojson


HEADER = "site_id,name,latitude,longitude,source_url,license,tradition,period,notes\n"
ROW = "fictional-1,虚构寺院,12.5,-42.25,https://example.org/source,CC0,Buddhist,,Synthetic example\n"


class GazetteerTests(unittest.TestCase):
    def test_unicode_and_geojson_coordinate_order(self):
        data = csv_to_geojson(HEADER + ROW)
        self.assertEqual(data["type"], "FeatureCollection")
        feature = data["features"][0]
        self.assertEqual(feature["geometry"]["coordinates"], [-42.25, 12.5])
        self.assertEqual(feature["properties"]["name"], "虚构寺院")
        self.assertEqual(feature["properties"]["tradition"], "Buddhist")
        self.assertNotIn("period", feature["properties"])

    def test_empty_rows_and_bom(self):
        self.assertEqual(csv_to_geojson("\ufeff" + HEADER)["features"], [])

    def test_missing_provenance(self):
        with self.assertRaisesRegex(ValueError, "missing license"):
            csv_to_geojson(HEADER + ROW.replace("CC0", ""))

    def test_duplicate_id(self):
        with self.assertRaisesRegex(ValueError, "duplicate site_id"):
            csv_to_geojson(HEADER + ROW + ROW)

    def test_invalid_coordinates(self):
        for latitude, longitude in [("91", "0"), ("0", "-181"), ("NaN", "0"), ("hello", "0")]:
            with self.subTest(latitude=latitude, longitude=longitude):
                with self.assertRaisesRegex(ValueError, "coordinates"):
                    csv_to_geojson(HEADER + ROW.replace("12.5,-42.25", f"{latitude},{longitude}"))

    def test_missing_columns(self):
        with self.assertRaisesRegex(ValueError, "Missing required CSV columns"):
            csv_to_geojson("site_id,name\na,b\n")

    def test_source_url_validation(self):
        with self.assertRaisesRegex(ValueError, "source_url"):
            csv_to_geojson(HEADER + ROW.replace("https://example.org/source", "ftp://example.org/source"))

    def test_extra_fields(self):
        with self.assertRaisesRegex(ValueError, "too many CSV fields"):
            csv_to_geojson(HEADER + ROW.rstrip("\n") + ",extra\n")


if __name__ == "__main__":
    unittest.main()
