import torch
import torch.nn as nn
from mmcv.cnn import ConvModule, DepthwiseSeparableConvModule
from mmseg.ops import resize
from mmseg.models.decode_heads.sep_aspp_head import DepthwiseSeparableASPPModule
from mmseg_ext.models.utils import GroupedConvFuse, SideConv
from mmseg_ext.models.builder import SEG_HEADS
from .manyedge_decode_head import BaseManyEdgeDecodeHead

@SEG_HEADS.register_module()
class CASENetMHJSBHead(BaseManyEdgeDecodeHead):

    def __init__(self, dilations=(1, 6, 12, 18), c1_in_channels=256, c1_channels=48, edge_key='fuse', log_edge_keys=('fuse', 'side5'), multilabel_edge_keys=('fuse', 'side5'), loss_multilabel_edge=dict(type='MultiLabelEdgeLoss', loss_weight=1.0), feature_resize_index=-1, **kwargs):
        super().__init__(input_transform='multiple_select', edge_key=edge_key, log_edge_keys=log_edge_keys, multilabel_edge_keys=multilabel_edge_keys, loss_multilabel_edge=loss_multilabel_edge, **kwargs)
        self.feature_resize_index = feature_resize_index
        _interp = 'bilinear'
        _bias = False
        self.side1 = SideConv(in_channels=self.in_channels[0], out_channels=1, conv_cfg=self.conv_cfg, norm_cfg=self.norm_cfg, bias=_bias, act_cfg=self.act_cfg, interpolation=_interp, align_corners=self.align_corners)
        self.side2 = SideConv(in_channels=self.in_channels[1], out_channels=1, conv_cfg=self.conv_cfg, norm_cfg=self.norm_cfg, bias=_bias, act_cfg=self.act_cfg, interpolation=_interp, align_corners=self.align_corners)
        self.side3 = SideConv(in_channels=self.in_channels[2], out_channels=1, conv_cfg=self.conv_cfg, norm_cfg=self.norm_cfg, bias=_bias, act_cfg=self.act_cfg, interpolation=_interp, align_corners=self.align_corners)
        self.side5 = SideConv(in_channels=self.in_channels[4], out_channels=self.num_edge_classes, conv_cfg=self.conv_cfg, norm_cfg=self.norm_cfg, bias=_bias, act_cfg=self.act_cfg, interpolation=_interp, align_corners=self.align_corners)
        self.fuse = GroupedConvFuse(num_classes=self.num_edge_classes, num_sides=4, conv_cfg=self.conv_cfg, bias=_bias)
        self.image_pool = nn.Sequential(nn.AdaptiveAvgPool2d(1), ConvModule(self.in_channels[4], self.channels, 1, conv_cfg=self.conv_cfg, norm_cfg=self.norm_cfg, act_cfg=self.act_cfg))
        self.aspp_modules = DepthwiseSeparableASPPModule(in_channels=self.in_channels[4], channels=self.channels, dilations=dilations, conv_cfg=self.conv_cfg, norm_cfg=self.norm_cfg, act_cfg=self.act_cfg)
        self.c1_bottleneck = ConvModule(in_channels=c1_in_channels, out_channels=c1_channels, kernel_size=1, conv_cfg=self.conv_cfg, norm_cfg=self.norm_cfg, act_cfg=self.act_cfg)
        self.bottleneck = ConvModule((len(dilations) + 1) * self.channels, self.channels, kernel_size=3, padding=1, conv_cfg=self.conv_cfg, norm_cfg=self.norm_cfg, act_cfg=self.act_cfg)
        self.sep_bottleneck = nn.Sequential(DepthwiseSeparableConvModule(in_channels=self.channels + c1_channels, out_channels=self.channels, kernel_size=3, padding=1, norm_cfg=self.norm_cfg, act_cfg=self.act_cfg), DepthwiseSeparableConvModule(in_channels=self.channels, out_channels=self.channels, kernel_size=3, padding=1, norm_cfg=self.norm_cfg, act_cfg=self.act_cfg))

    def forward(self, inputs):
        """Forward function"""
        x = [i for i in inputs]
        assert isinstance(x, list)
        (bs, c, h, w) = x[self.feature_resize_index].shape
        resize_to = (h, w)
        side1 = self.side1(x[0], resize_to)
        side2 = self.side2(x[1], resize_to)
        side3 = self.side3(x[2], resize_to)
        side5 = self.side5(x[4], resize_to)
        fused_edges = self.fuse([side1, side2, side3, side5])
        aspp_outs = [resize(self.image_pool(x[4]), size=x[4].size()[2:], mode='bilinear', align_corners=self.align_corners)]
        aspp_outs.extend(self.aspp_modules(x[4]))
        aspp_outs = torch.cat(aspp_outs, dim=1)
        output = self.bottleneck(aspp_outs)
        c1_output = self.c1_bottleneck(x[1])
        output = resize(input=output, size=c1_output.shape[2:], mode='bilinear', align_corners=self.align_corners)
        output = torch.cat([output, c1_output], dim=1)
        output = self.sep_bottleneck(output)
        output = self.cls_seg(output)
        return (output, dict(side1=side1, side2=side2, side3=side3, side5=side5, fuse=fused_edges))