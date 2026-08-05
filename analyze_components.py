"""Connected-component analysis of the logo alpha channel.

Goal: determine whether the baked-in wordmark ("READY SET IT") is topologically
separable from the circular circuit emblem + speed lines.
"""
from PIL import Image
import numpy as np
from collections import deque

im = Image.open('logo-onLight.png').convert('RGBA')
a = np.array(im)[:, :, 3]
H, W = a.shape
mask = a > 40

labels = np.zeros((H, W), dtype=np.int32)
cur = 0
comps = []

for sy in range(H):
    for sx in range(W):
        if not mask[sy, sx] or labels[sy, sx]:
            continue
        cur += 1
        q = deque([(sy, sx)])
        labels[sy, sx] = cur
        n = 0
        x0 = x1 = sx
        y0 = y1 = sy
        while q:
            y, x = q.popleft()
            n += 1
            if x < x0: x0 = x
            if x > x1: x1 = x
            if y < y0: y0 = y
            if y > y1: y1 = y
            for dy in (-1, 0, 1):
                for dx in (-1, 0, 1):
                    ny, nx = y + dy, x + dx
                    if 0 <= ny < H and 0 <= nx < W and mask[ny, nx] and not labels[ny, nx]:
                        labels[ny, nx] = cur
                        q.append((ny, nx))
        comps.append((n, cur, x0, y0, x1, y1))

comps.sort(reverse=True)
print(f"image {W}x{H}, {len(comps)} components")
for n, cid, x0, y0, x1, y1 in comps[:30]:
    print(f"  id={cid:3d} px={n:7d} bbox=({x0},{y0})-({x1},{y1}) w={x1-x0+1} h={y1-y0+1}")

np.save('_labels.npy', labels)
