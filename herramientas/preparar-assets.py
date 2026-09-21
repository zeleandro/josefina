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

# El crema exacto del papel de la tarjeta. Tiene que coincidir con
# --crema en css/estilos.css, o se va a ver el rectángulo de la ilustración.
PAPEL = (0xF6, 0xE7, 0xDA)

def sips(*args):
    subprocess.run(['sips'] + list(args), capture_output=True, check=True)

def recorte(origen, destino, y, x, alto, ancho):
    if os.path.exists(destino): os.remove(destino)
    sips('-c', str(alto), str(ancho), '--cropOffset', str(y), str(x), origen, '--out', destino)

def principal():
    os.makedirs(FOTOS, exist_ok=True)
    tarjeta = os.path.join(ORIG, 'tarjeta.jpg')
    tmp = os.path.join(DEST, '_tmp.jpg')

    # ── Ilustración: la escena central, sin los ramitos de las esquinas
    #    del marco, y con los bordes fundidos al color del papel.
    recorte(tarjeta, tmp, 40, 120, 572, 790)
    w, h, px = img.load(tmp)
    img.clone_soft(w, h, px, 0, 0, 0, 150, 195, 140, feather=45, edges='rb')
    img.clone_soft(w, h, px, 670, 0, 670, 160, 120, 120, feather=45, edges='lb')
    img.shift_to(w, h, px, img.bg_color(w, h, px, 380, 8, 14), PAPEL)
    img.feather_to_color(w, h, px, PAPEL, 34)
    png = os.path.join(DEST, '_ilus.png')
    img.save_png(png, w, h, px)
    sips('-s', 'format', 'jpeg', '-s', 'formatOptions', '84', png,
         '--out', os.path.join(DEST, 'ilustracion.jpg'))
    os.remove(png)

    # ── Ornamentos: esquina floral y guirnalda, con el fondo crema
    #    recortado a transparente para que se apoyen sobre cualquier tono.
    for nombre, (y, x, alto, ancho) in {
        'esquina':   (45, 40, 258, 240),
        'guirnalda': (1370, 337, 92, 350),
    }.items():
        recorte(tarjeta, tmp, y, x, alto, ancho)
        w, h, px = img.load(tmp)
        fondo = img.bg_color(w, h, px, w - 30, h - 30)
        img.save_png(os.path.join(DEST, nombre + '.png'), w, h, px,
                     img.alpha_key(w, h, px, fondo))
        print('ornamento', nombre)

    # ── Fotos de Josefina
    for nombre in ('nacimiento', 'bebe', 'ojitos', 'sonrisa', 'puchero', 'sunset'):
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
