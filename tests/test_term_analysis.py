import unittest
from src.term_analysis import count_terms


class TermAnalysisTests(unittest.TestCase):
    def test_case_insensitive_and_boundaries(self):
        self.assertEqual(count_terms("Karma karma karmic. Dharma!", ["karma", "dharma"]), {"karma": 2, "dharma": 1})

    def test_unicode_and_phrases(self):
        self.assertEqual(count_terms("空性与慈悲。空性。 middle   way; Middle way.", ["空性", "middle way"]), {"空性": 2, "middle way": 2})

    def test_blank_term_rejected(self):
        with self.assertRaises(ValueError):
            count_terms("some text", ["  "])


if __name__ == "__main__":
    unittest.main()
