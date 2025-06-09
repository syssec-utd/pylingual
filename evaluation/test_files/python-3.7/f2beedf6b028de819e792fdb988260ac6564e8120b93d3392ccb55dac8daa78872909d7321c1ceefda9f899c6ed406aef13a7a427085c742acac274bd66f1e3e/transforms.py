from __future__ import annotations
import argparse
import logging as log
import os.path as osp
import random
import re
from collections import Counter
from copy import deepcopy
from enum import Enum, auto
from itertools import chain
from typing import Dict, Iterable, List, Optional, Tuple, Union
import cv2
import numpy as np
import pycocotools.mask as mask_utils
import datumaro.util.mask_tools as mask_tools
from datumaro.components.annotation import AnnotationType, Bbox, Caption, Ellipse, Label, LabelCategories, Mask, MaskCategories, Points, PointsCategories, Polygon, PolyLine, RleMask
from datumaro.components.cli_plugin import CliPlugin
from datumaro.components.dataset_base import DEFAULT_SUBSET_NAME, DatasetInfo, DatasetItem, IDataset
from datumaro.components.errors import DatumaroError
from datumaro.components.media import Image
from datumaro.components.transformer import ItemTransform, Transform
from datumaro.util import NOTSET, filter_dict, parse_str_enum_value, take_by
from datumaro.util.annotation_util import find_group_leader, find_instances

class CropCoveredSegments(ItemTransform, CliPlugin):
    """
    Sorts polygons and masks ("segments") according to `z_order`,
    crops covered areas of underlying segments. If a segment is split
    into several independent parts by the segments above, produces
    the corresponding number of separate annotations joined into a group.
    """

    def transform_item(self, item):
        annotations = []
        segments = []
        for ann in item.annotations:
            if ann.type in {AnnotationType.polygon, AnnotationType.mask}:
                segments.append(ann)
            else:
                annotations.append(ann)
        if not segments:
            return item
        if not isinstance(item.media, Image):
            raise Exception('Image info is required for this transform')
        (h, w) = item.media.size
        segments = self.crop_segments(segments, w, h)
        annotations += segments
        return self.wrap_item(item, annotations=annotations)

    @classmethod
    def crop_segments(cls, segment_anns, img_width, img_height):
        segment_anns = sorted(segment_anns, key=lambda x: x.z_order)
        segments = []
        for s in segment_anns:
            if s.type == AnnotationType.polygon:
                segments.append(s.points)
            elif s.type == AnnotationType.mask:
                if isinstance(s, RleMask):
                    rle = s.rle
                else:
                    rle = mask_tools.mask_to_rle(s.image)
                segments.append(rle)
        segments = mask_tools.crop_covered_segments(segments, img_width, img_height)
        new_anns = []
        for (ann, new_segment) in zip(segment_anns, segments):
            fields = {'z_order': ann.z_order, 'label': ann.label, 'id': ann.id, 'group': ann.group, 'attributes': ann.attributes}
            if ann.type == AnnotationType.polygon:
                if fields['group'] is None:
                    fields['group'] = cls._make_group_id(segment_anns + new_anns, fields['id'])
                for polygon in new_segment:
                    new_anns.append(Polygon(points=polygon, **fields))
            else:
                rle = mask_tools.mask_to_rle(new_segment)
                rle = mask_utils.frPyObjects(rle, *rle['size'])
                new_anns.append(RleMask(rle=rle, **fields))
        return new_anns

    @staticmethod
    def _make_group_id(anns, ann_id):
        if ann_id:
            return ann_id
        max_gid = max(anns, default=0, key=lambda x: x.group)
        return max_gid + 1

class MergeInstanceSegments(ItemTransform, CliPlugin):
    """
    Replaces instance masks and, optionally, polygons with a single mask.
    A group of annotations with the same group id is considered an "instance".
    The largest annotation in the group is considered the group "head", so the
    resulting mask takes properties from that annotation.
    """

    @classmethod
    def build_cmdline_parser(cls, **kwargs):
        parser = super().build_cmdline_parser(**kwargs)
        parser.add_argument('--include-polygons', action='store_true', help='Include polygons')
        return parser

    def __init__(self, extractor, include_polygons=False):
        super().__init__(extractor)
        self._include_polygons = include_polygons

    def transform_item(self, item):
        annotations = []
        segments = []
        for ann in item.annotations:
            if ann.type in {AnnotationType.polygon, AnnotationType.mask}:
                segments.append(ann)
            else:
                annotations.append(ann)
        if not segments:
            return item
        if not isinstance(item.media, Image):
            raise Exception('Image info is required for this transform')
        (h, w) = item.media.size
        instances = self.find_instances(segments)
        segments = [self.merge_segments(i, w, h, self._include_polygons) for i in instances]
        segments = sum(segments, [])
        annotations += segments
        return self.wrap_item(item, annotations=annotations)

    @classmethod
    def merge_segments(cls, instance, img_width, img_height, include_polygons=False):
        polygons = [a for a in instance if a.type == AnnotationType.polygon]
        masks = [a for a in instance if a.type == AnnotationType.mask]
        if not polygons and (not masks):
            return []
        if not polygons and len(masks) == 1:
            return masks
        leader = find_group_leader(polygons + masks)
        instance = []
        mask = None
        if include_polygons and polygons:
            polygons = [p.points for p in polygons]
            mask = mask_tools.rles_to_mask(polygons, img_width, img_height)
        else:
            instance += polygons
        if masks:
            masks = (m.image for m in masks)
            if mask is not None:
                masks = chain(masks, [mask])
            mask = mask_tools.merge_masks(masks)
        if mask is None:
            return instance
        mask = mask_tools.mask_to_rle(mask)
        mask = mask_utils.frPyObjects(mask, *mask['size'])
        instance.append(RleMask(rle=mask, label=leader.label, z_order=leader.z_order, id=leader.id, attributes=leader.attributes, group=leader.group))
        return instance

    @staticmethod
    def find_instances(annotations):
        return find_instances((a for a in annotations if a.type in {AnnotationType.polygon, AnnotationType.mask}))

class PolygonsToMasks(ItemTransform, CliPlugin):
    _allowed_types = {AnnotationType.polygon, AnnotationType.ellipse}

    def transform_item(self, item):
        annotations = []
        for ann in item.annotations:
            if ann.type in self._allowed_types:
                if not isinstance(item.media, Image):
                    raise Exception('Image info is required for this transform')
                (h, w) = item.media.size
                annotations.append(self.convert_polygon(ann, h, w))
            else:
                annotations.append(ann)
        return self.wrap_item(item, annotations=annotations)

    @staticmethod
    def convert_polygon(polygon: Union[Polygon, Ellipse], img_h, img_w):
        rle = mask_utils.frPyObjects([polygon.as_polygon()], img_h, img_w)[0]
        return RleMask(rle=rle, label=polygon.label, z_order=polygon.z_order, id=polygon.id, attributes=polygon.attributes, group=polygon.group)

class BoxesToMasks(ItemTransform, CliPlugin):

    def transform_item(self, item):
        annotations = []
        for ann in item.annotations:
            if ann.type == AnnotationType.bbox:
                if not isinstance(item.media, Image):
                    raise Exception('Image info is required for this transform')
                (h, w) = item.media.size
                annotations.append(self.convert_bbox(ann, h, w))
            else:
                annotations.append(ann)
        return self.wrap_item(item, annotations=annotations)

    @staticmethod
    def convert_bbox(bbox, img_h, img_w):
        rle = mask_utils.frPyObjects([bbox.as_polygon()], img_h, img_w)[0]
        return RleMask(rle=rle, label=bbox.label, z_order=bbox.z_order, id=bbox.id, attributes=bbox.attributes, group=bbox.group)

class MasksToPolygons(ItemTransform, CliPlugin):

    def transform_item(self, item):
        annotations = []
        for ann in item.annotations:
            if ann.type == AnnotationType.mask:
                polygons = self.convert_mask(ann)
                if not polygons:
                    log.debug('[%s]: item %s: Mask conversion to polygons resulted in too small polygons, which were discarded' % (self.NAME, item.id))
                annotations.extend(polygons)
            else:
                annotations.append(ann)
        return self.wrap_item(item, annotations=annotations)

    @staticmethod
    def convert_mask(mask):
        polygons = mask_tools.mask_to_polygons(mask.image)
        return [Polygon(points=p, label=mask.label, z_order=mask.z_order, id=mask.id, attributes=mask.attributes, group=mask.group) for p in polygons]

class ShapesToBoxes(ItemTransform, CliPlugin):

    def transform_item(self, item):
        annotations = []
        for ann in item.annotations:
            if ann.type in {AnnotationType.mask, AnnotationType.polygon, AnnotationType.polyline, AnnotationType.points}:
                annotations.append(self.convert_shape(ann))
            else:
                annotations.append(ann)
        return self.wrap_item(item, annotations=annotations)

    @staticmethod
    def convert_shape(shape):
        bbox = shape.get_bbox()
        return Bbox(*bbox, label=shape.label, z_order=shape.z_order, id=shape.id, attributes=shape.attributes, group=shape.group)

class Reindex(Transform, CliPlugin):
    """
    Replaces dataset item IDs with sequential indices.
    """

    @classmethod
    def build_cmdline_parser(cls, **kwargs):
        parser = super().build_cmdline_parser(**kwargs)
        parser.add_argument('-s', '--start', type=int, default=1, help='Start value for item ids')
        return parser

    def __init__(self, extractor, start=1):
        super().__init__(extractor)
        self._length = 'parent'
        self._start = start

    def __iter__(self):
        for (i, item) in enumerate(self._extractor):
            yield self.wrap_item(item, id=i + self._start)

class MapSubsets(ItemTransform, CliPlugin):
    """
    Renames subsets in the dataset.
    """

    @staticmethod
    def _mapping_arg(s):
        parts = s.split(':')
        if len(parts) != 2:
            raise argparse.ArgumentTypeError()
        return parts

    @classmethod
    def build_cmdline_parser(cls, **kwargs):
        parser = super().build_cmdline_parser(**kwargs)
        parser.add_argument('-s', '--subset', action='append', type=cls._mapping_arg, dest='mapping', help="Subset mapping of the form: 'src:dst' (repeatable)")
        return parser

    def __init__(self, extractor, mapping=None):
        super().__init__(extractor)
        if mapping is None:
            mapping = {}
        elif not isinstance(mapping, dict):
            mapping = dict((tuple(m) for m in mapping))
        self._mapping = mapping
        if extractor.subsets():
            counts = Counter((mapping.get(s, s) or DEFAULT_SUBSET_NAME for s in extractor.subsets()))
            if all((c == 1 for c in counts.values())):
                self._length = 'parent'
            self._subsets = set(counts)

    def transform_item(self, item):
        return self.wrap_item(item, subset=self._mapping.get(item.subset, item.subset))

class RandomSplit(Transform, CliPlugin):
    """
    Joins all subsets into one and splits the result into few parts.
    It is expected that item ids are unique and subset ratios sum up to 1.|n
    |n
    Example:|n

    .. code-block::

    |s|s|s|s%(prog)s --subset train:.67 --subset test:.33
    """
    _default_split = [('train', 0.67), ('test', 0.33)]

    @staticmethod
    def _split_arg(s):
        parts = s.split(':')
        if len(parts) != 2:
            raise argparse.ArgumentTypeError()
        return (parts[0], float(parts[1]))

    @classmethod
    def build_cmdline_parser(cls, **kwargs):
        parser = super().build_cmdline_parser(**kwargs)
        parser.add_argument('-s', '--subset', action='append', type=cls._split_arg, dest='splits', help="Subsets in the form: '<subset>:<ratio>' (repeatable, default: %s)" % dict(cls._default_split))
        parser.add_argument('--seed', type=int, help='Random seed')
        return parser

    def __init__(self, extractor, splits, seed=None):
        super().__init__(extractor)
        if splits is None:
            splits = self._default_split
        assert 0 < len(splits), 'Expected at least one split'
        assert all((0.0 <= r and r <= 1.0 for (_, r) in splits)), 'Ratios are expected to be in the range [0; 1], but got %s' % splits
        total_ratio = sum((s[1] for s in splits))
        if not abs(total_ratio - 1.0) <= 1e-07:
            raise Exception('Sum of ratios is expected to be 1, got %s, which is %s' % (splits, total_ratio))
        dataset_size = len(extractor)
        indices = list(range(dataset_size))
        random.seed(seed)
        random.shuffle(indices)
        parts = []
        s = 0
        lower_boundary = 0
        for (split_idx, (subset, ratio)) in enumerate(splits):
            s += ratio
            upper_boundary = int(s * dataset_size)
            if split_idx == len(splits) - 1:
                upper_boundary = dataset_size
            subset_indices = set(indices[lower_boundary:upper_boundary])
            parts.append((subset_indices, subset))
            lower_boundary = upper_boundary
        self._parts = parts
        self._subsets = set((s[0] for s in splits))
        self._length = 'parent'

    def _find_split(self, index):
        for (subset_indices, subset) in self._parts:
            if index in subset_indices:
                return subset
        return subset

    def __iter__(self):
        for (i, item) in enumerate(self._extractor):
            yield self.wrap_item(item, subset=self._find_split(i))

class IdFromImageName(ItemTransform, CliPlugin):
    """
    Renames items in the dataset using image file name (without extension).
    """

    def transform_item(self, item):
        if isinstance(item.media, Image) and item.media.path:
            name = osp.splitext(osp.basename(item.media.path))[0]
            return self.wrap_item(item, id=name)
        else:
            log.debug("Can't change item id for item '%s': item has no image info" % item.id)
            return item

class Rename(ItemTransform, CliPlugin):
    """
    Renames items in the dataset. Supports regular expressions.
    The first character in the expression is a delimiter for
    the pattern and replacement parts. Replacement part can also
    contain `str.format` replacement fields with the `item`
    (of type `DatasetItem`) object available.|n
    Please use doulbe quotes to represent regex.|n
    |n
    Examples:|n
    |s|s- Replace 'pattern' with 'replacement':|n

      .. code-block::

    |s|s|s|srename -e "|pattern|replacement|"|n
    |n
    |s|s- Remove 'frame_' from item ids:|n

      .. code-block::

    |s|s|s|srename -e "|^frame_||"|n
    |n
    |s|s- Rename by regex:|n

      .. code-block::

    |s|s|s|srename -e "|frame_(\\d+)_extra|{item.subset}_id_\\1|"
    """

    @classmethod
    def build_cmdline_parser(cls, **kwargs):
        parser = super().build_cmdline_parser(**kwargs)
        parser.add_argument('-e', '--regex', help="Regex for renaming in the form '<sep><search><sep><replacement><sep>'")
        return parser

    def __init__(self, extractor, regex):
        super().__init__(extractor)
        assert regex and isinstance(regex, str)
        parts = regex.split(regex[0], maxsplit=3)
        (regex, sub) = parts[1:3]
        self._re = re.compile(regex)
        self._sub = sub

    def transform_item(self, item):
        return self.wrap_item(item, id=self._re.sub(self._sub, item.id).format(item=item))

class RemapLabels(ItemTransform, CliPlugin):
    """
    Changes labels in the dataset.|n
    |n
    A label can be:|n
    |s|s- renamed (and joined with existing) -|n
    |s|s|s|swhen '--label <old_name>:<new_name>' is specified|n
    |s|s- deleted - when '--label <name>:' is specified, or default action |n
    |s|s|s|sis 'delete' and the label is not mentioned in the list. |n
    |s|s|s|sWhen a label is deleted, all the associated annotations are removed|n
    |s|s- kept unchanged - when specified '--label <name>:<name>'|n
    |s|s|s|sor default action is 'keep' and the label is not mentioned in the list.|n
    |n
    Annotations with no label are managed by the default action policy.|n
    |n
    Examples:|n
    |n
    |s|s- Remove the 'person' label (and corresponding annotations):|n

    |s|s.. code-block::

    |s|s|s|s%(prog)s -l person: --default keep|n
    |n
    |s|s- Rename 'person' to 'pedestrian' and 'human' to 'pedestrian', join:|n

    |s|s.. code-block::

    |s|s|s|s%(prog)s -l person:pedestrian -l human:pedestrian --default keep|n
    |n
    |s|s- Rename 'person' to 'car' and 'cat' to 'dog', keep 'bus', remove others:|n

    |s|s.. code-block::

    |s|s|s|s%(prog)s -l person:car -l bus:bus -l cat:dog --default delete
    """

    class DefaultAction(Enum):
        keep = auto()
        delete = auto()

    @staticmethod
    def _split_arg(s):
        parts = s.split(':')
        if len(parts) != 2:
            raise argparse.ArgumentTypeError()
        return (parts[0], parts[1])

    @classmethod
    def build_cmdline_parser(cls, **kwargs):
        parser = super().build_cmdline_parser(**kwargs)
        parser.add_argument('-l', '--label', action='append', type=cls._split_arg, dest='mapping', help="Label in the form of: '<src>:<dst>' (repeatable)")
        parser.add_argument('--default', choices=[a.name for a in cls.DefaultAction], default=cls.DefaultAction.keep.name, help='Action for unspecified labels (default: %(default)s)')
        return parser

    def __init__(self, extractor: IDataset, mapping: Union[Dict[str, str], List[Tuple[str, str]]], default: Union[None, str, DefaultAction]=None):
        super().__init__(extractor)
        default = parse_str_enum_value(default, self.DefaultAction, self.DefaultAction.keep)
        self._default_action = default
        assert isinstance(mapping, (dict, list))
        if isinstance(mapping, list):
            mapping = dict(mapping)
        self._categories = {}
        src_categories = self._extractor.categories()
        src_label_cat = src_categories.get(AnnotationType.label)
        if src_label_cat is not None:
            self._make_label_id_map(src_label_cat, mapping, default)
        src_mask_cat = src_categories.get(AnnotationType.mask)
        if src_mask_cat is not None:
            assert src_label_cat is not None
            dst_mask_cat = MaskCategories(attributes=deepcopy(src_mask_cat.attributes))
            for (old_id, old_color) in src_mask_cat.colormap.items():
                new_id = self._map_id(old_id)
                if new_id is not None and new_id not in dst_mask_cat:
                    dst_mask_cat.colormap[new_id] = deepcopy(old_color)
            self._categories[AnnotationType.mask] = dst_mask_cat
        src_point_cat = src_categories.get(AnnotationType.points)
        if src_point_cat is not None:
            assert src_label_cat is not None
            dst_point_cat = PointsCategories(attributes=deepcopy(src_point_cat.attributes))
            for (old_id, old_cat) in src_point_cat.items.items():
                new_id = self._map_id(old_id)
                if new_id is not None and new_id not in dst_point_cat:
                    dst_point_cat.items[new_id] = deepcopy(old_cat)
            self._categories[AnnotationType.points] = dst_point_cat
        assert len(self._categories) == len(src_categories)

    def _make_label_id_map(self, src_label_cat, label_mapping, default_action):
        dst_label_cat = LabelCategories(attributes=deepcopy(src_label_cat.attributes))
        id_mapping = {}
        for (src_index, src_label) in enumerate(src_label_cat.items):
            dst_label = label_mapping.get(src_label.name, NOTSET)
            if dst_label is NOTSET and default_action == self.DefaultAction.keep:
                dst_label = src_label.name
            elif not dst_label or dst_label is NOTSET:
                continue
            dst_index = dst_label_cat.find(dst_label)[0]
            if dst_index is None:
                dst_index = dst_label_cat.add(dst_label, src_label.parent, deepcopy(src_label.attributes))
            id_mapping[src_index] = dst_index
        if log.getLogger().isEnabledFor(log.DEBUG):
            log.debug('Label mapping:')
            for (src_id, src_label) in enumerate(src_label_cat.items):
                if id_mapping.get(src_id) is not None:
                    log.debug("#%s '%s' -> #%s '%s'", src_id, src_label.name, id_mapping[src_id], dst_label_cat.items[id_mapping[src_id]].name)
                else:
                    log.debug("#%s '%s' -> <deleted>", src_id, src_label.name)
        self._map_id = lambda src_id: id_mapping.get(src_id, None)
        for label in dst_label_cat:
            if label.parent not in dst_label_cat:
                label.parent = ''
        self._categories[AnnotationType.label] = dst_label_cat

    def categories(self):
        return self._categories

    def transform_item(self, item):
        annotations = []
        for ann in item.annotations:
            if getattr(ann, 'label', None) is not None:
                conv_label = self._map_id(ann.label)
                if conv_label is not None:
                    annotations.append(ann.wrap(label=conv_label))
            elif self._default_action is self.DefaultAction.keep:
                annotations.append(ann.wrap())
        return item.wrap(annotations=annotations)

class ProjectInfos(Transform, CliPlugin):
    """
    Changes the content of infos.
    A user can add meta-data of dataset such as author, comments, or related papers.
    Infos values are not affect on the dataset structure.
    We thus can add any meta-data freely.
    """

    @classmethod
    def build_cmdline_parser(cls, **kwargs):
        parser = super().build_cmdline_parser(**kwargs)
        parser.add_argument('-i', '--infos', action='append', dest='dst_infos', help='A dictionary of the dataset meta-information')
        parser.add_argument('-o', '--overwrite', action='store_true', dest='overwrite', help='Overwrite the infos of src if True')
        return parser

    def __init__(self, extractor: IDataset, dst_infos: DatasetInfo, overwrite: bool=False):
        super().__init__(extractor)
        if overwrite:
            self._infos = dst_infos
        else:
            self._infos = deepcopy(extractor.infos())
            for (k, v) in dst_infos.items():
                self._infos[k] = v

    def __iter__(self):
        for item in self._extractor:
            if item is not None:
                yield item

    def infos(self):
        return self._infos

class ProjectLabels(ItemTransform):
    """
    Changes the order of labels in the dataset from the existing
    to the desired one, removes unknown labels and adds new labels.
    Updates or removes the corresponding annotations.|n
    |n
    Labels are matched by names (case dependent). Parent labels are only kept
    if they are present in the resulting set of labels. If new labels are
    added, and the dataset has mask colors defined, new labels will obtain
    generated colors.|n
    |n
    Useful for merging similar datasets, whose labels need to be aligned.|n
    |n
    Examples:|n
    |s|s- Align the source dataset labels to [person, cat, dog]:|n

    |s|s.. code-block::

    |s|s|s|s%(prog)s -l person -l cat -l dog
    """

    @classmethod
    def build_cmdline_parser(cls, **kwargs):
        parser = super().build_cmdline_parser(**kwargs)
        parser.add_argument('-l', '--label', action='append', dest='dst_labels', help='Label name (repeatable, ordered)')
        return parser

    def __init__(self, extractor: IDataset, dst_labels: Union[Iterable[str], LabelCategories]):
        super().__init__(extractor)
        self._categories = {}
        src_categories = self._extractor.categories()
        src_label_cat = src_categories.get(AnnotationType.label)
        if isinstance(dst_labels, LabelCategories):
            dst_label_cat = deepcopy(dst_labels)
        else:
            dst_labels = list(dst_labels)
            if src_label_cat:
                dst_label_cat = LabelCategories(attributes=deepcopy(src_label_cat.attributes))
                for dst_label in dst_labels:
                    assert isinstance(dst_label, str)
                    src_label = src_label_cat.find(dst_label)[1]
                    if src_label is not None:
                        dst_label_cat.add(dst_label, src_label.parent, deepcopy(src_label.attributes))
                    else:
                        dst_label_cat.add(dst_label)
            else:
                dst_label_cat = LabelCategories.from_iterable(dst_labels)
        for label in dst_label_cat:
            if label.parent not in dst_label_cat:
                label.parent = ''
        self._categories[AnnotationType.label] = dst_label_cat
        self._make_label_id_map(src_label_cat, dst_label_cat)
        src_mask_cat = src_categories.get(AnnotationType.mask)
        if src_mask_cat is not None:
            assert src_label_cat is not None
            dst_mask_cat = MaskCategories(attributes=deepcopy(src_mask_cat.attributes))
            for (old_id, old_color) in src_mask_cat.colormap.items():
                new_id = self._map_id(old_id)
                if new_id is not None and new_id not in dst_mask_cat:
                    dst_mask_cat.colormap[new_id] = deepcopy(old_color)
            existing_colors = set(dst_mask_cat.colormap.values())
            color_bank = iter(mask_tools.generate_colormap(len(dst_label_cat), include_background=False).values())
            for (new_id, new_label) in enumerate(dst_label_cat):
                if new_label.name in src_label_cat:
                    continue
                if new_id in dst_mask_cat:
                    continue
                color = next(color_bank)
                while color in existing_colors:
                    color = next(color_bank)
                dst_mask_cat.colormap[new_id] = color
            self._categories[AnnotationType.mask] = dst_mask_cat
        src_point_cat = src_categories.get(AnnotationType.points)
        if src_point_cat is not None:
            assert src_label_cat is not None
            dst_point_cat = PointsCategories(attributes=deepcopy(src_point_cat.attributes))
            for (old_id, old_cat) in src_point_cat.items.items():
                new_id = self._map_id(old_id)
                if new_id is not None and new_id not in dst_point_cat:
                    dst_point_cat.items[new_id] = deepcopy(old_cat)
            self._categories[AnnotationType.points] = dst_point_cat

    def _make_label_id_map(self, src_label_cat, dst_label_cat):
        id_mapping = {src_id: dst_label_cat.find(src_label_cat[src_id].name)[0] for src_id in range(len(src_label_cat or ()))}
        self._map_id = lambda src_id: id_mapping.get(src_id, None)

    def categories(self):
        return self._categories

    def transform_item(self, item):
        annotations = []
        for ann in item.annotations:
            if getattr(ann, 'label', None) is not None:
                conv_label = self._map_id(ann.label)
                if conv_label is not None:
                    annotations.append(ann.wrap(label=conv_label))
            else:
                annotations.append(ann.wrap())
        return item.wrap(annotations=annotations)

class AnnsToLabels(ItemTransform, CliPlugin):
    """
    Collects all labels from annotations (of all types) and
    transforms them into a set of annotations of type Label
    """

    def transform_item(self, item):
        labels = set((p.label for p in item.annotations if getattr(p, 'label') is not None))
        annotations = []
        for label in labels:
            annotations.append(Label(label=label))
        return item.wrap(annotations=annotations)

class BboxValuesDecrement(ItemTransform, CliPlugin):
    """
    Subtracts one from the coordinates of bounding boxes
    """

    def transform_item(self, item):
        annotations = [p for p in item.annotations if p.type != AnnotationType.bbox]
        bboxes = [p for p in item.annotations if p.type == AnnotationType.bbox]
        for bbox in bboxes:
            annotations.append(Bbox(bbox.x - 1, bbox.y - 1, bbox.w, bbox.h, label=bbox.label, attributes=bbox.attributes))
        return item.wrap(annotations=annotations)

class ResizeTransform(ItemTransform):
    """
    Resizes images and annotations in the dataset to the specified size.
    Supports upscaling, downscaling and mixed variants.|n
    |n
    Examples:|n
        - Resize all images to 256x256 size|n

        .. code-block::

        |s|s%(prog)s -dw 256 -dh 256
    """

    @classmethod
    def build_cmdline_parser(cls, **kwargs):
        parser = super().build_cmdline_parser(**kwargs)
        parser.add_argument('-dw', '--width', type=int, help='Destination image width')
        parser.add_argument('-dh', '--height', type=int, help='Destination image height')
        return parser

    def __init__(self, extractor: IDataset, width: int, height: int) -> None:
        super().__init__(extractor)
        assert width > 0 and height > 0
        self._width = width
        self._height = height

    @staticmethod
    def _lazy_resize_image(image, new_size):

        def _resize_image(_):
            (h, w) = image.size
            yscale = new_size[0] / float(h)
            xscale = new_size[1] / float(w)
            method = cv2.INTER_AREA if xscale * yscale < 1 else cv2.INTER_CUBIC
            resized_image = cv2.resize(image.data / 255.0, new_size[::-1], interpolation=method)
            resized_image *= 255.0
            return resized_image
        return Image(_resize_image, ext=image.ext, size=new_size)

    @staticmethod
    def _lazy_resize_mask(mask, new_size):

        def _resize_image():
            rescaled_mask = cv2.resize(mask.image.astype(np.float32), new_size[::-1], interpolation=cv2.INTER_NEAREST)
            return rescaled_mask.astype(np.uint8)
        return _resize_image

    def transform_item(self, item):
        if not isinstance(item.media, Image):
            raise DatumaroError('Item %s: image info is required for this transform' % (item.id,))
        (h, w) = item.media.size
        xscale = self._width / float(w)
        yscale = self._height / float(h)
        new_size = (self._height, self._width)
        resized_image = None
        if item.media.has_data:
            resized_image = self._lazy_resize_image(item.media, new_size)
        resized_annotations = []
        for ann in item.annotations:
            if isinstance(ann, Bbox):
                resized_annotations.append(ann.wrap(x=ann.x * xscale, y=ann.y * yscale, w=ann.w * xscale, h=ann.h * yscale))
            elif isinstance(ann, (Polygon, Points, PolyLine)):
                resized_annotations.append(ann.wrap(points=[p for t in ((x * xscale, y * yscale) for (x, y) in take_by(ann.points, 2)) for p in t]))
            elif isinstance(ann, Mask):
                rescaled_mask = self._lazy_resize_mask(ann, new_size)
                resized_annotations.append(ann.wrap(image=rescaled_mask))
            elif isinstance(ann, (Caption, Label)):
                resized_annotations.append(ann)
            else:
                assert False, f'Unexpected annotation type {type(ann)}'
        return self.wrap_item(item, media=resized_image, annotations=resized_annotations)

class RemoveItems(ItemTransform):
    """
    Allows to remove specific dataset items from dataset by their ids.|n
    |n
    Can be useful to clean the dataset from broken or unnecessary samples.|n
    |n
    Examples:|n
        - Remove specific items from the dataset|n

        .. code-block::

        |s|s%(prog)s --id 'image1:train' --id 'image2:test'
    """

    @staticmethod
    def _parse_id(s):
        full_id = s.split(':')
        if len(full_id) != 2:
            raise argparse.ArgumentTypeError(None, message="Invalid id format of '%s'. Expected a 'name:subset' pair." % s)
        return full_id

    @classmethod
    def build_cmdline_parser(cls, **kwargs):
        parser = super().build_cmdline_parser(**kwargs)
        parser.add_argument('--id', dest='ids', type=cls._parse_id, action='append', required=True, help="Item id to remove. Id is 'name:subset' pair (repeatable)")
        return parser

    def __init__(self, extractor: IDataset, ids: Iterable[Tuple[str, str]]):
        super().__init__(extractor)
        self._ids = set((tuple(v) for v in ids or []))

    def transform_item(self, item):
        if (item.id, item.subset) in self._ids:
            return None
        return item

class RemoveAnnotations(ItemTransform):
    """
    Allows to remove annotations on specific dataset items.|n
    |n
    Can be useful to clean the dataset from broken or unnecessary annotations.|n
    |n
    Examples:|n
        - Remove annotations from specific items in the dataset|n

        .. code-block::

        |s|s%(prog)s --id 'image1:train' --id 'image2:test'
    """

    @staticmethod
    def _parse_id(s):
        full_id = s.split(':')
        if len(full_id) != 2:
            raise argparse.ArgumentTypeError(None, message="Invalid id format of '%s'. Expected a 'name:subset' pair." % s)
        return full_id

    @classmethod
    def build_cmdline_parser(cls, **kwargs):
        parser = super().build_cmdline_parser(**kwargs)
        parser.add_argument('--id', dest='ids', type=cls._parse_id, action='append', help="Image id to clean from annotations. Id is 'name:subset' pair. If not specified, removes all annotations (repeatable)")
        return parser

    def __init__(self, extractor: IDataset, *, ids: Optional[Iterable[Tuple[str, str]]]=None):
        super().__init__(extractor)
        self._ids = set((tuple(v) for v in ids or []))

    def transform_item(self, item: DatasetItem):
        if not self._ids or (item.id, item.subset) in self._ids:
            return item.wrap(annotations=[])
        return item

class RemoveAttributes(ItemTransform):
    """
    Allows to remove item and annotation attributes in a dataset.|n
    |n
    Can be useful to clean the dataset from broken or unnecessary attributes.|n
    |n
    Examples:|n
        - Remove the `is_crowd` attribute from dataset|n

        .. code-block::

        |s|s%(prog)s --attr 'is_crowd'|n
        |n
        - Remove the `occluded` attribute from annotations of|n
        |s|sthe `2010_001705` item in the `train` subset|n

        .. code-block::

        |s|s%(prog)s --id '2010_001705:train' --attr 'occluded'
    """

    @staticmethod
    def _parse_id(s):
        full_id = s.split(':')
        if len(full_id) != 2:
            raise argparse.ArgumentTypeError(None, message="Invalid id format of '%s'. Expected a 'name:subset' pair." % s)
        return full_id

    @classmethod
    def build_cmdline_parser(cls, **kwargs):
        parser = super().build_cmdline_parser(**kwargs)
        parser.add_argument('--id', dest='ids', type=cls._parse_id, action='append', help="Image id to clean from annotations. Id is 'name:subset' pair. If not specified, affects all images and annotations (repeatable)")
        parser.add_argument('-a', '--attr', action='append', dest='attributes', help='Attribute name to be removed. If not specified, removes all attributes (repeatable)')
        return parser

    def __init__(self, extractor: IDataset, ids: Optional[Iterable[Tuple[str, str]]]=None, attributes: Optional[Iterable[str]]=None):
        super().__init__(extractor)
        self._ids = set((tuple(v) for v in ids or []))
        self._attributes = set(attributes or [])

    def _filter_attrs(self, attrs):
        if not self._attributes:
            return None
        else:
            return filter_dict(attrs, exclude_keys=self._attributes)

    def transform_item(self, item: DatasetItem):
        if not self._ids or (item.id, item.subset) in self._ids:
            filtered_annotations = []
            for ann in item.annotations:
                filtered_annotations.append(ann.wrap(attributes=self._filter_attrs(ann.attributes)))
            return item.wrap(attributes=self._filter_attrs(item.attributes), annotations=filtered_annotations)
        return item