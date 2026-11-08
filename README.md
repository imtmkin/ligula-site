# ligula-site

株式会社Ligula の自社サイト ligula.jp の中身。**ここが正本。**

2026-11-08 に社内の作業用リポジトリから切り出した。
お知らせの管理画面をあとで足すには、サイトがリポジトリそのものである必要があるため。

**配信は GitHub Pages**（`.github/workflows/pages.yml` が `site/` を公開する）。
`netlify.toml` は Netlify に戻すときのために残してある。いまは効いていない。

## 構成

| | |
| --- | --- |
| `site/` | 公開されるファイル。Netlify がこのフォルダをそのまま配信する |
| `build/` | ページを書き出す Python。ヘッダーとフッターの正本は `build/build.py` |
| `netlify.toml` | 配信設定（publish = site、セキュリティヘッダー） |

## 直し方

ヘッダー・フッター・共通の `<head>` は **`build/build.py` の HEAD / FOOT が正本**。
ここを直して `build*.py` を全部走らせる。各ページの HTML を直接いじると、次の書き出しで戻る。

```
cd build && python3 build.py && python3 build2.py && python3 build3.py && python3 build4.py
```

ローカル確認は `python3 -m http.server 8793 --directory site`。

公開前は Taste Skill の `inspect.mjs` を **`site/` の中から**走らせる(cwd が HTTP ルートになるため)。

## 台帳はここには無い

方針・要確認・料金の正本・クレドは、社内の別リポジトリにある。**このリポジトリは public。**

**サイトの計算機 `site/estimate.js` の `RATE` は、社内の料金台帳と同じ数字でなければならない。**
片方だけ直すとずれる。金額を変えるときは、必ず台帳のほうから。

## 入れてはいけないもの

- 顧客の連絡先・契約条件・見積額。
- パスワード、API キー、トークン。
- 公開対象から外した案件写真（社内の別リポジトリに置いてある）。
- 社内の判断や検討の記録。**ここは public なので、外に出してよいものだけ。**
