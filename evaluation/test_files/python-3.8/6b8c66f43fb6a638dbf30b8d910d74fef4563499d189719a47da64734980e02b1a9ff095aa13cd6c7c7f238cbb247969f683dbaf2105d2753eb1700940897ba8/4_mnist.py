import torch
from antares_core.frameworks.pytorch.custom_op import CustomOp
device = torch.device('cuda') if torch.cuda.is_available() else torch.device('cpu')
dtype = torch.float32
kwargs = {'dtype': dtype, 'device': device, 'requires_grad': False}
x = torch.ones([64, 28 * 28], **kwargs)
torch.manual_seed(0)

def create_param(name, shape):
    return (torch.rand(shape, **kwargs) - 0.5) * 0.01
w0 = create_param('dense_w0', [28 * 28, 512])
b0 = create_param('dense_b0', [512])
w1 = create_param('dense_w1', [512, 512])
b1 = create_param('dense_b1', [512])
w2 = create_param('dense_w2', [512, 10])
b2 = create_param('dense_b2', [10])
num_steps = 100
custom_op_fc0 = CustomOp(ir='\n  fc_out[N, M]       += data[N, K] * weight[K, M];\n  fc_out_bias[N, K]  =  fc_out[N, K] + bias[K];\n  fc_bias_relu[N, K] =  fc_out_bias[N, K].call(`max`, [0.0]);\n', input_orders={'data': x, 'weight': w0, 'bias': b0}, device=device).tune(step=num_steps, use_cache=True, timeout=600).emit()
custom_op_fc1 = CustomOp(ir='\n  fc_out[N, M]       += data[N, K] * weight[K, M];\n  fc_out_bias[N, K]  =  fc_out[N, K] + bias[K];\n  fc_bias_relu[N, K] =  fc_out_bias[N, K].call(`max`, [0.0]);\n', input_orders={'data': custom_op_fc0.output(0), 'weight': w1, 'bias': b1}, device=device).tune(step=num_steps, use_cache=True, timeout=600).emit()
custom_op_fc2 = CustomOp(ir='\n  fc_out[N, M]       += data[N, K] * weight[K, M];\n  fc_out_bias[N, K]  =  fc_out[N, K] + bias[K];\n', input_orders={'data': custom_op_fc1.output(0), 'weight': w2, 'bias': b2}, device=device).tune(step=num_steps, use_cache=True, timeout=600).emit()
y = custom_op_fc0(x, w0, b0)
y = custom_op_fc1(y, w1, b1)
y = custom_op_fc2(y, w2, b2)
print('The result of tensor from Antares is:\n%s' % y.view(-1))
z = torch.addmm(b0, x, w0)
z = torch.nn.functional.relu(z)
z = torch.addmm(b1, z, w1)
z = torch.nn.functional.relu(z)
z = torch.addmm(b2, z, w2)
print('The result of tensor from Pytorch is:\n%s' % z.view(-1))