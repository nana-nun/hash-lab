# Links

Web記事、仕様ページ、データセット、ツールなど、BibTeXにしにくい参考リンクをためる場所です。

## Format

```markdown
- Title:
  - URL:
  - Author / Organization:
  - Year / Accessed:
  - Note:
```

## Links

- Title: Dieharder: A Random Number Test Suite
  - URL: https://rgbrown.org/General/general.php
  - Author / Organization: Robert G. Brown, Dirk Eddelbuettel, David Bauer
  - Year / Accessed: 2026-05-10
  - Note: Diehard battery を拡張したRNG test suite。hash-lab ではすぐ外部tool依存にせず、frequency/runs/serial/correlation の小さなbaselineを実装した後、比較対象として参照する。
- Title: Practically Random
  - URL: https://sourceforge.net/projects/pracrand/
  - Author / Organization: PractRand project
  - Year / Accessed: 2026-05-10
  - Note: 大きなbit streamを継続的に検査するRNG test suite。hash-lab の小規模toy実験には重い可能性があるため、長いdigest streamを保存できる段階の参考候補に留める。
