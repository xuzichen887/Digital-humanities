"""Extract paragraph records from TEI P5 XML without external dependencies."""
import argparse
import json
import re
import xml.etree.ElementTree as ET
from pathlib import Path

NS = "{http://www.tei-c.org/ns/1.0}"
XML_ID = "{http://www.w3.org/XML/1998/namespace}id"
XML_LANG = "{http://www.w3.org/XML/1998/namespace}lang"

def extract_paragraphs(xml: str) -> list[dict]:
    root = ET.fromstring(xml)
    if root.tag != NS + "TEI":
        raise ValueError("Expected TEI P5 namespace")
    body = root.find(f"./{NS}text/{NS}body")
    if body is None:
        raise ValueError("Missing TEI text/body")
    records = []
    def walk(node, section="", language=""):
        language = node.get(XML_LANG, language)
        if node.tag == NS + "div":
            section = node.get(XML_ID, node.get("n", section))
        if node.tag == NS + "p":
            # Exclude editorial notes from the searchable reading text.
            copy = ET.fromstring(ET.tostring(node))
            for parent in copy.iter():
                for child in list(parent):
                    if child.tag == NS + "note":
                        parent.remove(child)
            content = re.sub(r"\s+", " ", "".join(copy.itertext())).strip()
            if content:
                records.append({"id": node.get(XML_ID, f"p{len(records)+1:04d}"),
                                "section": section, "language": language, "text": content})
            return
        for child in node:
            walk(child, section, language)
    walk(body)
    return records

def main():
    parser = argparse.ArgumentParser(description="TEI P5 paragraphs to JSONL")
    parser.add_argument("input", type=Path)
    args = parser.parse_args()
    for row in extract_paragraphs(args.input.read_text(encoding="utf-8")):
        print(json.dumps(row, ensure_ascii=False))

if __name__ == "__main__":
    main()
