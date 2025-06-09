import contextlib
from copy import deepcopy
from pathlib import Path
import thop
import torch
import torch.nn as nn
from ultralytics.nn.modules import C1, C2, C3, C3TR, SPP, SPPF, Bottleneck, BottleneckCSP, C2f, C3Ghost, C3x, Classify, Concat, Conv, ConvTranspose, Detect, DWConv, DWConvTranspose2d, Ensemble, Focus, GhostBottleneck, GhostConv, Segment
from ultralytics.yolo.utils import DEFAULT_CFG_DICT, DEFAULT_CFG_KEYS, LOGGER, RANK, colorstr, emojis, yaml_load
from ultralytics.yolo.utils.checks import check_requirements, check_yaml
from ultralytics.yolo.utils.torch_utils import fuse_conv_and_bn, fuse_deconv_and_bn, initialize_weights, intersect_dicts, make_divisible, model_info, scale_img, time_sync

class BaseModel(nn.Module):
    """
    The BaseModel class serves as a base class for all the models in the Ultralytics YOLO family.
    """

    def forward(self, x, profile=False, visualize=False):
        """
        Forward pass of the model on a single scale.
        Wrapper for `_forward_once` method.

        Args:
            x (torch.Tensor): The input image tensor
            profile (bool): Whether to profile the model, defaults to False
            visualize (bool): Whether to return the intermediate feature maps, defaults to False

        Returns:
            (torch.Tensor): The output of the network.
        """
        return self._forward_once(x, profile, visualize)

    def _forward_once(self, x, profile=False, visualize=False):
        """
        Perform a forward pass through the network.

        Args:
            x (torch.Tensor): The input tensor to the model
            profile (bool):  Print the computation time of each layer if True, defaults to False.
            visualize (bool): Save the feature maps of the model if True, defaults to False

        Returns:
            (torch.Tensor): The last output of the model.
        """
        (y, dt) = ([], [])
        for m in self.model:
            if m.f != -1:
                x = y[m.f] if isinstance(m.f, int) else [x if j == -1 else y[j] for j in m.f]
            if profile:
                self._profile_one_layer(m, x, dt)
            x = m(x)
            y.append(x if m.i in self.save else None)
            if visualize:
                LOGGER.info('visualize feature not yet supported')
        return x

    def _profile_one_layer(self, m, x, dt):
        """
        Profile the computation time and FLOPs of a single layer of the model on a given input.
        Appends the results to the provided list.

        Args:
            m (nn.Module): The layer to be profiled.
            x (torch.Tensor): The input data to the layer.
            dt (list): A list to store the computation time of the layer.

        Returns:
            None
        """
        c = m == self.model[-1]
        o = thop.profile(m, inputs=[x.clone() if c else x], verbose=False)[0] / 1000000000.0 * 2 if thop else 0
        t = time_sync()
        for _ in range(10):
            m(x.clone() if c else x)
        dt.append((time_sync() - t) * 100)
        if m == self.model[0]:
            LOGGER.info(f"{'time (ms)':>10s} {'GFLOPs':>10s} {'params':>10s}  module")
        LOGGER.info(f'{dt[-1]:10.2f} {o:10.2f} {m.np:10.0f}  {m.type}')
        if c:
            LOGGER.info(f"{sum(dt):10.2f} {'-':>10s} {'-':>10s}  Total")

    def fuse(self, verbose=True):
        """
        Fuse the `Conv2d()` and `BatchNorm2d()` layers of the model into a single layer, in order to improve the
        computation efficiency.

        Returns:
            (nn.Module): The fused model is returned.
        """
        if not self.is_fused():
            for m in self.model.modules():
                if isinstance(m, (Conv, DWConv)) and hasattr(m, 'bn'):
                    m.conv = fuse_conv_and_bn(m.conv, m.bn)
                    delattr(m, 'bn')
                    m.forward = m.forward_fuse
                if isinstance(m, ConvTranspose) and hasattr(m, 'bn'):
                    m.conv_transpose = fuse_deconv_and_bn(m.conv_transpose, m.bn)
                    delattr(m, 'bn')
                    m.forward = m.forward_fuse
            self.info(verbose=verbose)
        return self

    def is_fused(self, thresh=10):
        """
        Check if the model has less than a certain threshold of BatchNorm layers.

        Args:
            thresh (int, optional): The threshold number of BatchNorm layers. Default is 10.

        Returns:
            (bool): True if the number of BatchNorm layers in the model is less than the threshold, False otherwise.
        """
        bn = tuple((v for (k, v) in nn.__dict__.items() if 'Norm' in k))
        return sum((isinstance(v, bn) for v in self.modules())) < thresh

    def info(self, verbose=False, imgsz=640):
        """
        Prints model information

        Args:
            verbose (bool): if True, prints out the model information. Defaults to False
            imgsz (int): the size of the image that the model will be trained on. Defaults to 640
        """
        model_info(self, verbose=verbose, imgsz=imgsz)

    def _apply(self, fn):
        """
        `_apply()` is a function that applies a function to all the tensors in the model that are not
        parameters or registered buffers

        Args:
            fn: the function to apply to the model

        Returns:
            A model that is a Detect() object.
        """
        self = super()._apply(fn)
        m = self.model[-1]
        if isinstance(m, (Detect, Segment)):
            m.stride = fn(m.stride)
            m.anchors = fn(m.anchors)
            m.strides = fn(m.strides)
        return self

    def load(self, weights):
        """
        This function loads the weights of the model from a file

        Args:
            weights (str): The weights to load into the model.
        """
        raise NotImplementedError('This function needs to be implemented by derived classes!')

class DetectionModel(BaseModel):

    def __init__(self, cfg='yolov8n.yaml', ch=3, nc=None, verbose=True):
        super().__init__()
        self.yaml = cfg if isinstance(cfg, dict) else yaml_load(check_yaml(cfg), append_filename=True)
        ch = self.yaml['ch'] = self.yaml.get('ch', ch)
        if nc and nc != self.yaml['nc']:
            LOGGER.info(f"Overriding model.yaml nc={self.yaml['nc']} with nc={nc}")
            self.yaml['nc'] = nc
        (self.model, self.save) = parse_model(deepcopy(self.yaml), ch=ch, verbose=verbose)
        self.names = {i: f'{i}' for i in range(self.yaml['nc'])}
        self.inplace = self.yaml.get('inplace', True)
        m = self.model[-1]
        if isinstance(m, (Detect, Segment)):
            s = 256
            m.inplace = self.inplace
            forward = lambda x: self.forward(x)[0] if isinstance(m, Segment) else self.forward(x)
            m.stride = torch.tensor([s / x.shape[-2] for x in forward(torch.zeros(1, ch, s, s))])
            self.stride = m.stride
            m.bias_init()
        initialize_weights(self)
        if verbose:
            self.info()
            LOGGER.info('')

    def forward(self, x, augment=False, profile=False, visualize=False):
        if augment:
            return self._forward_augment(x)
        return self._forward_once(x, profile, visualize)

    def _forward_augment(self, x):
        img_size = x.shape[-2:]
        s = [1, 0.83, 0.67]
        f = [None, 3, None]
        y = []
        for (si, fi) in zip(s, f):
            xi = scale_img(x.flip(fi) if fi else x, si, gs=int(self.stride.max()))
            yi = self._forward_once(xi)[0]
            yi = self._descale_pred(yi, fi, si, img_size)
            y.append(yi)
        y = self._clip_augmented(y)
        return (torch.cat(y, -1), None)

    @staticmethod
    def _descale_pred(p, flips, scale, img_size, dim=1):
        p[:, :4] /= scale
        (x, y, wh, cls) = p.split((1, 1, 2, p.shape[dim] - 4), dim)
        if flips == 2:
            y = img_size[0] - y
        elif flips == 3:
            x = img_size[1] - x
        return torch.cat((x, y, wh, cls), dim)

    def _clip_augmented(self, y):
        nl = self.model[-1].nl
        g = sum((4 ** x for x in range(nl)))
        e = 1
        i = y[0].shape[-1] // g * sum((4 ** x for x in range(e)))
        y[0] = y[0][..., :-i]
        i = y[-1].shape[-1] // g * sum((4 ** (nl - 1 - x) for x in range(e)))
        y[-1] = y[-1][..., i:]
        return y

    def load(self, weights, verbose=True):
        csd = weights.float().state_dict()
        csd = intersect_dicts(csd, self.state_dict())
        self.load_state_dict(csd, strict=False)
        if verbose and RANK == -1:
            LOGGER.info(f'Transferred {len(csd)}/{len(self.model.state_dict())} items from pretrained weights')

class SegmentationModel(DetectionModel):

    def __init__(self, cfg='yolov8n-seg.yaml', ch=3, nc=None, verbose=True):
        super().__init__(cfg, ch, nc, verbose)

    def _forward_augment(self, x):
        raise NotImplementedError('WARNING ⚠️ SegmentationModel has not supported augment inference yet!')

class ClassificationModel(BaseModel):

    def __init__(self, cfg=None, model=None, ch=3, nc=None, cutoff=10, verbose=True):
        super().__init__()
        self._from_detection_model(model, nc, cutoff) if model is not None else self._from_yaml(cfg, ch, nc, verbose)

    def _from_detection_model(self, model, nc=1000, cutoff=10):
        from ultralytics.nn.autobackend import AutoBackend
        if isinstance(model, AutoBackend):
            model = model.model
        model.model = model.model[:cutoff]
        m = model.model[-1]
        ch = m.conv.in_channels if hasattr(m, 'conv') else m.cv1.conv.in_channels
        c = Classify(ch, nc)
        (c.i, c.f, c.type) = (m.i, m.f, 'models.common.Classify')
        model.model[-1] = c
        self.model = model.model
        self.stride = model.stride
        self.save = []
        self.nc = nc

    def _from_yaml(self, cfg, ch, nc, verbose):
        self.yaml = cfg if isinstance(cfg, dict) else yaml_load(check_yaml(cfg), append_filename=True)
        ch = self.yaml['ch'] = self.yaml.get('ch', ch)
        if nc and nc != self.yaml['nc']:
            LOGGER.info(f"Overriding model.yaml nc={self.yaml['nc']} with nc={nc}")
            self.yaml['nc'] = nc
        elif not nc and (not self.yaml.get('nc', None)):
            raise ValueError('nc not specified. Must specify nc in model.yaml or function arguments.')
        (self.model, self.save) = parse_model(deepcopy(self.yaml), ch=ch, verbose=verbose)
        self.stride = torch.Tensor([1])
        self.names = {i: f'{i}' for i in range(self.yaml['nc'])}
        self.info()

    def load(self, weights):
        model = weights['model'] if isinstance(weights, dict) else weights
        csd = model.float().state_dict()
        csd = intersect_dicts(csd, self.state_dict())
        self.load_state_dict(csd, strict=False)

    @staticmethod
    def reshape_outputs(model, nc):
        (name, m) = list((model.model if hasattr(model, 'model') else model).named_children())[-1]
        if isinstance(m, Classify):
            if m.linear.out_features != nc:
                m.linear = nn.Linear(m.linear.in_features, nc)
        elif isinstance(m, nn.Linear):
            if m.out_features != nc:
                setattr(model, name, nn.Linear(m.in_features, nc))
        elif isinstance(m, nn.Sequential):
            types = [type(x) for x in m]
            if nn.Linear in types:
                i = types.index(nn.Linear)
                if m[i].out_features != nc:
                    m[i] = nn.Linear(m[i].in_features, nc)
            elif nn.Conv2d in types:
                i = types.index(nn.Conv2d)
                if m[i].out_channels != nc:
                    m[i] = nn.Conv2d(m[i].in_channels, nc, m[i].kernel_size, m[i].stride, bias=m[i].bias is not None)

def torch_safe_load(weight):
    """
    This function attempts to load a PyTorch model with the torch.load() function. If a ModuleNotFoundError is raised,
    it catches the error, logs a warning message, and attempts to install the missing module via the
    check_requirements() function. After installation, the function again attempts to load the model using torch.load().

    Args:
        weight (str): The file path of the PyTorch model.

    Returns:
        The loaded PyTorch model.
    """
    from ultralytics.yolo.utils.downloads import attempt_download_asset
    file = attempt_download_asset(weight)
    try:
        return (torch.load(file, map_location='cpu'), file)
    except ModuleNotFoundError as e:
        if e.name == 'models':
            raise TypeError(emojis(f"ERROR ❌️ {weight} appears to be an Ultralytics YOLOv5 model originally trained with https://github.com/ultralytics/yolov5.\nThis model is NOT forwards compatible with YOLOv8 at https://github.com/ultralytics/ultralytics.\nRecommend fixes are to train a new model using the latest 'ultralytics' package or to run a command with an official YOLOv8 model, i.e. 'yolo predict model=yolov8n.pt'")) from e
        LOGGER.warning(f"WARNING ⚠️ {weight} appears to require '{e.name}', which is not in ultralytics requirements.\nAutoInstall will run now for '{e.name}' but this feature will be removed in the future.\nRecommend fixes are to train a new model using the latest 'ultralytics' package or to run a command with an official YOLOv8 model, i.e. 'yolo predict model=yolov8n.pt'")
        check_requirements(e.name)
        return (torch.load(file, map_location='cpu'), file)

def attempt_load_weights(weights, device=None, inplace=True, fuse=False):
    ensemble = Ensemble()
    for w in weights if isinstance(weights, list) else [weights]:
        (ckpt, w) = torch_safe_load(w)
        args = {**DEFAULT_CFG_DICT, **ckpt['train_args']}
        model = (ckpt.get('ema') or ckpt['model']).to(device).float()
        model.args = args
        model.pt_path = w
        model.task = guess_model_task(model)
        if not hasattr(model, 'stride'):
            model.stride = torch.tensor([32.0])
        ensemble.append(model.fuse().eval() if fuse and hasattr(model, 'fuse') else model.eval())
    for m in ensemble.modules():
        t = type(m)
        if t in (nn.Hardswish, nn.LeakyReLU, nn.ReLU, nn.ReLU6, nn.SiLU, Detect, Segment):
            m.inplace = inplace
        elif t is nn.Upsample and (not hasattr(m, 'recompute_scale_factor')):
            m.recompute_scale_factor = None
    if len(ensemble) == 1:
        return ensemble[-1]
    LOGGER.info(f'Ensemble created with {weights}\n')
    for k in ('names', 'nc', 'yaml'):
        setattr(ensemble, k, getattr(ensemble[0], k))
    ensemble.stride = ensemble[torch.argmax(torch.tensor([m.stride.max() for m in ensemble])).int()].stride
    assert all((ensemble[0].nc == m.nc for m in ensemble)), f'Models differ in class counts: {[m.nc for m in ensemble]}'
    return ensemble

def attempt_load_one_weight(weight, device=None, inplace=True, fuse=False):
    (ckpt, weight) = torch_safe_load(weight)
    args = {**DEFAULT_CFG_DICT, **ckpt['train_args']}
    model = (ckpt.get('ema') or ckpt['model']).to(device).float()
    model.args = {k: v for (k, v) in args.items() if k in DEFAULT_CFG_KEYS}
    model.pt_path = weight
    model.task = guess_model_task(model)
    if not hasattr(model, 'stride'):
        model.stride = torch.tensor([32.0])
    model = model.fuse().eval() if fuse and hasattr(model, 'fuse') else model.eval()
    for m in model.modules():
        t = type(m)
        if t in (nn.Hardswish, nn.LeakyReLU, nn.ReLU, nn.ReLU6, nn.SiLU, Detect, Segment):
            m.inplace = inplace
        elif t is nn.Upsample and (not hasattr(m, 'recompute_scale_factor')):
            m.recompute_scale_factor = None
    return (model, ckpt)

def parse_model(d, ch, verbose=True):
    if verbose:
        LOGGER.info(f"\n{'':>3}{'from':>20}{'n':>3}{'params':>10}  {'module':<45}{'arguments':<30}")
    (nc, gd, gw, act) = (d['nc'], d['depth_multiple'], d['width_multiple'], d.get('activation'))
    if act:
        Conv.default_act = eval(act)
        if verbose:
            LOGGER.info(f"{colorstr('activation:')} {act}")
    ch = [ch]
    (layers, save, c2) = ([], [], ch[-1])
    for (i, (f, n, m, args)) in enumerate(d['backbone'] + d['head']):
        m = getattr(torch.nn, m[3:]) if 'nn.' in m else globals()[m]
        for (j, a) in enumerate(args):
            with contextlib.suppress(NameError):
                args[j] = eval(a) if isinstance(a, str) else a
        n = n_ = max(round(n * gd), 1) if n > 1 else n
        if m in (Classify, Conv, ConvTranspose, GhostConv, Bottleneck, GhostBottleneck, SPP, SPPF, DWConv, Focus, BottleneckCSP, C1, C2, C2f, C3, C3TR, C3Ghost, nn.ConvTranspose2d, DWConvTranspose2d, C3x):
            (c1, c2) = (ch[f], args[0])
            if c2 != nc:
                c2 = make_divisible(c2 * gw, 8)
            args = [c1, c2, *args[1:]]
            if m in (BottleneckCSP, C1, C2, C2f, C3, C3TR, C3Ghost, C3x):
                args.insert(2, n)
                n = 1
        elif m is nn.BatchNorm2d:
            args = [ch[f]]
        elif m is Concat:
            c2 = sum((ch[x] for x in f))
        elif m in (Detect, Segment):
            args.append([ch[x] for x in f])
            if m is Segment:
                args[2] = make_divisible(args[2] * gw, 8)
        else:
            c2 = ch[f]
        m_ = nn.Sequential(*(m(*args) for _ in range(n))) if n > 1 else m(*args)
        t = str(m)[8:-2].replace('__main__.', '')
        m.np = sum((x.numel() for x in m_.parameters()))
        (m_.i, m_.f, m_.type) = (i, f, t)
        if verbose:
            LOGGER.info(f'{i:>3}{str(f):>20}{n_:>3}{m.np:10.0f}  {t:<45}{str(args):<30}')
        save.extend((x % i for x in ([f] if isinstance(f, int) else f) if x != -1))
        layers.append(m_)
        if i == 0:
            ch = []
        ch.append(c2)
    return (nn.Sequential(*layers), sorted(save))

def guess_model_task(model):
    """
    Guess the task of a PyTorch model from its architecture or configuration.

    Args:
        model (nn.Module) or (dict): PyTorch model or model configuration in YAML format.

    Returns:
        str: Task of the model ('detect', 'segment', 'classify').

    Raises:
        SyntaxError: If the task of the model could not be determined.
    """

    def cfg2task(cfg):
        m = cfg['head'][-1][-2].lower()
        if m in ('classify', 'classifier', 'cls', 'fc'):
            return 'classify'
        if m == 'detect':
            return 'detect'
        if m == 'segment':
            return 'segment'
    if isinstance(model, dict):
        with contextlib.suppress(Exception):
            return cfg2task(model)
    if isinstance(model, nn.Module):
        for x in ('model.args', 'model.model.args', 'model.model.model.args'):
            with contextlib.suppress(Exception):
                return eval(x)['task']
        for x in ('model.yaml', 'model.model.yaml', 'model.model.model.yaml'):
            with contextlib.suppress(Exception):
                return cfg2task(eval(x))
        for m in model.modules():
            if isinstance(m, Detect):
                return 'detect'
            elif isinstance(m, Segment):
                return 'segment'
            elif isinstance(m, Classify):
                return 'classify'
    if isinstance(model, (str, Path)):
        model = Path(model)
        if '-seg' in model.stem or 'segment' in model.parts:
            return 'segment'
        elif '-cls' in model.stem or 'classify' in model.parts:
            return 'classify'
        elif 'detect' in model.parts:
            return 'detect'
    LOGGER.warning("WARNING ⚠️ Unable to automatically guess model task, assuming 'task=detect'. Explicitly define task for your model, i.e. 'task=detect', 'task=segment' or 'task=classify'.")
    return 'detect'