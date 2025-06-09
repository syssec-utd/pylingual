import os
import sys
import json
import pickle
import argparse
import importlib
import torch
import torch.optim as optim
import torch.nn as nn
import numpy as np
from torch.utils.data import DataLoader
from datetime import datetime
from tqdm import tqdm
from copy import deepcopy
sys.path.append(os.path.join(os.getcwd()))
from lib.config import CONF
from lib.visual_grounding.dataset import ScannetReferenceDataset
from lib.visual_grounding.solver import Solver
from lib.ap_helper import APCalculator, parse_predictions, parse_groundtruths
from lib.loss_helper.loss_grounding import get_loss
from lib.visual_grounding.eval_helper import get_eval
from models.refnet.refnet import RefNet
from data.scannet.model_util_scannet import ScannetDatasetConfig
print('Import Done', flush=True)
SCANREFER_TRAIN = json.load(open(os.path.join(CONF.PATH.DATA, 'ScanRefer_filtered_train.json')))
SCANREFER_VAL = json.load(open(os.path.join(CONF.PATH.DATA, 'ScanRefer_filtered_val.json')))

def get_dataloader(args, scanrefer, scanrefer_new, all_scene_list, split, config):
    dataset = ScannetReferenceDataset(scanrefer=scanrefer, scanrefer_new=scanrefer_new, scanrefer_all_scene=all_scene_list, split=split, num_points=args.num_points, use_color=args.use_color, use_height=not args.no_height, use_normal=args.use_normal, use_multiview=args.use_multiview, lang_num_max=args.lang_num_max)
    print('evaluate on {} samples'.format(len(dataset)))
    dataloader = DataLoader(dataset, batch_size=args.batch_size, shuffle=True)
    return (dataset, dataloader)

def get_model(args, config):
    input_channels = int(args.use_multiview) * 128 + int(args.use_normal) * 3 + int(args.use_color) * 3 + int(not args.no_height)
    model = RefNet(num_class=config.num_class, num_heading_bin=config.num_heading_bin, num_size_cluster=config.num_size_cluster, mean_size_arr=config.mean_size_arr, num_proposal=args.num_proposals, input_feature_dim=input_channels, use_lang_classifier=not args.no_lang_cls, use_bidir=args.use_bidir, dataset_config=config).cuda()
    model_name = 'model_last.pth' if args.detection else 'model.pth'
    path = os.path.join(CONF.PATH.OUTPUT, args.folder, model_name)
    model.load_state_dict(torch.load(path), strict=False)
    model.eval()
    return model

def get_scannet_scene_list(split):
    scene_list = sorted([line.rstrip() for line in open(os.path.join(CONF.PATH.SCANNET_META, 'scannetv2_{}.txt'.format(split)))])
    return scene_list

def get_scanrefer(args):
    if args.detection:
        scene_list = get_scannet_scene_list('val')
        scanrefer = []
        for scene_id in scene_list:
            data = deepcopy(SCANREFER_TRAIN[0])
            data['scene_id'] = scene_id
            scanrefer.append(data)
    else:
        scanrefer = SCANREFER_TRAIN if args.use_train else SCANREFER_VAL
        scene_list = sorted(list(set([data['scene_id'] for data in scanrefer])))
        if args.num_scenes != -1:
            scene_list = scene_list[:args.num_scenes]
        scanrefer = [data for data in scanrefer if data['scene_id'] in scene_list]
        new_scanrefer_val = scanrefer
        scanrefer_val_new = []
        scanrefer_val_new_scene = []
        scene_id = ''
        for data in scanrefer:
            if scene_id != data['scene_id']:
                scene_id = data['scene_id']
                if len(scanrefer_val_new_scene) > 0:
                    scanrefer_val_new.append(scanrefer_val_new_scene)
                scanrefer_val_new_scene = []
            if len(scanrefer_val_new_scene) >= args.lang_num_max:
                scanrefer_val_new.append(scanrefer_val_new_scene)
                scanrefer_val_new_scene = []
            scanrefer_val_new_scene.append(data)
        if len(scanrefer_val_new_scene) > 0:
            scanrefer_val_new.append(scanrefer_val_new_scene)
    return (scanrefer, scene_list, scanrefer_val_new)

def eval_ref(args):
    print('evaluate localization...')
    DC = ScannetDatasetConfig()
    print('preparing data...')
    (scanrefer, scene_list, scanrefer_val_new) = get_scanrefer(args)
    (_, dataloader) = get_dataloader(args, scanrefer, scanrefer_val_new, scene_list, 'val', DC)
    model = get_model(args, DC)
    POST_DICT = {'remove_empty_box': True, 'use_3d_nms': True, 'nms_iou': 0.25, 'use_old_type_nms': False, 'cls_nms': True, 'per_class_proposal': True, 'conf_thresh': 0.05, 'dataset_config': DC} if not args.no_nms else None
    seeds = [args.seed] + [2 * i for i in range(args.repeat - 1)]
    print('evaluating...')
    score_path = os.path.join(CONF.PATH.OUTPUT, args.folder, 'scores.p')
    pred_path = os.path.join(CONF.PATH.OUTPUT, args.folder, 'predictions.p')
    gen_flag = not os.path.exists(score_path) or args.force or args.repeat > 1
    if gen_flag:
        ref_acc_all = []
        ious_all = []
        masks_all = []
        others_all = []
        lang_acc_all = []
        for seed in seeds:
            torch.manual_seed(seed)
            torch.backends.cudnn.deterministic = True
            torch.backends.cudnn.benchmark = False
            np.random.seed(seed)
            print('generating the scores for seed {}...'.format(seed))
            ref_acc = []
            ious = []
            masks = []
            others = []
            lang_acc = []
            predictions = {}
            for data in tqdm(dataloader):
                for key in data:
                    data[key] = data[key].cuda()
                with torch.no_grad():
                    data = model(data)
                    data = get_loss(data_dict=data, config=DC, detection=True, reference=True, use_lang_classifier=not args.no_lang_cls)
                    data = get_eval(data_dict=data, config=DC, reference=True, use_lang_classifier=not args.no_lang_cls, use_oracle=args.use_oracle, use_cat_rand=args.use_cat_rand, use_best=args.use_best, post_processing=POST_DICT)
                    ref_acc += data['ref_acc']
                    ious += data['ref_iou']
                    masks += data['ref_multiple_mask']
                    others += data['ref_others_mask']
                    lang_acc.append(data['lang_acc'].item())
                    ids = data['scan_idx'].detach().cpu().numpy()
                    for i in range(ids.shape[0]):
                        idx = ids[i]
                        scene_id = scanrefer[idx]['scene_id']
                        object_id = scanrefer[idx]['object_id']
                        ann_id = scanrefer[idx]['ann_id']
                        if scene_id not in predictions:
                            predictions[scene_id] = {}
                        if object_id not in predictions[scene_id]:
                            predictions[scene_id][object_id] = {}
                        if ann_id not in predictions[scene_id][object_id]:
                            predictions[scene_id][object_id][ann_id] = {}
                        predictions[scene_id][object_id][ann_id]['pred_bbox'] = data['pred_bboxes'][i]
                        predictions[scene_id][object_id][ann_id]['gt_bbox'] = data['gt_bboxes'][i]
                        predictions[scene_id][object_id][ann_id]['iou'] = data['ref_iou'][i]
            with open(pred_path, 'wb') as f:
                pickle.dump(predictions, f)
            ref_acc_all.append(ref_acc)
            ious_all.append(ious)
            masks_all.append(masks)
            others_all.append(others)
            lang_acc_all.append(lang_acc)
        ref_acc = np.array(ref_acc_all)
        ious = np.array(ious_all)
        masks = np.array(masks_all)
        others = np.array(others_all)
        lang_acc = np.array(lang_acc_all)
        with open(score_path, 'wb') as f:
            scores = {'ref_acc': ref_acc_all, 'ious': ious_all, 'masks': masks_all, 'others': others_all, 'lang_acc': lang_acc_all}
            pickle.dump(scores, f)
    else:
        print('loading the scores...')
        with open(score_path, 'rb') as f:
            scores = pickle.load(f)
            ref_acc = np.array(scores['ref_acc'])
            ious = np.array(scores['ious'])
            masks = np.array(scores['masks'])
            others = np.array(scores['others'])
            lang_acc = np.array(scores['lang_acc'])
    multiple_dict = {'unique': 0, 'multiple': 1}
    others_dict = {'not_in_others': 0, 'in_others': 1}
    stats = {k: np.sum(masks[0] == v) for (k, v) in multiple_dict.items()}
    stats['overall'] = masks[0].shape[0]
    stats = {}
    for (k, v) in multiple_dict.items():
        stats[k] = {}
        for (k_o, v_o) in others_dict.items():
            stats[k][k_o] = np.sum(np.logical_and(masks[0] == v, others[0] == v_o))
        stats[k]['overall'] = np.sum(masks[0] == v)
    stats['overall'] = {}
    for (k_o, v_o) in others_dict.items():
        stats['overall'][k_o] = np.sum(others[0] == v_o)
    stats['overall']['overall'] = masks[0].shape[0]
    scores = {}
    for (k, v) in multiple_dict.items():
        for k_o in others_dict.keys():
            (ref_accs, acc_025ious, acc_05ious) = ([], [], [])
            for i in range(masks.shape[0]):
                running_ref_acc = np.mean(ref_acc[i][np.logical_and(masks[i] == multiple_dict[k], others[i] == others_dict[k_o])]) if np.sum(np.logical_and(masks[i] == multiple_dict[k], others[i] == others_dict[k_o])) > 0 else 0
                running_acc_025iou = ious[i][np.logical_and(np.logical_and(masks[i] == multiple_dict[k], others[i] == others_dict[k_o]), ious[i] >= 0.25)].shape[0] / ious[i][np.logical_and(masks[i] == multiple_dict[k], others[i] == others_dict[k_o])].shape[0] if np.sum(np.logical_and(masks[i] == multiple_dict[k], others[i] == others_dict[k_o])) > 0 else 0
                running_acc_05iou = ious[i][np.logical_and(np.logical_and(masks[i] == multiple_dict[k], others[i] == others_dict[k_o]), ious[i] >= 0.5)].shape[0] / ious[i][np.logical_and(masks[i] == multiple_dict[k], others[i] == others_dict[k_o])].shape[0] if np.sum(np.logical_and(masks[i] == multiple_dict[k], others[i] == others_dict[k_o])) > 0 else 0
                ref_accs.append(running_ref_acc)
                acc_025ious.append(running_acc_025iou)
                acc_05ious.append(running_acc_05iou)
            if k not in scores:
                scores[k] = {k_o: {} for k_o in others_dict.keys()}
            scores[k][k_o]['ref_acc'] = np.mean(ref_accs)
            scores[k][k_o]['acc@0.25iou'] = np.mean(acc_025ious)
            scores[k][k_o]['acc@0.5iou'] = np.mean(acc_05ious)
        (ref_accs, acc_025ious, acc_05ious) = ([], [], [])
        for i in range(masks.shape[0]):
            running_ref_acc = np.mean(ref_acc[i][masks[i] == multiple_dict[k]]) if np.sum(masks[i] == multiple_dict[k]) > 0 else 0
            running_acc_025iou = ious[i][np.logical_and(masks[i] == multiple_dict[k], ious[i] >= 0.25)].shape[0] / ious[i][masks[i] == multiple_dict[k]].shape[0] if np.sum(masks[i] == multiple_dict[k]) > 0 else 0
            running_acc_05iou = ious[i][np.logical_and(masks[i] == multiple_dict[k], ious[i] >= 0.5)].shape[0] / ious[i][masks[i] == multiple_dict[k]].shape[0] if np.sum(masks[i] == multiple_dict[k]) > 0 else 0
            ref_accs.append(running_ref_acc)
            acc_025ious.append(running_acc_025iou)
            acc_05ious.append(running_acc_05iou)
        scores[k]['overall'] = {}
        scores[k]['overall']['ref_acc'] = np.mean(ref_accs)
        scores[k]['overall']['acc@0.25iou'] = np.mean(acc_025ious)
        scores[k]['overall']['acc@0.5iou'] = np.mean(acc_05ious)
    scores['overall'] = {}
    for k_o in others_dict.keys():
        (ref_accs, acc_025ious, acc_05ious) = ([], [], [])
        for i in range(masks.shape[0]):
            running_ref_acc = np.mean(ref_acc[i][others[i] == others_dict[k_o]]) if np.sum(others[i] == others_dict[k_o]) > 0 else 0
            running_acc_025iou = ious[i][np.logical_and(others[i] == others_dict[k_o], ious[i] >= 0.25)].shape[0] / ious[i][others[i] == others_dict[k_o]].shape[0] if np.sum(others[i] == others_dict[k_o]) > 0 else 0
            running_acc_05iou = ious[i][np.logical_and(others[i] == others_dict[k_o], ious[i] >= 0.5)].shape[0] / ious[i][others[i] == others_dict[k_o]].shape[0] if np.sum(others[i] == others_dict[k_o]) > 0 else 0
            ref_accs.append(running_ref_acc)
            acc_025ious.append(running_acc_025iou)
            acc_05ious.append(running_acc_05iou)
        scores['overall'][k_o] = {}
        scores['overall'][k_o]['ref_acc'] = np.mean(ref_accs)
        scores['overall'][k_o]['acc@0.25iou'] = np.mean(acc_025ious)
        scores['overall'][k_o]['acc@0.5iou'] = np.mean(acc_05ious)
    (ref_accs, acc_025ious, acc_05ious) = ([], [], [])
    for i in range(masks.shape[0]):
        running_ref_acc = np.mean(ref_acc[i])
        running_acc_025iou = ious[i][ious[i] >= 0.25].shape[0] / ious[i].shape[0]
        running_acc_05iou = ious[i][ious[i] >= 0.5].shape[0] / ious[i].shape[0]
        ref_accs.append(running_ref_acc)
        acc_025ious.append(running_acc_025iou)
        acc_05ious.append(running_acc_05iou)
    scores['overall']['overall'] = {}
    scores['overall']['overall']['ref_acc'] = np.mean(ref_accs)
    scores['overall']['overall']['acc@0.25iou'] = np.mean(acc_025ious)
    scores['overall']['overall']['acc@0.5iou'] = np.mean(acc_05ious)
    print('\nstats:')
    for k_s in stats.keys():
        for k_o in stats[k_s].keys():
            print('{} | {}: {}'.format(k_s, k_o, stats[k_s][k_o]))
    for k_s in scores.keys():
        print('\n{}:'.format(k_s))
        for k_m in scores[k_s].keys():
            for metric in scores[k_s][k_m].keys():
                print('{} | {} | {}: {}'.format(k_s, k_m, metric, scores[k_s][k_m][metric]))
    print('\nlanguage classification accuracy: {}'.format(np.mean(lang_acc)))

def eval_det(args):
    print('evaluate detection...')
    DC = ScannetDatasetConfig()
    print('preparing data...')
    (scanrefer, scene_list) = get_scanrefer(args)
    (_, dataloader) = get_dataloader(args, scanrefer, scene_list, 'val', DC)
    model = get_model(args, DC)
    POST_DICT = {'remove_empty_box': True, 'use_3d_nms': True, 'nms_iou': 0.25, 'use_old_type_nms': False, 'cls_nms': True, 'per_class_proposal': True, 'conf_thresh': 0.05, 'dataset_config': DC}
    AP_IOU_THRESHOLDS = [0.25, 0.5]
    AP_CALCULATOR_LIST = [APCalculator(iou_thresh, DC.class2type) for iou_thresh in AP_IOU_THRESHOLDS]
    sem_acc = []
    for data in tqdm(dataloader):
        for key in data:
            data[key] = data[key].cuda()
        with torch.no_grad():
            data = model(data)
            (_, data) = get_loss(data_dict=data, config=DC, detection=True, reference=False)
            data = get_eval(data_dict=data, config=DC, reference=False, post_processing=POST_DICT)
            sem_acc.append(data['sem_acc'].item())
            batch_pred_map_cls = parse_predictions(data, POST_DICT)
            batch_gt_map_cls = parse_groundtruths(data, POST_DICT)
            for ap_calculator in AP_CALCULATOR_LIST:
                ap_calculator.step(batch_pred_map_cls, batch_gt_map_cls)
    print('\nobject detection sem_acc: {}'.format(np.mean(sem_acc)))
    for (i, ap_calculator) in enumerate(AP_CALCULATOR_LIST):
        print()
        print('-' * 10, 'iou_thresh: %f' % AP_IOU_THRESHOLDS[i], '-' * 10)
        metrics_dict = ap_calculator.compute_metrics()
        for key in metrics_dict:
            print('eval %s: %f' % (key, metrics_dict[key]))
if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--folder', type=str, help='Folder containing the model')
    parser.add_argument('--gpu', type=str, help='gpu', default='0')
    parser.add_argument('--batch_size', type=int, help='batch size', default=8)
    parser.add_argument('--lang_num_max', type=int, help='lang num max', default=32)
    parser.add_argument('--num_points', type=int, default=40000, help='Point Number [default: 40000]')
    parser.add_argument('--num_proposals', type=int, default=256, help='Proposal number [default: 256]')
    parser.add_argument('--num_scenes', type=int, default=-1, help='Number of scenes [default: -1]')
    parser.add_argument('--force', action='store_true', help='enforce the generation of results')
    parser.add_argument('--seed', type=int, default=42, help='random seed')
    parser.add_argument('--repeat', type=int, default=1, help='Number of times for evaluation')
    parser.add_argument('--no_height', action='store_true', help='Do NOT use height signal in input.')
    parser.add_argument('--no_lang_cls', action='store_true', help='Do NOT use language classifier.')
    parser.add_argument('--no_nms', action='store_true', help='do NOT use non-maximum suppression for post-processing.')
    parser.add_argument('--use_color', action='store_true', help='Use RGB color in input.')
    parser.add_argument('--use_normal', action='store_true', help='Use RGB color in input.')
    parser.add_argument('--use_multiview', action='store_true', help='Use multiview images.')
    parser.add_argument('--use_bidir', action='store_true', help='Use bi-directional GRU.')
    parser.add_argument('--use_train', action='store_true', help='Use train split in evaluation.')
    parser.add_argument('--use_oracle', action='store_true', help='Use ground truth bounding boxes.')
    parser.add_argument('--use_cat_rand', action='store_true', help='Use randomly selected bounding boxes from correct categories as outputs.')
    parser.add_argument('--use_best', action='store_true', help='Use best bounding boxes as outputs.')
    parser.add_argument('--reference', action='store_true', help='evaluate the reference localization results')
    parser.add_argument('--detection', action='store_true', help='evaluate the object detection results')
    args = parser.parse_args()
    assert args.lang_num_max == 1, 'lang max num == 1; avoid bugs'
    os.environ['CUDA_VISIBLE_DEVICES'] = args.gpu
    os.environ['CUDA_LAUNCH_BLOCKING'] = '1'
    if args.reference:
        eval_ref(args)
    if args.detection:
        eval_det(args)