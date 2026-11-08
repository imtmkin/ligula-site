#!/bin/sh
# ligula.jp（Xserver）へ site/ の中身を送る。
#
#   sh deploy/push-to-xserver.sh            … 何が変わるか見るだけ（送らない）
#   sh deploy/push-to-xserver.sh --go       … 実際に送る
#
# 前提: Xserver のサーバーパネルで SSH を ON にし、公開鍵を登録してあること。
# パスワードはこのファイルにも、このリポジトリにも書かない。鍵は ~/.ssh に置く。

set -eu

HOST="${XS_HOST:-sv12775.xserver.jp}"
PORT="${XS_PORT:-10022}"
USER="${XS_USER:-xs314724}"
DOCROOT="${XS_DOCROOT:-/home/$USER/ligula.jp/public_html}"
KEY="${XS_KEY:-$HOME/.ssh/xserver_ligula}"

HERE=$(cd "$(dirname "$0")/.." && pwd)
SRC="$HERE/site/"

[ -d "$SRC" ] || { echo "site/ が見つからない: $SRC"; exit 1; }
[ -f "$KEY" ] || { echo "鍵が見つからない: $KEY"; exit 1; }

# .htaccess は deploy/htaccess を名前を変えて送る
cp "$HERE/deploy/htaccess" "$SRC/.htaccess"

SSH="ssh -p $PORT -i $KEY"

DRY="--dry-run"
[ "${1:-}" = "--go" ] && DRY=""

# 安全装置: 本当に送るときだけ、送り先にまだ WordPress が残っていないか見る。
# WordPress の index.php が残っていると、そちらが先に表示されてしまう。
if [ -z "$DRY" ] && $SSH "$USER@$HOST" "ls $DOCROOT/wp-config.php" >/dev/null 2>&1; then
  echo "止めました。送り先にまだ WordPress があります: $DOCROOT"
  echo "先にバックアップを取り、WordPress を public_html の外へ移してから、もう一度。"
  echo "（サブドメイン8つのフォルダは消さないこと）"
  exit 1
fi

echo "送り先: $USER@$HOST:$DOCROOT"
[ -n "$DRY" ] && echo "（下見だけ。実際に送るには --go を付ける）"

# --delete は使わない。public_html にサブドメイン8つが同居しているため。
# 送るのは site/ の中身だけ。あちらにしか無いものには一切触らない。
# 公開しなくてよいリポジトリ用のファイルも送らない。
# --chmod は必須。手元のファイルが 600 だと、そのまま送られて Web から読めず 403 になる。
# （2026-11-08 に logo.png がこれで表示されなかった）
rsync -rlptz $DRY --chmod=D755,F644 \
  --exclude '.DS_Store' \
  --exclude '.taste-skill/' \
  --exclude '*.ligula.jp/' \
  --exclude 'CNAME' \
  --exclude '_redirects' \
  --exclude 'README.md' \
  -e "$SSH" \
  "$SRC" "$USER@$HOST:$DOCROOT/"

rm -f "$SRC/.htaccess"
echo "おわり。"
