import torch
from torch import Tensor

class PositionalEncoding(torch.nn.Module):
    """The positional encoding scheme from `"Attention Is All You Need"
    <https://arxiv.org/pdf/1706.03762.pdf>`_ paper

    .. math::

        PE(x)_{2 \\cdot i} &= \\sin(x / 10000^{2 \\cdot i / d})

        PE(x)_{2 \\cdot i + 1} &= \\cos(x / 10000^{2 \\cdot i / d})

    where :math:`x` is the position and :math:`i` is the dimension.

    Args:
        out_channels (int): Size :math:`d` of each output sample.
        base_freq (float, optional): The base frequency of sinusoidal
            functions. (default: :obj:`1e-4`)
        granularity (float, optional): The granularity of the positions. If
            set to smaller value, the encoder will capture more fine-grained
            changes in positions. (default: :obj:`1.0`)
    """

    def __init__(self, out_channels: int, base_freq: float=0.0001, granularity: float=1.0):
        super().__init__()
        if out_channels % 2 != 0:
            raise ValueError(f"Cannot use sinusoidal positional encoding with odd 'out_channels' (got {out_channels}).")
        self.out_channels = out_channels
        self.base_freq = base_freq
        self.granularity = granularity
        frequency = torch.logspace(0, 1, out_channels // 2, base_freq)
        self.register_buffer('frequency', frequency)

    def forward(self, x: Tensor) -> Tensor:
        """"""
        x = x / self.granularity if self.granularity != 1.0 else x
        out = x.view(-1, 1) * self.frequency.view(1, -1)
        return torch.cat([torch.sin(out), torch.cos(out)], dim=-1)

    def __repr__(self) -> str:
        return f'{self.__class__.__name__}({self.out_channels})'