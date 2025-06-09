from fedbase.utils.data_loader import data_process, log
from fedbase.nodes.node import node
from fedbase.server.server import server_class
import torch
from torch.utils.data import DataLoader
import torch.optim as optim
import os
from functools import partial

def run(dataset_splited, batch_size, num_nodes, model, objective, optimizer, global_rounds, local_steps, finetune_steps, device=torch.device('cuda' if torch.cuda.is_available() else 'cpu')):
    (train_splited, test_splited, split_para) = dataset_splited
    server = server_class(device)
    server.assign_model(model())
    nodes = [node(i, device) for i in range(num_nodes)]
    local_models = [model() for i in range(num_nodes)]
    local_loss = [objective() for i in range(num_nodes)]
    for i in range(num_nodes):
        nodes[i].assign_train(DataLoader(train_splited[i], batch_size=batch_size, shuffle=True))
        nodes[i].assign_test(DataLoader(test_splited[i], batch_size=batch_size, shuffle=False))
        nodes[i].assign_model(local_models[i])
        nodes[i].assign_objective(local_loss[i])
        nodes[i].assign_optim(optimizer(nodes[i].model.parameters()))
    server.distribute(nodes, list(range(num_nodes)))
    for i in range(global_rounds):
        print('-------------------Global round %d start-------------------' % i)
        for j in range(num_nodes):
            nodes[j].local_update_steps(local_steps, partial(nodes[j].train_single_step))
        server.aggregate(nodes, list(range(num_nodes)))
        server.distribute(nodes, list(range(num_nodes)))
        for j in range(num_nodes):
            nodes[j].local_test()
        server.acc(nodes, list(range(num_nodes)))
    for j in range(num_nodes):
        nodes[j].local_update_steps(finetune_steps, partial(nodes[j].train_single_step))
        nodes[j].local_test()
    server.acc(nodes, list(range(num_nodes)))
    log(os.path.basename(__file__)[:-3] + '_' + split_para, nodes, server)