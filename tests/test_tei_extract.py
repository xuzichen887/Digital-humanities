import unittest
from src.tei_extract import extract_paragraphs

URI = "http://www.tei-c.org/ns/1.0"

class TEITests(unittest.TestCase):
    def test_paragraphs_and_metadata(self):
        xml = f'<TEI xmlns="{URI}"><text><body><div n="1"><p xml:id="a" xml:lang="zh">空性 <hi>慈悲</hi></p><p>Middle way</p></div></body></text></TEI>'
        rows = extract_paragraphs(xml)
        self.assertEqual(rows[0], {"id":"a","section":"1","language":"zh","text":"空性 慈悲"})
        self.assertEqual(rows[1]["text"], "Middle way")

    def test_invalid_namespace(self):
        with self.assertRaises(ValueError):
            extract_paragraphs("<TEI><text><body/></text></TEI>")

    def test_no_body(self):
        with self.assertRaises(ValueError):
            extract_paragraphs(f'<TEI xmlns="{URI}"/>')

if __name__ == "__main__":
    unittest.main()
