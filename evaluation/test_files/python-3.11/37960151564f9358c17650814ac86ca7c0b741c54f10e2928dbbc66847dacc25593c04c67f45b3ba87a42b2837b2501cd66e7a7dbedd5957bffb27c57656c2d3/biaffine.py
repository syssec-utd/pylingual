import torch
import torch.nn as nn

class Biaffine(nn.Module):

    def __init__(self, n_in, n_out=1, bias_x=True, bias_y=True, diagonal=False):
        super(Biaffine, self).__init__()
        self.n_in = n_in
        self.n_out = n_out
        self.bias_x = bias_x
        self.bias_y = bias_y
        self.diagonal = diagonal
        if self.diagonal:
            self.weight = nn.Parameter(torch.Tensor(n_out, n_in + bias_x))
        else:
            self.weight = nn.Parameter(torch.Tensor(n_out, n_in + bias_x, n_in + bias_y))
        self.reset_parameters()

    def extra_repr(self):
        s = f'n_in={self.n_in}, n_out={self.n_out}'
        if self.bias_x:
            s += f', bias_x={self.bias_x}'
        if self.bias_y:
            s += f', bias_y={self.bias_y}'
        return s

    def reset_parameters(self):
        nn.init.zeros_(self.weight)

    def forward(self, x, y):
        if self.bias_x:
            x = torch.cat((x, torch.ones_like(x[..., :1])), -1)
        if self.bias_y:
            y = torch.cat((y, torch.ones_like(y[..., :1])), -1)
        if self.diagonal:
            s = torch.einsum('bxi,byi,oi->boxy', x, y, self.weight)
        else:
            s = torch.einsum('bxi,oij,byj->boxy', x, self.weight, y)
        s = s.squeeze(1)
        return s