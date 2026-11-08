# Xserver へ出す（DNS を触らない方法）

ligula.jp のネームサーバーも A レコードも**触らずに**、いまのサーバーの中身だけを
WordPress から静的サイトへ差し替える手順。**メールの危険はゼロ。**

| | |
| --- | --- |
| サーバー | `sv12775.xserver.jp`（183.181.96.136） |
| 置き場所 | `/home/<アカウント>/ligula.jp/public_html` |
| 送る中身 | `site/` の全部 ＋ `deploy/htaccess` を `.htaccess` として |

**パスワードはこのリポジトリに書かない。**公開リポジトリなので、鍵もここには置かない。

## 1回だけの準備

### SSH を ON にする

サーバーパネル → **SSH設定** → 「ONにする」。

### 鍵を作って登録する

Mac で（鍵は `~/.ssh` に置く。リポジトリには入れない）:

```
[ -f ~/.ssh/xserver_ligula ] || ssh-keygen -t ed25519 -f ~/.ssh/xserver_ligula -N "" -C "ligula-site deploy"; cat ~/.ssh/xserver_ligula.pub
```

出てきた1行をコピーして、サーバーパネル → SSH設定 → **公開鍵登録・設定** に貼る。

### つながるか試す

```
ssh -p 10022 <アカウント>@sv12775.xserver.jp -i ~/.ssh/xserver_ligula
```

アカウント名はサーバーパネルの「FTPアカウント設定」で確認できる（初期ドメイン `xs314724` と同じはず）。

## 出すとき

```
sh deploy/push-to-xserver.sh        # 下見。何が変わるか出るだけ
sh deploy/push-to-xserver.sh --go   # 実際に送る
```

- アカウント名や置き場所が違うときは、`XS_USER=... XS_DOCROOT=... sh deploy/push-to-xserver.sh` のように渡す。
- **送り先に WordPress が残っていると、スクリプトは止まる。**`--delete` で消してしまうため。
  先にバックアップを取り、WordPress を `public_html` の外へ移すこと。

## WordPress の退避（最初の1回）

**消さない。外へ出すだけ。**戻せるようにしておく。

1. サーバーパネル → **バックアップ** で、ファイルとデータベースの両方を取る。
   （自動バックアップからの復元は有料のことがある。**手元にも落としておく。**）
2. SSH で、`public_html` の中身を一段上の退避フォルダへ移す。
3. 静的サイトを送る。

**`doc.ligula.jp` は別のフォルダなので触らない。**`liguee.net` も別。

## あとで GitHub Pages に戻すとき

`site/CNAME` と `.github/workflows/pages.yml` はそのまま残してある。
DNS を GitHub の4本（185.199.108〜111.153）に向ければ切り替わる。
**そのときは先に MX を直すこと**（社内の台帳 `mail-migration.md` 参照）。
