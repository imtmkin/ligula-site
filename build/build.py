# -*- coding: utf-8 -*-
"""ligula.jp の4ページを組む。ヘッダーとフッターは全ページ同一。"""
import os, io

HERE = os.path.dirname(os.path.abspath(__file__))
SITE = os.path.normpath(os.path.join(HERE, "..", "site"))

HEAD = '''<!doctype html>
<html lang="ja">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>{title}</title>
<meta name="description" content="{desc}">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Zen+Kaku+Gothic+New:wght@400;500;700;900&display=swap" rel="stylesheet">
<link rel="stylesheet" href="/style.css">
<link rel="canonical" href="https://ligula.jp{path}">
<meta property="og:type" content="website">
<meta property="og:site_name" content="株式会社Ligula">
<meta property="og:url" content="https://ligula.jp{path}">
<meta property="og:title" content="{title}">
<meta property="og:description" content="{desc}">
<meta property="og:image" content="https://ligula.jp/assets/ogp.jpg">
<meta property="og:locale" content="ja_JP">
<meta name="twitter:card" content="summary_large_image">
<meta name="theme-color" content="#606F8C">
<link rel="icon" href="/favicon.ico" sizes="any">
<link rel="icon" href="/assets/icon-192.png" type="image/png">
<link rel="apple-touch-icon" href="/assets/apple-touch-icon.png">
</head>
<body>
<a class="skip" href="#main">本文へ</a>

<header class="top">
 <div class="wrap">
  <a class="top__logo" href="/" aria-label="株式会社Ligula ホーム">
    <img src="/assets/logo.png" width="492" height="146" alt="株式会社Ligula">
  </a>
  <nav class="top__nav" aria-label="主要">
    <a href="/#service">事業</a>
    <a href="/#projects">プロジェクト</a>
    <a href="/#think">考え方</a>
    <a href="/#creed">理念</a>
    <a href="/#company">会社</a>
    <a class="btn" href="#say">相談する</a>
  </nav>
 </div>
</header>

<main id="main">
'''

FOOT = '''</main>

<footer class="foot">
 <div class="wrap">
  <div class="foot__row">
    <div class="foot__brand">
      <img src="/assets/logo.png" width="492" height="146" alt="株式会社Ligula">
      <a href="mailto:info@ligula.jp">info@ligula.jp</a>
    </div>
    <div class="foot__cols">
      <nav aria-labelledby="f1">
        <h2 id="f1">事業</h2>
        <a href="/service/web/">Web運営</a>
        <a href="/service/tarareba-board/">たらればボード</a>
        <a href="/service/event/">イベント受付</a>
      </nav>
      <nav aria-labelledby="f2">
        <h2 id="f2">会社</h2>
        <a href="/#company">会社概要</a>
        <a href="/#projects">プロジェクト</a>
        <a href="/news/">お知らせ</a>
        <a href="/past-projects/">これまでの事業</a>
      </nav>
      <nav aria-labelledby="f3">
        <h2 id="f3">規約</h2>
        <a href="/terms-of-service/">利用規約</a>
        <a href="/privacy-policy/">プライバシーポリシー</a>
        <a href="/law-1/">特定商取引法に基づく表記</a>
      </nav>
    </div>
  </div>
  <div class="foot__last">
    <p>画像は<a href="https://commons.wikimedia.org/wiki/File:Sj%C3%B6llingstad_IMG_3301_Jacquard_german_1939_Sachsische_Webstuhlfabrik_(Louis_Sch%C3%B6nherr)_Chemnitz.jpg">ジャカード織機</a>・<a href="https://commons.wikimedia.org/wiki/File:Masson_Mills_WTM_10_Jacquard_Card_Cutter_5890.jpg">カード穿孔機</a>・<a href="https://commons.wikimedia.org/wiki/File:India_-_Sights_%26_Culture_-_Hand-loom_pattern_cards_for_silk_sari_weaving_(2507306023).jpg">紋紙</a>（CC BY / CC BY-SA, via Wikimedia Commons）、<a href="https://www.metmuseum.org/art/collection/search/69235">伊勢型紙</a>（メトロポリタン美術館, CC0）。</p>
    <p>© 株式会社Ligula</p>
  </div>
 </div>
</footer>

<script src="/site.js"></script>
{extra}</body>
</html>
'''

def say(h2, span, placeholder, label):
    return '''
  <section class="say" id="say">
    <div class="say__in">
      <h2>%s<span>%s</span></h2>
      <form class="say__form" id="askform">
        <input id="askline" type="text" placeholder="%s" aria-label="%s">
        <button class="say__go" type="submit" aria-label="メールを書く">→</button>
      </form>
      <p class="say__next">押すと、件名と本文を書いた状態でメールソフトが開きます。送信はご自身の操作で行われます。</p>
      <dl class="say__rows">
        <div><dt>メール</dt><dd><a href="mailto:info@ligula.jp">info@ligula.jp</a></dd></div>
      </dl>
    </div>
  </section>
''' % (h2, span, placeholder, label)


def pic(src, w, h, alt, ratio="band", screen=False, cls=""):
    k = "pic pic--" + ratio + (" pic--screen" if screen else "")
    if cls:
        k = cls + " " + k
    return ('<figure class="%s rise">\n'
            '        <img src="/assets/%s" width="%d" height="%d" loading="lazy" alt="%s">\n'
            '      </figure>' % (k, src, w, h, alt))


# ---------------------------------------------------------------- トップ
top = HEAD.format(
    path="/",
    title="株式会社Ligula",
    desc="株式会社Ligula。Webを経営の視点で管理します。何を出し、何をやめるかを数字から決めます。",
)

top = top.replace('<link rel="stylesheet" href="/style.css">',
                  '<link href="https://fonts.googleapis.com/css2?family=Yuji+Boku&text=%E5%9E%8B%E3%82%92%E7%A0%B4%E3%82%8A%E3%80%81%E4%B8%96%E7%95%8C%E5%BA%83%E3%81%92%E3%82%8B%E3%80%82%E9%81%B8%E6%8A%9E%E3%81%A8%E9%9B%86%E4%B8%AD%EF%BC%81%E3%83%AA%E3%82%B0%E3%82%8C&display=swap" rel="stylesheet">\n' + '<link rel="stylesheet" href="/style.css">')

top += '''
  <section class="hero" id="top" tabindex="0" aria-label="最初の画面。クリックすると背景の型が割れます">
    <canvas class="hero__bg" id="lattice" aria-hidden="true"></canvas>
    <div class="smash" id="smash" aria-hidden="true"></div>

    <div class="broke" id="broke" role="dialog" aria-modal="false" aria-labelledby="broke-h" hidden>
      <div class="broke__in">
        <h2 class="broke__mission" id="broke-h">型を破り、世界を広げる。</h2>
        <p class="broke__lead">効かないものはやめます、と書きました。その証拠です。</p>
        <p class="broke__creed">選択と集中。</p>
        <dl class="broke__list">
          <div>
            <dt>Ligula広告 20_20<em>2026-02 〜 2026-08｜提供終了</em></dt>
            <dd>月額300円から看板を掲載できる広告プラットフォーム。数字が立たず、2026年8月に終了しました。残っていた枠は日割りで返金しています。</dd>
          </div>
          <div>
            <dt>Spalie（スペイリー）<em>〜 2025-12｜譲渡</em></dt>
            <dd>「地球と自分の未来を考える」を掲げたアパレルブランド。株式会社WASABI のほうが前に進められると判断し、事業譲渡しました。</dd>
          </div>
          <div>
            <dt>Ligula ID / Ligula Portal<em>〜 2026｜開発停止</em></dt>
            <dd>各サービスをひとつのアカウントでつなぐ共通IDとポータル。受託に軸を移したため、新しい機能の開発は行っていません。</dd>
          </div>
        </dl>
        <p class="broke__after">始めることより、終えることのほうが難しい。ここが私たちの一番の課題でした。だから、終えた記録のほうを残しています。</p>
        <p class="broke__verb">リグれ。</p>
        <p class="broke__note">リグる＝殻を破ってチャレンジする。社名から生まれた、私たちの動詞です。</p>
        <div class="broke__go">
          <a class="btn btn--gold" href="/#service">事業を見る <i>→</i></a>
          <a class="broke__alt" href="/past-projects/">これまでの事業</a>
          <button class="broke__close" id="brokeclose" type="button">閉じる</button>
        </div>
      </div>
    </div>
    <div class="wrap"><div class="hero__in">
      <img class="hero__mark rise" src="/assets/logo.png" width="492" height="146" alt="" aria-hidden="true">
      <h1 class="rise">Webを、経営の視点で管理します。</h1>
      <p class="hero__sub rise">何を出し、何をやめるかを、数字から決めます。手を動かす作業は仕組みに寄せてあるので、続けても毎月の手間が増えません。</p>
      <div class="hero__go rise">
        <a class="btn" href="#say">相談する <i>→</i></a>
        <a class="plain" href="#service">事業を見る</a>
      </div>
      <p class="hero__hint rise">背景の格子は、なぞるとたわみます。クリックすると割れます。</p>
    </div></div>
  </section>

  <section class="svc field" id="service">
    <div class="wrap grid">
      <div class="svc__head">
        <h2 class="head rise">事業</h2>
        <p class="rise">三つやっています。どれも「作る作業は機械に寄せ、人は決めることと現場だけを持つ」という同じ考え方で組んであります。</p>
      </div>
      <div class="svc__list">
        <a class="svc__row rise" href="/service/web/">
          <span class="pic pic--wide"><img src="/assets/india-sights-culture-hand-loom-pattern-cards.jpg" width="1500" height="1125" loading="lazy" alt="織機にかけられた紋紙"></span>
          <span><b>Web運営<em>月額の受託</em></b>
          <p>ホームページとSNSを、経営の数字から管理します。追う数字をひとつ決め、ひと月の打ち手を組み、効いていなければやめます。</p></span>
        </a>
        <a class="svc__row rise" href="/service/tarareba-board/">
          <span class="pic pic--wide"><img src="/assets/board-monitor.jpg" width="1400" height="787" loading="lazy" alt="会場モニターに流れる来場者の声"></span>
          <span><b>たらればボード<em>自社プロダクト</em></b>
          <p>催しの来場者の「こうだったらいいのに」とファン投票を、QRと会場モニターで集めて、その場で見せます。</p></span>
        </a>
        <a class="svc__row rise" href="/service/event/">
          <span class="pic pic--wide"><img src="/assets/masson-mills-wtm-10-jacquard-card-cutter.jpg" width="1500" height="1125" loading="lazy" alt="紋紙に穴を開けるカード穿孔機"></span>
          <span><b>イベント受付<em>催しの日だけ</em></b>
          <p>受付の流れを設計して、当日は人が現地に入ります。写真の記録と、終わったあとの報告まで。</p></span>
        </a>
      </div>
    </div>
  </section>

  <section class="field" id="think">
    <div class="wrap grid">
      <h2 class="head think__head rise">作る値段は、下がり続ける。</h2>
      <div class="think__body rise">
        <p>文章も、画像も、毎月の更新も、機械が数分で出すようになりました。作る作業そのものに、昔ほどの値段はつきません。</p>
        <p>残るのは、何のために出すかを決めること。そして、機械に渡せない現場に立つことです。私たちはそこだけを人が持ち、ほかは仕組みに渡しています。</p>
      </div>
      <figure class="think__pic pic pic--tall rise">
        <img src="/assets/sjollingstad-img-3301-jacquard-german-1939-sachsische.jpg" width="1000" height="1500" loading="lazy"
             alt="ジャカード織機の頭部に垂れ下がる紋紙の帯">
      </figure>
      <div class="facts">
        <div class="facts__row">
          <div class="rise"><b>3回</b><span>ひと月の判断の回数</span></div>
          <div class="rise"><b>50分</b><span>ひと月に使う時間</span></div>
          <div class="rise"><b>翌月5日</b><span>経営報告が届く日</span></div>
        </div>
      </div>
    </div>
  </section>

  <section class="prj field" id="projects">
    <div class="wrap grid">
      <figure class="prj__band pic pic--band rise">
        <img src="/assets/ise-katagami-2.jpg" width="1400" height="1214" loading="lazy"
             alt="松の文様を彫り抜いた伊勢型紙。社名の「型破り」の由来にあたる職人の型">
      </figure>
      <div class="prj__head">
        <h2 class="head rise">プロジェクト</h2>
        <p class="rise">受託の枠に収まらない取り組みです。自分たちで始めたものと、立ち上げから一緒にやっているもの。ここで形になったことが、次の商品になります。</p>
      </div>
      <div class="prj__list">
        <div class="prj__item rise">
          <h3>ハレバ<em>湘南台｜室内BBQ・イベント会場</em></h3>
          <p>湘南台駅前の約100坪を使う、期間限定開催のイベント会場。Webと発信の立ち上げから一緒にやっています。</p>
          <div class="prj__foot">
            <a href="https://hare-bar.com" target="_blank" rel="noopener">サイト</a>
            <span class="prj__state">開業準備中</span>
          </div>
        </div>
        <div class="prj__item rise">
          <h3>Liguee<em>リグイー｜アパレル</em></h3>
          <p>一歩踏み出したい人のためのブースターとして作った服。「リグる」を体現するために始めたブランドで、在庫を持たない受注生産です。</p>
          <div class="prj__foot">
            <a href="https://liguee.net" target="_blank" rel="noopener">サイト</a>
            <a href="https://shop.liguee.net" target="_blank" rel="noopener">ショップ</a>
          </div>
        </div>
        <div class="prj__item rise">
          <h3>夢を語る会<em>月1回・90分</em></h3>
          <p>やりたいことを人前で話して、聞いてもらう場。2026年に専用のツールを公開しました。自分の会社を持ちたい人が集まっています。</p>
          <div class="prj__foot">
            <a href="https://yume.liguee.net/" target="_blank" rel="noopener">サイト</a>
            <span class="prj__state">継続中</span>
          </div>
        </div>
        <div class="prj__item rise">
          <h3>山口の農地再生<em>2026年から</em></h3>
          <p>山口の農地で学生が育てたニンニクを買い取り、都市側の催しの場で売る取り組み。作る人と売る場所をつなぐと何が起きるかを、数字で確かめています。</p>
          <div class="prj__foot">
            <a href="https://www.instagram.com/hatakeno_megumi/" target="_blank" rel="noopener">Instagram</a>
            <span class="prj__state">検証中</span>
          </div>
        </div>
      </div>
    </div>
  </section>

  <section class="creed field" id="creed">
    <div class="wrap">
      <div class="creed__top">
        <p class="creed__mission rise">型を破り、世界を広げる。</p>
        <p class="creed__lead rise">社名はラテン語で「型破り」。会社の名前が、そのまま目的です。殻を破って挑むことを、私たちは「リグる」と呼んでいます。</p>
      </div>

      <div class="creed__block">
        <h2 class="creed__h rise">理念</h2>
        <p class="creed__sub rise">数えるものを、三つに決めています。</p>
        <div class="creed__three">
          <div class="creed__it rise"><b>実践<i>値</i></b><p>やってみて出た数字だけを、値として数えます。資料の中で完成させません。</p></div>
          <div class="creed__it rise"><b>経験<i>値</i></b><p>一度やったことは残ります。終えた事業も値になります。</p></div>
          <div class="creed__it rise"><b>絶対<i>値</i></b><p>他と比べません。動いた大きさだけを見ます。動かなかったときだけ、値はゼロです。</p></div>
        </div>
      </div>

      <div class="creed__block">
        <h2 class="creed__h rise">行動指針</h2>
        <p class="creed__sub rise">捨てて、残して、一緒に伸びる。この順番で動きます。</p>
        <div class="creed__three">
          <div class="creed__it rise"><b>選択と集中</b><em>捨てる</em><p>効かないものはやめます。やめた記録を残します。</p></div>
          <div class="creed__it rise"><b>仕組み化</b><em>残す</em><p>人がやらなくていいことは、人がやりません。決めることと現場だけを持ちます。</p></div>
          <div class="creed__it rise"><b>共伸<span>きょうしん</span></b><em>伸ばす</em><p>クライアントと共に伸びます。相手が伸びなければ、私たちも伸びない形にします。</p></div>
        </div>
      </div>
    </div>
  </section>

  <section class="co field" id="company">
    <div class="wrap grid">
      <div class="co__head">
        <h2 class="head rise">会社</h2>
        <p class="rise">社名はラテン語で「型破り」。小さな会社の「決める」を引き受けます。いまはWebと、催しの現場から。2026年に数字の立たない事業を自分で終わらせた経験が、そのまま仕事の中身になっています。</p>
      </div>
      <dl class="co__table rise">
        <div><dt>社名</dt><dd>株式会社Ligula（リグラ）</dd></div>
        <div><dt>設立</dt><dd>2022年8月31日</dd></div>
        <div><dt>代表取締役</dt><dd>今井 智紀</dd></div>
        <div><dt>事業内容</dt><dd>Web運営の受託、イベント受付、自社プロダクトの開発・提供</dd></div>
        <div><dt>所在地</dt><dd>〒257-0001　神奈川県秦野市鶴巻北二丁目5番20号</dd></div>
        <div><dt>連絡先</dt><dd><a href="mailto:info@ligula.jp">info@ligula.jp</a></dd></div>
      </dl>
      <figure class="co__band pic pic--band rise">
        <img src="/assets/stencil-with-pattern-of-irises-on-a.jpg" width="1500" height="1480" loading="lazy"
             alt="菖蒲の文様を彫り抜いた伊勢型紙">
      </figure>
    </div>
  </section>
'''

top += say("いま、どの数字で困っていますか。", "一行だけ書いて、送ってください。",
           "例：問い合わせが月1件から増えない", "いま困っている数字")
top += FOOT.format(extra="")

# ---------------------------------------------------------------- Web運営
web = HEAD.format(
    path="/service/web/",
    title="Web運営 — 株式会社Ligula",
    desc="ホームページとSNSの運営を月額で引き受けます。追う数字をひとつ決め、ひと月の打ち手を組み、効いていなければやめます。",
)
web += '''
  <section class="ph">
    <div class="wrap grid">
      <h1>Webを、経営の数字から管理する。</h1>
      <p class="ph__sub">ホームページとSNSの運営を月額で引き受けます。追う数字をひとつ決め、そこから逆算してひと月の打ち手を組み、効いていなければやめます。</p>
    </div>
  </section>

  <section class="field" style="padding-top:0">
    <div class="wrap grid">
      <figure class="rowpic pic pic--band rise">
        <img src="/assets/india-sights-culture-hand-loom-pattern-cards.jpg" width="1500" height="1125" loading="lazy"
             alt="織機にかけられた紋紙。穴の並びが模様の指示になっている">
      </figure>
    </div>
  </section>

  <section class="field">
    <div class="wrap grid">
      <h2 class="step steps__head rise">ひと月の通り道</h2>
      <div class="steps steps--seq">
        <div class="stepline rise"><b>2日</b><p>はじめに、数字を見て、ひと月の打ち手を組み立てます。出すもの、直すもの、やめるものを並べてお持ちします。</p></div>
        <div class="stepline rise"><b>15分</b><p>つぎに、経営者が決めます。出すか、直すか、やめるか。判断の材料は毎回こちらで揃えます。</p></div>
        <div class="stepline rise"><b>ひと月</b><p>あとは、仕組みが動かします。予約投稿も、更新の反映も、表示の点検も、人の手を使いません。</p></div>
        <div class="stepline rise"><b>翌月5日</b><p>おわりに、1枚の経営報告が届きます。何をして、どの数字がどう動いたかだけを書きます。</p></div>
      </div>
    </div>
  </section>

  <section class="field" style="padding-top:0">
    <div class="wrap grid">
      <h2 class="step rise" style="grid-column:1/13;margin-bottom:28px">やること</h2>
      <div class="steps steps--set">
        <div class="stepline rise"><b>数字を読む</b><p>アクセス、問い合わせ、予約、来店。追う数字を最初にひとつ決めて、そこだけを見ます。</p></div>
        <div class="stepline rise"><b>やめる判断</b><p>効いていない施策は止めます。続けること自体を目的にしません。</p></div>
        <div class="stepline rise"><b>保守</b><p>文章と写真の差し替え、表示とリンクの点検、不具合の一次対応、サーバーと証明書の管理。</p></div>
        <div class="stepline rise"><b>SNS</b><p>ひと月ぶんの計画、画像と文章の制作、予約投稿、コメントとメッセージの一次対応。</p></div>
        <div class="stepline rise"><b>ライティング</b><p>聞き取り、構成、執筆、事実と表記の確認、公開までを引き受けます。</p></div>
        <div class="stepline rise"><b>経営報告</b><p>翌月5日に、何をして、どの数字がどう動いたかを1枚にまとめて送ります。</p></div>
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
      <p class="picnote rise" style="margin-top:16px">穴を開けるのは人、読んで数えるのは機械。90年前から、分けどころは変わっていません。写真は当社の仕事ではなく、その分けどころを示すための資料です。</p>
    </div>
  </section>

  <section class="tot field">
    <div class="wrap grid">
      <div class="tot__left">
        <h2 class="step rise">経営者が使う時間</h2>
        <div class="tot__fig rise">
          <b>50分</b>
          <span>決めることだけを残すと、ひと月に使っていただく時間はこれだけになります。催しの日がある月は、現地の時間を別にいただきます。</span>
        </div>
      </div>
      <div class="slip rise">
        <h3>決める</h3>
        <div class="slip__row"><span>ひと月ぶんの計画を見る</span><i>…………………………</i><span>10分</span></div>
        <div class="slip__row"><span>直しを伝える</span><i>…………………………</i><span>10分</span></div>
        <div class="slip__row"><span>公開前の確認</span><i>…………………………</i><span>10分</span></div>
        <h3>読む</h3>
        <div class="slip__row"><span>月次の経営報告</span><i>…………………………</i><span>20分</span></div>
        <div class="slip__sum"><span>合計</span><span>50分</span></div>
      </div>
    </div>
  </section>

  <section class="field" id="price">
    <div class="wrap">
      <h2 class="head rise">料金</h2>
      <p class="lead rise" style="margin-top:16px;max-width:62ch">月額は低くしてあります。そのかわり、WebやSNSから生まれた売上の一部をいただきます。<b>生まれなかった月にいただくのは、月額だけです。</b></p>

      <h3 class="step rise" style="margin-top:clamp(34px,5vh,60px)">毎月の運営</h3>
      <div class="price rise">
        <div class="price__it rise">
          <p class="price__name">保守<span>月1〜2時間</span></p>
          <p class="price__yen">10,000円<i>／月</i></p>
          <p class="price__txt">点検、文章と写真の差し替え（月2件まで）、不具合の一次対応、サーバーと証明書の管理、月次の経営報告。</p>
        </div>
        <div class="price__it rise">
          <p class="price__name">運営<span>月3時間</span></p>
          <p class="price__yen">25,000円<i>／月</i></p>
          <p class="price__txt">保守のすべてに加えて、追う数字の設計、ひと月の打ち手、やめる判断。</p>
        </div>
        <div class="price__it rise">
          <p class="price__name">運営＋制作<span>月6時間</span></p>
          <p class="price__yen">45,000円<i>／月</i></p>
          <p class="price__txt">運営のすべてに加えて、ライティング（月1本）、撮影の手配、ページの追加（月1枚まで）。</p>
        </div>
      </div>

      <h3 class="step rise" style="margin-top:clamp(34px,5vh,60px)">SNS運用（別立て）</h3>
      <p class="note rise" style="margin-top:12px">毎月の運営には入れていません。SNSの運用は、それだけで成り立つ仕事なので、混ぜると中身が薄くなります。1アカウントにつきの金額で、2つ目からは20％引きです。</p>
      <div class="price rise">
        <div class="price__it rise">
          <p class="price__name">ライト<span>月4本／月8時間</span></p>
          <p class="price__yen">50,000円<i>／月</i></p>
          <p class="price__txt">ひと月の計画、画像と文章の制作、予約投稿、コメントとメッセージの一次対応。</p>
        </div>
        <div class="price__it rise">
          <p class="price__name">スタンダード<span>月8本＋ストーリーズ週2／月15時間</span></p>
          <p class="price__yen">100,000円<i>／月</i></p>
          <p class="price__txt">ライトのすべてに加えて、数字のレポートと、月1回の打ち合わせ。</p>
        </div>
        <div class="price__it rise">
          <p class="price__name">フル<span>月12本＋動画2本／月26時間</span></p>
          <p class="price__yen">180,000円<i>／月</i></p>
          <p class="price__txt">スタンダードのすべてに加えて、リールの編集と、月1日の現地撮影。</p>
        </div>
      </div>

      <div class="share rise">
        <h3>月額は低く。<br>増えた分を、分けます。</h3>
        <div class="share__body">
        <p>WebやSNSを経由して生まれた売上、または一緒に立ち上げた新しい収益源の売上に対して、<b>10％</b>をいただきます。仕入れの重いお仕事では、売上ではなく<b>粗利の25％</b>で。<b>上限は設けません。</b>伸びた分はこちらも伸びる、という形にしたいからです。</p>
        <p class="share__fine">何にかけるかは、契約の前に一緒に決めて、紙に書きます。数えられないものにはかけません。歩合は契約全体で一本で、Web運営とSNS運用で二重にはいただきません。</p>
        </div>
      </div>

      <div class="pricefoot">
        <div class="notice rise">
          <b>入らないもの。</b>広告の出稿費、サーバー・ドメイン・有料ツールの利用料、撮影の交通費、催しの日の現地対応。かかった額のまま別途ご請求します（上乗せはしません）。金額はすべて税別です。
        </div>
        <div class="notice rise">
          <b>まずは3か月。</b>打ち手が数字に出るまで3か月かかるので、そこまではお付き合いください。以降は1か月前にお知らせいただければ終われます。段は月単位で上げ下げできます。
        </div>
      </div>
    </div>
  </section>

  <section class="field">
    <div class="wrap grid">
      <h2 class="step faq__head rise">よくある質問</h2>
      <div class="faq__body rise">
        <p><b>制作会社や広告代理店と何が違いますか。</b>作ることと出稿することを目的にしていない点です。先に追う数字をひとつ決め、そこから逆算して毎月の打ち手を組み、効いていなければやめます。私たち自身が、数字の立たない事業を自分で終わらせた会社です。</p>
        <p><b>いまあるホームページでも頼めますか。</b>はい。いまの作りのまま引き取れるか、作り直したほうが早いかを先に見てからお伝えします。</p>
        <p><b>打ち合わせは毎月ありますか。</b>決まった定例は置いていません。ひと月に3回、出すか・直すか・やめるかを決めていただくだけです。</p>
        <p><b>遠方でも頼めますか。</b>打ち合わせも承認もオンラインで回るように組んであります。現地での撮影や受付が必要な場合だけ、回数と範囲を先に決めます。</p>
        <p><b>アカウントの名義はどうなりますか。</b>お客さまの名義で作り、権限をお預かりする形にしています。契約が終わればお預かりを外すだけです。</p>
        <p><b>やめたいときはどうすればいいですか。</b>その旨をお知らせください。アカウントと原稿、画像の一式をお渡しして終わります。</p>
        <p><b>急ぎの更新にも対応しますか。</b>営業日であれば当日中の着手を基本にしています。日付の決まっているものは先に予定へ組み込みます。</p>
        <p><b>料金はいくらですか。</b><a href="#price">上の「料金」</a>に段ごとの月額を出しています。範囲が目安を超えるときは、その月だけ上の段に上げるか、単発でお見積もりします。催しの日の現地対応は別です。</p>
      </div>
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
'''
web += say("いま、どの数字で困っていますか。", "一行だけ書いて、送ってください。",
           "例：問い合わせが月1件から増えない", "ご相談")
web += FOOT.format(extra="")

# ---------------------------------------------------------------- 404
notfound = HEAD.format(
    path="/404.html",
    title="ページが見つかりません — 株式会社Ligula",
    desc="お探しのページは見つかりませんでした。株式会社Ligula。",
) + '''
  <section class="field ph--big">
    <div class="wrap">
      <h1 class="rise">ページが、<br>ありません。</h1>
      <p class="lead rise" style="margin-top:24px;max-width:50ch">住所が変わったか、終えた事業のページかもしれません。
      終えたものの記録は「これまでの事業」に残してあります。</p>
      <div class="hero__go" style="margin-top:32px">
        <a class="btn rise" href="/">最初のページへ <i>→</i></a>
        <a class="plain rise" href="/past-projects/">これまでの事業</a>
      </div>
      <p class="note rise" style="margin-top:28px">お探しのものが見つからないときは <a href="mailto:info@ligula.jp">info@ligula.jp</a> へ。住所をそのまま貼って送ってください。</p>
    </div>
  </section>
''' + FOOT.format(extra="")
open(os.path.join(SITE, "404.html"), "w").write(notfound)

open(os.path.join(SITE, "index.html"), "w").write(top)
open(os.path.join(SITE, "service/web/index.html"), "w").write(web)
print("トップと Web運営 を書き出しました")
