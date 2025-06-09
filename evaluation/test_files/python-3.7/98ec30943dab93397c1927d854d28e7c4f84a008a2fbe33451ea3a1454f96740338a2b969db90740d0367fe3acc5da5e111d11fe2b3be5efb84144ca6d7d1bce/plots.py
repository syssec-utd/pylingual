"""
Plotting utils
"""
import math
import os
from copy import copy
from pathlib import Path
from urllib.error import URLError
import cv2
import matplotlib
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import seaborn as sn
import torch
from PIL import Image, ImageDraw, ImageFont
from utils.general import CONFIG_DIR, FONT, LOGGER, Timeout, check_font, check_requirements, clip_coords, increment_path, is_ascii, threaded, try_except, xywh2xyxy, xyxy2xywh
from utils.metrics import fitness
RANK = int(os.getenv('RANK', -1))
matplotlib.rc('font', **{'size': 11})
matplotlib.use('Agg')

class Colors:

    def __init__(self):
        hexs = ('FF3838', 'FF9D97', 'FF701F', 'FFB21D', 'CFD231', '48F90A', '92CC17', '3DDB86', '1A9334', '00D4BB', '2C99A8', '00C2FF', '344593', '6473FF', '0018EC', '8438FF', '520085', 'CB38FF', 'FF95C8', 'FF37C7')
        self.palette = [self.hex2rgb(f'#{c}') for c in hexs]
        self.n = len(self.palette)

    def __call__(self, i, bgr=False):
        c = self.palette[int(i) % self.n]
        return (c[2], c[1], c[0]) if bgr else c

    @staticmethod
    def hex2rgb(h):
        return tuple((int(h[1 + i:1 + i + 2], 16) for i in (0, 2, 4)))
colors = Colors()

def check_pil_font(font=FONT, size=10):
    font = Path(font)
    font = font if font.exists() else CONFIG_DIR / font.name
    try:
        return ImageFont.truetype(str(font) if font.exists() else font.name, size)
    except Exception:
        try:
            check_font(font)
            return ImageFont.truetype(str(font), size)
        except TypeError:
            check_requirements('Pillow>=8.4.0')
        except URLError:
            return ImageFont.load_default()

class Annotator:

    def __init__(self, im, line_width=None, font_size=None, font='Arial.ttf', pil=False, example='abc'):
        assert im.data.contiguous, 'Image not contiguous. Apply np.ascontiguousarray(im) to Annotator() input images.'
        non_ascii = not is_ascii(example)
        self.pil = pil or non_ascii
        if self.pil:
            self.im = im if isinstance(im, Image.Image) else Image.fromarray(im)
            self.draw = ImageDraw.Draw(self.im)
            self.font = check_pil_font(font='Arial.Unicode.ttf' if non_ascii else font, size=font_size or max(round(sum(self.im.size) / 2 * 0.035), 12))
        else:
            self.im = im
        self.lw = line_width or max(round(sum(im.shape) / 2 * 0.003), 2)

    def box_label(self, box, label='', color=(128, 128, 128), txt_color=(255, 255, 255)):
        if self.pil or not is_ascii(label):
            self.draw.rectangle(box, width=self.lw, outline=color)
            if label:
                (w, h) = self.font.getsize(label)
                outside = box[1] - h >= 0
                self.draw.rectangle((box[0], box[1] - h if outside else box[1], box[0] + w + 1, box[1] + 1 if outside else box[1] + h + 1), fill=color)
                self.draw.text((box[0], box[1] - h if outside else box[1]), label, fill=txt_color, font=self.font)
        else:
            (p1, p2) = ((int(box[0]), int(box[1])), (int(box[2]), int(box[3])))
            cv2.rectangle(self.im, p1, p2, color, thickness=self.lw, lineType=cv2.LINE_AA)
            if label:
                tf = max(self.lw - 1, 1)
                (w, h) = cv2.getTextSize(label, 0, fontScale=self.lw / 3, thickness=tf)[0]
                outside = p1[1] - h >= 3
                p2 = (p1[0] + w, p1[1] - h - 3 if outside else p1[1] + h + 3)
                cv2.rectangle(self.im, p1, p2, color, -1, cv2.LINE_AA)
                cv2.putText(self.im, label, (p1[0], p1[1] - 2 if outside else p1[1] + h + 2), 0, self.lw / 3, txt_color, thickness=tf, lineType=cv2.LINE_AA)

    def fundus_zones(self, cx, cy, radius):
        colors = [(255, 255, 255), (200, 200, 200), (128, 128, 128)]
        idx = 0
        for r in [radius, 1.3 * radius, 2 * radius]:
            r = round(r)
            if self.pil:
                bbox = (cx - r, cy - r, cx + r, cy + r)
                self.draw.ellipse(bbox, fill=None, outline=colors[idx], width=self.lw)
            else:
                center_coordinates = (cx, cy)
                axesLength = (r, r)
                cv2.ellipse(self.im, center_coordinates, axesLength, 0, 0, 360, colors[idx], self.lw)
            idx = idx + 1

    def rectangle(self, xy, fill=None, outline=None, width=1):
        self.draw.rectangle(xy, fill, outline, width)

    def text(self, xy, text, txt_color=(255, 255, 255)):
        (w, h) = self.font.getsize(text)
        self.draw.text((xy[0], xy[1] - h + 1), text, fill=txt_color, font=self.font)

    def result(self):
        return np.asarray(self.im)

def feature_visualization(x, module_type, stage, n=32, save_dir=Path('runs/detect/exp')):
    """
    x:              Features to be visualized
    module_type:    Module type
    stage:          Module stage within model
    n:              Maximum number of feature maps to plot
    save_dir:       Directory to save results
    """
    if 'Detect' not in module_type:
        (batch, channels, height, width) = x.shape
        if height > 1 and width > 1:
            f = save_dir / f"stage{stage}_{module_type.split('.')[-1]}_features.png"
            blocks = torch.chunk(x[0].cpu(), channels, dim=0)
            n = min(n, channels)
            (fig, ax) = plt.subplots(math.ceil(n / 8), 8, tight_layout=True)
            ax = ax.ravel()
            plt.subplots_adjust(wspace=0.05, hspace=0.05)
            for i in range(n):
                ax[i].imshow(blocks[i].squeeze())
                ax[i].axis('off')
            LOGGER.info(f'Saving {f}... ({n}/{channels})')
            plt.savefig(f, dpi=300, bbox_inches='tight')
            plt.close()
            np.save(str(f.with_suffix('.npy')), x[0].cpu().numpy())

def hist2d(x, y, n=100):
    (xedges, yedges) = (np.linspace(x.min(), x.max(), n), np.linspace(y.min(), y.max(), n))
    (hist, xedges, yedges) = np.histogram2d(x, y, (xedges, yedges))
    xidx = np.clip(np.digitize(x, xedges) - 1, 0, hist.shape[0] - 1)
    yidx = np.clip(np.digitize(y, yedges) - 1, 0, hist.shape[1] - 1)
    return np.log(hist[xidx, yidx])

def butter_lowpass_filtfilt(data, cutoff=1500, fs=50000, order=5):
    from scipy.signal import butter, filtfilt

    def butter_lowpass(cutoff, fs, order):
        nyq = 0.5 * fs
        normal_cutoff = cutoff / nyq
        return butter(order, normal_cutoff, btype='low', analog=False)
    (b, a) = butter_lowpass(cutoff, fs, order=order)
    return filtfilt(b, a, data)

def output_to_target(output):
    targets = []
    for (i, o) in enumerate(output):
        for (*box, conf, cls) in o.cpu().numpy():
            targets.append([i, cls, *list(*xyxy2xywh(np.array(box)[None])), conf])
    return np.array(targets)

@threaded
def plot_images(images, targets, paths=None, fname='images.jpg', names=None, max_size=1920, max_subplots=16):
    if isinstance(images, torch.Tensor):
        images = images.cpu().float().numpy()
    if isinstance(targets, torch.Tensor):
        targets = targets.cpu().numpy()
    if np.max(images[0]) <= 1:
        images *= 255
    (bs, _, h, w) = images.shape
    bs = min(bs, max_subplots)
    ns = np.ceil(bs ** 0.5)
    mosaic = np.full((int(ns * h), int(ns * w), 3), 255, dtype=np.uint8)
    for (i, im) in enumerate(images):
        if i == max_subplots:
            break
        (x, y) = (int(w * (i // ns)), int(h * (i % ns)))
        im = im.transpose(1, 2, 0)
        mosaic[y:y + h, x:x + w, :] = im
    scale = max_size / ns / max(h, w)
    if scale < 1:
        h = math.ceil(scale * h)
        w = math.ceil(scale * w)
        mosaic = cv2.resize(mosaic, tuple((int(x * ns) for x in (w, h))))
    fs = int((h + w) * ns * 0.01)
    annotator = Annotator(mosaic, line_width=round(fs / 10), font_size=fs, pil=True, example=names)
    for i in range(i + 1):
        (x, y) = (int(w * (i // ns)), int(h * (i % ns)))
        annotator.rectangle([x, y, x + w, y + h], None, (255, 255, 255), width=2)
        if paths:
            annotator.text((x + 5, y + 5 + h), text=Path(paths[i]).name[:40], txt_color=(220, 220, 220))
        if len(targets) > 0:
            ti = targets[targets[:, 0] == i]
            boxes = xywh2xyxy(ti[:, 2:6]).T
            classes = ti[:, 1].astype('int')
            labels = ti.shape[1] == 6
            conf = None if labels else ti[:, 6]
            if boxes.shape[1]:
                if boxes.max() <= 1.01:
                    boxes[[0, 2]] *= w
                    boxes[[1, 3]] *= h
                elif scale < 1:
                    boxes *= scale
            boxes[[0, 2]] += x
            boxes[[1, 3]] += y
            for (j, box) in enumerate(boxes.T.tolist()):
                cls = classes[j]
                color = colors(cls)
                cls = names[cls] if names else cls
                if labels or conf[j] > 0.25:
                    label = f'{cls}' if labels else f'{cls} {conf[j]:.1f}'
                    annotator.box_label(box, label, color=color)
    annotator.im.save(fname)

def plot_lr_scheduler(optimizer, scheduler, epochs=300, save_dir=''):
    (optimizer, scheduler) = (copy(optimizer), copy(scheduler))
    y = []
    for _ in range(epochs):
        scheduler.step()
        y.append(optimizer.param_groups[0]['lr'])
    plt.plot(y, '.-', label='LR')
    plt.xlabel('epoch')
    plt.ylabel('LR')
    plt.grid()
    plt.xlim(0, epochs)
    plt.ylim(0)
    plt.savefig(Path(save_dir) / 'LR.png', dpi=200)
    plt.close()

def plot_val_txt():
    x = np.loadtxt('val.txt', dtype=np.float32)
    box = xyxy2xywh(x[:, :4])
    (cx, cy) = (box[:, 0], box[:, 1])
    (fig, ax) = plt.subplots(1, 1, figsize=(6, 6), tight_layout=True)
    ax.hist2d(cx, cy, bins=600, cmax=10, cmin=0)
    ax.set_aspect('equal')
    plt.savefig('hist2d.png', dpi=300)
    (fig, ax) = plt.subplots(1, 2, figsize=(12, 6), tight_layout=True)
    ax[0].hist(cx, bins=600)
    ax[1].hist(cy, bins=600)
    plt.savefig('hist1d.png', dpi=200)

def plot_targets_txt():
    x = np.loadtxt('targets.txt', dtype=np.float32).T
    s = ['x targets', 'y targets', 'width targets', 'height targets']
    (fig, ax) = plt.subplots(2, 2, figsize=(8, 8), tight_layout=True)
    ax = ax.ravel()
    for i in range(4):
        ax[i].hist(x[i], bins=100, label=f'{x[i].mean():.3g} +/- {x[i].std():.3g}')
        ax[i].legend()
        ax[i].set_title(s[i])
    plt.savefig('targets.jpg', dpi=200)

def plot_val_study(file='', dir='', x=None):
    save_dir = Path(file).parent if file else Path(dir)
    plot2 = False
    if plot2:
        ax = plt.subplots(2, 4, figsize=(10, 6), tight_layout=True)[1].ravel()
    (fig2, ax2) = plt.subplots(1, 1, figsize=(8, 4), tight_layout=True)
    for f in sorted(save_dir.glob('study*.txt')):
        y = np.loadtxt(f, dtype=np.float32, usecols=[0, 1, 2, 3, 7, 8, 9], ndmin=2).T
        x = np.arange(y.shape[1]) if x is None else np.array(x)
        if plot2:
            s = ['P', 'R', 'mAP@.5', 'mAP@.5:.95', 't_preprocess (ms/img)', 't_inference (ms/img)', 't_NMS (ms/img)']
            for i in range(7):
                ax[i].plot(x, y[i], '.-', linewidth=2, markersize=8)
                ax[i].set_title(s[i])
        j = y[3].argmax() + 1
        ax2.plot(y[5, 1:j], y[3, 1:j] * 100.0, '.-', linewidth=2, markersize=8, label=f.stem.replace('study_coco_', '').replace('yolo', 'YOLO'))
    ax2.plot(1000.0 / np.array([209, 140, 97, 58, 35, 18]), [34.6, 40.5, 43.0, 47.5, 49.7, 51.5], 'k.-', linewidth=2, markersize=8, alpha=0.25, label='EfficientDet')
    ax2.grid(alpha=0.2)
    ax2.set_yticks(np.arange(20, 60, 5))
    ax2.set_xlim(0, 57)
    ax2.set_ylim(25, 55)
    ax2.set_xlabel('GPU Speed (ms/img)')
    ax2.set_ylabel('COCO AP val')
    ax2.legend(loc='lower right')
    f = save_dir / 'study.png'
    print(f'Saving {f}...')
    plt.savefig(f, dpi=300)

@try_except
@Timeout(30)
def plot_labels(labels, names=(), save_dir=Path('')):
    LOGGER.info(f"Plotting labels to {save_dir / 'labels.jpg'}... ")
    (c, b) = (labels[:, 0], labels[:, 1:].transpose())
    nc = int(c.max() + 1)
    x = pd.DataFrame(b.transpose(), columns=['x', 'y', 'width', 'height'])
    sn.pairplot(x, corner=True, diag_kind='auto', kind='hist', diag_kws=dict(bins=50), plot_kws=dict(pmax=0.9))
    plt.savefig(save_dir / 'labels_correlogram.jpg', dpi=200)
    plt.close()
    matplotlib.use('svg')
    ax = plt.subplots(2, 2, figsize=(8, 8), tight_layout=True)[1].ravel()
    y = ax[0].hist(c, bins=np.linspace(0, nc, nc + 1) - 0.5, rwidth=0.8)
    try:
        [y[2].patches[i].set_color([x / 255 for x in colors(i)]) for i in range(nc)]
    except Exception:
        pass
    ax[0].set_ylabel('instances')
    if 0 < len(names) < 30:
        ax[0].set_xticks(range(len(names)))
        ax[0].set_xticklabels(names, rotation=90, fontsize=10)
    else:
        ax[0].set_xlabel('classes')
    sn.histplot(x, x='x', y='y', ax=ax[2], bins=50, pmax=0.9)
    sn.histplot(x, x='width', y='height', ax=ax[3], bins=50, pmax=0.9)
    labels[:, 1:3] = 0.5
    labels[:, 1:] = xywh2xyxy(labels[:, 1:]) * 2000
    img = Image.fromarray(np.ones((2000, 2000, 3), dtype=np.uint8) * 255)
    for (cls, *box) in labels[:1000]:
        ImageDraw.Draw(img).rectangle(box, width=1, outline=colors(cls))
    ax[1].imshow(img)
    ax[1].axis('off')
    for a in [0, 1, 2, 3]:
        for s in ['top', 'right', 'left', 'bottom']:
            ax[a].spines[s].set_visible(False)
    plt.savefig(save_dir / 'labels.jpg', dpi=200)
    matplotlib.use('Agg')
    plt.close()

def plot_evolve(evolve_csv='path/to/evolve.csv'):
    evolve_csv = Path(evolve_csv)
    data = pd.read_csv(evolve_csv)
    keys = [x.strip() for x in data.columns]
    x = data.values
    f = fitness(x)
    j = np.argmax(f)
    plt.figure(figsize=(10, 12), tight_layout=True)
    matplotlib.rc('font', **{'size': 8})
    print(f'Best results from row {j} of {evolve_csv}:')
    for (i, k) in enumerate(keys[7:]):
        v = x[:, 7 + i]
        mu = v[j]
        plt.subplot(6, 5, i + 1)
        plt.scatter(v, f, c=hist2d(v, f, 20), cmap='viridis', alpha=0.8, edgecolors='none')
        plt.plot(mu, f.max(), 'k+', markersize=15)
        plt.title(f'{k} = {mu:.3g}', fontdict={'size': 9})
        if i % 5 != 0:
            plt.yticks([])
        print(f'{k:>15}: {mu:.3g}')
    f = evolve_csv.with_suffix('.png')
    plt.savefig(f, dpi=200)
    plt.close()
    print(f'Saved {f}')

def plot_results(file='path/to/results.csv', dir=''):
    save_dir = Path(file).parent if file else Path(dir)
    (fig, ax) = plt.subplots(2, 5, figsize=(12, 6), tight_layout=True)
    ax = ax.ravel()
    files = list(save_dir.glob('results*.csv'))
    assert len(files), f'No results.csv files found in {save_dir.resolve()}, nothing to plot.'
    for f in files:
        try:
            data = pd.read_csv(f)
            s = [x.strip() for x in data.columns]
            x = data.values[:, 0]
            for (i, j) in enumerate([1, 2, 3, 4, 5, 8, 9, 10, 6, 7]):
                y = data.values[:, j].astype('float')
                ax[i].plot(x, y, marker='.', label=f.stem, linewidth=2, markersize=8)
                ax[i].set_title(s[j], fontsize=12)
        except Exception as e:
            LOGGER.info(f'Warning: Plotting error for {f}: {e}')
    ax[1].legend()
    fig.savefig(save_dir / 'results.png', dpi=200)
    plt.close()

def profile_idetection(start=0, stop=0, labels=(), save_dir=''):
    ax = plt.subplots(2, 4, figsize=(12, 6), tight_layout=True)[1].ravel()
    s = ['Images', 'Free Storage (GB)', 'RAM Usage (GB)', 'Battery', 'dt_raw (ms)', 'dt_smooth (ms)', 'real-world FPS']
    files = list(Path(save_dir).glob('frames*.txt'))
    for (fi, f) in enumerate(files):
        try:
            results = np.loadtxt(f, ndmin=2).T[:, 90:-30]
            n = results.shape[1]
            x = np.arange(start, min(stop, n) if stop else n)
            results = results[:, x]
            t = results[0] - results[0].min()
            results[0] = x
            for (i, a) in enumerate(ax):
                if i < len(results):
                    label = labels[fi] if len(labels) else f.stem.replace('frames_', '')
                    a.plot(t, results[i], marker='.', label=label, linewidth=1, markersize=5)
                    a.set_title(s[i])
                    a.set_xlabel('time (s)')
                    for side in ['top', 'right']:
                        a.spines[side].set_visible(False)
                else:
                    a.remove()
        except Exception as e:
            print(f'Warning: Plotting error for {f}; {e}')
    ax[1].legend()
    plt.savefig(Path(save_dir) / 'idetection_profile.png', dpi=200)

def save_one_box(xyxy, im, file=Path('im.jpg'), gain=1.02, pad=10, square=False, BGR=False, save=True):
    xyxy = torch.tensor(xyxy).view(-1, 4)
    b = xyxy2xywh(xyxy)
    if square:
        b[:, 2:] = b[:, 2:].max(1)[0].unsqueeze(1)
    b[:, 2:] = b[:, 2:] * gain + pad
    xyxy = xywh2xyxy(b).long()
    clip_coords(xyxy, im.shape)
    crop = im[int(xyxy[0, 1]):int(xyxy[0, 3]), int(xyxy[0, 0]):int(xyxy[0, 2]), ::1 if BGR else -1]
    if save:
        file.parent.mkdir(parents=True, exist_ok=True)
        f = str(increment_path(file).with_suffix('.jpg'))
        Image.fromarray(cv2.cvtColor(crop, cv2.COLOR_BGR2RGB)).save(f, quality=95, subsampling=0)
    return crop