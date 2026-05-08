# Research Plan

## Research Question

暗号学的ハッシュ関数は、ラウンド数が増えるにつれてどの段階で機械学習から見てもランダムに近づくのか。

## MVP Hypotheses

1. ラウンド数が少ない toy hash は Avalanche Effect が弱い。
2. ラウンド数が少ない toy hash の出力は、簡単な識別器でランダム列から区別しやすい。
3. ラウンド数を増やすと、bit flip 率は 50% に近づき、識別器の精度は 50% に近づく。

## Experiments

### 1. Avalanche Effect

入力をランダム生成し、1 bit だけ反転させる。元入力と反転入力のハッシュ出力のハミング距離を測る。

指標:

- mean flip ratio
- min/max flip ratio
- standard deviation

理想値:

```text
mean flip ratio ~= 0.5
```

### 2. Distinguishing Experiment

同じ長さの二種類のデータを用意する。

- class 1: toy hash の出力
- class 0: ランダム bit 列

簡単なロジスティック回帰を標準ライブラリだけで実装し、出力 bit から class を予測する。

指標:

- train accuracy
- test accuracy

理想的なハッシュ:

```text
test accuracy ~= 0.5
```

## Next Steps

- 実 SHA256 の reduced-round compression に近い実装を追加する
- 入力差分を固定した differential dataset を作る
- PyTorch 版のニューラル識別器を追加する
- 結果を CSV/JSON に保存し、グラフ化する
