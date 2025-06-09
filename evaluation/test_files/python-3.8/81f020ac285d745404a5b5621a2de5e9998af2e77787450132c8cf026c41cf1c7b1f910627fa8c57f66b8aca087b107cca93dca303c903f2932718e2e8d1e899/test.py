import numpy as np
import paddle
from paddle.distributed import fleet
from paddle.vision.models import ResNet
from paddle.vision.models.resnet import BottleneckBlock
from paddle.io import Dataset, BatchSampler, DataLoader
base_lr = 0.1
momentum_rate = 0.9
l2_decay = 0.0001
epoch = 3
batch_num = 1
batch_size = 1
class_dim = 102

class RandomDataset(Dataset):

    def __init__(self, num_samples):
        self.num_samples = num_samples

    def __getitem__(self, idx):
        image = np.random.random([3, 224, 224]).astype('float32')
        label = np.random.randint(0, class_dim - 1, (1,)).astype('int64')
        return (image, label)

    def __len__(self):
        return self.num_samples

def optimizer_setting(parameter_list=None):
    optimizer = paddle.optimizer.Momentum(learning_rate=base_lr, momentum=momentum_rate, weight_decay=paddle.regularizer.L2Decay(l2_decay), parameters=parameter_list)
    return optimizer

def train_resnet():
    fleet.init(is_collective=True)
    resnet = ResNet(BottleneckBlock, 18, num_classes=class_dim)
    optimizer = optimizer_setting(parameter_list=resnet.parameters())
    optimizer = fleet.distributed_optimizer(optimizer)
    resnet = fleet.distributed_model(resnet)
    dataset = RandomDataset(batch_num * batch_size)
    train_loader = DataLoader(dataset, batch_size=batch_size, shuffle=True, drop_last=True, num_workers=2)
    print('Distributed training start...')
    for eop in range(epoch):
        resnet.train()
        for (batch_id, data) in enumerate(train_loader()):
            (img, label) = data
            label.stop_gradient = True
            out = resnet(img)
            loss = paddle.nn.functional.cross_entropy(input=out, label=label)
            avg_loss = paddle.mean(x=loss)
            acc_top1 = paddle.metric.accuracy(input=out, label=label, k=1)
            acc_top5 = paddle.metric.accuracy(input=out, label=label, k=5)
            avg_loss.backward()
            optimizer.step()
            resnet.clear_gradients()
            print('[Epoch %d, batch %d] loss: %.5f, acc1: %.5f, acc5: %.5f' % (eop, batch_id, avg_loss, acc_top1, acc_top5))
    print('Distributed training completed')
if __name__ == '__main__':
    import os
    nnodes = os.getenv('PADDLE_NNODES')
    cn = os.getenv('PADDLE_LOCAL_SIZE')
    print(f'Prepare distributed training with {nnodes} nodes {cn} cards')
    train_resnet()