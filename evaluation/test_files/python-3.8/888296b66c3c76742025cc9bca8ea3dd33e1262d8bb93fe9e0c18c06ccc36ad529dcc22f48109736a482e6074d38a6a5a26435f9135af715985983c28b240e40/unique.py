import shutil
import sys
from pathlib import Path
import fiftyone as fo
import fiftyone.brain as fob

def best_group_size(n_total, group_size):
    if n_total <= group_size:
        return n_total
    (a, b) = divmod(n_total, group_size)
    (c, d) = divmod(b, a)
    group_size = group_size + c
    if d > 0:
        group_size = group_size + 1
    return group_size

def find_unique(export_dir, dataset_dir, count=1, model=None):
    dataset = fo.Dataset.from_dir(dataset_dir=dataset_dir, dataset_type=fo.types.ImageDirectory)
    results = fob.compute_similarity(dataset, brain_key='img_sim', model=model)
    results.find_unique(count)
    unique_ids = results.unique_ids
    unique_view = dataset.select(unique_ids)
    shutil.rmtree(export_dir, ignore_errors=True)
    unique_view.export(export_dir=(Path(export_dir) / 'data').as_posix(), dataset_type=fo.types.ImageDirectory)
    return (len(unique_view), len(dataset))

def find_unique2(export_dir, dataset_dir, count=1, model=None, group_size=1000):
    dataset = fo.Dataset.from_images_dir(dataset_dir)
    sorted_view = dataset.sort_by('filepath')
    n_total = len(sorted_view)
    group_size = best_group_size(n_total, group_size)
    print(f'[INFO] total: {n_total}, group size: {group_size}')
    unique_ids = set()
    for skip in range(0, n_total, group_size):
        sliced_sorted_view = sorted_view.skip(skip).limit(group_size)
        results = fob.compute_similarity(sliced_sorted_view, brain_key='img_sim', model=model)
        results.find_unique(count)
        unique_ids.update(results.unique_ids)
    unique_view = dataset.select(unique_ids)
    shutil.rmtree(export_dir, ignore_errors=True)
    unique_view.export(export_dir=(Path(export_dir) / 'data').as_posix(), dataset_type=fo.types.ImageDirectory)
    return (len(unique_view), len(dataset))

def func(export_dir, dataset_dir, function, count, model, group_size):
    if function == 'unique':
        if group_size is None:
            (n_unique, n_total) = find_unique(export_dir, dataset_dir, count, model)
            print(f'kept: {n_unique}, total: {n_total}')
        else:
            (n_unique, n_total) = find_unique2(export_dir, dataset_dir, count, model, group_size)
            print(f'kept: {n_unique}, total: {n_total}')
    elif function == 'duplicate':
        raise NotImplementedError
    else:
        raise NotImplementedError
    return '\n[END]'

def parse_args(args=None):
    from argparse import ArgumentDefaultsHelpFormatter, ArgumentParser
    parser = ArgumentParser(formatter_class=ArgumentDefaultsHelpFormatter)
    parser.add_argument('export_dir', type=str, help='a directory')
    parser.add_argument('dataset_dir', type=str, help='the dataset directory')
    parser.add_argument('-f', dest='function', type=str, default='unique', choices=['unique', 'duplicate'])
    parser.add_argument('-n', dest='count', type=int, default=1, help='the desired number of unique examples')
    parser.add_argument('-m', dest='model', type=str, default='resnet50-imagenet-torch', help='a fiftyone.core.models.Model or the name')
    parser.add_argument('-g', dest='group_size', type=int, default=None, help='compute similarity by group')
    args = parser.parse_args(args=args)
    return vars(args)

def main(args=None):
    kwargs = parse_args(args)
    print(f'{__file__}: {kwargs}')
    print(func(**kwargs))
    return 0
if __name__ == '__main__':
    sys.exit(main())