// penidelema.com: entrances, phone menu, the + drawing, the welcome.
(function () {
  var root = document.documentElement;

  // Entrances: once, when a part of a section comes into view.
  // A shutter is clipped shut, so its parent is watched instead.
  var parts = document.querySelectorAll('[data-reveal], .shutter');
  if ('IntersectionObserver' in window && parts.length) {
    root.classList.add('js');
    var io = new IntersectionObserver(function (entries) {
      entries.forEach(function (e) {
        if (!e.isIntersecting) return;
        var t = e.target.__part || e.target;
        t.classList.add('is-in'); io.unobserve(e.target);
      });
    }, { rootMargin: '0px 0px -8% 0px', threshold: 0.05 });
    parts.forEach(function (el) {
      if (el.classList.contains('shutter')) { var w = el.parentElement; w.__part = el; io.observe(w); }
      else io.observe(el);
    });
  }

  // Phone menu
  var overlay = document.querySelector('.overlay');
  document.querySelectorAll('[data-menu]').forEach(function (b) {
    b.addEventListener('click', function () {
      var open = b.dataset.menu === 'open';
      overlay.hidden = !open;
      document.querySelectorAll('[data-menu="open"]').forEach(function (o) { o.setAttribute('aria-expanded', open ? 'true' : 'false'); });
    });
  });
  document.addEventListener('keydown', function (e) { if (e.key === 'Escape' && overlay && !overlay.hidden) overlay.hidden = true; });

  // The +: one line per visit. Lines are not shared yet; that comes with a database.
  var cv = document.querySelector('.plus-frame canvas');
  if (cv) {
    var fr = cv.parentElement, ctx = cv.getContext('2d');
    var seed = [[0.22, 0.70], [0.27, 0.52], [0.36, 0.41], [0.47, 0.37], [0.55, 0.39]], mine = [], drawing = false, done = false;
    var seg = function (p, w, h) { if (p.length < 2) return; ctx.beginPath(); ctx.moveTo(p[0][0] * w, p[0][1] * h); for (var i = 1; i < p.length; i++) ctx.lineTo(p[i][0] * w, p[i][1] * h); ctx.stroke(); };
    var draw = function () { var r = fr.getBoundingClientRect(); ctx.clearRect(0, 0, r.width, r.height); ctx.lineCap = 'round'; ctx.lineJoin = 'round'; ctx.lineWidth = 2.5; ctx.strokeStyle = '#111214'; seg(seed, r.width, r.height); ctx.strokeStyle = '#1c2a66'; seg(mine, r.width, r.height); };
    var size = function () { var r = fr.getBoundingClientRect(); if (!r.width) return; var d = window.devicePixelRatio || 1; cv.width = r.width * d; cv.height = r.height * d; ctx.setTransform(d, 0, 0, d, 0, 0); draw(); };
    var pt = function (e) { var r = cv.getBoundingClientRect(); return [(e.clientX - r.left) / r.width, (e.clientY - r.top) / r.height]; };
    var status = document.querySelector('[data-plus-status]');
    cv.addEventListener('pointerdown', function (e) { if (done) return; drawing = true; mine = [pt(e)]; cv.setPointerCapture(e.pointerId); });
    cv.addEventListener('pointermove', function (e) { if (drawing) { mine.push(pt(e)); draw(); } });
    cv.addEventListener('pointerup', function () { drawing = false; done = mine.length > 1; if (done && status) status.textContent = 'Your line is in. Thank you.'; });
    // Keyboard: Enter adds a line from the last one's end.
    cv.addEventListener('keydown', function (e) {
      if (done || (e.key !== 'Enter' && e.key !== ' ')) return;
      e.preventDefault();
      var a = seed[seed.length - 1]; mine = [a, [a[0] + 0.12, a[1] + 0.08], [a[0] + 0.22, a[1] + 0.22]]; done = true; draw();
      if (status) status.textContent = 'Your line is in. Thank you.';
    });
    window.addEventListener('resize', size);
    size();
  }

  // Welcome: two strokes, a breath, then the logo opens like a window. Once per visit.
  var wel = document.querySelector('.welcome');
  if (wel) {
    var seen = false;
    try { seen = sessionStorage.getItem('pl-welcome') === '1'; sessionStorage.setItem('pl-welcome', '1'); } catch (e) {}
    if (seen || window.matchMedia('(prefers-reduced-motion: reduce)').matches) { wel.remove(); return; }
    wel.hidden = false;
    var s1 = wel.querySelector('#s1'), s2 = wel.querySelector('#s2'), winG = wel.querySelector('#win-g'),
        photo = wel.querySelector('#photo'), ink = wel.querySelector('#ink-g'), fill = wel.querySelector('#mfill');
    var L1 = s1.getTotalLength(), L2 = s2.getTotalLength(), raf;
    var ease = function (t) { return t < .5 ? 4 * t * t * t : 1 - Math.pow(-2 * t + 2, 3) / 2; };
    var frame = function (t) {
      var a = Math.min(Math.max(t / 0.55, 0), 1), b = Math.min(Math.max((t - 0.55) / 0.5, 0), 1);
      s1.style.strokeDasharray = L1; s1.style.strokeDashoffset = L1 * (1 - ease(a));
      s2.style.strokeDasharray = L2; s2.style.strokeDashoffset = L2 * (1 - ease(b));
      var o = Math.min(Math.max((t - 1.45) / 1.5, 0), 1);
      photo.setAttribute('opacity', o > 0 ? 1 : 0);
      winG.setAttribute('transform', 'translate(800 450) scale(' + (1 + Math.pow(ease(o), 2.2) * 60) + ')');
      fill.setAttribute('opacity', Math.max(0, (o - 0.55) / 0.45));
      ink.setAttribute('opacity', o > 0 ? Math.max(0, 1 - o * 4) : 1);
      wel.style.opacity = t > 3.0 ? Math.max(0, 1 - (t - 3.0) / 0.5) : 1;
    };
    var end = function () { cancelAnimationFrame(raf); wel.remove(); };
    wel.addEventListener('click', end);
    var t0 = performance.now();
    (function tick(now) { var t = (now - t0) / 1000; frame(t); if (t < 3.5) raf = requestAnimationFrame(tick); else end(); })(t0);
  }
})();
