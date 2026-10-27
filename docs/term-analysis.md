# Term frequency analysis (starter)

This small command-line utility helps researchers count vocabulary across
UTF-8 text documents, including Buddhist and philosophical texts.

## Try it

Save a text you have permission to process as `passage.txt`, then run:

```bash
python src/term_analysis.py passage.txt karma dharma "middle way"
python -m unittest discover -s tests -v
```

The tool prints a JSON object mapping each requested term to its count.
It accepts Unicode and case-insensitive matching, and normalizes whitespace
within multiword search phrases.

## Research cautions

- Counts are not interpretations, translations, or measures of significance.
- Inflected forms, spelling variants, and different translations are counted
  separately unless explicitly supplied as different search terms.
- Chinese or other languages without space-separated words may require
  segmentation for meaningful word-level analysis.
- Record the edition, translator, source URL, date accessed, and text license
  for each corpus before publishing any comparative results.
- No third-party text or copyrighted corpus is bundled with this project.

## Next steps

Add documented corpora with appropriate permissions, normalize terminology
across translations, and visualize relative frequencies by chapter.
