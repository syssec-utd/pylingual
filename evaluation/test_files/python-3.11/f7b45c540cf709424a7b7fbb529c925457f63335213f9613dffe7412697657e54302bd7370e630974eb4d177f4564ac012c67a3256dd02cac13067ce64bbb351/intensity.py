import numpy as np
__all__ = ['normalize_intensity', 'keep_top_n_inten']

def normalize_intensity(inten, max_num=None, exclude_low_inten=None, no_drop=False):
    """
    The max_num here is the maximum number of intensity, and it will be 1 if is not defined
    输入 list 时可以返回和输入相同的长度，低于 low inten 的部分填充 False
    """
    if max_num is None:
        max_num = 1
    if exclude_low_inten is None:
        exclude_low_inten = 0
    if isinstance(inten, dict):
        max_intensity = max(inten.values())
        scale = max_num / max_intensity
        inten_dict = dict()
        for each_fragment, frag_inten in inten.items():
            scaled_inten = frag_inten * scale
            if scaled_inten > exclude_low_inten:
                inten_dict[each_fragment] = scaled_inten
        return inten_dict
    elif isinstance(inten, (list, tuple, np.ndarray)):
        max_intensity = max(inten)
        scale = max_num / max_intensity
        scaled_inten_list = [_ * scale for _ in inten]
        return [_ for _ in scaled_inten_list if _ > exclude_low_inten]
    else:
        raise

def keep_top_n_inten(inten, top_n=25):
    """
    可以作为 low inten filter 加入 normalize_intensity
    """
    if len(inten) <= top_n:
        return inten
    if isinstance(inten, dict):
        top_n_inten = sorted(inten.values(), reverse=True)[top_n]
        return {frag: inten_value for frag, inten_value in inten.items() if inten_value > top_n_inten}
    elif isinstance(inten, list):
        top_n_inten = sorted(inten, reverse=True)[top_n]
        return [inten_value for inten_value in inten if inten_value > top_n_inten]
    else:
        raise