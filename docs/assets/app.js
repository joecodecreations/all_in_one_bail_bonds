// Small, dependency-free enhancements. The site works fully without JavaScript.
(function () {
  var btn = document.querySelector('.menu-btn'), drawer = document.getElementById('drawer');
  if (btn && drawer) {
    btn.addEventListener('click', function () {
      var open = drawer.classList.toggle('open');
      btn.setAttribute('aria-expanded', open ? 'true' : 'false');
    });
  }

  // Premium calculator: NC law caps the premium at 15% of the bond amount.
  var amt = document.getElementById('bond-amount'), out = document.getElementById('bond-max');
  if (amt && out) {
    var fmt = function (n) { return '$' + n.toLocaleString('en-US', { minimumFractionDigits: 0, maximumFractionDigits: 2 }); };
    var upd = function () {
      var v = parseFloat(String(amt.value).replace(/[^0-9.]/g, ''));
      out.textContent = v > 0 ? fmt(Math.round(v * 15) / 100) : '$0';
    };
    amt.addEventListener('input', upd); upd();
  }

  // Bond request form: builds an email (or a text message) in the visitor's own app.
  // Nothing is sent to or stored on a server.
  var form = document.getElementById('bond-form');
  if (form) {
    var body = function () {
      var f = form.elements, L = form.dataset.lang === 'es';
      return [
        (L ? 'Solicitud de fianza' : 'Bail bond request'),
        (L ? 'Mi nombre: ' : 'My name: ') + f.yourname.value,
        (L ? 'Mi teléfono: ' : 'My phone: ') + f.phone.value,
        (L ? 'Persona detenida: ' : 'Person in custody: ') + f.defendant.value,
        (L ? 'Cárcel / condado: ' : 'Jail / county: ') + f.county.value,
        (L ? 'Monto de la fianza: ' : 'Bond amount (if known): ') + f.amount.value,
        (L ? 'Notas: ' : 'Notes: ') + f.notes.value
      ].join('\n');
    };
    form.addEventListener('submit', function (e) {
      e.preventDefault();
      window.location.href = 'mailto:' + form.dataset.email + '?subject=' +
        encodeURIComponent('Bail bond request') + '&body=' + encodeURIComponent(body());
    });
    var sms = document.getElementById('bond-sms');
    if (sms) sms.addEventListener('click', function (e) {
      e.preventDefault();
      window.location.href = 'sms:' + form.dataset.sms + '?&body=' + encodeURIComponent(body());
    });
  }
})();
