/* ─────────────────────────────────────────────────────────────
   DATOS DE LA INVITACIÓN
   Este es el único archivo que hace falta tocar para actualizar
   la web. Cambiá el valor, guardá, y hacé `git push`.
   Si algún valor queda en 'COMPLETAR', esa línea (o la sección entera,
   si es un link) no se muestra, en vez de quedar rota.
   ───────────────────────────────────────────────────────────── */

const DATOS = {

  // Fecha y hora de la ceremonia, con la zona horaria de Argentina (-03:00).
  // El offset explícito hace que la cuenta regresiva dé bien también para
  // los invitados que la abran desde otro país.
  fecha: '2026-10-24T17:00:00-03:00',

  iglesia: {
    nombre: 'Iglesia de la Asunción',
    direccion: 'Asunción 685, Resistencia, Chaco',
    maps: 'https://www.google.com/maps/search/?api=1&query=Asunci%C3%B3n%20685%2C%20H3508%20Resistencia%2C%20Chaco',
  },

  festejo: {
    titulo: 'En casa de Meli, Fede y Josefina',
    direccion: 'Felipe Gallardo 1050, Resistencia, Chaco',
    hora: 'A continuación de la ceremonia',
    maps: 'https://www.google.com/maps/search/?api=1&query=-27.420571,-58.934523',
  },

  // Google Form de confirmación de asistencia (link para compartir).
  formulario: 'https://forms.gle/yiZaa56oKGBNnAdd9',

  // Álbum compartido de Google Photos, creado con la opción
  // "Permitir que colaboren" para que los invitados puedan subir fotos.
  // El QR de la página se genera solo a partir de este link.
  album: 'https://photos.app.goo.gl/NZ3LQqaH943cowEo6',
};
