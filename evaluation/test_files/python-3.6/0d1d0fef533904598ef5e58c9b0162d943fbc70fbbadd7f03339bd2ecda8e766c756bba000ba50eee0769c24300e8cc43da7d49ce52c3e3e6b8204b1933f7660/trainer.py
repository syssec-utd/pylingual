import datetime
import os
import time
from loguru import logger
import torch
from torch.nn.parallel import DistributedDataParallel as DDP
from torch.utils.tensorboard import SummaryWriter
from tepe.core import Trainer as BaseTrainer
from ..data import DataPrefetcher
from ..utils import ModelEMA, all_reduce_norm, get_model_info, gpu_mem_usage, is_parallel, occupy_mem, synchronize

class Trainer(BaseTrainer):

    def before_train(self):
        torch.cuda.set_device(self.local_rank)
        model = self.task.get_model(train=True)
        logger.info('Model Summary: {}'.format(get_model_info(model, self.task.test_size)))
        model.to(self.device)
        self.optimizer = self.task.get_optimizer()
        model = self.resume_train(model)
        self.no_aug = self.start_epoch >= self.max_epoch - self.task.no_aug_epochs
        self.train_loader = self.task.get_train_loader()
        if self.no_aug:
            self.train_loader.close_mosaic()
        logger.info('init prefetcher, this might take one minute or less...')
        self.prefetcher = DataPrefetcher(self.train_loader)
        self.max_iter = len(self.train_loader)
        self.lr_scheduler = self.task.get_lr_scheduler()
        if self.task.occupy:
            occupy_mem(self.local_rank)
        if self.is_distributed:
            model = DDP(model, device_ids=[self.local_rank], broadcast_buffers=False)
        if self.use_model_ema:
            self.ema_model = ModelEMA(model, 0.9998)
            self.ema_model.updates = self.max_iter * self.start_epoch
        self.model = model
        self.model.train()
        self.evaluator = self.task.get_evaluator(train=True)
        self.best_eval_value = ['map', 0]
        if self.rank == 0:
            self.tblogger = SummaryWriter(self.train_result_path)
        self.t0 = time.time()
        logger.info('Training start...')
        logger.info('\n{}'.format(model))

    def before_epoch(self):
        logger.info('---> start train epoch{}'.format(self.epoch + 1))
        if self.epoch + 1 == self.max_epoch - self.task.no_aug_epochs or self.no_aug:
            logger.info('--->No mosaic aug now!')
            self.train_loader.close_mosaic()
            logger.info('--->Add additional L1 loss now!')
            if self.is_distributed:
                self.model.module.head.use_l1 = True
            else:
                self.model.head.use_l1 = True
            self.task.eval_interval = 1
            if not self.no_aug:
                self.save_ckpt(ckpt_name='last_mosaic_epoch')

    def train_one_epoch(self):
        for self.iter in range(self.max_iter):
            self.before_iter()
            self.train_one_iter()
            self.after_iter()

    def train_one_iter(self):
        (inps, targets) = self.prefetcher.next()
        inps = inps.to(self.data_type)
        targets = targets.to(self.data_type)
        targets.requires_grad = False
        data_end_time = time.time()
        with torch.cuda.amp.autocast(enabled=self.amp_training):
            outputs = self.model(inps, targets)
        loss = outputs['total_loss']
        self.optimizer.zero_grad()
        self.scaler.scale(loss).backward()
        self.scaler.step(self.optimizer)
        self.scaler.update()
        if self.use_model_ema:
            self.ema_model.update(self.model)
        lr = self.lr_scheduler.update_lr(self.progress_in_iter + 1)
        for param_group in self.optimizer.param_groups:
            param_group['lr'] = lr
        iter_end_time = time.time()
        self.meter.update(iter_time=iter_end_time - self.iter_start_time, data_time=data_end_time - self.iter_start_time, lr=lr, **outputs)

    def after_iter(self):
        """
        `after_iter` contains two parts of logic:
            * log information
            * reset setting of resize
        """
        if (self.iter + 1) % self.task.print_interval == 0:
            left_iters = self.max_iter * self.max_epoch - (self.progress_in_iter + 1)
            eta_seconds = self.meter['iter_time'].global_avg * left_iters
            eta_str = 'ETA: {}'.format(datetime.timedelta(seconds=int(eta_seconds)))
            progress_str = 'epoch: {}/{}, iter: {}/{}'.format(self.epoch + 1, self.max_epoch, self.iter + 1, self.max_iter)
            loss_meter = self.meter.get_filtered_meter('loss')
            loss_str = ', '.join(['{}: {:.1f}'.format(k, v.latest) for (k, v) in loss_meter.items()])
            time_meter = self.meter.get_filtered_meter('time')
            time_str = ', '.join(['{}: {:.3f}s'.format(k, v.avg) for (k, v) in time_meter.items()])
            logger.info('{}, mem: {:.0f}Mb, {}, {}, lr: {:.3e}'.format(progress_str, gpu_mem_usage(), time_str, loss_str, self.meter['lr'].latest) + ', size: {:d}, {}'.format(self.input_size[0], eta_str))
            self.meter.clear_meters()
        if (self.progress_in_iter + 1) % 10 == 0:
            self.input_size = self.task.random_resize(self.train_loader, self.epoch, self.rank, self.is_distributed)

    def after_epoch(self):
        if (self.epoch + 1) % self.task.eval_interval == 0:
            all_reduce_norm(self.model)
        return super().after_epoch()

    def validate(self):
        if self.use_model_ema:
            evalmodel = self.ema_model.ema
        else:
            evalmodel = self.model
            if is_parallel(evalmodel):
                evalmodel = evalmodel.module
        eval_result = self.evaluator.evaluate(evalmodel)
        (ap50_95, ap50, summary) = (eval_result['ap50'], eval_result['ap'], eval_result['summary'])
        self.model.train()
        if self.rank == 0:
            self.tblogger.add_scalar('val/COCOAP50', ap50, self.epoch + 1)
            self.tblogger.add_scalar('val/COCOAP50_95', ap50_95, self.epoch + 1)
        synchronize()
        update_ckpt = self.best_eval_value[1] < ap50_95
        self.best_eval_value[1] = max(self.best_eval_value[1], ap50_95)
        return (update_ckpt, ap50_95)