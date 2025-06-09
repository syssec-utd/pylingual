import sys
import cv2
import numpy as np
from .util import *
nclr = 17
pts = [[0, 0], [2, 2], [0, 2], [2, 0], [1, 1], [3, 3], [3, 1], [1, 3], [2, 3], [0, 1], [0, 3], [2, 1], [1, 0], [3, 2], [1, 2], [3, 1]]
"\nsettings = [\n    {'fc': 0, 'bc': 0, 'k': 0}, # b\n    {'fc': 85, 'bc': 0, 'k': 1}, \n    {'fc': 85, 'bc': 0, 'k': 2}, \n    {'fc': 85, 'bc': 0, 'k': 3}, \n    {'fc': 85, 'bc': 0, 'k': 4}, \n    {'fc': 85, 'bc': 0, 'k': 5}, \n    {'fc': 85, 'bc': 0, 'k': 6}, \n    {'fc': 85, 'bc': 0, 'k': 7}, \n    {'fc': 85, 'bc': 0, 'k': 8}, \n    {'fc': 85, 'bc': 0, 'k': 9}, \n    {'fc': 85, 'bc': 0, 'k': 10}, \n    {'fc': 85, 'bc': 0, 'k': 11}, \n    {'fc': 85, 'bc': 0, 'k': 12}, \n    {'fc': 85, 'bc': 0, 'k': 13}, \n    {'fc': 85, 'bc': 0, 'k': 14}, \n    {'fc': 85, 'bc': 0, 'k': 15}, \n    {'fc': 0, 'bc': 85, 'k': 0}, # c1\n    {'fc': 85, 'bc': 170, 'k': 15}, \n    {'fc': 85, 'bc': 170, 'k': 14}, \n    {'fc': 85, 'bc': 170, 'k': 13}, \n    {'fc': 85, 'bc': 170, 'k': 12}, \n    {'fc': 85, 'bc': 170, 'k': 11}, \n    {'fc': 85, 'bc': 170, 'k': 10}, \n    {'fc': 85, 'bc': 170, 'k': 9}, \n    {'fc': 85, 'bc': 170, 'k': 8}, \n    {'fc': 85, 'bc': 170, 'k': 7}, \n    {'fc': 85, 'bc': 170, 'k': 6}, \n    {'fc': 85, 'bc': 170, 'k': 5}, \n    {'fc': 85, 'bc': 170, 'k': 4}, \n    {'fc': 85, 'bc': 170, 'k': 3}, \n    {'fc': 85, 'bc': 170, 'k': 2}, \n    {'fc': 85, 'bc': 170, 'k': 1}, \n    {'fc': 0, 'bc': 170, 'k': 0}, # c2\n    {'fc': 255, 'bc': 170, 'k': 1}, \n    {'fc': 255, 'bc': 170, 'k': 2}, \n    {'fc': 255, 'bc': 170, 'k': 3}, \n    {'fc': 255, 'bc': 170, 'k': 4}, \n    {'fc': 255, 'bc': 170, 'k': 5}, \n    {'fc': 255, 'bc': 170, 'k': 6}, \n    {'fc': 255, 'bc': 170, 'k': 7}, \n    {'fc': 255, 'bc': 170, 'k': 8}, \n    {'fc': 255, 'bc': 170, 'k': 9}, \n    {'fc': 255, 'bc': 170, 'k': 10}, \n    {'fc': 255, 'bc': 170, 'k': 11}, \n    {'fc': 255, 'bc': 170, 'k': 12}, \n    {'fc': 255, 'bc': 170, 'k': 13}, \n    {'fc': 255, 'bc': 170, 'k': 14}, \n    {'fc': 255, 'bc': 170, 'k': 15}, \n    {'fc': 0, 'bc': 255, 'k': 0}, # w\n]\n"
'\ndef make_noise(size, fc=0, bc=255, k=8):\n    # P(fc) = k/16, P(bc) = (16-k)/16\n    if k == 0: return np.zeros(size) + bc\n    idx = np.random.random(size) < k/16\n    img = np.where(idx, fc, bc)\n    return img\n'

def make_grid(size, fc=0, bc=255, k=8):
    img = np.zeros(size) + bc
    for i in range(k):
        r, c = pts[i]
        img[r::4, c::4] = fc
    return img

def grid(img):
    assert img.ndim == 2
    patterns = [make_grid([4, 4], fc=255, bc=0, k=k) for k in range(nclr)]
    clrs = np.linspace(0, 255, nclr).astype(int)
    delims = (clrs[1:] + clrs[:-1]) // 2
    delims = np.asarray([0, *delims, 256])
    idcs = [np.where((img >= st) & (img < ed)) for st, ed in zip(delims[:-1], delims[1:])]
    img = img.copy()
    for idx, pt in zip(idcs, patterns):
        idxm4 = (idx[0] % 4, idx[1] % 4)
        img[idx] = pt[idxm4]
    return img

def grid_bts(img):
    if not is_img_data(img):
        return img
    img = conv2png(img)
    img = np.frombuffer(img, np.uint8)
    img = cv2.imdecode(img, cv2.IMREAD_GRAYSCALE)
    if img is None:
        return None
    img = grid(img).astype(np.uint8)
    img = cv2.imencode('.png', img, [cv2.IMWRITE_PNG_BILEVEL, 1])[1]
    return bytes(img)
"\ndef noise(img):\n    assert img.ndim == 2\n\n    clrs = np.linspace(0, 255, len(settings)).astype(int)\n    delims = (clrs[1:] + clrs[:-1]) // 2\n    delims = np.asarray([0, *delims, 256])\n    idcs = [np.where((img >= st) & (img < ed)) for st, ed in zip(delims[:-1], delims[1:])]\n    \n    img = img.copy()\n    for idx, kw in zip(idcs, settings):\n        img[idx] = make_noise(len(idx[0]), **kw)\n    \n    return img\n\ndef noise_bts(img):\n    if not is_img_data(img): return img\n    img = conv2png(img)\n    img = np.frombuffer(img, np.uint8)\n    img = cv2.imdecode(img, cv2.IMREAD_GRAYSCALE)\n    if img is None: return None\n    img = noise(img).astype(np.uint8)\n    img = cv2.imencode(\n        '.png', img, \n        [cv2.IMWRITE_PNG_COMPRESSION, 9]\n    )[1]\n    return bytes(img)\n"

def noise(img):
    assert img.ndim == 2
    r = np.random.randint(255, size=img.shape)
    img = np.where(r < img, 255, 0)
    return img

def noise_bts(img):
    if not is_img_data(img):
        return img
    img = conv2png(img)
    img = np.frombuffer(img, np.uint8)
    img = cv2.imdecode(img, cv2.IMREAD_GRAYSCALE)
    if img is None:
        return None
    img = noise(img).astype(np.uint8)
    img = cv2.imencode('.png', img, [cv2.IMWRITE_PNG_BILEVEL, 1])[1]
    return bytes(img)
noisebw = noise
noisebw_bts = noise_bts

def main():
    fname = sys.argv[1]
    img = open(fname, 'rb').read()
    img = grid_bts(img)
    with open(fname, 'wb') as f:
        f.write(img)
if __name__ == '__main__':
    main()