"""Utilidades de imagen sin dependencias: BMP (via sips) -> pixeles -> PNG."""
import struct, subprocess, zlib, os, sys, tempfile

def load(path):
    """Devuelve (w, h, bytearray RGB) de cualquier imagen que sips sepa leer."""
    tmp = tempfile.mktemp(suffix='.bmp')
    subprocess.run(['sips', '-s', 'format', 'bmp', path, '--out', tmp],
                   capture_output=True, check=True)
    d = open(tmp, 'rb').read()
    os.remove(tmp)
    off = struct.unpack_from('<I', d, 10)[0]
    w = struct.unpack_from('<i', d, 18)[0]
    h_raw = struct.unpack_from('<i', d, 22)[0]
    h = abs(h_raw)
    n = struct.unpack_from('<H', d, 28)[0] // 8
    row = ((w * n + 3) // 4) * 4
    px = bytearray(w * h * 3)
    for j in range(h):
        src = off + (j if h_raw < 0 else h - 1 - j) * row
        linea = d[src:src + w * n]
        if n == 4:
            linea = bytes(b for i in range(0, len(linea), 4) for b in linea[i:i + 3])
        out = bytearray(linea)
        out[0::3] = linea[2::3]      # BMP guarda BGR
        out[2::3] = linea[0::3]
        px[j * w * 3:(j + 1) * w * 3] = out
    return w, h, px

def crop(w, h, px, x, y, bw, bh):
    """Recorta desde la esquina superior izquierda (sips lo hace desde el centro)."""
    bw = min(bw, w - x); bh = min(bh, h - y)
    out = bytearray(bw * bh * 3)
    for j in range(bh):
        s = ((y + j) * w + x) * 3
        out[j * bw * 3:(j + 1) * bw * 3] = px[s:s + bw * 3]
    return bw, bh, out

def save_png(path, w, h, px, alpha=None):
    """px = RGB plano. alpha = bytearray w*h opcional -> PNG RGBA."""
    ch = 4 if alpha else 3
    raw = bytearray()
    for j in range(h):
        raw.append(0)
        if alpha:
            for i in range(w):
                s = (j * w + i) * 3
                raw += px[s:s + 3]; raw.append(alpha[j * w + i])
        else:
            raw += px[j * w * 3:(j + 1) * w * 3]
    def chunk(tag, data):
        c = tag + data
        return struct.pack('>I', len(data)) + c + struct.pack('>I', zlib.crc32(c) & 0xffffffff)
    ihdr = struct.pack('>IIBBBBB', w, h, 8, 6 if alpha else 2, 0, 0, 0)
    open(path, 'wb').write(b'\x89PNG\r\n\x1a\n' + chunk(b'IHDR', ihdr)
                           + chunk(b'IDAT', zlib.compress(bytes(raw), 9)) + chunk(b'IEND', b''))

def fill(w, h, px, x0, y0, x1, y1, color):
    r, g, b = color
    for j in range(max(0, y0), min(h, y1)):
        for i in range(max(0, x0), min(w, x1)):
            s = (j * w + i) * 3
            px[s] = r; px[s + 1] = g; px[s + 2] = b

def clone(w, h, px, dx, dy, sx, sy, bw, bh):
    """Copia un bloque de fondo limpio sobre otra zona (clone stamp)."""
    src = bytearray(px)
    for j in range(bh):
        for i in range(bw):
            s = ((sy + j) * w + sx + i) * 3
            d = ((dy + j) * w + dx + i) * 3
            px[d:d + 3] = src[s:s + 3]

def clone_soft(w, h, px, dx, dy, sx, sy, bw, bh, feather=30, edges='all'):
    """Clone stamp con bordes difuminados para que no se vea el rectangulo.
    edges: que lados difuminar, p.ej. 'rb' = derecha y abajo."""
    src = bytearray(px)
    for j in range(bh):
        for i in range(bw):
            a = 1.0
            if 'l' in edges or edges == 'all': a = min(a, i / feather)
            if 'r' in edges or edges == 'all': a = min(a, (bw - 1 - i) / feather)
            if 't' in edges or edges == 'all': a = min(a, j / feather)
            if 'b' in edges or edges == 'all': a = min(a, (bh - 1 - j) / feather)
            a = max(0.0, min(1.0, a))
            if a == 0: continue
            s = ((sy + j) * w + sx + i) * 3
            d = ((dy + j) * w + dx + i) * 3
            for k in range(3):
                px[d + k] = int(src[s + k] * a + px[d + k] * (1 - a) + 0.5)

def alpha_key(w, h, px, bg, t0=12, t1=30):
    """Alpha suave: transparente donde el pixel esta cerca del crema de fondo.
    Los blancos (petalos, paloma) quedan porque estan lejos del crema."""
    br, bgc, bb = bg
    a = bytearray(w * h)
    for i in range(w * h):
        s = i * 3
        d = ((px[s] - br) ** 2 + (px[s + 1] - bgc) ** 2 + (px[s + 2] - bb) ** 2) ** 0.5
        if d <= t0: a[i] = 0
        elif d >= t1: a[i] = 255
        else: a[i] = int(255 * (d - t0) / (t1 - t0))
    return a

def bg_color(w, h, px, x, y, s=12):
    """Color promedio de un parche, para detectar el crema del papel."""
    t = [0, 0, 0]
    for j in range(y, y + s):
        for i in range(x, x + s):
            p = (j * w + i) * 3
            t[0] += px[p]; t[1] += px[p + 1]; t[2] += px[p + 2]
    n = s * s
    return (t[0] // n, t[1] // n, t[2] // n)

def shift_to(w, h, px, actual, objetivo):
    """Desplaza el color global para que 'actual' quede en 'objetivo',
    sin empujar los blancos fuera de rango."""
    d = [objetivo[k] - actual[k] for k in range(3)]
    for i in range(w * h):
        s = i * 3
        for k in range(3):
            v = px[s + k]
            nv = v + d[k] * (1 - (v / 255.0) ** 3)
            px[s + k] = 0 if nv < 0 else (255 if nv > 255 else int(nv + .5))

def feather_to_color(w, h, px, color, pad):
    """Funde los bordes de la imagen hacia un color plano, para que el
    recorte se apoye sobre el papel sin que se note el rectangulo."""
    for j in range(h):
        for i in range(w):
            d = min(i, j, w - 1 - i, h - 1 - j)
            if d >= pad: continue
            t = d / pad
            a = t * t * (3 - 2 * t)          # smoothstep
            s = (j * w + i) * 3
            for k in range(3):
                px[s + k] = int(px[s + k] * a + color[k] * (1 - a) + .5)
