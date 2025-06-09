from copy import deepcopy
import logging
import torch
import torch.nn as nn
import torch.nn.functional as F
from antgo.framework.helper.models.builder import MODELS, build_model

class BasicBlock(nn.Module):

    def __init__(self, in_planes, out_planes, stride, dropout=0.0, activate_before_residual=False):
        super(BasicBlock, self).__init__()
        self.bn1 = nn.BatchNorm2d(in_planes, momentum=0.001)
        self.relu1 = nn.LeakyReLU(negative_slope=0.1, inplace=True)
        self.conv1 = nn.Conv2d(in_planes, out_planes, kernel_size=3, stride=stride, padding=1, bias=False)
        self.bn2 = nn.BatchNorm2d(out_planes, momentum=0.001)
        self.relu2 = nn.LeakyReLU(negative_slope=0.1, inplace=True)
        self.conv2 = nn.Conv2d(out_planes, out_planes, kernel_size=3, stride=1, padding=1, bias=False)
        self.dropout = dropout
        self.equalInOut = in_planes == out_planes
        self.convShortcut = not self.equalInOut and nn.Conv2d(in_planes, out_planes, kernel_size=1, stride=stride, padding=0, bias=False) or None
        self.activate_before_residual = activate_before_residual

    def forward(self, x):
        out = self.relu1(self.bn1(x))
        out = self.relu2(self.bn2(self.conv1(out)))
        if self.dropout > 0:
            out = F.dropout(out, p=self.dropout, training=self.training)
        out = self.conv2(out)
        return torch.add(x if self.equalInOut else self.convShortcut(x), out)

class NetworkBlock(nn.Module):

    def __init__(self, nb_layers, in_planes, out_planes, block, stride, dropout=0.0, activate_before_residual=False):
        super(NetworkBlock, self).__init__()
        self.layer = self._make_layer(block, in_planes, out_planes, nb_layers, stride, dropout, activate_before_residual)

    def _make_layer(self, block, in_planes, out_planes, nb_layers, stride, dropout, activate_before_residual):
        layers = []
        for i in range(int(nb_layers)):
            layers.append(block(i == 0 and in_planes or out_planes, out_planes, i == 0 and stride or 1, dropout, activate_before_residual))
        return nn.Sequential(*layers)

    def forward(self, x):
        return self.layer(x)

@MODELS.register_module()
class WideResNet(nn.Module):

    def __init__(self, num_classes, depth=28, widen_factor=2, dropout=0.0, dense_dropout=0.0, **kwargs):
        super(WideResNet, self).__init__()
        channels = [16, 16 * widen_factor, 32 * widen_factor, 64 * widen_factor]
        assert (depth - 4) % 6 == 0
        n = (depth - 4) / 6
        block = BasicBlock
        self.conv1 = nn.Conv2d(3, channels[0], kernel_size=3, stride=1, padding=1, bias=False)
        self.block1 = NetworkBlock(n, channels[0], channels[1], block, 1, dropout, activate_before_residual=True)
        self.block2 = NetworkBlock(n, channels[1], channels[2], block, 2, dropout)
        self.block3 = NetworkBlock(n, channels[2], channels[3], block, 2, dropout)
        self.bn1 = nn.BatchNorm2d(channels[3], momentum=0.001)
        self.relu = nn.LeakyReLU(negative_slope=0.1, inplace=True)
        self.drop = nn.Dropout(dense_dropout)
        self.fc = nn.Linear(channels[3], num_classes)
        self.channels = channels[3]
        for m in self.modules():
            if isinstance(m, nn.Conv2d):
                nn.init.kaiming_normal_(m.weight, mode='fan_out', nonlinearity='leaky_relu')
            elif isinstance(m, nn.BatchNorm2d):
                nn.init.constant_(m.weight, 1.0)
                nn.init.constant_(m.bias, 0.0)
            elif isinstance(m, nn.Linear):
                nn.init.xavier_normal_(m.weight)
                nn.init.constant_(m.bias, 0.0)

    def train_step(self, images, labels=None, **kwargs):
        return self.forward(images, labels, **kwargs)

    def forward(self, images, labels=None, **kwargs):
        out = self.conv1(images)
        out = self.block1(out)
        out = self.block2(out)
        out = self.block3(out)
        out = self.relu(self.bn1(out))
        out = F.adaptive_avg_pool2d(out, 1)
        out = out.view(-1, self.channels)
        out = self.fc(self.drop(out))
        return (out,)