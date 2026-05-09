# References

研究で使う参考文献をためておく場所です。

## Files

- `reading-list.md`: 人間が読みやすい参考文献リスト
- `papers.bib`: BibTeX形式の文献データ
- `links.md`: Web記事、仕様ページ、関連リンク
- `notes/`: 論文・記事ごとの読書メモ

## Note Template

`notes/` に文献ごとのメモを追加するときは、次の形を推奨します。

```markdown
# Title

## Citation

- Authors:
- Year:
- Link:
- BibTeX key:

## Summary

## Important Ideas

## Relation to hash-lab

## Questions
```

## Scope

この研究では、実システムへの攻撃手順ではなく、縮小ラウンド・toy hash・機械学習による識別実験・暗号学的性質の理解に関係する文献を優先します。

## Priority for Individual Notes

`notes/` の個別メモは、次の順で優先します。

- 現在の実験解釈に直接関係する主軸文献。例: avalanche / SAC、reduced-round SHA-like analysis、neural distinguisher。
- `reading-list.md` で同じ分野の基準点になる文献。例: Webster/Tavares、Forré、Gohr、Benamira et al.
- 実験項目や baseline を増やす判断に使う文献。例: SAC、BIC、randomness tests、low-order statistics。
- 背景理解には重要だが hash-lab の実験に直接つながらない文献は、まず `reading-list.md` の短い説明に留めます。
