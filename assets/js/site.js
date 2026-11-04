// penidelema.com: room walking, phone menu, the + drawing, the welcome, copy email.
(function () {
  var wide = function () { return window.matchMedia('(min-width: 761px)').matches; };

  // Rooms: a vertical wheel walks sideways; drag with the mouse too.
  var track = document.querySelector('.track');
  if (track) {
    var prog = document.querySelector('.progress i');
    var where = document.querySelector('[data-where]');
    var walls = track.querySelectorAll('.wall');
    track.addEventListener('wheel', function (e) {
      if (!wide()) return;
      if (Math.abs(e.deltaY) > Math.abs(e.deltaX)) { track.scrollLeft += e.deltaY; e.preventDefault(); }
    }, { passive: false });
    var update = function () {
      var max = track.scrollWidth - track.clientWidth;
      if (prog) prog.style.width = (max > 0 ? track.scrollLeft / max * 100 : 0) + '%';
      if (where) {
        var mid = track.scrollLeft + track.clientWidth * 0.45, name = walls[0] ? walls[0].dataset.where : '';
        walls.forEach(function (w) { if (w.offsetLeft <= mid) name = w.dataset.where; });
        where.textContent = name;
      }
    };
    track.addEventListener('scroll', update);
    window.addEventListener('resize', update);
    var down = false, sx = 0, sl = 0;
    track.addEventListener('pointerdown', function (e) {
      if (e.pointerType !== 'mouse' || !wide() || e.target.closest('a, canvas')) return;
      down = true; sx = e.clientX; sl = track.scrollLeft;
    });
    window.addEventListener('pointermove', function (e) { if (down) track.scrollLeft = sl - (e.clientX - sx); });
    window.addEventListener('pointerup', function () { down = false; });
    track.addEventListener('dragstart', function (e) { e.preventDefault(); });
    window.addEventListener('keydown', function (e) {
      if (!wide()) return;
      if (e.key === 'ArrowRight') track.scrollBy({ left: track.clientWidth * 0.6, behavior: 'smooth' });
      if (e.key === 'ArrowLeft') track.scrollBy({ left: -track.clientWidth * 0.6, behavior: 'smooth' });
    });
    update();
  }

  // Phone menu
  var overlay = document.querySelector('.overlay');
  document.querySelectorAll('[data-menu]').forEach(function (b) {
    b.addEventListener('click', function () { overlay.hidden = b.dataset.menu === 'close'; });
  });

  // The +: one line per visit. Lines are not saved yet; that comes with the shared database.
  var cv = document.querySelector('.plus-frame canvas');
  if (cv) {
    var fr = cv.parentElement, ctx = cv.getContext('2d');
    var seed = [[0.30, 0.62], [0.34, 0.48], [0.42, 0.40], [0.52, 0.38]], mine = [], drawing = false, done = false;
    var seg = function (p, w, h) { if (p.length < 2) return; ctx.beginPath(); ctx.moveTo(p[0][0] * w, p[0][1] * h); for (var i = 1; i < p.length; i++) ctx.lineTo(p[i][0] * w, p[i][1] * h); ctx.stroke(); };
    var draw = function () { var r = fr.getBoundingClientRect(); ctx.clearRect(0, 0, r.width, r.height); ctx.lineCap = 'round'; ctx.lineJoin = 'round'; ctx.lineWidth = 2; ctx.strokeStyle = '#111214'; seg(seed, r.width, r.height); ctx.strokeStyle = '#1c2a66'; seg(mine, r.width, r.height); };
    var size = function () { var r = fr.getBoundingClientRect(); if (!r.width) return; var d = window.devicePixelRatio || 1; cv.width = r.width * d; cv.height = r.height * d; ctx.setTransform(d, 0, 0, d, 0, 0); draw(); };
    var pt = function (e) { var r = cv.getBoundingClientRect(); return [(e.clientX - r.left) / r.width, (e.clientY - r.top) / r.height]; };
    cv.addEventListener('pointerdown', function (e) { if (done) return; drawing = true; mine = [pt(e)]; cv.setPointerCapture(e.pointerId); });
    cv.addEventListener('pointermove', function (e) { if (drawing) { mine.push(pt(e)); draw(); } });
    cv.addEventListener('pointerup', function () { drawing = false; done = mine.length > 1; });
    window.addEventListener('resize', size);
    size();
  }

  // Copy email
  var copy = document.querySelector('[data-copy]');
  if (copy) {
    copy.addEventListener('click', function () {
      var el = document.getElementById(copy.dataset.copy);
      var sel = function () { var r = document.createRange(); r.selectNodeContents(el); var s = window.getSelection(); s.removeAllRanges(); s.addRange(r); };
      try { navigator.clipboard.writeText(el.textContent).then(function () { copy.textContent = 'Copied'; setTimeout(function () { copy.textContent = 'Copy email'; }, 1600); }, sel); } catch (e) { sel(); }
    });
  }

  // Welcome: two strokes, a breath, then the logo opens like a window. Once per visit.
  var welcome = function () {
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
  };

  // Preview gate: a curtain while the site is in preparation, not real security.
  var gate = document.querySelector('[data-gate]');
  var root = document.documentElement;
  if (gate && root.classList.contains('locked')) {
    var pw = gate.querySelector('input'), no = gate.querySelector('.gate-no');
    pw.focus();
    gate.addEventListener('submit', function (e) {
      e.preventDefault();
      if (pw.value.trim() === '1111') {
        try { localStorage.setItem('pl-preview', '1'); } catch (err) {}
        root.classList.remove('locked');
        window.dispatchEvent(new Event('resize'));
        welcome();
      } else {
        no.textContent = 'Not quite.'; pw.value = ''; pw.focus();
      }
    });
  } else {
    welcome();
  }
})();
