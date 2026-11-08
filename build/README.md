# build — サイトを組むスクリプト

`site/` の HTML は**手で書かない。このフォルダのスクリプトが書き出す。**
ヘッダーとフッターを1か所で持つため(全ページ同一にする、という 2026-11-03 の決定)。

| ファイル | 書き出すもの |
| --- | --- |
| `build.py` | トップ `/`、`/service/web/`、`404.html`。**HEAD と FOOT の正本はここ** |
| `build2.py` | `/service/tarareba-board/`、`/service/event/`。build.py の HEAD/FOOT を読む |
| `build3.py` | `/company/`、`/law-1/`、`/privacy-policy/`、`/terms-of-service/`。同上 |

```bash
cd /Users/imaitomoki/work/maimai_os && for f in ligula/web/build/build*.py; do python3 "$f"; done
```

- 書き出し先は各スクリプトの `SITE`(絶対パス)。**リポジトリを別の場所に置いたら直す。**
- 直したら `site/README.md` のとおり `inspect.mjs` にかける。
- **残り7枚の下層ページ**(`/news/`、`/past-projects/`、PR4枚)はまだ旧デザインで、ここでは組んでいない。

## ビルドで再生成されないファイル

`site/CNAME`（独自ドメイン）、`site/inquiry/index.html`（旧 URL の転送）、
`site/robots.txt`、`site/_redirects` は手書き。`build*.py` は触らないので、消さないこと。
