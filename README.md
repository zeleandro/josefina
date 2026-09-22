# Invitación al bautismo de Josefina

Sitio de una sola página para el bautismo de Josefina — sábado **24 de octubre de 2026, 17 hs**,
Iglesia de la Asunción. Publicado en GitHub Pages:

**https://zeleandro.github.io/josefina/**

Tiene cuenta regresiva en vivo, botones para agendar el evento, mapas, galería de fotos, álbum
compartido con QR y confirmación de asistencia.

---

## Lo que hay que completar

Todo lo que cambia está en **`js/datos.js`**. Editás el valor, guardás, y hacés push.
Lo que diga `COMPLETAR` simplemente no se muestra en la página, así que no queda nada roto
mientras tanto.

| Dato | Qué es |
|---|---|
| `iglesia.direccion` | Calle y localidad de la iglesia |
| `iglesia.maps` | Link de Google Maps de la iglesia |
| `festejo.direccion` | Dirección de la casa |
| `festejo.hora` | Por ejemplo, `'desde las 19:30 hs'` |
| `festejo.maps` | Link de Google Maps de la casa |
| `formulario` | Link para compartir del Google Form de confirmación |
| `album` | Link del álbum compartido de Google Photos (el QR se genera solo) |

Para ver cómo va a quedar la página con esos datos ya cargados, abrila con `?demo` al final:
`https://zeleandro.github.io/josefina/?demo`. Muestra valores de ejemplo, sin tocar nada.

### El álbum de Google Photos

Al crearlo hay que activar **"Permitir que colaboren"**, si no los invitados pueden mirar pero no
subir. El QR de la página se arma automáticamente con ese link: no hay que generarlo aparte.

### Si cambiás la dirección de la iglesia

`bautismo-josefina.ics` (el archivo que se bajan los de iPhone y Outlook) tiene la dirección
escrita adentro, en la línea `LOCATION:`. Es el único lugar que no se actualiza solo desde
`datos.js` — conviene corregirlo a mano de paso. La fecha y la hora sí están bien y no hay que
tocarlas.

---

## Publicar un cambio

```bash
git add -A
git commit -m "lo que cambiaste"
git push
```

Un minuto después ya está online. Si no ves el cambio, refrescá con Cmd+Shift+R.

## Verlo local antes de publicar

```bash
python3 -m http.server 8777
```

Y abrís http://localhost:8777

---

## Cómo está armado

Sin frameworks, sin build, sin dependencias que se instalen. Son archivos que el navegador abre
tal cual, así que esto va a seguir funcionando igual dentro de un año sin que nadie lo mantenga.

```
index.html              la página entera
css/estilos.css         paleta y tipografías, sacadas de la tarjeta
js/datos.js             👈 lo único que hace falta tocar
js/invitacion.js        cuenta regresiva, mapas, QR, galería, música
js/qrcode.js            generador de QR (librería MIT, incluida para no depender de internet)
bautismo-josefina.ics   el evento para Apple Calendar y Outlook
assets/                 ilustración y flores recortadas de la tarjeta, fotos optimizadas
assets/audio/           la música de fondo
originales/             las fotos y la tarjeta como las mandaron, sin tocar
herramientas/           scripts para regenerar assets/ si cambia una foto
```

### La música

Suena *Träumerei*, el séptimo movimiento de **Escenas de infancia** de Robert Schumann, al piano
por **Donald Betts**. La grabación es de [Musopen](https://musopen.org) y está en **dominio
público** (Creative Commons Public Domain Mark 1.0), vía
[Wikimedia Commons](https://commons.wikimedia.org/wiki/File:Robert_Schumann_-_scenes_from_childhood,_op._15_-_vii._dreaming.ogg).
Musopen pide atribución aunque no sea obligatoria, así que acá está.

Para cambiar el tema, reemplazá los archivos de `assets/audio/` y actualizá los `<source>` de
`index.html`. Tené en cuenta que el repositorio es público: no subas música con derechos.

**Nunca arranca sola.** Los navegadores bloquean el audio automático desde hace años, así que un
autoplay ni siquiera sonaría — solo quedaría roto. Hay un botón flotante abajo a la derecha, y con
`preload="none"` el archivo no se descarga hasta que alguien lo toca.

### Si hay que cambiar una foto

Poné la nueva en `originales/`, agregá o cambiá su nombre en la lista `GALERIA` de
`herramientas/preparar-assets.py`, y corré:

```bash
python3 herramientas/preparar-assets.py
```

Recorta, redimensiona y optimiza todo de nuevo. No necesita instalar nada: usa `sips`, que ya
viene con macOS.

Si una foto muy vertical queda recortada con la cara afuera, en `index.html` esa `<figure>` lleva
un `style="--enfoque: 6%"` que sube el recorte. 50% es el centro, 0% el borde de arriba.

La imagen de preview que se ve al pegar el link en WhatsApp (`assets/og.jpg`) se arma abriendo
`herramientas/og.html` en el navegador con la ventana en 1200×630 y sacando una captura, o con
`./herramientas/captura.sh 1200 630 og.png http://localhost:8777/herramientas/og.html`.

Para comprobar que el QR apunta de verdad al álbum (y no solo que "parece un QR"), está
`herramientas/leerqr.swift`, que lo decodifica con el framework Vision de macOS.

### Una advertencia sobre la paleta

El crema del fondo (`--crema` en `css/estilos.css`, hoy `#F6E9DD`) tiene que coincidir exactamente
con la constante `PAPEL` de `herramientas/preparar-assets.py`. La ilustración trae sus bordes fundidos a
ese color para que se apoye sobre el papel sin que se note el recorte: si cambiás uno y no el
otro, aparece un rectángulo alrededor de la nena.
