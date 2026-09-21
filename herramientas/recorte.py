import sys; sys.path.insert(0, __import__('os').path.dirname(__file__)); import img
src, dst, x, y, w, h = sys.argv[1], sys.argv[2], *map(int, sys.argv[3:7])
W, H, px = img.load(src)
bw, bh, out = img.crop(W, H, px, x, y, w, h)
img.save_png(dst, bw, bh, out)
