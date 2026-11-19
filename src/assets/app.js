// Small, dependency-free enhancements. Every page works fully without JavaScript.
(function () {
  var d = document, de = d.documentElement;
  de.classList.add('js');
  var reduce = window.matchMedia && matchMedia('(prefers-reduced-motion: reduce)').matches;
  if (/[?&]shot\b/.test(location.search)) { reduce = true; d.querySelectorAll('img[loading=lazy]').forEach(function (i) { i.loading = 'eager'; }); d.querySelectorAll('picture source').forEach(function (x) { x.remove(); }); } // screenshot mode

  // mobile menu
  var btn = d.querySelector('.menu-btn'), drawer = d.getElementById('drawer');
  if (btn && drawer) btn.addEventListener('click', function () {
    var open = drawer.classList.toggle('open');
    btn.setAttribute('aria-expanded', open ? 'true' : 'false');
  });

  // hero video: skip it for reduced motion or data saver; the poster image stays
  var v = d.querySelector('.hero-media video');
  if (v) {
    var save = navigator.connection && navigator.connection.saveData;
    if (reduce || save) { v.removeAttribute('autoplay'); v.pause(); v.preload = 'none'; }
    else { var p = v.play && v.play(); if (p && p.catch) p.catch(function () {}); }
  }

  // reveal on scroll
  var rv = d.querySelectorAll('.rv');
  if ('IntersectionObserver' in window && !reduce) {
    var io = new IntersectionObserver(function (es) {
      es.forEach(function (e) { if (e.isIntersecting) { e.target.classList.add('in'); io.unobserve(e.target); } });
    }, { rootMargin: '0px 0px -8% 0px' });
    rv.forEach(function (el) { io.observe(el); });
  } else rv.forEach(function (el) { el.classList.add('in'); });

  // count-up numbers
  var counters = d.querySelectorAll('[data-count]');
  var run = function (el) {
    var to = parseFloat(el.dataset.count), dec = (el.dataset.count.split('.')[1] || '').length, t0 = null;
    if (reduce) { el.textContent = el.dataset.count; return; }
    var step = function (t) {
      if (!t0) t0 = t; var k = Math.min(1, (t - t0) / 1400), e = 1 - Math.pow(1 - k, 3);
      el.textContent = (to * e).toFixed(dec); if (k < 1) requestAnimationFrame(step);
    }; requestAnimationFrame(step);
  };
  if ('IntersectionObserver' in window) {
    var co = new IntersectionObserver(function (es) {
      es.forEach(function (e) { if (e.isIntersecting) { run(e.target); co.unobserve(e.target); } });
    }); counters.forEach(function (c) { co.observe(c); });
  }

  // premium calculator with sliders. NC law caps the premium at 15% of the bond amount.
  var money = function (n) { return '$' + Math.round(n).toLocaleString('en-US'); };
  var STEPS = [];
  (function () {
    var a; for (a = 250; a < 1000; a += 250) STEPS.push(a);
    for (a = 1000; a < 10000; a += 500) STEPS.push(a);
    for (a = 10000; a < 50000; a += 2500) STEPS.push(a);
    for (a = 50000; a <= 250000; a += 10000) STEPS.push(a);
  })();
  var nearest = function (x) { var best = 0; STEPS.forEach(function (s, i) { if (Math.abs(s - x) < Math.abs(STEPS[best] - x)) best = i; }); return best; };
  d.querySelectorAll('[data-calc]').forEach(function (c) {
    var amt = c.querySelector('.r-amount'), cnt = c.querySelector('.r-count');
    var oAmt = c.querySelector('.o-amount'), oCnt = c.querySelector('.o-count');
    var oPrem = c.querySelector('.o-premium'), oCash = c.querySelector('.o-cash'), oKeep = c.querySelector('.o-keep');
    var bCash = c.querySelector('.bar-cash'), bPrem = c.querySelector('.bar-prem');
    var chips = c.querySelectorAll('.chips button');
    amt.max = STEPS.length - 1; amt.value = nearest(parseFloat(amt.dataset.start || 5000));
    var paint = function (r) { r.style.setProperty('--p', (100 * (r.value - r.min) / (r.max - r.min)) + '%'); };
    var upd = function () {
      var a = STEPS[+amt.value], n = cnt ? +cnt.value : 1, cash = a * n, prem = cash * 0.15;
      oAmt.textContent = money(a); if (oCnt) oCnt.textContent = n + (n === 1 ? ' bond' : ' bonds');
      oPrem.textContent = money(prem); oCash.textContent = money(cash); if (oKeep) oKeep.textContent = money(cash - prem);
      amt.setAttribute('aria-valuetext', money(a));
      if (bCash) { bCash.style.width = '100%'; bPrem.style.width = '15%'; }
      chips.forEach(function (b) { b.setAttribute('aria-pressed', +b.dataset.v === a ? 'true' : 'false'); });
      paint(amt); if (cnt) paint(cnt);
    };
    amt.addEventListener('input', upd); if (cnt) cnt.addEventListener('input', upd);
    chips.forEach(function (b) { b.addEventListener('click', function () { amt.value = nearest(+b.dataset.v); upd(); }); });
    upd();
  });

  // bond request form: opens the visitor's own email or text app. Nothing is sent to or stored on a server.
  var form = d.getElementById('bond-form');
  if (form) {
    var body = function () {
      var f = form.elements, L = form.dataset.lang === 'es';
      return [(L ? 'Solicitud de fianza' : 'Bail bond request'),
        (L ? 'Mi nombre: ' : 'My name: ') + f.yourname.value,
        (L ? 'Mi teléfono: ' : 'My phone: ') + f.phone.value,
        (L ? 'Persona detenida: ' : 'Person in custody: ') + f.defendant.value,
        (L ? 'Cárcel / condado: ' : 'Jail / county: ') + f.county.value,
        (L ? 'Monto de la fianza: ' : 'Bond amount (if known): ') + f.amount.value,
        (L ? 'Notas: ' : 'Notes: ') + f.notes.value].join('\n');
    };
    form.addEventListener('submit', function (e) {
      e.preventDefault();
      location.href = 'mailto:' + form.dataset.email + '?subject=' + encodeURIComponent('Bail bond request') + '&body=' + encodeURIComponent(body());
    });
    var sms = d.getElementById('bond-sms');
    if (sms) sms.addEventListener('click', function (e) { e.preventDefault(); location.href = 'sms:' + form.dataset.sms + '?&body=' + encodeURIComponent(body()); });
  }
})();
