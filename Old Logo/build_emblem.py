"""Build emblem-only logo assets by excising the baked-in wordmark.

The source artwork bakes "READY SET IT" inside the circular circuit emblem.
We now set the company name as live HTML text beside the mark, so keeping the
baked text would print the name twice.

Connected-component analysis showed the glyphs are topologically separate from
the ring / circuit traces / speed lines. Rather than hardcoding component ids
(which differ between the light and dark crops), we identify the wordmark
geometrically: the glyphs are the compact blobs living inside the central text
band of the emblem. The ring and the speed lines are excluded because they are
either far larger or extend outside that band.
"""
from PIL import Image
import numpy as np
from collections import deque


def label_components(mask):
    H, W = mask.shape
    labels = np.zeros((H, W), dtype=np.int32)
    cur = 0
    boxes = {}
    for sy in range(H):
        row = mask[sy]
        for sx in range(W):
            if not row[sx] or labels[sy, sx]:
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
            boxes[cur] = (n, x0, y0, x1, y1)
    return labels, boxes


def build(src, dst):
    im = Image.open(src).convert('RGBA')
    arr = np.array(im).astype(np.int16)
    H, W = arr.shape[:2]

    labels, boxes = label_components(arr[:, :, 3] > 40)

    # The wordmark occupies the central horizontal band of the emblem and sits
    # to the right of the speed lines. Glyphs are compact: bounded in both
    # dimensions, and never as tall or wide as the ring.
    band_top, band_bot = 0.28 * H, 0.72 * H
    kill_ids = []
    for cid, (n, x0, y0, x1, y1) in boxes.items():
        w, h = x1 - x0 + 1, y1 - y0 + 1
        if w > 0.55 * W and h > 0.55 * H:
            continue                       # the ring itself
        if x0 < 0.36 * W:
            continue                       # speed lines on the left
        if y0 < band_top or y1 > band_bot:
            continue                       # circuit traces above/below the band
        if h > 0.30 * H:
            continue                       # anything unexpectedly tall
        kill_ids.append(cid)

    kill = np.isin(labels, kill_ids)

    # The labelling threshold (alpha > 40) ignores anti-aliased edge pixels, so
    # each excised glyph leaves a faint ghost outline behind. Dilate the kill
    # mask and sweep away any weak, unlabelled pixel in its neighbourhood --
    # unlabelled means it was never part of a solid surviving structure.
    dil = kill.copy()
    for _ in range(6):
        d = dil.copy()
        d[1:, :] |= dil[:-1, :]
        d[:-1, :] |= dil[1:, :]
        d[:, 1:] |= dil[:, :-1]
        d[:, :-1] |= dil[:, 1:]
        dil = d
    ghost = dil & (labels == 0)

    arr[kill | ghost, 3] = 0

    alpha = arr[:, :, 3]
    ys, xs = np.nonzero(alpha > 8)
    y0, y1 = ys.min(), ys.max()
    x0, x1 = xs.min(), xs.max()

    out = Image.fromarray(arr.astype(np.uint8)).crop((x0, y0, x1 + 1, y1 + 1))
    out.save(dst)
    print(f"{dst}: {out.size} removed {len(kill_ids)} components {sorted(kill_ids)}")


build('logo-onLight.png', 'emblem-onLight.png')
build('logo-onDark.png', 'emblem-onDark.png')
