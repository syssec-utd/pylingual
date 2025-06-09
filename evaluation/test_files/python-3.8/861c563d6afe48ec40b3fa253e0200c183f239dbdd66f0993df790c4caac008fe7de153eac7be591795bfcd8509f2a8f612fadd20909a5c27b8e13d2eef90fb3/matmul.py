__all__ = ['OnnxMatMul']
import torch
from torch import nn
from onnx2torch.node_converters.registry import add_converter
from onnx2torch.onnx_graph import OnnxGraph
from onnx2torch.onnx_node import OnnxNode
from onnx2torch.utils.common import OnnxToTorchModule
from onnx2torch.utils.common import OperationConverterResult
from onnx2torch.utils.common import onnx_mapping_from_node

class OnnxMatMul(nn.Module, OnnxToTorchModule):

    def forward(self, x: torch.Tensor, y: torch.Tensor) -> torch.Tensor:
        return torch.matmul(x, y)

@add_converter(operation_type='MatMul', version=1)
@add_converter(operation_type='MatMul', version=9)
@add_converter(operation_type='MatMul', version=13)
def _(node: OnnxNode, graph: OnnxGraph) -> OperationConverterResult:
    return OperationConverterResult(torch_module=OnnxMatMul(), onnx_mapping=onnx_mapping_from_node(node=node))