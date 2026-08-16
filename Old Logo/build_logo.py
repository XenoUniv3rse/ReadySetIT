from PIL import Image
import numpy as np, os

# Source: ReadySetIT2.png -- dark/coloured strokes on a near-white plate
# (inverse of the old ReadySetIT-Dark.png artwork). The correct key here is
# the multiply-key: on a white plate, coverage is carried by the DARKEST
# channel, not by luminance. Using luminance would erase the saturated
# blue/teal strokes, whose luma sits high despite being fully opaque ink.

os.chdir(os.path.dirname(os.path.abspath(__file__)))
src = Image.open("ReadySetIT2.png").convert("RGB")
a = np.asarray(src).astype(np.float32) / 255.0

plate = 0.9961                      # measured corner value of the white plate
mn = a.min(axis=2)                  # darkest channel == ink coverage
alpha = np.clip((plate - mn) / plate, 0.0, 1.0)

# Kill sensor/JPEG-ish noise in the plate, then restore full opacity in cores.
alpha[alpha < 0.02] = 0.0
alpha = np.clip(alpha * 1.06, 0.0, 1.0)

# Un-premultiply against white: observed = ink*alpha + white*(1-alpha)
safe = np.maximum(alpha, 1e-3)[..., None]
rgb = np.clip((a - (1.0 - safe)) / safe, 0.0, 1.0)


def crop_and_save(img, name):
    bb = img.split()[-1].getbbox()
    img = img.crop(bb)
    img.save(name)
    return img.size, bb


# --- Asset 1: light-background version (nav) -------------------------------
# The artwork is already tuned for white. Ship the straight key.
img_light = Image.fromarray(
    (np.dstack([rgb, alpha]) * 255).astype(np.uint8), "RGBA")
s2, b2 = crop_and_save(img_light, "logo-onLight.png")

# --- Asset 2: dark-background version (footer) -----------------------------
# On #0f172a navy the indigo strokes go muddy. Lift them toward neon:
# push value up, keep hue, and thicken the 1px circuit traces so they
# survive at 56px.
lift = np.clip(rgb * 1.25 + 0.30, 0.0, 1.0)
a2 = np.clip(alpha * 1.35, 0.0, 1.0) ** 0.85
img_neon = Image.fromarray(
    (np.dstack([lift, a2]) * 255).astype(np.uint8), "RGBA")
s1, b1 = crop_and_save(img_neon, "logo-onDark.png")

print("onLight", s2, "bbox", b2)
print("onDark ", s1, "bbox", b1)
print("alpha coverage:", round(float((alpha > 0.5).mean()) * 100, 2), "%")
