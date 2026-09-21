/* ─────────────────────────────────────────────────────────────
   DATOS DE LA INVITACIÓN
   Este es el único archivo que hace falta tocar para actualizar
   la web. Cambiá el valor, guardá, y hacé `git push`.
   Lo que diga 'COMPLETAR' se muestra en la página como
   "a confirmar" en vez de romperse.
   ───────────────────────────────────────────────────────────── */

const DATOS = {

  // Fecha y hora de la ceremonia, con la zona horaria de Argentina (-03:00).
  // El offset explícito hace que la cuenta regresiva dé bien también para
  // los invitados que la abran desde otro país.
  fecha: '2026-10-24T17:00:00-03:00',

  iglesia: {
    nombre: 'Iglesia de la Asunción',
    direccion: 'COMPLETAR',          // ej: 'Av. Ejemplo 1234, San Isidro'
    maps: 'COMPLETAR',               // link de Google Maps del lugar
  },

  festejo: {
    titulo: 'En casa de Meli, Fede y Josefina',
    direccion: 'COMPLETAR',          // ej: 'Calle Ejemplo 567, Pilar'
    hora: 'COMPLETAR',               // ej: 'desde las 19 hs'
    maps: 'COMPLETAR',
  },

  // Google Form de confirmación de asistencia (link para compartir).
  formulario: 'COMPLETAR',

  // Álbum compartido de Google Photos, creado con la opción
  // "Permitir que colaboren" para que los invitados puedan subir fotos.
  // El QR de la página se genera solo a partir de este link.
  album: 'COMPLETAR',
};
