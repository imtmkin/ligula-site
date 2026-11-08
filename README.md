# ligula-site

株式会社Ligula の自社サイト ligula.jp の中身。**ここが正本。**

2026-11-08 に `maimai_os/ligula/web/` から切り出した。
お知らせの管理画面（Decap CMS）をあとで足すには、サイトがリポジトリそのものである必要があるため。

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

方針・移行手順・要確認は `maimai_os/ligula/web/plan.md`。
料金の正本は `maimai_os/ligula/pricing.md`（**サイトの計算機 `site/estimate.js` の RATE と同じ数字にする。片方だけ直すとずれる**）。
クレドは `maimai_os/ligula/credo.md`。

## 入れてはいけないもの

- 顧客の連絡先・契約条件・見積額。
- パスワード、API キー、トークン。
- 公開対象から外した案件写真（`maimai_os/ligula/web/_unused-assets/` に置いてある）。
