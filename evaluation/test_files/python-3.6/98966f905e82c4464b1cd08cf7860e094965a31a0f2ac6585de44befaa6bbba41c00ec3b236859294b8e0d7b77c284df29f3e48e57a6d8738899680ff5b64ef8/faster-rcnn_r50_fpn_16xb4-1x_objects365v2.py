_base_ = ['../_base_/models/faster-rcnn_r50_fpn.py', '../_base_/datasets/objects365v2_detection.py', '../_base_/schedules/schedule_1x.py', '../_base_/default_runtime.py']
model = dict(roi_head=dict(bbox_head=dict(num_classes=365)))
train_dataloader = dict(batch_size=4)
optim_wrapper = dict(type='OptimWrapper', optimizer=dict(type='SGD', lr=0.08, momentum=0.9, weight_decay=0.0001), clip_grad=dict(max_norm=35, norm_type=2))
param_scheduler = [dict(type='LinearLR', start_factor=1.0 / 1000, by_epoch=False, begin=0, end=1000), dict(type='MultiStepLR', begin=0, end=12, by_epoch=True, milestones=[8, 11], gamma=0.1)]
auto_scale_lr = dict(base_batch_size=64)