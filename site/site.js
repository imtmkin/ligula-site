/* 株式会社Ligula — 動き。ライブラリなし。 */
(function () {
  'use strict';
  var reduce = window.matchMedia('(prefers-reduced-motion: reduce)').matches;

  /* ---- 各部の立ち上がり ---- */
  function reveal() {
    var items = document.querySelectorAll('.rise');
    if (reduce || !('IntersectionObserver' in window)) {
      items.forEach(function (el) { el.classList.add('in'); });
      return;
    }
    var io = new IntersectionObserver(function (es) {
      es.forEach(function (e) {
        if (!e.isIntersecting) return;
        var p = e.target.parentElement;
        var sibs = p ? Array.prototype.filter.call(p.children, function (c) { return c.classList.contains('rise'); }) : [];
        var i = Math.max(0, sibs.indexOf(e.target));
        setTimeout(function () { e.target.classList.add('in'); }, Math.min(i, 6) * 70);
        io.unobserve(e.target);
      });
    }, { rootMargin: '0px 0px -8% 0px', threshold: 0.1 });

    /* 最初の画面にあるものは監視を待たずに出す。空の画面を見せないため */
    var shown = 0;
    items.forEach(function (el) {
      if (el.getBoundingClientRect().top < window.innerHeight * 0.92) {
        var d = Math.min(shown++, 6) * 70;
        setTimeout(function () { el.classList.add('in'); }, d);
      } else {
        io.observe(el);
      }
    });
  }

  /* ---- 最初の画面の格子。
         なぞると型がたわみ、クリックすると割れる。
         ひびが走り、割れた板が飛び、開いた穴がゆっくり閉じる ---- */
  function lattice() {
    var cv = document.getElementById('lattice');
    var hero = document.querySelector('.hero');
    if (!cv || !hero) return;
    var ctx = cv.getContext('2d');
    var dpr = Math.min(2, window.devicePixelRatio || 1);
    var W = 0, H = 0, cols = 0, rows = 0, step = 0, nodes = [];
    var px = -9999, py = -9999, live = true, raf = 0;
    var breaks = [], plates = [], shake = 0;
    var SHOUT = '型破り！';
    /* 連打で全部割れる。10回まで。2.5秒さわらないと1回ぶん戻る */
    var hits = 0, lastHit = 0, HITS = 10;
    var collapsed = false, fallAt = 0, knit = 1, knitAt = 0;
    var LIFE = 1400, MAXBREAK = 4, MAXPLATE = 72;

    function build() {
      W = hero.clientWidth; H = hero.clientHeight;
      cv.width = W * dpr; cv.height = H * dpr;
      cv.style.width = W + 'px'; cv.style.height = H + 'px';
      ctx.setTransform(dpr, 0, 0, dpr, 0, 0);
      step = W < 700 ? 40 : 56;
      cols = Math.ceil(W / step) + 1;
      rows = Math.ceil(H / step) + 1;
      nodes = [];
      for (var j = 0; j < rows; j++) {
        for (var i = 0; i < cols; i++) nodes.push({ x: i * step, y: j * step, ox: 0, oy: 0, vx: 0, vy: 0 });
      }
    }
    function at(i, j) { return nodes[j * cols + i]; }
    function easeOut(t) { return 1 - Math.pow(1 - t, 3); }

    /* 筆で「型破り！」と出る。出る場所は毎回ちがう */
    function shout() {
      var host = document.getElementById('smash');
      if (!host || reduce) return;
      host.textContent = '';
      var at = document.createElement('div');
      at.className = 'smash__at';
      at.style.left = (W * (0.28 + Math.random() * 0.44)) + 'px';
      at.style.top = (H * (0.24 + Math.random() * 0.52)) + 'px';
      var w = document.createElement('div');
      w.className = 'smash__w';
      w.style.transform = 'rotate(' + (Math.random() * 9 - 4.5).toFixed(1) + 'deg)';
      for (var i = 0; i < SHOUT.length; i++) {
        var c = document.createElement('i');
        c.textContent = SHOUT.charAt(i);
        c.style.animationDelay = (i * 85) + 'ms';
        w.appendChild(c);
      }
      at.appendChild(w);
      host.appendChild(at);
      setTimeout(function () { if (at.parentNode) at.parentNode.removeChild(at); }, 1900);
    }

    /* 型が割れる */
    function breakAt(x, y) {
      if (reduce) return;
      var R = Math.max(190, Math.min(W, H) * 0.34);
      var k, n, dx, dy, d, f, i, s;

      /* 節を外へ突き飛ばす */
      for (k = 0; k < nodes.length; k++) {
        n = nodes[k];
        dx = n.x + n.ox - x; dy = n.y + n.oy - y;
        d = Math.sqrt(dx * dx + dy * dy);
        if (d > R || d < 0.01) continue;
        f = 1 - d / R;
        n.vx += (dx / d) * f * f * 44;
        n.vy += (dy / d) * f * f * 44;
      }

      /* ひび。折れながら外へ伸びる */
      var count = 6 + Math.floor(Math.random() * 3);
      var rays = [], base = Math.random() * Math.PI * 2;
      for (i = 0; i < count; i++) {
        var a = base + (i / count) * Math.PI * 2 + (Math.random() - 0.5) * 0.45;
        var len = R * (0.6 + Math.random() * 0.7);
        var pts = [{ x: x, y: y }], cur = a;
        for (s = 1; s <= 4; s++) {
          cur += (Math.random() - 0.5) * 0.45;
          var dd = len * (s / 4);
          pts.push({ x: x + Math.cos(cur) * dd, y: y + Math.sin(cur) * dd });
        }
        rays.push(pts);
      }
      breaks.push({ x: x, y: y, R: R, born: performance.now(), rays: rays });
      if (breaks.length > MAXBREAK) breaks.shift();

      /* 割れた板。ひびとひびのあいだの殻が、外へ飛ぶ。中心は空ける */
      for (i = 0; i < count; i++) {
        var r1 = rays[i], r2 = rays[(i + 1) % count];
        var lo = 1 + Math.floor(Math.random() * 2);      /* 1 か 2 から */
        var hi = lo + 1 + Math.floor(Math.random() * 2); /* その外側まで */
        if (hi > 4) hi = 4;
        var poly = [
          { x: r1[lo].x - x, y: r1[lo].y - y },
          { x: r1[hi].x - x, y: r1[hi].y - y },
          { x: r2[hi].x - x, y: r2[hi].y - y },
          { x: r2[lo].x - x, y: r2[lo].y - y }
        ];
        var cx = (poly[0].x + poly[1].x + poly[2].x + poly[3].x) / 4;
        var cy = (poly[0].y + poly[1].y + poly[2].y + poly[3].y) / 4;
        var m = Math.sqrt(cx * cx + cy * cy) || 1;
        var sp = 2.8 + Math.random() * 4.2;
        plates.push({
          x: x, y: y, p: poly,
          vx: (cx / m) * sp, vy: (cy / m) * sp,
          rot: 0, vrot: (Math.random() - 0.5) * 0.09, life: 1
        });
      }
      if (plates.length > MAXPLATE) plates.splice(0, plates.length - MAXPLATE);

      shake = 1;
      shout();

      hits++; lastHit = performance.now();
      if (hits >= HITS) collapseAll();
    }

    /* 全部割れる。金の閃光とともに格子が落ちる */
    function collapseAll() {
      if (collapsed) return;
      collapsed = true;
      fallAt = performance.now();
      breaks = []; plates = []; shake = 1;
      var cx = W / 2, cy = H / 2, k, n, dx, dy, d;
      for (k = 0; k < nodes.length; k++) {
        n = nodes[k];
        dx = n.x + n.ox - cx; dy = n.y + n.oy - cy;
        d = Math.sqrt(dx * dx + dy * dy) || 1;
        n.vx = (dx / d) * (6 + Math.random() * 10);
        n.vy = (dy / d) * (4 + Math.random() * 8) - (2 + Math.random() * 4);
      }
      hero.classList.add('hero--broke');
      setTimeout(showBroke, 820);
    }

    function showBroke() {
      var el = document.getElementById('broke');
      if (!el) return;
      el.hidden = false;
      requestAnimationFrame(function () { el.classList.add('in'); });
      var btn = document.getElementById('brokeclose');
      if (btn) btn.focus();
    }

    function closeBroke() {
      var el = document.getElementById('broke');
      if (el) { el.classList.remove('in'); setTimeout(function () { el.hidden = true; }, 500); }
      hero.classList.remove('hero--broke');
      collapsed = false; hits = 0;
      build();
      knit = 0; knitAt = performance.now();
    }

    /* 穴の半径。開いて、少し保って、閉じる */
    function holeR(b, now) {
      var e = (now - b.born) / LIFE;
      if (e >= 1) return -1;
      if (e < 0.2) return b.R * 0.74 * easeOut(e / 0.2);
      if (e < 0.46) return b.R * 0.74;
      var c = (e - 0.46) / 0.54;
      return b.R * 0.74 * (1 - c * c);
    }

    function covered(mx, my, holes) {
      for (var t = 0; t < holes.length; t++) {
        var dx = mx - holes[t].x, dy = my - holes[t].y, r = holes[t].r;
        if (dx * dx + dy * dy < r * r) return true;
      }
      return false;
    }

    function draw() {
      var now = performance.now();
      ctx.setTransform(dpr, 0, 0, dpr, 0, 0);
      ctx.clearRect(0, 0, W, H);

      /* 割れた瞬間、画面がわずかに震える */
      if (shake > 0.01) {
        ctx.translate((Math.random() - 0.5) * shake * 6, (Math.random() - 0.5) * shake * 6);
        shake *= 0.84;
      } else { shake = 0; }

      var i, j, n, a, b, k, s, dx, dy;

      /* さわらずにいると、割った回数が戻る */
      if (!collapsed && hits > 0 && now - lastHit > 2500) { hits--; lastHit = now; }
      /* 閉じたあと、格子が編み直される */
      if (knit < 1) { knit = Math.min(1, (now - knitAt) / 1600); }
      var fade = collapsed ? Math.max(0, 1 - (now - fallAt) / 900) : 1;

      if (collapsed) {
        for (k = 0; k < nodes.length; k++) {
          n = nodes[k];
          n.vy += 0.34; n.vx *= 0.995; n.vy *= 0.995;
          n.ox += n.vx; n.oy += n.vy;
        }
      } else if (!reduce) {
        for (k = 0; k < nodes.length; k++) {
          n = nodes[k];
          dx = n.x + n.ox - px; dy = n.y + n.oy - py;
          var d2 = dx * dx + dy * dy, r = 170;
          if (d2 < r * r && d2 > 0.01) {
            var d = Math.sqrt(d2), f = (1 - d / r) * 26;
            n.vx += (dx / d) * f * 0.12;
            n.vy += (dy / d) * f * 0.12;
          }
          var sp = Math.max(0.022, 0.06 - hits * 0.004);
          n.vx += -n.ox * sp; n.vy += -n.oy * sp;
          n.vx *= 0.86; n.vy *= 0.86;
          n.ox += n.vx; n.oy += n.vy;
        }
      }

      /* 生きている穴 */
      var holes = [];
      for (k = breaks.length - 1; k >= 0; k--) {
        var hr = holeR(breaks[k], now);
        if (hr < 0) { breaks.splice(k, 1); continue; }
        holes.push({ x: breaks[k].x, y: breaks[k].y, r: hr });
      }

      /* 格子。穴の中は描かない */
      ctx.lineWidth = 1;
      for (j = 0; j < rows; j++) {
        for (i = 0; i < cols; i++) {
          a = at(i, j);
          var alpha = (0.24 + Math.min(0.6, (Math.abs(a.ox) + Math.abs(a.oy)) / 46)) * knit * fade;
          ctx.strokeStyle = collapsed
            ? 'rgba(217,180,91,' + Math.min(1, alpha * 2.2) + ')'
            : 'rgba(96,111,140,' + alpha + ')';
          if (i < cols - 1) {
            b = at(i + 1, j);
            if (!holes.length || !covered((a.x + a.ox + b.x + b.ox) / 2, (a.y + a.oy + b.y + b.oy) / 2, holes)) {
              ctx.beginPath(); ctx.moveTo(a.x + a.ox, a.y + a.oy); ctx.lineTo(b.x + b.ox, b.y + b.oy); ctx.stroke();
            }
          }
          if (j < rows - 1) {
            b = at(i, j + 1);
            if (!holes.length || !covered((a.x + a.ox + b.x + b.ox) / 2, (a.y + a.oy + b.y + b.oy) / 2, holes)) {
              ctx.beginPath(); ctx.moveTo(a.x + a.ox, a.y + a.oy); ctx.lineTo(b.x + b.ox, b.y + b.oy); ctx.stroke();
            }
          }
        }
      }

      /* 割れた板 */
      for (k = plates.length - 1; k >= 0; k--) {
        var pl = plates[k];
        pl.life -= 0.019;
        if (pl.life <= 0) { plates.splice(k, 1); continue; }
        pl.x += pl.vx; pl.y += pl.vy;
        pl.vx *= 0.972; pl.vy = pl.vy * 0.972 + 0.06;
        pl.rot += pl.vrot;
        ctx.save();
        ctx.translate(pl.x, pl.y); ctx.rotate(pl.rot);
        ctx.beginPath();
        ctx.moveTo(pl.p[0].x, pl.p[0].y);
        for (i = 1; i < pl.p.length; i++) ctx.lineTo(pl.p[i].x, pl.p[i].y);
        ctx.closePath();
        ctx.fillStyle = 'rgba(96,111,140,' + (pl.life * 0.14) + ')';
        ctx.fill();
        ctx.strokeStyle = 'rgba(23,26,32,' + (pl.life * 0.6) + ')';
        ctx.lineWidth = 1.3;
        ctx.stroke();
        ctx.restore();
      }

      /* ひび。太い線で、折れながら伸びる */
      for (k = 0; k < breaks.length; k++) {
        var bk = breaks[k], e = (now - bk.born) / LIFE;
        var grow = Math.min(1, e / 0.16);
        var fade = e < 0.4 ? 1 : Math.max(0, 1 - (e - 0.4) / 0.6);
        if (fade <= 0) continue;
        ctx.strokeStyle = 'rgba(23,26,32,' + (0.8 * fade) + ')';
        ctx.lineWidth = 2.2;
        ctx.lineCap = 'round';
        for (i = 0; i < bk.rays.length; i++) {
          var ray = bk.rays[i], segs = ray.length - 1, t = grow * segs;
          ctx.beginPath();
          ctx.moveTo(ray[0].x, ray[0].y);
          for (s = 1; s <= segs; s++) {
            if (t >= s) { ctx.lineTo(ray[s].x, ray[s].y); }
            else if (t > s - 1) {
              var u = t - (s - 1);
              ctx.lineTo(ray[s - 1].x + (ray[s].x - ray[s - 1].x) * u,
                         ray[s - 1].y + (ray[s].y - ray[s - 1].y) * u);
              break;
            } else { break; }
          }
          ctx.stroke();
        }
        ctx.lineWidth = 1; ctx.lineCap = 'butt';

        /* 当たった瞬間の閃光 */
        if (e < 0.12) {
          var fp = e / 0.12;
          ctx.fillStyle = 'rgba(96,111,140,' + (0.4 * (1 - fp)) + ')';
          ctx.beginPath(); ctx.arc(bk.x, bk.y, bk.R * 0.34 * easeOut(fp), 0, Math.PI * 2); ctx.fill();
        }
      }

      /* 崩れた瞬間の、金の閃光 */
      if (collapsed) {
        var fe = (now - fallAt) / 520;
        if (fe < 1) {
          var g = ctx.createRadialGradient(W / 2, H / 2, 0, W / 2, H / 2, Math.max(W, H) * 0.75);
          g.addColorStop(0, 'rgba(240,214,148,' + (0.75 * (1 - fe)) + ')');
          g.addColorStop(0.45, 'rgba(217,180,91,' + (0.38 * (1 - fe)) + ')');
          g.addColorStop(1, 'rgba(217,180,91,0)');
          ctx.fillStyle = g;
          ctx.fillRect(0, 0, W, H);
        }
      }

      if (live && !reduce) raf = requestAnimationFrame(draw);
    }

    build(); draw();
    window.addEventListener('resize', function () { build(); if (reduce) draw(); }, { passive: true });
    hero.addEventListener('pointermove', function (e) {
      var r = hero.getBoundingClientRect();
      px = e.clientX - r.left; py = e.clientY - r.top;
    });
    hero.addEventListener('pointerleave', function () { px = -9999; py = -9999; });
    hero.addEventListener('touchmove', function (e) {
      var r = hero.getBoundingClientRect(), t = e.touches[0];
      px = t.clientX - r.left; py = t.clientY - r.top;
    }, { passive: true });

    /* クリック・タップで割る。ボタンやリンクの上では何もしない */
    hero.addEventListener('pointerdown', function (e) {
      if (collapsed) return;
      if (e.target.closest && e.target.closest('a,button,input,label,.broke')) return;
      var r = hero.getBoundingClientRect();
      px = e.clientX - r.left; py = e.clientY - r.top;
      breakAt(px, py);
    });

    /* キーボードだけで使う人にも。最初の画面でEnterかスペース */
    hero.addEventListener('keydown', function (e) {
      if (e.target !== hero) return;
      if (e.key !== 'Enter' && e.key !== ' ') return;
      e.preventDefault();
      breakAt(W * (0.25 + Math.random() * 0.5), H * (0.3 + Math.random() * 0.4));
    });

    var closeBtn = document.getElementById('brokeclose');
    if (closeBtn) closeBtn.addEventListener('click', closeBroke);
    document.addEventListener('keydown', function (e) {
      if (e.key === 'Escape' && collapsed) closeBroke();
    });

    if ('IntersectionObserver' in window) {
      new IntersectionObserver(function (es) {
        live = es[0].isIntersecting;
        if (live && !reduce) { cancelAnimationFrame(raf); raf = requestAnimationFrame(draw); }
      }, { threshold: 0 }).observe(hero);
    }
  }

  /* ---- 問い合わせ。送信せず、メールソフトを開く ---- */
  function ask() {
    var form = document.getElementById('askform');
    if (!form) return;
    form.addEventListener('submit', function (e) {
      e.preventDefault();
      var line = (document.getElementById('askline').value || '').trim();
      var body = [
        '株式会社Ligula ご担当者さま', '',
        'ご相談：' + line, '',
        '（事業の内容、いまのサイトやSNS、日程などを書いてください）', '',
        'お名前：',
        '会社・屋号：',
        'サイトのURL：'
      ].join('\n');
      window.location.href = 'mailto:info@ligula.jp?subject=' +
        encodeURIComponent(line ? '相談：' + line : '相談') + '&body=' + encodeURIComponent(body);
    });
  }

  /* 筆書体は4文字だけ。最初のクリックで間に合うように先に読んでおく */
  function inkFont() {
    if (!document.fonts || !document.fonts.load) return;
    try { document.fonts.load("1em 'Yuji Boku'", '型を破り、世界広げる。選択と集中！リグれ'); } catch (e) { /* 使えなければ代替書体で出る */ }
  }

  reveal(); lattice(); ask(); inkFont();
})();
