import numpy as np
from PIL import Image


def _to_array(src, size=(128, 128)):
    img = src if isinstance(src, Image.Image) else Image.open(src)
    return np.asarray(img.convert("RGB").resize(size), dtype=np.float32) / 255.0


def _rgb_to_hsv(arr):
    r, g, b = arr[..., 0], arr[..., 1], arr[..., 2]
    mx, mn = np.max(arr, axis=-1), np.min(arr, axis=-1)
    diff = mx - mn + 1e-8
    h = np.zeros_like(mx)
    h[mx == r] = (((g - b) / diff) % 6)[mx == r]
    h[mx == g] = (((b - r) / diff) + 2)[mx == g]
    h[mx == b] = (((r - g) / diff) + 4)[mx == b]
    return np.stack([h / 6.0, diff / (mx + 1e-8), mx], axis=-1)


def extract_features(src):
    arr = _to_array(src)
    hsv = _rgb_to_hsv(arr)
    feats = []
    for a in (arr, hsv):
        for c in range(3):
            ch = a[..., c].ravel()
            feats += [ch.mean(), ch.std(), np.percentile(ch, 25), np.percentile(ch, 75)]
    feats += list(np.histogram(hsv[..., 0], bins=8, range=(0, 1))[0] / hsv[..., 0].size)
    feats += list(np.histogram(hsv[..., 2], bins=8, range=(0, 1))[0] / hsv[..., 2].size)
    gray = arr.mean(axis=-1)
    feats += [np.abs(np.diff(gray, axis=1)).mean(),
              np.abs(np.diff(gray, axis=0)).mean(), gray.std()]
    return np.array(feats, dtype=np.float32)


FEATURE_DIM = len(extract_features(Image.new("RGB", (128, 128), (120, 90, 140))))
