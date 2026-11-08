# -*- coding: utf-8 -*-
"""たらればボードとイベント受付のページ。概算見積りつき。"""
import os

HERE = os.path.dirname(os.path.abspath(__file__))
SITE = os.path.normpath(os.path.join(HERE, "..", "site"))

# build.py と同じ骨格を読み直す（実行はしない）
src = open(os.path.join(HERE, "build.py")).read()
ns = {"__file__": os.path.join(HERE, "build.py")}
exec(src.split("# ---------------------------------------------------------------- トップ")[0], ns)
HEAD, FOOT, say = ns["HEAD"], ns["FOOT"], ns["say"]


def num(name, label, value, unit, lo, hi, step=1):
    return ('        <label><span>%s</span>'
            '<input type="number" name="%s" value="%d" min="%d" max="%d" step="%d" '
            'inputmode="numeric" data-unit="%s"><i>%s</i></label>\n'
            % (label, name, value, lo, hi, step, unit, unit))


def sw(name, title, note, on=False):
    return ('        <label class="sw"><input type="checkbox" name="%s"%s>'
            '<span class="sw__box" aria-hidden="true"></span>'
            '<span class="sw__txt"><b>%s</b><em>%s</em></span></label>\n'
            % (name, " checked" if on else "", title, note))


def estimator(kind, fields, options):
    return '''
  <section class="est field" id="estimate">
    <div class="wrap grid">
      <div class="est__head">
        <h2 class="head rise">概算を出す</h2>
        <p class="rise">数を入れて、要るものを選ぶと、その場で金額が出ます。これは画面上の概算です。正式なお見積もりは、催しの内容を伺ってからお出しします。</p>
      </div>

      <form class="est__form rise" id="estform" data-est="%s">
        <div class="est__num">
%s        </div>
        <div class="est__opts">
%s        </div>
      </form>

      <div class="est__out rise">
        <div class="slip">
          <h3>概算見積書</h3>
          <div id="estrows"><p class="note">数を入れると、ここに明細が出ます。</p></div>
          <div class="slip__sum"><span>合計（税別）</span><span id="esttotal">—</span></div>
        </div>
        <div id="estnotes"></div>
        <div class="est__go">
          <button class="btn" id="estsend" type="button">保存して仮発注する <i>→</i></button>
          <p class="note">入力した内容はこの端末に残ります。押すと、明細を書いた状態でメールソフトが開きます。送信はご自身の操作で行われます。仮発注の時点では費用は発生しません。</p>
        </div>
      </div>
    </div>
  </section>
''' % (kind, fields, options)


# ---------------------------------------------------------------- たらればボード
board_fields = (num("guests", "来場者数の見込み", 300, "人", 0, 100000, 50)
                + num("days", "開催日数", 1, "日", 1, 14)
                + num("monitors", "会場モニターの台数（主催者ご用意）", 1, "台", 1, 10))
board_opts = (sw("onsite", "当日の設置と運用を任せる", "人が現地に入り、設置から撤収までを持ちます")
              + sw("copy", "文言と選択肢を作る", "何を聞くかから一緒に決めます")
              + sw("report", "事後レポート", "集まった声と投票を1枚にまとめます")
              + sw("exhibitor", "出展者に渡す結果ページ", "出展者や協賛先にそのまま渡せる形にします"))

board = HEAD.format(
    path="/service/tarareba-board/",
    title="たらればボード — 株式会社Ligula",
    desc="催しの来場者の声とファン投票を、QRと会場モニターでその場に出す自社プロダクト。概算見積りを画面で出せます。",
)
board += '''
  <section class="ph">
    <div class="wrap grid">
      <h1>来場者の声を、その場で集める。</h1>
      <p class="ph__sub">QRで読んで、スマホから書いて、会場のモニターに出す。催しが終わったら、集まった声と投票をまとめた1枚が残ります。</p>
    </div>
  </section>

  <section class="field" style="padding-top:0">
    <div class="wrap grid">
      <figure class="rowpic pic pic--band pic--screen rise">
        <img src="/assets/board-monitor.jpg" width="1400" height="787" loading="lazy"
             alt="会場モニターの画面。来場者から届いた「たられば」が並んでいる">
      </figure>
      <p class="picnote rise" style="margin-top:16px">会場に置くモニターの画面です。届いた声が次々に流れ、読まれているのが見えるので、見た人がまた書きます。画面の中身はデモ用で、実際の催しでは文言も選択肢も主催者ごとに作ります。</p>
    </div>
  </section>

  <section class="field">
    <div class="wrap grid">
      <h2 class="step steps__head rise">催しの日に起きること</h2>
      <div class="steps steps--seq">
        <div class="stepline rise"><b>置く</b><p>会場にQRコードを置きます。アプリは要りません。来場者はスマホで読むだけです。</p></div>
        <div class="stepline rise"><b>書く</b><p>「こうだったらいいのに」を書いてもらいます。用意した選択肢へのファン投票も同じ画面から。</p></div>
        <div class="stepline rise"><b>出る</b><p>届いた声が会場のモニターに流れます。読まれているのが見えるので、次の人が書きます。</p></div>
        <div class="stepline rise"><b>残る</b><p>終わったあと、集まった声と投票結果をまとめた1枚が残ります。次の企画の材料になります。</p></div>
      </div>
    </div>
  </section>

  <section class="field" style="padding-top:0">
    <div class="wrap grid">
      <div class="rowpair pair">
        <figure class="pic pic--tall pic--screen rise">
          <img src="/assets/board-participant-tarareba.jpg" width="647" height="1400" loading="lazy"
               alt="来場者が書き込むスマホの画面。選択肢と自由記入の欄が並ぶ">
        </figure>
        <figure class="pic pic--tall pic--screen rise">
          <img src="/assets/board-result-top.jpg" width="1186" height="1400" loading="lazy"
               alt="催しのあとに残る結果ページ。集まった声と投票が一覧になっている">
        </figure>
      </div>
      <p class="picnote rise" style="margin-top:16px">左が来場者の手元で、右が催しのあとに残る1枚です。集まった声と投票結果がそのまま一覧になるので、次の企画を決めるときの材料として、出展者や協賛先にも渡せます。</p>
    </div>
  </section>

  <section class="field" style="padding-top:0">
    <div class="wrap grid">
      <h2 class="step rise" style="grid-column:1/13;margin-bottom:28px">使う場面</h2>
      <div class="steps steps--set">
        <div class="stepline rise"><b>来場者の声</b><p>アンケート用紙を配らずに済みます。書いた人も、ほかの人が何を書いたかを見られます。</p></div>
        <div class="stepline rise"><b>ファン投票</b><p>次に出すもの、次にやることを、その場で来場者に選んでもらえます。</p></div>
        <div class="stepline rise"><b>事後の報告</b><p>集まった声と投票結果を、出展者や協賛先に渡せる形でまとめます。</p></div>
        <div class="stepline rise"><b>会場の飾り</b><p>モニターが文字で埋まっていくので、何もしていない壁が減ります。</p></div>
      </div>
    </div>
  </section>
'''
board += '''
  <section class="field" style="padding-top:0">
    <div class="wrap grid">
      <figure class="rowpic pic pic--band pic--screen rise">
        <img src="/assets/board-admin.jpg" width="1200" height="900" loading="lazy"
             alt="主催者が使う管理画面。届いた投稿を一覧で見て、表示する／しないを切り替える">
      </figure>
      <p class="picnote rise" style="margin-top:16px">主催者の手元です。届いた投稿は一覧で見られて、会場に出す・出さないをその場で切り替えられます。荒れたときに止める手段を、主催者側に必ず残してあります。</p>
    </div>
  </section>
'''
board += estimator("board", board_fields, board_opts)
board += say("どんな催しをやっていますか。", "一行だけ書いて、送ってください。",
             "例：11月に地域のマルシェを主催します", "ご相談")
board += FOOT.format(extra='<script src="/estimate.js"></script>\n')

# ---------------------------------------------------------------- イベント受付
event_fields = (num("guests", "来場者数の見込み", 300, "人", 0, 100000, 50)
                + num("days", "開催日数", 1, "日", 1, 14)
                + num("people", "受付に立つ人数", 2, "人", 1, 30)
                + num("hours", "1日の拘束時間", 8, "時間", 1, 16))
event_opts = (sw("design", "受付の流れを設計する", "名簿、導線、必要な人数と道具を先に決めます", True)
              + sw("photo", "写真を記録する", "使ってよい範囲を先に決めてから撮ります")
              + sw("gear", "受付机まわりを手配する", "机・筆記具・案内の紙もの。画面はご用意ください")
              + sw("board", "たらればボードを付ける", "来場者の声をその場で集めます")
              + sw("report", "事後レポート", "来場者数、集まった声、写真を1枚にまとめます"))

event = HEAD.format(
    path="/service/event/",
    title="イベント受付 — 株式会社Ligula",
    desc="催しの受付の流れを設計し、当日は現地に立ちます。写真の記録と事後の報告まで。概算見積りを画面で出せます。",
)
event += '''
  <section class="ph">
    <div class="wrap grid">
      <h1>催しの日だけ、人が入る。</h1>
      <p class="ph__sub">受付の流れを設計して、当日は現地に立ちます。写真の記録と、終わったあとの報告まで引き受けます。</p>
    </div>
  </section>

  <section class="field" style="padding-top:0">
    <div class="wrap grid">
      <figure class="rowpic pic pic--band rise">
        <img src="/assets/wooden-jacquard-loom-mosi-11-5547.jpg" width="1400" height="1050" loading="lazy"
             alt="木製のジャカード織機。紋紙を通して糸を動かす仕組み">
      </figure>
    </div>
  </section>

  <section class="field">
    <div class="wrap grid">
      <h2 class="step steps__head rise">引き受ける範囲</h2>
      <div class="steps steps--seq">
        <div class="stepline rise"><b>前</b><p>受付の流れを設計します。名簿の作り方、当日の導線、必要な人数と道具を決めて先にお渡しします。</p></div>
        <div class="stepline rise"><b>当日</b><p>人が現地に入ります。受付、案内、来場者の声を集める道具の設置と撤収まで。</p></div>
        <div class="stepline rise"><b>記録</b><p>写真を撮ります。あとで使えるように、使ってよい範囲を先に決めてから撮ります。</p></div>
        <div class="stepline rise"><b>後</b><p>来場者数、集まった声、写真をまとめた1枚をお送りします。</p></div>
      </div>
    </div>
  </section>

  <section class="field" style="padding-top:0">
    <div class="wrap grid">
      <div class="rowpair pair">
        <figure class="pic pic--wide rise">
          <img src="/assets/a-woman-with-a-hollerith-pantograph-punch.jpg" width="1400" height="1103" loading="lazy"
               alt="1940年ごろ、カードに穴を開ける機械を操作する人">
        </figure>
        <figure class="pic pic--wide rise">
          <img src="/assets/masson-mills-wtm-10-jacquard-card-cutter.jpg" width="1500" height="1125" loading="lazy"
               alt="紋紙に穴を開けるカード穿孔機。鍵盤と歯車が並ぶ">
        </figure>
      </div>
      <p class="picnote rise" style="margin-top:16px">機械に渡せる作業と、人が立たないと進まない場所。写真は当社の仕事ではなく、その分けどころを示すための資料です。</p>
    </div>
  </section>

  <section class="field" style="padding-top:0">
    <div class="wrap grid">
      <h2 class="step rise" style="grid-column:1/13;margin-bottom:28px">考え方</h2>
      <div class="steps steps--set">
        <div class="stepline rise"><b>現場だけ</b><p>機械に渡せる作業は渡してあります。人が現地に入るのは、渡せない部分があるからです。</p></div>
        <div class="stepline rise"><b>回数で</b><p>毎月の契約ではなく、日程が決まった日だけの受託です。続けても毎月の手間は増えません。</p></div>
        <div class="stepline rise"><b>声を持ち帰る</b><p>受付だけで終わらせず、たらればボードで来場者の声を集めて、次の企画の材料にします。</p></div>
      </div>
    </div>
  </section>
'''
event += estimator("event", event_fields, event_opts)
event += '''
  <section class="field" style="padding-top:0">
    <div class="wrap grid">
      <figure class="rowpic pic pic--band rise">
        <img src="/assets/ise-katagami.jpg" width="1081" height="1400" loading="lazy"
             alt="彫り抜かれた伊勢型紙">
      </figure>
    </div>
  </section>
'''
event += say("催しの日程は決まっていますか。", "一行だけ書いて、送ってください。",
             "例：12月の社内イベントで受付を任せたい", "ご相談")
event += FOOT.format(extra='<script src="/estimate.js"></script>\n')

open(os.path.join(SITE, "service/tarareba-board/index.html"), "w").write(board)
open(os.path.join(SITE, "service/event/index.html"), "w").write(event)
print("たらればボードとイベント受付を書き出しました")
