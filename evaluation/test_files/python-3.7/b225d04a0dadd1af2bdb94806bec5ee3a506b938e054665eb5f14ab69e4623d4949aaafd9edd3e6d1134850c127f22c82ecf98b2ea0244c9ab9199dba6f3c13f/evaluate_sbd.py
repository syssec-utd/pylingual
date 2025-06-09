import argparse
import os.path as osp
import time
from pyEdgeEval.evaluators.sbd import SBDEvaluator
from pyEdgeEval.utils import get_root_logger, mkdir_or_exist
__all__ = ['evaluate_sbd']

def parse_args():
    parser = argparse.ArgumentParser(description='Evaluate SBD output')
    parser.add_argument('sbd_path', type=str, help='the root path of the SBD dataset')
    parser.add_argument('pred_path', type=str, help='the root path of the predictions')
    parser.add_argument('--cls-dir', type=str, default='cls_orig', help='directory name for class labels')
    parser.add_argument('--inst-dir', type=str, default='inst_orig', help='directory name for instance labels')
    parser.add_argument('--pred-suffix', type=str, default='.png', help='suffix for predicted images')
    parser.add_argument('--output-path', type=str, help='the root path of where the results are populated')
    parser.add_argument('--categories', type=str, help='the category number to evaluate; can be multiple values')
    parser.add_argument('--raw', action='store_true', help='option to remove the thinning process (i.e. uses raw predition)')
    parser.add_argument('--pre-seal', action='store_true', help='prior to SEAL, the evaluations were not as strict')
    parser.add_argument('--nonIS', action='store_true', help='non instance sensitive evaluation')
    parser.add_argument('--max-dist', type=float, default=0.02, help='tolerance distance (default: 0.02)')
    parser.add_argument('--thresholds', type=str, default='99', help='the number of thresholds (could be a list of floats); use 99 for eval')
    parser.add_argument('--apply-nms', action='store_true', help='applies NMS before evaluation')
    parser.add_argument('--nproc', type=int, default=4, help='the number of parallel threads')
    return parser.parse_args()

def evaluate(sbd_path: str, pred_path: str, cls_dir: str, inst_dir: str, pred_suffix: str, output_path: str, categories: str, pre_seal: bool, apply_thinning: bool, apply_nms: bool, nonIS: bool, max_dist: float, thresholds: str, nproc: int):
    """Evaluate SBD"""
    if categories is None:
        print('use all categories')
        categories = list(range(1, len(SBDEvaluator.CLASSES) + 1))
    else:
        categories = categories.strip()
        try:
            categories = [int(categories)]
        except ValueError:
            try:
                if categories.startswith('[') and categories.endswith(']'):
                    categories = categories[1:-1]
                    categories = [int(cat.strip()) for cat in categories.split(',')]
                else:
                    print('Bad categories format; should be a python list of floats (`[a, b, c]`)')
                    return
            except ValueError:
                print('Bad categories format; should be a python list of ints (`[a, b, c]`)')
                return
    for cat in categories:
        assert 0 < cat < 21, f'category needs to be between 1 ~ 19, but got {cat}'
    thresholds = thresholds.strip()
    try:
        n_thresholds = int(thresholds)
        thresholds = n_thresholds
    except ValueError:
        try:
            if thresholds.startswith('[') and thresholds.endswith(']'):
                thresholds = thresholds[1:-1]
                thresholds = [float(t.strip()) for t in thresholds.split(',')]
            else:
                print('Bad threshold format; should be a python list of floats (`[a, b, c]`)')
                return
        except ValueError:
            print('Bad threshold format; should be a python list of ints (`[a, b, c]`)')
            return
    if output_path is None:
        timestamp = time.strftime('%Y%m%d_%H%M%S', time.localtime())
        output_path = osp.join(osp.normpath(pred_path), f'edge_results_{timestamp}')
    mkdir_or_exist(output_path)
    timestamp = time.strftime('%Y%m%d_%H%M%S', time.localtime())
    log_file = osp.join(output_path, f'{timestamp}.log')
    logger = get_root_logger(log_file=log_file, log_level='INFO')
    logger.info('Running SBD Evaluation')
    logger.info(f'cls_dir:    \t{cls_dir}')
    logger.info(f'inst_dir:   \t{inst_dir}')
    logger.info(f'pred_suffix:\t{pred_suffix}')
    logger.info(f'categories: \t{categories}')
    logger.info(f'thresholds: \t{thresholds}')
    logger.info(f'pre-seal:   \t{pre_seal}')
    logger.info(f'thin:       \t{apply_thinning}')
    logger.info(f'nms:        \t{apply_nms}')
    logger.info(f'nonIS:      \t{nonIS}')
    logger.info(f'max_dist    \t{max_dist}')
    print('\n\n')
    evaluator = SBDEvaluator(dataset_root=sbd_path, pred_root=pred_path, cls_dir=cls_dir, inst_dir=inst_dir, pred_suffix=pred_suffix)
    if evaluator.sample_names is None:
        evaluator.set_sample_names()
    eval_mode = 'pre-seal' if pre_seal else 'post-seal'
    instance_sensitive = not nonIS
    evaluator.set_eval_params(eval_mode=eval_mode, scale=1.0, apply_thinning=apply_thinning, apply_nms=apply_nms, max_dist=max_dist, instance_sensitive=instance_sensitive)
    evaluator.evaluate(categories=categories, thresholds=thresholds, nproc=nproc, save_dir=output_path)

def evaluate_sbd():
    args = parse_args()
    apply_thinning = not args.raw
    evaluate(sbd_path=args.sbd_path, pred_path=args.pred_path, cls_dir=args.cls_dir, inst_dir=args.inst_dir, pred_suffix=args.pred_suffix, output_path=args.output_path, categories=args.categories, pre_seal=args.pre_seal, apply_thinning=apply_thinning, apply_nms=args.apply_nms, nonIS=args.nonIS, max_dist=args.max_dist, thresholds=args.thresholds, nproc=args.nproc)

def evaluate_reanno(sbd_path: str, pred_path: str, cls_dir: str, inst_dir: str, pred_suffix: str, output_path: str, categories: str, apply_thinning: bool, apply_nms: bool, nonIS: bool, thresholds: str, nproc: int):
    """Evaluate Re-annotated SBD"""
    if categories is None:
        print('use all categories')
        categories = list(range(1, len(SBDEvaluator.CLASSES) + 1))
    else:
        categories = categories.strip()
        try:
            categories = [int(categories)]
        except ValueError:
            try:
                if categories.startswith('[') and categories.endswith(']'):
                    categories = categories[1:-1]
                    categories = [int(cat.strip()) for cat in categories.split(',')]
                else:
                    print('Bad categories format; should be a python list of floats (`[a, b, c]`)')
                    return
            except ValueError:
                print('Bad categories format; should be a python list of ints (`[a, b, c]`)')
                return
    for cat in categories:
        assert 0 < cat < 21, f'category needs to be between 1 ~ 19, but got {cat}'
    thresholds = thresholds.strip()
    try:
        n_thresholds = int(thresholds)
        thresholds = n_thresholds
    except ValueError:
        try:
            if thresholds.startswith('[') and thresholds.endswith(']'):
                thresholds = thresholds[1:-1]
                thresholds = [float(t.strip()) for t in thresholds.split(',')]
            else:
                print('Bad threshold format; should be a python list of floats (`[a, b, c]`)')
                return
        except ValueError:
            print('Bad threshold format; should be a python list of ints (`[a, b, c]`)')
            return
    if output_path is None:
        timestamp = time.strftime('%Y%m%d_%H%M%S', time.localtime())
        output_path = osp.join(osp.normpath(pred_path), f'edge_results_{timestamp}')
    mkdir_or_exist(output_path)
    timestamp = time.strftime('%Y%m%d_%H%M%S', time.localtime())
    log_file = osp.join(output_path, f'{timestamp}.log')
    logger = get_root_logger(log_file=log_file, log_level='INFO')
    logger.info('Running Re-Annotated SBD Evaluation')
    logger.info(f'cls_dir:    \t{cls_dir}')
    logger.info(f'inst_dir:   \t{inst_dir}')
    logger.info(f'pred_suffix:\t{pred_suffix}')
    logger.info(f'categories: \t{categories}')
    logger.info(f'thresholds: \t{thresholds}')
    logger.info(f'thin:       \t{apply_thinning}')
    logger.info(f'nms:        \t{apply_nms}')
    logger.info(f'nonIS:      \t{nonIS}')
    print('\n\n')
    evaluator = SBDEvaluator(dataset_root=sbd_path, pred_root=pred_path, cls_dir=cls_dir, inst_dir=inst_dir, pred_suffix=pred_suffix)
    if evaluator.sample_names is None:
        evaluator.set_sample_names()
    instance_sensitive = not nonIS
    evaluator.set_eval_params(eval_mode='reanno', scale=1.0, apply_thinning=apply_thinning, apply_nms=apply_nms, max_dist=0.0075, instance_sensitive=instance_sensitive)
    evaluator.evaluate(categories=categories, thresholds=thresholds, nproc=nproc, save_dir=output_path)

def evaluate_reanno_sbd():
    args = parse_args()
    apply_thinning = not args.raw
    evaluate_reanno(sbd_path=args.sbd_path, pred_path=args.pred_path, cls_dir=args.cls_dir, inst_dir=args.inst_dir, pred_suffix=args.pred_suffix, output_path=args.output_path, categories=args.categories, apply_thinning=apply_thinning, apply_nms=args.apply_nms, nonIS=args.nonIS, max_dist=args.max_dist, thresholds=args.thresholds, nproc=args.nproc)