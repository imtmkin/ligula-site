/* 概算見積り — たらればボード / イベント受付
   単価はすべてここに集めてある。変えるときはこの RATE だけを触る。
   単価は 2026-11-08 に確定（正本は maimai_os/ligula/pricing.md）。片方だけ直すとずれる。 */

var RATE = {
  board: {
    base: 20000,          /* 1日・表示1画面・来場300人まで（モニターは主催者ご用意。貸し出しはしない。2026-11-04 に 30,000 から改定） */
    guests: [             /* 来場者数の段 */
      { upto: 300,  add: 0,      label: '来場300人まで' },
      { upto: 1000, add: 20000,  label: '来場1,000人まで' },
      { upto: 3000, add: 50000,  label: '来場3,000人まで' },
      { upto: 1e9,  add: 100000, label: '来場3,001人以上' }
    ],
    day: 15000,           /* 2日目以降 1日あたり */
    monitor: 8000,        /* 表示を増やす設定 2画面目以降 1画面あたり（機材は主催者ご用意） */
    onsite: 25000,        /* 当日の設置と運用 1日あたり */
    copy: 15000,          /* 文言と選択肢の作成 */
    report: 20000,        /* 事後レポート */
    exhibitor: 15000      /* 出展者に渡す結果ページ */
  },
  event: {
    design: 40000,        /* 受付の流れの設計 */
    staff: 20000,         /* 1人1日・8時間まで */
    over: 2500,           /* 8時間を超えた分 1人1時間あたり */
    photo: 25000,         /* 写真の記録 1日あたり */
    report: 20000,        /* 事後レポート */
    board: 20000,         /* たらればボードを付ける。ボードの基本料と同額にそろえる */
    gear: 15000           /* 受付机まわりの手配 1日あたり。画面(サイネージ)は含まない。2026-11-08 に「サイネージ」を外した */
  }
};

var yen = function (n) { return n.toLocaleString('ja-JP') + '円'; };

/* 入力を読む。足りない値は既定値に寄せる */
function readForm(form) {
  var v = {};
  Array.prototype.forEach.call(form.querySelectorAll('input'), function (el) {
    if (el.type === 'checkbox') { v[el.name] = el.checked; }
    else {
      var n = parseInt(el.value, 10);
      if (isNaN(n) || n < 0) { n = parseInt(el.getAttribute('min'), 10) || 0; }
      var max = parseInt(el.getAttribute('max'), 10);
      if (!isNaN(max) && n > max) { n = max; }
      v[el.name] = n;
    }
  });
  return v;
}

/* 明細を組む。戻り値は { rows: [{name, qty, amount}], total, notes: [] } */
var BUILD = {
  board: function (v) {
    var r = RATE.board, rows = [], step = null, i;
    rows.push({ name: '基本料', qty: '1日・表示1画面', amount: r.base });

    for (i = 0; i < r.guests.length; i++) {
      if (v.guests <= r.guests[i].upto) { step = r.guests[i]; break; }
    }
    if (step && step.add > 0) {
      rows.push({ name: '規模の加算', qty: step.label, amount: step.add });
    }
    if (v.days > 1) {
      rows.push({ name: '開催日の追加', qty: (v.days - 1) + '日', amount: r.day * (v.days - 1) });
    }
    if (v.monitors > 1) {
      rows.push({ name: '表示を増やす設定', qty: (v.monitors - 1) + '画面', amount: r.monitor * (v.monitors - 1) });
    }
    if (v.onsite)    { rows.push({ name: '当日の設置と運用', qty: v.days + '日', amount: r.onsite * v.days }); }
    if (v.copy)      { rows.push({ name: '文言と選択肢の作成', qty: '一式', amount: r.copy }); }
    if (v.report)    { rows.push({ name: '事後レポート', qty: '1本', amount: r.report }); }
    if (v.exhibitor) { rows.push({ name: '出展者に渡す結果ページ', qty: '1本', amount: r.exhibitor }); }

    var notes = ['モニターは主催者のご用意が前提です。機材の貸し出しも手配の代行もしていませんが、何をどこで借りればよいかのご相談には、費用をいただかずにお答えします。'];
    if (v.onsite) { notes.push('現地までの交通費は実費で別途いただきます。'); }
    return { rows: rows, notes: notes };
  },

  event: function (v) {
    var r = RATE.event, rows = [], notes = [];
    if (v.design) { rows.push({ name: '受付の流れの設計', qty: '一式', amount: r.design }); }

    rows.push({
      name: '当日のスタッフ',
      qty: v.people + '人 × ' + v.days + '日',
      amount: r.staff * v.people * v.days
    });
    if (v.hours > 8) {
      rows.push({
        name: '8時間を超える分',
        qty: v.people + '人 × ' + v.days + '日 × ' + (v.hours - 8) + '時間',
        amount: r.over * v.people * v.days * (v.hours - 8)
      });
    }
    if (v.photo)  { rows.push({ name: '写真の記録', qty: v.days + '日', amount: r.photo * v.days }); }
    if (v.gear)   { rows.push({ name: '受付机まわりの手配', qty: v.days + '日', amount: r.gear * v.days }); }
    if (v.board)  { rows.push({ name: 'たらればボードを付ける', qty: '一式', amount: r.board }); }
    if (v.report) { rows.push({ name: '事後レポート', qty: '1本', amount: r.report }); }

    notes.push('現地までの交通費は実費で別途いただきます。');
    if (v.guests > 0 && v.people * 200 < v.guests) {
      notes.push('来場' + v.guests.toLocaleString('ja-JP') + '人なら、' +
                 Math.ceil(v.guests / 200) + '人ほどが目安です。人数を増やすと列が短くなります。');
    }
    return { rows: rows, notes: notes };
  }
};

function estimate() {
  var form = document.getElementById('estform');
  if (!form || !BUILD[form.dataset.est]) { return; }

  var kind = form.dataset.est;
  var slip = document.getElementById('estrows');
  var totalEl = document.getElementById('esttotal');
  var noteEl = document.getElementById('estnotes');
  var key = 'ligula-est-' + kind;
  var last = { rows: [], total: 0, notes: [] };

  function draw() {
    var v = readForm(form);
    var out = BUILD[kind](v);
    var total = out.rows.reduce(function (s, row) { return s + row.amount; }, 0);
    var html = '';

    out.rows.forEach(function (row) {
      html += '<div class="slip__row"><span>' + row.name +
              '</span><i>…………………………</i><span>' + yen(row.amount) + '</span></div>' +
              '<div class="slip__qty">' + row.qty + '</div>';
    });
    slip.innerHTML = html;
    totalEl.textContent = yen(total);
    noteEl.innerHTML = out.notes.map(function (n) { return '<p>' + n + '</p>'; }).join('');

    last = { rows: out.rows, total: total, notes: out.notes, v: v };
    try { localStorage.setItem(key, JSON.stringify(v)); } catch (e) { /* 使えない端末では保存しないだけ */ }
  }

  /* 前回の入力を戻す */
  try {
    var saved = JSON.parse(localStorage.getItem(key) || 'null');
    if (saved) {
      Array.prototype.forEach.call(form.querySelectorAll('input'), function (el) {
        if (!(el.name in saved)) { return; }
        if (el.type === 'checkbox') { el.checked = !!saved[el.name]; }
        else { el.value = saved[el.name]; }
      });
    }
  } catch (e) { /* 壊れていたら既定値のまま */ }

  form.addEventListener('input', draw);
  form.addEventListener('change', draw);
  form.addEventListener('submit', function (e) { e.preventDefault(); });
  draw();

  /* 仮発注。メールの本文に明細を書いて開く。送信は本人の操作 */
  var send = document.getElementById('estsend');
  if (!send) { return; }
  send.addEventListener('click', function () {
    var title = kind === 'board' ? 'たらればボード' : 'イベント受付';
    var lines = ['【' + title + '】概算の仮発注', ''];

    lines.push('■ 入力した内容');
    Array.prototype.forEach.call(form.querySelectorAll('input'), function (el) {
      var label = el.closest('label');
      var name = label ? (label.querySelector('b') || label.querySelector('span')).textContent.trim() : el.name;
      if (el.type === 'checkbox') { lines.push('・' + name + '：' + (el.checked ? 'はい' : 'いいえ')); }
      else { lines.push('・' + name + '：' + el.value + (el.dataset.unit || '')); }
    });

    lines.push('', '■ 概算の明細');
    last.rows.forEach(function (row) { lines.push('・' + row.name + '（' + row.qty + '）　' + yen(row.amount)); });
    lines.push('　合計（税別）　' + yen(last.total));

    if (last.notes.length) { lines.push('', '■ 備考'); last.notes.forEach(function (n) { lines.push('・' + n); }); }

    lines.push('', '■ こちらから記入してください',
               '・催しの名称：', '・開催日：', '・会場：', '・ご担当者のお名前：', '・お電話番号：', '', '・ご要望：', '');
    lines.push('※ この金額は画面上の概算です。正式なお見積もりではありません。');

    location.href = 'mailto:info@ligula.jp?subject=' +
      encodeURIComponent('【仮発注】' + title + 'の概算（' + yen(last.total) + '）') +
      '&body=' + encodeURIComponent(lines.join('\n'));
  });
}

document.addEventListener('DOMContentLoaded', estimate);
