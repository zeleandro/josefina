#!/usr/bin/env python3
"""
Regenera todo lo que hay en assets/ a partir de originales/.

Sirve si cambian una foto, o si retocan la tarjeta y hay que volver a
recortar la ilustración y las flores de las esquinas.

    python3 herramientas/preparar-assets.py

No necesita instalar nada: usa `sips` (viene con macOS) y Python puro.
"""
import os, subprocess, sys

AQUI = os.path.dirname(os.path.abspath(__file__))
RAIZ = os.path.dirname(AQUI)
sys.path.insert(0, AQUI)
import img

ORIG = os.path.join(RAIZ, 'originales')
DEST = os.path.join(RAIZ, 'assets')
FOTOS = os.path.join(DEST, 'fotos')

TARJETA = 'tarjeta-modificada.jpg'

# El crema exacto del papel de la tarjeta. Tiene que coincidir con
# --crema en css/estilos.css, o se va a ver el rectángulo de la ilustración.
PAPEL = (0xF6, 0xE9, 0xDD)

# Las fotos de Josefina, en el mismo orden en que aparecen en la galería.
GALERIA = ['recien-nacida', 'primeros-dias', 'ojitos', 'bebe',
           'felicidad', 'puchero', 'merienda', 'alegria', 'sunset']
# La que encabeza la sección de la ceremonia.
CEREMONIA = 'pequenita'

def sips(*args):
    subprocess.run(['sips'] + list(args), capture_output=True, check=True)

def recorte(origen, destino, y, x, alto, ancho):
    if os.path.exists(destino): os.remove(destino)
    sips('-c', str(alto), str(ancho), '--cropOffset', str(y), str(x), origen, '--out', destino)

def principal():
    os.makedirs(FOTOS, exist_ok=True)
    tarjeta = os.path.join(ORIG, TARJETA)
    tmp = os.path.join(DEST, '_tmp.jpg')

    # ── Ilustración: la escena central (nena, paloma, flores).
    #    Hay que tapar dos cosas que se cuelan en el recorte: el ramo de la
    #    esquina superior izquierda y una voluta del marco arriba a la derecha.
    #    No hay fondo limpio para clonar, así que se rellenan planos y se
    #    difuminan hacia adentro.
    recorte(tarjeta, tmp, 35, 40, 710, 950)
    w, h, px = img.load(tmp)
    # El ramo de la esquina ocupa una L: dos rectangulos, para no rozar
    # el pelo de la nena, que empieza en x~295.
    img.fill_soft(w, h, px, 0, 0, 310, 200, (0xF5, 0xE7, 0xDC), feather=35, edges='rb')
    img.fill_soft(w, h, px, 0, 0, 230, 360, (0xF4, 0xE6, 0xDB), feather=35, edges='rb')
    img.fill_soft(w, h, px, 845, 0, 105, 80, (0xF8, 0xEA, 0xE1), feather=25, edges='lb')
    img.shift_to(w, h, px, img.bg_color(w, h, px, 380, 20, 14), PAPEL)
    img.feather_to_color(w, h, px, PAPEL, 34)
    png = os.path.join(DEST, '_ilus.png')
    img.save_png(png, w, h, px)
    sips('-s', 'format', 'jpeg', '-s', 'formatOptions', '84', png,
         '--out', os.path.join(DEST, 'ilustracion.jpg'))
    os.remove(png)
    print('ilustración')

    # ── Esquina floral: se espeja para la esquina opuesta. Lleva pegada una
    #    vuelta del corazón del marco, que se tapa.
    recorte(tarjeta, tmp, 32, 34, 310, 280)
    w, h, px = img.load(tmp)
    img.fill_soft(w, h, px, 0, 0, 46, 44, (0xF5, 0xE7, 0xDC), feather=18, edges='rb')
    fondo = img.bg_color(w, h, px, w - 30, h - 30)
    img.save_png(os.path.join(DEST, 'esquina.png'), w, h, px,
                 img.alpha_key(w, h, px, fondo))
    print('esquina')

    # ── Guirnalda del pie: laurel y corazón.
    recorte(tarjeta, tmp, 1378, 330, 95, 360)
    w, h, px = img.load(tmp)
    fondo = img.bg_color(w, h, px, w - 30, h - 30)
    img.save_png(os.path.join(DEST, 'guirnalda.png'), w, h, px,
                 img.alpha_key(w, h, px, fondo))
    print('guirnalda')

    # ── Fotos de Josefina
    for nombre in GALERIA + [CEREMONIA]:
        sips('-Z', '1200', '-s', 'format', 'jpeg', '-s', 'formatOptions', '80',
             os.path.join(ORIG, nombre + '.jpg'), '--out', os.path.join(FOTOS, nombre + '.jpg'))
        print('foto', nombre)

    # ── Centro de mesa: es una captura de pantalla, hay que sacarle
    #    los controles negros de arriba y la píldora de abajo.
    recorte(os.path.join(ORIG, 'centro de mesa.jpg'), tmp, 58, 0, 1255, 1320)
    sips('-Z', '1200', '-s', 'format', 'jpeg', '-s', 'formatOptions', '78',
         tmp, '--out', os.path.join(FOTOS, 'mesa.jpg'))
    os.remove(tmp)
    print('foto mesa')
    print('\nListo. La imagen de preview (assets/og.jpg) se arma aparte,')
    print('con herramientas/og.html abierto en el navegador a 1200x630.')

if __name__ == '__main__':
    principal()
