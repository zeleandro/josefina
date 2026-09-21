/* ══════════════════════════════════════════════════════════════
   Invitación al bautismo de Josefina
   Todo lo que cambia en la página sale de js/datos.js
   ══════════════════════════════════════════════════════════════ */
(function () {
  'use strict';

  var PENDIENTE = 'COMPLETAR';

  /* Modo demo: agregando ?demo a la URL se ven las secciones que todavía
     no tienen datos reales, con valores de ejemplo. Sirve para previsualizar
     cómo va a quedar la página cuando lleguen las direcciones y los links. */
  if (/[?&]demo\b/.test(location.search)) {
    DATOS.iglesia.direccion = 'Av. del Libertador 1234, Vicente López';
    DATOS.iglesia.maps = 'https://www.google.com/maps/search/?api=1&query=Iglesia+de+la+Asuncion';
    DATOS.festejo.direccion = 'Los Aromos 456, Pilar';
    DATOS.festejo.hora = 'desde las 19:30 hs';
    DATOS.festejo.maps = 'https://www.google.com/maps/search/?api=1&query=Pilar';
    DATOS.formulario = 'https://forms.gle/ejemplo';
    DATOS.album = 'https://photos.app.goo.gl/ejemplo';
  }
  var INICIO = new Date(DATOS.fecha);
  var DURACION_HS = 6;                                  // ceremonia + festejo
  var FIN = new Date(INICIO.getTime() + DURACION_HS * 3600e3);

  function valor(ruta) {
    return ruta.split('.').reduce(function (o, k) {
      return (o == null) ? undefined : o[k];
    }, DATOS);
  }
  function falta(v) { return !v || v === PENDIENTE; }

  /* Lo que todavía no tiene dato no se muestra: es preferible una página
     completa con menos renglones que una llena de "a confirmar". */

  /* ── Datos de texto ─────────────────────────────────────── */
  document.querySelectorAll('[data-dato]').forEach(function (el) {
    var v = valor(el.dataset.dato);
    if (falta(v)) el.hidden = true;
    else el.textContent = v;
  });

  /* ── Links (mapas, formulario, álbum) ───────────────────── */
  document.querySelectorAll('[data-link]').forEach(function (el) {
    var v = valor(el.dataset.link);
    if (falta(v)) (el.closest('p') || el).hidden = true;
    else el.href = v;
  });

  /* ── Secciones que dependen de un link ──────────────────── */
  document.querySelectorAll('[data-requiere]').forEach(function (el) {
    if (falta(valor(el.dataset.requiere))) el.hidden = true;
  });

  /* ── Agregar a Google Calendar ──────────────────────────── */
  (function calendario() {
    var btn = document.getElementById('btn-google');
    if (!btn) return;

    function utc(d) {
      return d.toISOString().replace(/[-:]/g, '').replace(/\.\d{3}/, '');
    }
    var lugar = falta(DATOS.iglesia.direccion)
      ? DATOS.iglesia.nombre
      : DATOS.iglesia.nombre + ', ' + DATOS.iglesia.direccion;

    var detalle = 'Bautismo de Josefina.\n'
      + 'Ceremonia en ' + DATOS.iglesia.nombre + ' a las 17 hs.\n'
      + 'Después seguimos festejando ' + DATOS.festejo.titulo.toLowerCase() + '.\n\n'
      + location.href;

    btn.href = 'https://calendar.google.com/calendar/render?action=TEMPLATE'
      + '&text=' + encodeURIComponent('Bautismo de Josefina')
      + '&dates=' + utc(INICIO) + '/' + utc(FIN)
      + '&details=' + encodeURIComponent(detalle)
      + '&location=' + encodeURIComponent(lugar)
      + '&ctz=America/Argentina/Buenos_Aires';
  })();

  /* ── Cuenta regresiva ───────────────────────────────────── */
  (function cuenta() {
    var caja = document.getElementById('cuenta');
    var msg = document.getElementById('cuenta-mensaje');
    if (!caja) return;

    var campos = {
      dias:  document.getElementById('c-dias'),
      horas: document.getElementById('c-horas'),
      min:   document.getElementById('c-min'),
      seg:   document.getElementById('c-seg')
    };

    function mostrarMensaje(texto) {
      caja.hidden = true;
      msg.hidden = false;
      msg.textContent = texto;
    }

    function tick() {
      var resto = INICIO - Date.now();

      if (resto <= 0) {
        if (Date.now() < FIN) {
          mostrarMensaje('¡Hoy es el gran día!');
        } else {
          mostrarMensaje('Gracias por acompañarnos');
        }
        clearInterval(reloj);
        return;
      }

      var s = Math.floor(resto / 1000);
      campos.dias.textContent  = Math.floor(s / 86400);
      campos.horas.textContent = String(Math.floor(s / 3600) % 24).padStart(2, '0');
      campos.min.textContent   = String(Math.floor(s / 60) % 60).padStart(2, '0');
      campos.seg.textContent   = String(s % 60).padStart(2, '0');
    }

    tick();
    var reloj = setInterval(tick, 1000);
  })();

  /* ── QR del álbum compartido ────────────────────────────── */
  (function qr() {
    var caja = document.getElementById('qr');
    if (!caja) return;

    if (falta(DATOS.album) || typeof qrcode !== 'function') {
      caja.classList.add('qr--vacio');
      caja.textContent = 'próximamente';
      return;
    }
    var q = qrcode(0, 'M');
    q.addData(DATOS.album);
    q.make();
    caja.innerHTML = q.createSvgTag({ scalable: true, margin: 0 });
    caja.setAttribute('aria-hidden', 'true');
  })();

  /* ── Aparición al scrollear ─────────────────────────────── */
  (function revelar() {
    var items = document.querySelectorAll('.revelar');
    if (!('IntersectionObserver' in window)) {
      items.forEach(function (el) { el.classList.add('visible'); });
      return;
    }
    var obs = new IntersectionObserver(function (entradas) {
      entradas.forEach(function (e) {
        if (e.isIntersecting) {
          e.target.classList.add('visible');
          obs.unobserve(e.target);
        }
      });
    }, { rootMargin: '0px 0px -12% 0px', threshold: 0.08 });
    items.forEach(function (el) { obs.observe(el); });
  })();

  /* ── Visor de fotos ─────────────────────────────────────── */
  (function visor() {
    var caja = document.getElementById('visor');
    var img = document.getElementById('visor-img');
    if (!caja || !img) return;

    var fotos = Array.prototype.slice.call(document.querySelectorAll('.galeria .foto img'));
    var actual = 0;
    var ultimoFoco = null;

    function abrir(i) {
      actual = (i + fotos.length) % fotos.length;
      img.src = fotos[actual].src;
      img.alt = fotos[actual].alt;
      caja.hidden = false;
      document.body.style.overflow = 'hidden';
      document.getElementById('visor-cerrar').focus();
    }
    function cerrar() {
      caja.hidden = true;
      document.body.style.overflow = '';
      if (ultimoFoco) ultimoFoco.focus();
    }

    fotos.forEach(function (f, i) {
      f.tabIndex = 0;
      f.setAttribute('role', 'button');
      f.addEventListener('click', function () { ultimoFoco = f; abrir(i); });
      f.addEventListener('keydown', function (e) {
        if (e.key === 'Enter' || e.key === ' ') { e.preventDefault(); ultimoFoco = f; abrir(i); }
      });
    });

    document.getElementById('visor-cerrar').addEventListener('click', cerrar);
    document.getElementById('visor-prev').addEventListener('click', function () { abrir(actual - 1); });
    document.getElementById('visor-next').addEventListener('click', function () { abrir(actual + 1); });
    caja.addEventListener('click', function (e) { if (e.target === caja) cerrar(); });

    document.addEventListener('keydown', function (e) {
      if (caja.hidden) return;
      if (e.key === 'Escape') cerrar();
      if (e.key === 'ArrowLeft') abrir(actual - 1);
      if (e.key === 'ArrowRight') abrir(actual + 1);
    });
  })();

})();
