#!/bin/bash
# captura.sh ancho alto salida [url]
# Envuelve la pagina en un iframe para conseguir un viewport angosto de verdad
# (Chrome headless no abre ventanas de menos de 500px).
W="$1"; H="$2"; OUT="$3"; URL="${4:-http://localhost:8777/index.html}"
CH="/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"
cat > herramientas/_frame.html <<HTML
<!doctype html><meta charset=utf-8>
<style>html,body{margin:0;padding:0;background:#fff}iframe{display:block;border:0;width:${W}px;height:${H}px}</style>
<iframe src="${URL}" scrolling="no"></iframe>
HTML
OW=$(( W > 500 ? W : 500 ))
rm -f "$OUT"
"$CH" --headless --disable-gpu --hide-scrollbars --force-device-scale-factor=1 \
      --window-size=$OW,$H --virtual-time-budget=9000 --screenshot="$OUT" \
      "http://localhost:8777/herramientas/_frame.html" 2>/dev/null
if [ "$OW" != "$W" ]; then
  python3 herramientas/recorte.py "$OUT" "$OUT" 0 0 "$W" "$H"
fi
sips -g pixelWidth -g pixelHeight "$OUT" 2>/dev/null | tail -2 | tr -d '\n'; echo
