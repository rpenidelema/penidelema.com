// penidelema.com: the line (Rodrigo's signature, continued down the page), entrances, phone menu, the +.
(function () {
  // Rodrigo's logo, traced from his drawing: the small stroke first, then the loop.
  var LOGO = [
    { w: 8.9, d: "M69.4 554.8 C73.0 552.7 83.2 545.9 91.0 541.8 C98.8 537.7 107.7 533.9 116.0 530.5 C124.3 527.0 132.7 524.4 141.0 521.1 C149.3 517.8 157.7 513.7 166.0 510.6 C174.3 507.5 182.7 504.9 191.0 502.6 C199.3 500.2 207.8 498.3 216.0 496.6 C224.2 494.9 231.9 492.8 240.0 492.5 C248.1 492.1 260.7 490.6 264.7 494.6 C268.7 498.7 268.3 509.6 264.2 516.7 C260.0 523.9 248.2 530.6 240.0 537.7 C231.8 544.7 223.1 551.4 215.0 558.9 C206.9 566.5 197.7 575.2 191.3 583.0 C184.9 590.8 179.1 601.9 176.6 605.6" },
    { w: 13.4, d: "M30.5 360.6 C33.0 357.4 39.7 348.1 45.6 341.0 C51.5 333.9 58.9 325.5 65.8 318.0 C72.7 310.5 79.8 302.9 87.0 296.0 C94.2 289.1 101.5 283.1 109.0 276.7 C116.5 270.4 124.3 264.3 132.0 257.9 C139.7 251.6 147.5 245.1 155.0 238.8 C162.5 232.5 169.5 226.2 177.0 220.3 C184.5 214.4 192.3 208.7 200.0 203.4 C207.7 198.0 215.3 193.1 223.0 188.2 C230.7 183.3 238.5 178.5 246.0 174.0 C253.5 169.5 260.5 165.4 268.0 161.1 C275.5 156.7 283.3 152.1 291.0 147.9 C298.7 143.7 306.5 139.6 314.0 135.7 C321.5 131.9 328.5 128.3 336.0 124.7 C343.5 121.1 351.3 117.4 359.0 114.1 C366.7 110.8 374.5 107.5 382.0 104.8 C389.5 102.1 396.5 100.1 404.0 97.9 C411.5 95.7 419.3 93.6 427.0 91.6 C434.7 89.7 442.3 87.9 450.0 86.3 C457.7 84.7 465.5 83.0 473.0 81.9 C480.5 80.9 487.5 80.4 495.0 80.0 C502.5 79.6 510.3 79.4 518.0 79.8 C525.7 80.3 533.5 81.2 541.0 82.8 C548.5 84.4 555.5 85.9 563.0 89.6 C570.5 93.4 579.3 98.8 586.0 105.2 C592.7 111.6 599.0 120.5 603.1 128.0 C607.1 135.5 608.9 142.5 610.6 150.0 C612.2 157.5 612.9 165.3 613.0 173.0 C613.1 180.7 612.3 188.3 611.3 196.0 C610.3 203.7 608.9 211.5 607.2 219.0 C605.4 226.5 603.2 233.5 600.7 241.0 C598.3 248.5 595.5 256.3 592.4 264.0 C589.3 271.7 585.7 279.5 582.1 287.0 C578.5 294.5 574.9 301.5 570.8 309.0 C566.7 316.5 562.2 324.3 557.4 332.0 C552.6 339.7 547.3 347.5 541.8 355.0 C536.4 362.5 531.0 369.5 524.8 377.0 C518.6 384.5 511.8 392.3 504.6 400.0 C497.5 407.7 489.6 415.6 482.0 423.0 C474.4 430.4 466.5 437.7 459.0 444.4 C451.5 451.1 444.5 457.1 437.0 463.3 C429.5 469.5 421.7 475.7 414.0 481.6 C406.3 487.5 398.5 493.3 391.0 498.7 C383.5 504.1 376.5 509.0 369.0 514.0 C361.5 519.0 353.7 524.1 346.0 528.9 C338.3 533.7 330.5 538.5 323.0 542.8 C315.5 547.1 308.5 550.7 301.0 554.7 C293.5 558.8 283.2 562.6 278.0 567.2 C272.8 571.9 267.6 580.8 269.9 582.7 C272.3 584.6 284.7 580.3 292.0 578.7 C299.3 577.2 306.5 574.9 314.0 573.2 C321.5 571.5 329.3 569.9 337.0 568.5 C344.7 567.1 352.5 565.7 360.0 564.9 C367.5 564.2 374.5 563.8 382.0 564.0 C389.5 564.2 397.5 563.8 405.0 566.3 C412.5 568.8 421.6 573.5 427.3 579.1 C432.9 584.6 436.8 596.2 438.7 599.6" }
  ];
  var END = [438.7, 599.6], DIR = [0.48, 0.88];
  var root = document.documentElement;
  var still = window.matchMedia('(prefers-reduced-motion: reduce)').matches;
  var phone = window.matchMedia('(max-width: 760px)');
  var NS = 'http://www.w3.org/2000/svg';
  root.classList.add('js');

  // ---------- The line ----------
  // One thin line, like a fountain pen: the signature, then on down the page to its bottom edge.
  // Laid out once (and again only when the page changes size), drawn as far as the reader has read.
  var svg = document.querySelector('svg.line'), logoBox = document.querySelector('[data-logo]');
  if (svg && logoBox) {
    var hero = logoBox.dataset.logo === 'hero';
    var logoG = document.createElementNS(NS, 'g'), cont = document.createElementNS(NS, 'path');
    svg.appendChild(logoG); svg.appendChild(cont);
    var seen = false;
    try { seen = sessionStorage.getItem('pl-drawn') === '1'; sessionStorage.setItem('pl-drawn', '1'); } catch (e) {}
    var instant = still || (hero && seen);
    // The pen presses a little harder on the long stroke than on the short one.
    var PEN = hero ? [1.1, 1.5] : [0.9, 1.1];
    var strokes = LOGO.map(function (s, i) {
      var p = document.createElementNS(NS, 'path'); p.setAttribute('d', s.d);
      p.setAttribute('stroke-width', PEN[i]); p.setAttribute('vector-effect', 'non-scaling-stroke');
      logoG.appendChild(p);
      var L = p.getTotalLength(); p.__L = L; p.style.strokeDasharray = L; p.style.strokeDashoffset = instant ? 0 : L; return p;
    });

    var page = document.querySelector('.page');
    var box = function (el) { var r = el.getBoundingClientRect(); return { x: r.left + scrollX, y: r.top + scrollY, w: r.width, h: r.height }; };
    var wob = function (i) { return Math.abs(Math.sin(i * 12.9898) * 43758.5453 % 1); };
    var catmull = function (pts) {
      var f = function (v) { return v.toFixed(1); }, d = 'M' + f(pts[0][0]) + ' ' + f(pts[0][1]);
      for (var i = 0; i < pts.length - 1; i++) {
        var p0 = pts[i - 1] || pts[i], p1 = pts[i], p2 = pts[i + 1], p3 = pts[i + 2] || p2;
        d += ' C' + f(p1[0] + (p2[0] - p0[0]) / 6) + ' ' + f(p1[1] + (p2[1] - p0[1]) / 6) + ' ' +
          f(p2[0] - (p3[0] - p1[0]) / 6) + ' ' + f(p2[1] - (p3[1] - p1[1]) / 6) + ' ' + f(p2[0]) + ' ' + f(p2[1]);
      }
      return d;
    };
    // lens[i] is a length along the line; low[i] the lowest point the line reaches before it.
    var lens = [], low = [], total = 0, drawn = 0, shown = 0, ready = instant, running = false, lastW = 0, lastH = 0;

    var layout = function () {
      var W = root.clientWidth, H = page.offsetHeight;
      if (W === lastW && H === lastH && total) return;
      lastW = W; lastH = H;
      svg.setAttribute('width', W); svg.setAttribute('height', H); svg.setAttribute('viewBox', '0 0 ' + W + ' ' + H);
      var b = box(logoBox), s = Math.min(b.w / 654, b.h / 724);
      var ox = b.x + (b.w - 654 * s) / 2, oy = b.y + (b.h - 724 * s) / 2;
      logoG.setAttribute('transform', 'translate(' + ox.toFixed(1) + ' ' + oy.toFixed(1) + ') scale(' + s.toFixed(4) + ')');
      var e = [ox + END[0] * s, oy + END[1] * s], lead = hero ? 46 * s : 60 * s;
      var pts = [e, [e[0] + DIR[0] * lead, e[1] + DIR[1] * lead]];
      var n = 0, small = phone.matches;
      // Beside the words themselves, on their emptier side: close enough to follow, never on top.
      var lane = function (r, el) {
        var a = Infinity, z = -Infinity;
        [].forEach.call(el.children.length ? el.children : [el], function (c) { var q = box(c); if (q.w) { a = Math.min(a, q.x); z = Math.max(z, q.x + q.w); } });
        if (a === Infinity) { a = r.x; z = r.x + r.w; }
        var left = a, right = W - z, side = small ? '' : (el.dataset.side || '');
        if (side === 'left' || (!side && left > right)) return Math.max(a - Math.min(72, left / 2), 14);
        return Math.min(z + Math.min(72, right / 2), W - 14);
      };
      document.querySelectorAll('[data-line], [data-line-phone]').forEach(function (el) {
        var kind = small && el.dataset.linePhone ? el.dataset.linePhone : el.dataset.line;
        if (!kind || kind === 'none' || el.offsetParent === null) return;
        var r = box(el), cx = r.x + r.w / 2;
        if (kind === 'through') {
          // Behind the picture: in at the top, out at the bottom, clear of the caption on the left.
          var pic = el.querySelector('img, canvas'); if (pic) { r = box(pic); cx = r.x + r.w / 2; }
          var ox2 = small ? r.x + r.w * .93 : r.x + r.w * (.7 + .06 * (wob(++n) - .5));
          pts.push([cx + r.w * .06 * (wob(++n) - .5), r.y + r.h * .3], [ox2, r.y + r.h * .74], [ox2, r.y + r.h + (small ? 14 : 56)]);
        } else if (kind === 'avoid') {
          // Down the emptier side of a block of words.
          var lx = lane(r, el);
          pts.push([lx, r.y - 24], [lx + 8 * (wob(++n) - .5), r.y + r.h + 24]);
        }
      });
      // And on to the bottom edge of the page, through the widest gap in the foot nearest the pen.
      var last = pts[pts.length - 1], fx = last[0], foot = document.querySelector('.foot');
      if (foot) {
        var fb = box(foot), spans = [], best = -1;
        [].forEach.call(foot.children, function (c) {
          [].forEach.call(c.children.length ? c.children : [c], function (k) { var q = box(k); spans.push([q.x, q.x + q.w]); });
        });
        spans.sort(function (u, v) { return u[0] - v[0]; });
        var edge = Math.max(fb.x, 0) + 8;
        spans.concat([[W - 8, W]]).forEach(function (sp) {
          var g = sp[0] - edge;
          if (g > 40) { var c = edge + g / 2, score = g - Math.abs(c - last[0]) * .5; if (score > best) { best = score; fx = c; } }
          edge = Math.max(edge, sp[1]);
        });
      }
      if (last[1] < H - 160) pts.push([fx, Math.max(last[1] + 80, H - 160)]);
      pts.push([fx, H]);

      cont.setAttribute('d', catmull(pts));
      cont.setAttribute('stroke-width', small ? .9 : 1);
      cont.setAttribute('vector-effect', 'non-scaling-stroke');
      total = cont.getTotalLength();
      cont.style.strokeDasharray = total + ' ' + total;
      lens = []; low = [];
      var m = -Infinity, step = Math.max(12, total / 1500);
      for (var l = 0; l <= total; l += step) { m = Math.max(m, cont.getPointAtLength(l).y); lens.push(l); low.push(m); }
      lens.push(total); low.push(Infinity);
      if (still) drawn = shown = total;
      drawn = Math.min(drawn, total); shown = Math.min(shown, total);
      cont.style.strokeDashoffset = total - shown;
      wake();
    };

    // How far the pen has got: as far as the reader has read, never back.
    var reach = function () {
      if (scrollY + innerHeight >= root.scrollHeight - 4) { drawn = total; return; }
      var T = scrollY + innerHeight * .82, lo = 0, hi = low.length - 1;
      while (lo < hi) { var mid = (lo + hi + 1) >> 1; if (low[mid] <= T) lo = mid; else hi = mid - 1; }
      drawn = Math.max(drawn, lens[lo] || 0);
    };
    var tick = function () {
      reach(); shown += (drawn - shown) * .2; if (drawn - shown < .5) shown = drawn;
      cont.style.strokeDashoffset = total - shown;
      if (shown < drawn) requestAnimationFrame(tick); else running = false;
    };
    var wake = function () { if (!ready || !lens.length) return; reach(); if (!running && shown < drawn) { running = true; requestAnimationFrame(tick); } };
    window.addEventListener('scroll', wake, { passive: true });

    // The signature writes itself: on the home page once a visit, in the corner in half a second.
    var heroText = document.querySelector('.hero-text');
    var draw = function () {
      if (instant) { if (heroText) heroText.classList.add('on'); wake(); return; }
      var ease = function (t) { return t < .5 ? 4 * t * t * t : 1 - Math.pow(-2 * t + 2, 3) / 2; };
      var k = hero ? .75 : .25, t0 = performance.now();
      (function f(now) {
        var t = (now - t0) / 1000 / k;
        var a = Math.min(Math.max((t - .1) / .6, 0), 1), b = Math.min(Math.max((t - .6) / 1.4, 0), 1);
        strokes[0].style.strokeDashoffset = strokes[0].__L * (1 - ease(a));
        strokes[1].style.strokeDashoffset = strokes[1].__L * (1 - ease(b));
        if (t > 1.2 && heroText) heroText.classList.add('on');
        if (t >= 2) { ready = true; wake(); return; }
        requestAnimationFrame(f);
      })(t0);
    };

    layout(); draw();
    var rt, relayout = function () { clearTimeout(rt); rt = setTimeout(layout, 150); };
    window.addEventListener('resize', relayout);
    window.addEventListener('load', layout);
    if ('ResizeObserver' in window) new ResizeObserver(relayout).observe(page);
  } else {
    var ht = document.querySelector('.hero-text'); if (ht) ht.classList.add('on');
  }

  // ---------- Entrances ----------
  var parts = document.querySelectorAll('[data-in]');
  if ('IntersectionObserver' in window && !still) {
    var io = new IntersectionObserver(function (es) {
      es.forEach(function (e) { if (e.isIntersecting) { e.target.classList.add('is-in'); io.unobserve(e.target); } });
    }, { rootMargin: '0px 0px -8% 0px', threshold: .05 });
    parts.forEach(function (el) { io.observe(el); });
  } else parts.forEach(function (el) { el.classList.add('is-in'); });

  // ---------- Phone menu ----------
  var overlay = document.querySelector('.overlay');
  document.querySelectorAll('[data-menu]').forEach(function (b) {
    b.addEventListener('click', function () {
      var open = b.dataset.menu === 'open';
      overlay.hidden = !open;
      document.querySelectorAll('[data-menu="open"]').forEach(function (o) { o.setAttribute('aria-expanded', open ? 'true' : 'false'); });
      if (open) { var c = overlay.querySelector('[data-menu="close"]'); if (c) c.focus(); }
    });
  });
  document.addEventListener('keydown', function (e) { if (e.key === 'Escape' && overlay && !overlay.hidden) overlay.hidden = true; });

  // ---------- The +: the page's line ends on the paper; each visitor adds one more ----------
  // Lines are not shared between visitors yet; that comes with a database.
  var cv = document.querySelector('.sheet canvas');
  if (cv) {
    var ctx = cv.getContext('2d');
    var seedLine = [[0.3, 0], [0.3, 0.1], [0.285, 0.24], [0.32, 0.38], [0.4, 0.47], [0.5, 0.5], [0.58, 0.47]], mine = [], down = false, done = false;
    var seg = function (p, w, h) {
      if (p.length < 2) return; ctx.beginPath(); ctx.moveTo(p[0][0] * w, p[0][1] * h);
      for (var i = 1; i < p.length - 1; i++) ctx.quadraticCurveTo(p[i][0] * w, p[i][1] * h, (p[i][0] + p[i + 1][0]) / 2 * w, (p[i][1] + p[i + 1][1]) / 2 * h);
      ctx.lineTo(p[p.length - 1][0] * w, p[p.length - 1][1] * h); ctx.stroke();
    };
    var paint = function () {
      var r = cv.getBoundingClientRect(); ctx.clearRect(0, 0, r.width, r.height); ctx.lineCap = 'round'; ctx.lineJoin = 'round';
      ctx.lineWidth = 1; ctx.strokeStyle = '#000'; seg(seedLine, r.width, r.height);
      ctx.lineWidth = 1.4; seg(mine, r.width, r.height);
    };
    var size = function () { var r = cv.getBoundingClientRect(); if (!r.width) return; var d = window.devicePixelRatio || 1; cv.width = r.width * d; cv.height = r.height * d; ctx.setTransform(d, 0, 0, d, 0, 0); paint(); };
    var at = function (e) { var r = cv.getBoundingClientRect(); return [(e.clientX - r.left) / r.width, (e.clientY - r.top) / r.height]; };
    var status = document.querySelector('[data-plus-status]');
    var thanks = function () { if (status) status.textContent = 'Your line is in. Thank you.'; };
    cv.addEventListener('pointerdown', function (e) { if (done) return; down = true; mine = [at(e)]; cv.setPointerCapture(e.pointerId); });
    cv.addEventListener('pointermove', function (e) { if (down) { mine.push(at(e)); paint(); } });
    cv.addEventListener('pointerup', function () { down = false; done = mine.length > 1; if (done) thanks(); });
    cv.addEventListener('keydown', function (e) {
      if (done || (e.key !== 'Enter' && e.key !== ' ')) return;
      e.preventDefault(); var a = seedLine[seedLine.length - 1];
      mine = [a, [a[0] + 0.1, a[1] - 0.08], [a[0] + 0.2, a[1] + 0.06], [a[0] + 0.3, a[1] + 0.02]]; done = true; paint(); thanks();
    });
    window.addEventListener('resize', size); size();
    if (document.fonts) document.fonts.ready.then(size);
  }

  // ---------- Copy the address ----------
  document.querySelectorAll('[data-copy]').forEach(function (btn) {
    btn.addEventListener('click', function () {
      var t = btn.dataset.copy, label = btn.textContent;
      var ok = function () { btn.textContent = 'Copied'; setTimeout(function () { btn.textContent = label; }, 1600); };
      try { navigator.clipboard.writeText(t).then(ok, function () {}); } catch (e) {}
    });
  });
})();
