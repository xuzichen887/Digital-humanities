# TEI P5 paragraph extraction

TEI (Text Encoding Initiative) P5 is a widely used XML vocabulary for scholarly editions. This tool extracts paragraph text from `<text><body>` into JSON Lines, retaining paragraph IDs, nearest division identifiers and language annotations.

```bash
python src/tei_extract.py path/to/permitted-edition.xml > paragraphs.jsonl
python -m unittest discover -s tests -v
```

Each line is a JSON object with `id`, `section`, `language`, and `text`. UTF-8 Chinese and other Unicode scripts are preserved. Editorial `<note>` elements are excluded. The extractor does not perform Chinese word segmentation, interpret doctrine, or preserve the full critical apparatus. It is a starter for corpus preparation, not a complete TEI processor.

## Provenance and permissions

No third-party texts are bundled. Before processing or distributing an edition, check its license and record the original edition, editor/translator, repository URL, date accessed, and permitted reuse terms. The TEI P5 Guidelines are maintained by the Text Encoding Initiative Consortium: https://tei-c.org/guidelines/p5/.
