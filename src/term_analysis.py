"""Small, dependency-free text analysis utilities for digital humanities research.

Counts user-specified terms in a document. Results are descriptive, not an
interpretation of the text or evidence of an author's intent.
"""
from collections import Counter
from pathlib import Path
import argparse
import json
import re


def count_terms(text: str, terms: list[str]) -> dict[str, int]:
    """Count whole-term matches (case-insensitive), including multiword terms.

    Whitespace between words in a term can vary in the text. Terms are matched
    independently, so overlapping phrases may each be counted.
    """
    results: dict[str, int] = {}
    for term in terms:
        normalized = " ".join(term.split())
        if not normalized:
            raise ValueError("Terms must not be blank.")
        words = [re.escape(word) for word in normalized.split(" ")]
        pattern = r"(?<!\w)" + r"\s+".join(words) + r"(?!\w)"
        results[term] = len(re.findall(pattern, text, flags=re.IGNORECASE))
    return results


def main() -> None:
    parser = argparse.ArgumentParser(description="Count concepts in a UTF-8 text.")
    parser.add_argument("file", type=Path, help="UTF-8 text document")
    parser.add_argument("terms", nargs="+", help="Words or quoted phrases to count")
    args = parser.parse_args()
    text = args.file.read_text(encoding="utf-8")
    print(json.dumps(count_terms(text, args.terms), ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
