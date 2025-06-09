import jax
import jax.numpy as jnp

class LossDeflector:

    def __init__(self, x_order=0, y_order=0):
        self.x_order = x_order
        self.y_order = y_order

    def __call__(self, value, target=1, *args, **kwargs):
        (de_ri, de_ti) = value
        c_x = de_ti.shape[0] // 2
        c_y = de_ti.shape[1] // 2
        res = de_ti[c_x + self.x_order, c_y + self.y_order]
        return target - res

class LossSpectrumL2:

    def __init__(self):
        pass

    def __call__(self, pred, target, *args, **kwargs):
        gap = jnp.linalg.norm(pred, target)
        return gap