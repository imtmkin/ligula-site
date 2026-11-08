# -*- coding: utf-8 -*-
"""お知らせ一覧・これまでの事業・お知らせ記事5本を組む。build.py の HEAD / FOOT を使う。"""
import os, importlib.util

HERE = os.path.dirname(os.path.abspath(__file__))
code = open(os.path.join(HERE, "build.py"), encoding="utf-8").read()
head = code.split("# ---------------------------------------------------------------- 404")[0]
ns = {"__file__": os.path.join(os.path.dirname(os.path.abspath(__file__)), "build.py")}
exec(compile(head, "build.py", "exec"), ns)
HEAD, FOOT, SITE = ns["HEAD"], ns["FOOT"], ns["SITE"]

# 記事の一覧。日付の新しい順。news と各記事の「ほかのお知らせ」で使い回す。
POSTS = [
    ("/yume_liguee_net_pr/", "2026-08-13", "夢を語る会の専用ツールを公開",
     "夢を語り、仲間と出会い、行動する場所。専用プラットフォーム「夢を語る会 by Liguee」を公開しました。", False),
    ("/20_20_se/", "2026-08-13", "Ligula広告 20_20、提供終了",
     "月額300円から看板を掲載できる広告プラットフォームの提供を終了しました。残っていた枠は日割りで返金しています。", True),
    ("/20_20_pr/", "2026-02-03", "Ligula広告 20_20 を公開",
     "月額300円から。売上の30%を広告運用に再投資し、出稿者全員で集客力を育てる広告枠を公開しました。", True),
    ("/ligula_id_pr/", "2025-12-26", "Ligula ID と Ligula Portal を公開",
     "当社のサービスをひとつのアカウントでつなぐ共通IDと、ポータルサイトを公開しました。", True),
    ("/spalie_ma/", "2025-12-16", "Spalie を株式会社WASABI へ譲渡",
     "アパレルブランド「Spalie」を株式会社WASABI へ事業譲渡しました。", True),
]

CORP = '''
      <h2 class="rise">会社概要</h2>
      <dl class="co__table law__table rise" style="margin-top:20px">
        <div class="rise"><dt>社名</dt><dd>株式会社Ligula（リグラ）</dd></div>
        <div class="rise"><dt>代表者</dt><dd>代表取締役　今井 智紀</dd></div>
        <div class="rise"><dt>所在地</dt><dd>神奈川県秦野市</dd></div>
        <div class="rise"><dt>お問い合わせ</dt><dd><a href="mailto:info@ligula.jp">info@ligula.jp</a></dd></div>
      </dl>
'''

def othernews(current):
    rows = "".join(
        '        <a class="rise" href="%s"><b>%s</b><span>%s</span></a>\n' % (u, d, t)
        for u, d, t, _s, _e in POSTS if u != current)
    return '''
  <section class="field lawnav">
    <div class="wrap">
      <h2 class="step rise">ほかのお知らせ</h2>
      <div class="newslist rise">
%s      </div>
      <p class="note" style="margin-top:24px">取材・掲載のご依頼は <a href="mailto:info@ligula.jp">info@ligula.jp</a> へ。
      <a href="/past-projects/">これまでの事業</a>　<a href="/company/">会社概要</a></p>
    </div>
  </section>
''' % rows

def page(path, title, desc, body, out):
    html = HEAD.format(path=path, title=title, desc=desc) + body + FOOT.format(extra="")
    full = os.path.join(SITE, out)
    os.makedirs(os.path.dirname(full), exist_ok=True)
    open(full, "w", encoding="utf-8").write(html)

def release(path, h1, date, lead, notice, blocks, out, title, desc):
    body = '''
  <section class="ph ph--big">
    <div class="wrap grid">
      <h1>%s</h1>
      <p class="ph__sub">株式会社Ligula からのお知らせです。<br><b>%s</b></p>
    </div>
  </section>

  <section class="field">
    <div class="wrap grid">
      <aside class="meta rise">
        <div><dt>日付</dt><dd>%s</dd></div>
        <div><dt>出したところ</dt><dd>株式会社Ligula</dd></div>
        <div><dt>連絡先</dt><dd><a href="mailto:info@ligula.jp">info@ligula.jp</a></dd></div>
        <div><dt>関連</dt><dd><a href="/news/">お知らせ一覧</a><br><a href="/past-projects/">これまでの事業</a></dd></div>
      </aside>
      <div class="doc rise">
''' % (h1, date, date)
    if notice:
        body += '        <p class="notice rise">%s</p>\n' % notice
    body += '        <p class="doc__lead rise">%s</p>\n' % lead
    for h, parts in blocks:
        if h:
            body += '        <h2 class="rise">%s</h2>\n' % h
        for b in parts:
            if isinstance(b, tuple):
                body += '        <ul class="rise">\n' + "".join('          <li>%s</li>\n' % li for li in b) + '        </ul>\n'
            else:
                body += '        <p class="rise">%s</p>\n' % b
    body += CORP + '''      </div>
    </div>
  </section>
''' + othernews(path)
    page(path, title, desc, body, out)

# ---------------------------------------------------------------- 夢を語る会のツール
release("/yume_liguee_net_pr/", "夢を語る会の<br>ツールを公開", "2026年8月13日",
  "予約、内省シートの作成、当日の進行、イベント主催までをひとつで。株式会社Ligula（本社：神奈川県秦野市、代表取締役：今井 智紀）は、夢を言語化し現実にするための専用Webツール「夢を語る会 by Liguee」を公開しました。",
  None,
  [(None, ["本ツールは、イベントの参加予約から「やりたいことシート・アクションシート」の作成と提出、当日の画面共有やタイマーを備えたイベント進行、主催者向けの運営管理までを、ひとつのプラットフォームで行えるものです。"]),
   ("開発の背景", ["「夢を語る会」を開催・運営するなかで、参加者の事前課題（夢の言語化）の共有や、当日の進行とタイマーの管理、次回への案内など、複数のツールをまたぐことが体験を損ねていました。",
                 "そこで「夢を語り、叶えるためだけに特化した場所を作りたい」という想いから、参加者と主催者の双方にとって良い体験になるよう、ひとつにまとめたプラットフォームを作りました。"]),
   ("参加者向けの機能", [("<b>やりたいことメーカー</b>　1年後や将来に叶えたい夢を、カード形式で言語化します。",
                     "<b>アクションシート</b>　夢を現実にするための最初の一歩と、具体的な期日をセットで計画し、提出します。",
                     "<b>夢データの蓄積</b>　過去のシートと参加履歴がマイページに残り、いつでも見返せます。",
                     "<b>Ligula ID 連携</b>　共通IDと連携し、当社のサービスへそのままアクセスできます。")]),
   ("主催者向けの機能", [("<b>画面共有のプレゼンテーションモード</b>　参加者のシートを画面の中央に投影できます。",
                     "<b>プレゼンタイマー</b>　3分 / 5分 / 10分などを、ワンクリックでカウントダウンします。",
                     "<b>管理ダッシュボード</b>　イベントの作成と複製、参加者一覧、課題の提出状況、一括メール配信までを一元管理します。")]),
   ("夢を叶える5つの段", [("やりたいことを言語化する",
                     "夢を語る会に参加し、想いを共有する",
                     "専用コミュニティで仲間を作る",
                     "Liguee のアパレルを着て、日常に落とし込む",
                     "当社と協働する共創プロジェクトへ提案する")]),
   ("代表取締役 今井 智紀のコメント", ['「夢を語るということは、自分の内面と向き合い、未来の可能性を言葉にするプロセスです。今回のツールは、夢を発信する側はもちろん、それを受け止めてイベントを支える主催者の体験も、できるかぎり簡単にすることを目指しました。過去の夢やアクションプランが資産として溜まり、ここから新しい共創プロジェクトや仲間が生まれていく未来を楽しみにしています。」']),
   (None, ['サービスURL：<a href="https://yume.liguee.net/" target="_blank" rel="noopener">https://yume.liguee.net/</a>']),
  ],
  "yume_liguee_net_pr/index.html",
  "夢を語る会の専用ツールを公開 — 株式会社Ligula",
  "夢を言語化し現実にするための専用Webツール「夢を語る会 by Liguee」を公開しました。2026年8月13日。")

# ---------------------------------------------------------------- 20_20 終了
release("/20_20_se/", "Ligula広告 20_20<br>を終了します", "2026年8月13日",
  "株式会社Ligula（本社：神奈川県秦野市、代表取締役：今井 智紀）は、月額300円（税込）から看板を掲載できる広告プラットフォーム「Ligula広告 20_20」の提供を終了することをお知らせいたします。ご愛顧いただいた出稿者ならびに関係者の皆様に、心より感謝申し上げます。",
  None,
  [("終了の背景", ["「おにぎり2個分やコーヒー1杯分の予算で、面白い挑戦をしている人がつながれる場所を作りたい」という想いのもと、売上の最大30%をWeb広告費へ再投資する集客共創型のモデルとして運営してまいりました。",
               "しかしながら、今後の事業方針の見直しとリソースの最適化にともない、サービスの継続が難しいと判断し、提供を終了することといたしました。"]),
   ("出稿中のお客さまへ", [("<b>定期課金の停止</b>　終了に合わせて、すべての自動更新決済を解約処理いたします。お客さまによる個別の解約手続きは不要です。",
                     "<b>契約期間が残っている場合</b>　日割り計算で返金いたします。対象のお客さまには、順次ご登録のメールアドレスへご案内をお送りします。")]),
   ("代表取締役 今井 智紀のコメント", ['「『Ligula広告 20_20』を通じて、アフィリエイターやクリエイター、起業家をはじめとする多くの挑戦者の方々とつながれたことは、私たちにとって大きな財産になりました。400マスという小さな枠から生まれた熱量とコミュニティに、心より感謝申し上げます。プラットフォームとしての形は一度幕を閉じますが、今後も形を変えて挑戦者を応援する取り組みを続けてまいります。」']),
   (None, ['公開時のお知らせは <a href="/20_20_pr/">こちら</a>。本件に関するお問い合わせは <a href="mailto:info@ligula.jp">info@ligula.jp</a> までお願いいたします。']),
  ],
  "20_20_se/index.html",
  "Ligula広告 20_20、提供終了のお知らせ — 株式会社Ligula",
  "月額300円から看板を掲載できる広告プラットフォーム「Ligula広告 20_20」の提供を終了しました。2026年8月13日。")

# ---------------------------------------------------------------- 20_20 公開
release("/20_20_pr/", "Ligula広告 20_20<br>を公開しました", "2026年2月3日",
  "株式会社Ligula（本社：神奈川県秦野市、代表取締役：今井 智紀）は、2026年2月3日、月額300円（税込）から自分の看板を掲載できる広告プラットフォーム「Ligula広告 20_20」を公開しました。",
  'このサービスは 2026年8月13日に提供を終了しました。以下は公開当時の記事です。終了のお知らせは <a href="/20_20_se/">こちら</a>。',
  [("開発の背景", ["個人がWeb上で自分を知ってもらうための広告枠は、多額の予算が必要だったり、運用の専門知識が求められたりするのが一般的です。「もっと気軽に、おにぎり2個分やコーヒー1杯分の予算で、面白い挑戦をしている人がつながれる場所を作りたい」という想いから、このサービスは生まれました。"]),
   ("サービスの特徴", [("<b>低い価格</b>　20×20マスの小さな看板枠を月額300円で提供します。個人のクリエイターや駆け出しの起業家でも、負担なく続けられます。",
                   "<b>集客力の共創</b>　広告売上の最大30%を、このページ自体へのアクセスを増やすためのWeb広告費として再投資します。枠を買う人が増えるほどページ全体の認知が上がり、出稿者全員の露出が増える仕組みです。",
                   "<b>コミュニティ</b>　契約者限定の交流イベントを定期開催します。広告を出して終わりではなく、そこから新しい仕事やコラボレーションが生まれる場を目指します。")]),
   ("代表取締役 今井 智紀のコメント", ['「アフィリエイター、クリエイター、起業家など、何かを企んでいる面白い人たちが集まる場所にしたいと考えています。400マスという物理的な制限があるからこそ、そこに並ぶ看板ひとつひとつに物語が宿るはずです。まずは枠を確保して、一緒にこのプラットフォームを育てていきましょう。」']),
  ],
  "20_20_pr/index.html",
  "Ligula広告 20_20 を公開 — 株式会社Ligula",
  "月額300円から自分の看板を掲載できる広告プラットフォーム「Ligula広告 20_20」を公開しました。2026年2月3日。")

# ---------------------------------------------------------------- Ligula ID
release("/ligula_id_pr/", "Ligula ID を<br>公開しました", "2025年12月26日",
  "株式会社Ligula（本社：神奈川県秦野市、代表取締役：今井 智紀）は、当社が展開するアパレルブランドやWebサービスをひとつのアカウントで使えるようにする共通ID「Ligula ID」と、各サービスへアクセスできる「Ligula Portal」を公開しました。",
  'このサービスは、受託に軸を移したため新しい機能の開発を終えています。いまの事業は <a href="/">トップページ</a> をご覧ください。',
  [("公開の背景", ["私たちは「型を破り、世界を広げる」を掲げて活動しています。これまで独立していた各種WebサービスをひとつのIDでつなぐことで、より快適な体験を届けたいという想いから、開発に至りました。"]),
   ("Ligula ID でできること", [("<b>ひとつのIDで、すべてのサービスへ</b>　当社が提供するWebアプリケーションへのログインが、ひとつのアカウントで行えます。",
                        "<b>サポーター機能</b>　当社の活動や特定のプロジェクト（「夢を語る会」など）を直接応援できます。マイページでサポートの履歴が見られ、バッジが付きます。",
                        "<b>記録とランキング</b>　Ligula ID でログインして各アプリを使うとスコアが記録され、ランキングに参加できます。")]),
   ("今後の展望", ["Ligula ID を土台に、アパレルの購入とWebサービスの利用が連携するポイントプログラムやコミュニティ機能の拡充を予定しています。"]),
  ],
  "ligula_id_pr/index.html",
  "Ligula ID と Ligula Portal を公開 — 株式会社Ligula",
  "当社のサービスをひとつのアカウントでつなぐ共通ID「Ligula ID」とポータルサイトを公開しました。2025年12月26日。")

# ---------------------------------------------------------------- Spalie 譲渡
release("/spalie_ma/", "Spalie を<br>WASABI へ譲渡", "2025年12月16日",
  "株式会社Ligula（本社：神奈川県秦野市、代表取締役：今井 智紀、以下「Ligula社」）は、展開するアパレルブランド「Spalie（スペイリー）」の事業を、移動式ゴミ箱事業「BinGo」を運営する株式会社WASABI（本社：東京都渋谷区、代表取締役：木戸 洵成、以下「WASABI社」）へ譲渡しました。",
  None,
  [(None, ["本件は、環境問題に対する社会の行動変容を促すという共通のミッションを持つ両社が、それぞれの強みを活かし、その実現を早めることを目的としています。"]),
   ("背景", ["Ligula社が展開してきた「Spalie」は、“ゴミを拾う宇宙人”をトレードマークに、「地球と自分の未来を考える」というミッションを掲げてきました。",
           "一方、WASABI社が運営する「BinGo」は、街中のゴミ問題を若者から解決することを軸に、捨てたいときに捨てられる場所を作るため、移動式のゴミ箱を展開してきました。",
           "かねてより両社はコラボレーションを通じて連携してきましたが、Spalie の掲げるミッションを持続的に社会へ浸透させるには、現場での行動を促す BinGo と、意識を変えるメッセージを持つ Spalie の統合が必要だという結論に至りました。",
           "これにより WASABI社は BinGo の活動をアパレルという形で表現し、Ligula社は主力ブランドである Liguee に資源を集中します。"]),
   ("株式会社Ligula 代表取締役 今井 智紀", ["Ligula社は Liguee を中心に新たな世界への一歩目を後押ししてきましたが、その一歩を踏み出す基盤となる地球環境の課題は避けて通れません。Spalie は、その問いに宇宙的な視点から光を当てるブランドとして生まれました。Spalie が掲げる「自分と地球の未来」を本気で実現するには、ゴミ拾いという具体的な行動を全国に広めている WASABI社の実行力が欠かせないと、代表の木戸氏との度重なる意見交換で確信しました。今回は単なるブランドの売却ではなく、共通のミッションを早めるための提携です。"]),
   ("株式会社WASABI 代表取締役 木戸 洵成 氏", ["WASABI社は街中のゴミ問題を若者の力で解決することを軸に、移動式ゴミ箱広告 BinGo を展開してきました。活動のなかで、ゴミ問題の解決だけでなく、インバウンドの方への対応や道ゆく人とのコミュニケーションなど、町全体を活性化させる活動だと確信しています。この活動をより多くの人に広めるために、今井氏率いる Ligula社の Spalie との提携を決断しました。今後は Spalie のデザインを使ったユニフォームでの活動や、全国で支援してくださる方にも Spalie の服を着てもらい、ゴミ拾い活動を行っていきたいと考えています。"]),
   ("株式会社WASABI", ['所在地：東京都渋谷区／代表取締役　木戸 洵成／移動式ゴミ箱事業「BinGo」等の企画・運営／<a href="https://wasabi-jp.biz" target="_blank" rel="noopener">wasabi-jp.biz</a>']),
  ],
  "spalie_ma/index.html",
  "Spalie を株式会社WASABI へ譲渡 — 株式会社Ligula",
  "アパレルブランド「Spalie」を株式会社WASABI へ事業譲渡しました。2025年12月16日。")


# ---------------------------------------------------------------- お知らせ一覧
rows_now = "".join('        <a class="rise" href="%s"><b>%s</b><span>%s<em>%s</em></span></a>\n' % (u, d, t, x)
                   for u, d, t, x, ended in POSTS if not ended)
rows_end = "".join('        <a class="rise" href="%s"><b>%s</b><span>%s<em>%s</em></span></a>\n' % (u, d, t, x)
                   for u, d, t, x, ended in POSTS if ended)
news = '''
  <section class="ph ph--big">
    <div class="wrap grid">
      <h1>お知らせ</h1>
      <p class="ph__sub">サービスの公開や終了、事業譲渡のお知らせです。取材・掲載のご依頼も、下の連絡先へお願いします。</p>
    </div>
  </section>

  <section class="field">
    <div class="wrap">
      <h2 class="step rise">いまのサービス</h2>
      <div class="newslist newslist--full rise">
%s      </div>
      <h2 class="step rise" style="margin-top:clamp(40px,6vh,72px)">提供を終えたサービス</h2>
      <div class="newslist newslist--full rise">
%s      </div>
      <p class="note" style="margin-top:28px">2025年11月より前のお知らせは <a href="/past-projects/">これまでの事業</a> にまとめています。</p>
    </div>
  </section>

  <section class="field lawnav">
    <div class="wrap">
      <h2 class="step rise">関連</h2>
      <div class="lawnav__row rise">
        <a href="/past-projects/">これまでの事業</a>
        <a href="/company/">会社概要</a>
        <a href="/">いまやっている仕事</a>
      </div>
      <p class="note" style="margin-top:20px">取材・掲載のご依頼は <a href="mailto:info@ligula.jp">info@ligula.jp</a> へ。</p>
    </div>
  </section>
''' % (rows_now, rows_end)
page("/news/", "お知らせ — 株式会社Ligula",
     "株式会社Ligula のお知らせ。サービスの公開や終了、事業譲渡のお知らせです。", news, "news/index.html")

# ---------------------------------------------------------------- これまでの事業
def rec(items):
    out = '      <div class="rec rise">\n'
    for term, name, desc, state in items:
        out += ('        <div class="rec__it rise"><b>%s</b><div><h3>%s</h3><p>%s</p>%s</div></div>\n'
                % (term, name, desc, ('<em>%s</em>' % state) if state else ''))
    return out + '      </div>\n'

past = '''
  <section class="ph ph--big">
    <div class="wrap grid">
      <h1>始めた数より、<br>終えた数。</h1>
      <p class="ph__sub">2022年の創業から、いくつもの事業を始めて、いくつも終えてきました。続いているものと、終えたものを並べます。</p>
    </div>
  </section>

  <section class="field">
    <div class="wrap">
      <h2 class="head rise">いま続いているもの</h2>
''' + rec([
  ("2022〜", "事業者向けの月額受託", 'ホームページの制作と保守、SNS運用、ライティング。いまの中心です。中身は <a href="/service/web/">Web運営</a> に書いてあります。', ""),
  ("2026〜", "イベント受付と「たらればボード」", '催しの当日に受付へ人が立ち、来場者の声をその場で集めて会場のモニターに出す仕組みを持ち込みます。<a href="/service/event/">イベント受付</a>／<a href="/service/tarareba-board/">たらればボード</a>', ""),
  ("2022〜", "Liguee（リグイー）", '「一歩踏み出したい人のためのブースター」を掲げたアパレル。糸の鳥がトレードマークです。受注生産で公式ショップを続けています。', ""),
  ("2022〜", "夢を語る会", '月に一度、自分のやりたいことや将来を語り合う集まり。2026年8月に <a href="/yume_liguee_net_pr/">専用ツールを公開</a> しました。', ""),
]) + '''
      <h2 class="head rise" style="margin-top:clamp(48px,7vh,88px)">終えたもの、譲ったもの</h2>
''' + rec([
  ("2026-02〜2026-08", "Ligula広告 20_20", '月額300円から看板を掲載できる広告プラットフォーム。出稿者どうしで集客を育てる仕組みでしたが、事業方針の見直しにともない2026年8月13日に提供を終了しました。契約が残っていた枠は日割りで返金しています。<a href="/20_20_se/">終了のお知らせ</a>', "提供終了"),
  ("〜2025-12", "Spalie（スペイリー）", '「地球と自分の未来を考える」を掲げたアパレルブランド。同じ志を持つ株式会社WASABI のほうが前に進められると判断し、2025年12月16日に事業譲渡しました。<a href="/spalie_ma/">譲渡のお知らせ</a>', "譲渡"),
  ("〜2026", "Ligula ID / Ligula Portal", '各サービスをひとつのアカウントでつなぐ共通IDとポータル。受託に軸を移したため、新しい機能の開発は行っていません。<a href="/ligula_id_pr/">公開時のお知らせ</a>', "開発終了"),
  ("〜更新終了", "シン・LiguRadio / LiguRadio", '高校生起業家3人が、気になるトピックをゲストと話し合うポッドキャスト。のちに代表がひとりで発信する形に変えて続けました。', "更新終了"),
  ("〜終了", "Ligula創研", 'LiguRadio のサイト内で運営していたWebメディア。現場の課題を聞き出すインタビュー記事を発信していました。', "終了"),
]) + '''
      <p class="rise" style="margin-top:clamp(40px,6vh,72px);font-size:var(--s-step);font-weight:900;letter-spacing:-.035em;line-height:1.5;max-width:30ch">始めたことだけでなく、終えた判断もここに残しています。</p>
      <p class="rise" style="margin-top:16px;font-size:var(--s-body);line-height:1.9;max-width:60ch">何をやめたかが分かるほうが、いま何をやっている会社なのかも伝わると考えているからです。</p>
    </div>
  </section>

  <section class="field lawnav">
    <div class="wrap">
      <h2 class="step rise">関連</h2>
      <div class="lawnav__row rise">
        <a href="/">いまやっている仕事</a>
        <a href="/news/">お知らせ</a>
        <a href="/company/">会社概要</a>
      </div>
      <p class="note" style="margin-top:20px">終えた事業についてのお問い合わせは <a href="mailto:info@ligula.jp">info@ligula.jp</a> へ。</p>
    </div>
  </section>
'''
page("/past-projects/", "これまでの事業 — 株式会社Ligula",
     "2022年の創業から始めた事業と、終えた事業・譲った事業を並べています。株式会社Ligula。",
     past, "past-projects/index.html")
print("7ページを書き出しました")
