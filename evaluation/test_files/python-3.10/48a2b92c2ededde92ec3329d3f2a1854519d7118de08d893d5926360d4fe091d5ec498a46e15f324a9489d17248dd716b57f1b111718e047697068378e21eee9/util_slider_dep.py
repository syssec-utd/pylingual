import itertools as it
import numpy as np
import torch
import ubelt as ub
import torch.utils.data as torch_data

class SlidingSlices(ub.NiceRepr):
    """
    Generates basis for "sliding window" slices to break a large image into
    smaller pieces. Use it.product to slide across the coordinates.

    DEPRECATED IN FAVOR OF SLIDING WINDOW

    Args:
        source (ndarray): array to slice across. It is typically best to ensure
            this is in CHW or CDHW format for maximum compatibility.

        target_shape (tuple): (chan, depth, height, width) of the window
            (be sure to include channels). CHW or CDHW format.

        overlap (float): a number between 0 and 1 indicating the fraction of
            overlap that parts will have. Must be `0 <= overlap < 1`.

        keepbound (bool): if True, a non-uniform step will be taken to ensure
            that the right / bottom of the image is returned as a slice if
            needed. Such a slice will not obey the overlap constraints.
            (Defaults to False)

    Attributes:
        basis_shape - shape of the grid corresponding to the number of steps
            the sliding window will take.
        basis_slices - slices that will be taken in every dimension

    Yields:
        tuple(slice, slice): row and column slices used for numpy indexing

    Example:
        >>> source = np.zeros((220, 220))
        >>> target_shape = (10, 10)
        >>> slider = SlidingSlices(source, target_shape, step=5)
        >>> list(slider.slices)[41:45]
        [(slice(0, 10, None), slice(205, 215, None)),
         (slice(0, 10, None), slice(210, 220, None)),
         (slice(5, 15, None), slice(0, 10, None)),
         (slice(5, 15, None), slice(5, 15, None))]
        >>> print('slider.overlap = {!r}'.format(slider.overlap))
        slider.overlap = [0.5, 0.5]

    Example:
        >>> source = np.zeros((250, 200, 200))
        >>> target_shape = (10, 10, 10)
        >>> slider = SlidingSlices(source, target_shape, step=(1, 2, 2))
        >>> chip = next(slider.chips)
        >>> print('chip.shape = {!r}'.format(chip.shape))
        chip.shape = (10, 10, 10)

    Example:
        >>> source = np.zeros((16, 16))
        >>> target_shape = (4, 4)
        >>> slider = SlidingSlices(source, target_shape, overlap=(.5, .25))
        >>> print('slider.step = {!r}'.format(slider.step))
        slider.step = [2, 3]
        >>> list(ub.chunks(slider.grid, 5))
        [[(0, 0), (0, 1), (0, 2), (0, 3), (0, 4)],
         [(1, 0), (1, 1), (1, 2), (1, 3), (1, 4)],
         [(2, 0), (2, 1), (2, 2), (2, 3), (2, 4)],
         [(3, 0), (3, 1), (3, 2), (3, 3), (3, 4)],
         [(4, 0), (4, 1), (4, 2), (4, 3), (4, 4)],
         [(5, 0), (5, 1), (5, 2), (5, 3), (5, 4)],
         [(6, 0), (6, 1), (6, 2), (6, 3), (6, 4)]]
    """

    def __init__(slider, source, target_shape, overlap=None, step=None, keepbound=False, allow_overshoot=False):
        img_shape = source.shape
        assert len(target_shape) == len(img_shape), 'incompatible dims: {} {}'.format(len(target_shape), len(img_shape))
        assert all((d <= D for (d, D) in zip(target_shape, img_shape))), 'window must be smaller than target'
        (step, overlap) = slider._compute_step(overlap, step, img_shape, target_shape)
        if not all(step):
            raise ValueError('Step must be positive everywhere. Got={}'.format(step))
        stide_kw = [dict(margin=d, stop=D, step=s, keepbound=keepbound, check=not keepbound and (not allow_overshoot)) for (d, D, s) in zip(target_shape, img_shape, step)]
        undershot_shape = []
        overshoots = []
        for kw in stide_kw:
            final_pos = kw['stop'] - kw['margin']
            n_steps = final_pos // kw['step']
            overshoot = final_pos % kw['step']
            undershot_shape.append(n_steps + 1)
            overshoots.append(overshoot)
        if not allow_overshoot and any(overshoots):
            raise ValueError('overshoot={} stide_kw={}'.format(overshoots, stide_kw))
        slider.step = step
        slider.overlap = overlap
        slider.source = source
        slider.window = target_shape
        slider.undershot_shape = undershot_shape
        from netharn.util import wide_strides_1d
        slider.basis_slices = [tuple(wide_strides_1d(**kw)) for kw in stide_kw]
        slider.basis_shape = [len(b) for b in slider.basis_slices]
        slider.n_total = np.prod(slider.basis_shape)

    def __nice__(slider):
        return '{}, step={}'.format(slider.basis_shape, slider.step)

    def _compute_step(slider, overlap, step, img_shape, target_shape):
        """
        Ensures that step hasoverlap the correct shape.  If step is not provided,
        compute step from desired overlap.
        """
        if not (overlap is None) ^ (step is None):
            raise ValueError('specify overlap({}) XOR step ({})'.format(overlap, step))
        if step is None:
            if not isinstance(overlap, (list, tuple)):
                overlap = [overlap] * len(target_shape)
            if any((frac < 0 or frac >= 1 for frac in overlap)):
                raise ValueError('part overlap was {}, but fractional overlaps must be in the range [0, 1)'.format(overlap))
            step = [int(round(d - d * frac)) for (frac, d) in zip(overlap, target_shape)]
        elif not isinstance(step, (list, tuple)):
            step = [step] * len(target_shape)
        overlap = [(d - s) / d for (s, d) in zip(step, target_shape)]
        assert len(step) == len(img_shape), 'incompatible dims'
        return (step, overlap)

    def __len__(slider):
        return slider.n_total

    def _iter_basis_frac(slider):
        for slices in slider._iter_slices():
            frac = [sl.start / D for (sl, D) in zip(slices, slider.source.shape)]
            yield frac

    def _iter_basis_idxs(slider):
        basis_indices = map(range, slider.basis_shape)
        for basis_idxs in it.product(*basis_indices):
            yield basis_idxs

    def _iter_slices(slider):
        for slices in it.product(*slider.basis_slices):
            yield slices

    def _iter_chips(slider):
        for slices in slider._iter_slices():
            chip = slider.source[slices]
            yield chip

    def __iter__(slider):
        for _ in zip(slider.slices, slider.chips):
            yield _

    @property
    def grid(self):
        return self._iter_basis_idxs()

    @property
    def slices(self):
        return self._iter_slices()

    @property
    def chips(self):
        return self._iter_chips()

    def to_dataset(self):
        slider_dset = SlidingIndexDataset(self)
        return slider_dset

    def clf_upscale_transform(slider, dims=(-2, -1)):
        """
        Find transformation to upscale a single scalar classification for each
        window back to the spatial resolution of the original data.

        FIXME:
            This contains bugs that will cause slight alignment errors.

            NOTE:
                returned scales are not correct

                * This does work when the window size is 1x1
                * This does work when the step size is 1

        Args:
            dims (tuple): indices of the spatial (height and width) dimensions

        Example:
            >>> # xdoctest: +REQUIRES(module:kwimage)
            >>> import cv2
            >>> source = np.zeros((3, 25, 25))
            >>> window = (3, 5, 5)
            >>> step = 2
            >>> slider = SlidingSlices(source, window, step=step)
            >>> dims = (-2, -1)
            >>> # Make dummy predicted data
            >>> pred_shape = list(ub.take(slider.basis_shape, dims))
            >>> pred = np.arange(slider.n_total).reshape(pred_shape)
            >>> # upscale using computed transforms
            >>> (yscale, xscale), padding, prepad_shape = slider.clf_upscale_transform(dims)
            >>> cv2.resize(pred.astype(np.uint8), prepad_shape)[0].shape
            >>> resized = cv2.resize(pred.astype(np.uint8), prepad_shape)
            >>> resized = np.pad(resized, padding, mode='constant')
            >>> # FIXME: Following scale doesnt work right
            >>> import kwimage
            >>> kwimage.imresize(pred.astype(np.uint8), (xscale, yscale))[0].shape
        """

        def slcenter(sl):
            """ center of the window defined by a slice """
            return sl.start + (sl.stop - sl.start - 1) / 2

        def slstep(slices):
            return slices[1].start - slices[0].start
        (ydim, xdim) = dims
        orig_h = slider.source.shape[ydim]
        orig_w = slider.source.shape[xdim]
        yslices = slider.basis_slices[ydim]
        xslices = slider.basis_slices[xdim]
        yscale = slstep(yslices)
        xscale = slstep(xslices)
        top = int(np.floor(slcenter(yslices[0])))
        left = int(np.floor(slcenter(xslices[0])))
        bot = yslices[-1].stop - int(np.floor(slcenter(yslices[-1]))) - 1
        right = xslices[-1].stop - int(np.floor(slcenter(xslices[-1]))) - 1
        padding = ((top, bot), (left, right))
        prepad_h = orig_h - left - right
        prepad_w = orig_w - top - bot
        prepad_shape = (prepad_h, prepad_w)
        (pred_h, pred_w) = list(ub.take(slider.basis_shape, dims))
        return ((yscale, xscale), padding, prepad_shape)

    def upscale_overlay(slider, pred, dims=(-2, -1)):
        """
        Upscales a prediction computed at each point in the sliding window to
        overlay on top of the original spatial resolution (albiet coarsley)

        TODO:
            handle the case where overshoots happen, should there be an extra
            translation to account for them? Or does this scheme already take
            that into account?

            It does not because the steps might be nonlinear when keepbound=True,
            but when it is False the steps are linear and this does handle it.

        Example:
            >>> source = np.zeros((3, 11, 11))
            >>> window = (3, 5, 5)
            >>> step = 6
            >>> slider = SlidingSlices(source, window, step=step)
            >>> dims = (-2, -1)
            >>> # Make dummy predicted data
            >>> pred_shape = list(ub.take(slider.basis_shape, dims))
            >>> pred = np.arange(1, slider.n_total + 1).reshape(pred_shape).astype(float)
            >>> # upscale using computed transforms
            >>> upscaled = slider.upscale_overlay(pred)

        Example:
            >>> source = np.zeros((3, 20, 20))
            >>> window = (3, 3, 3)
            >>> step = 6
            >>> slider = SlidingSlices(source, window, step=step, allow_overshoot=True)
            >>> dims = (-2, -1)
            >>> # Make dummy predicted data
            >>> pred_shape = list(ub.take(slider.basis_shape, dims))
            >>> pred = np.arange(1, slider.n_total + 1).reshape(pred_shape).astype(float)
            >>> # upscale using computed transforms
            >>> upscaled = slider.upscale_overlay(pred)
        """
        import cv2
        (ydim, xdim) = dims
        orig_h = slider.source.shape[ydim]
        orig_w = slider.source.shape[xdim]
        sy = slider.step[ydim]
        sx = slider.step[xdim]
        ty = slider.window[ydim] / 2 - 0.5
        tx = slider.window[xdim] / 2 - 0.5
        aff = np.array([[sx, 0, tx], [0, sy, ty]])
        dsize = (orig_w, orig_h)
        if pred.dtype.kind == 'i':
            upscaled = cv2.warpAffine(pred, aff, dsize, flags=cv2.INTER_NEAREST)
        else:
            upscaled = cv2.warpAffine(pred, aff, dsize, flags=cv2.INTER_LINEAR)
        return upscaled

class SlidingIndexDataset(torch_data.Dataset):
    """
    Faster loading of slices at cost of memory

    slider_dset = SlidingIndexDataset(slider)

    slider_loader = torch_data.DataLoader(slider_dset, shuffle=False, batch_size=128)
    slider_iter = iter(slider_loader)
    batch = next(slider_iter)

    """

    def __init__(slider_dset, slider):
        slider_dset.slider = slider

    def __len__(slider_dset):
        return slider_dset.slider.n_total

    def __getitem__(slider_dset, index):
        slider = slider_dset.slider
        basis_idx = np.unravel_index(index, slider.basis_shape)
        slices = tuple([bdim[i] for (bdim, i) in zip(slider.basis_slices, basis_idx)])
        chip = slider.source[slices]
        tensor_chip = torch.FloatTensor(chip)
        tensor_basis_idx = torch.LongTensor(np.array(basis_idx))
        return (tensor_basis_idx, tensor_chip)