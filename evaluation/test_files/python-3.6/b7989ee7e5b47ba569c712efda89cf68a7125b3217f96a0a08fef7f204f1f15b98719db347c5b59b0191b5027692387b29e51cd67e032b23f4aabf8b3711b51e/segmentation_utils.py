"""This module implements segmentation related utilities."""
import warnings
from copy import copy
from typing import List, Optional, Sequence, Tuple, cast
import cv2
import numpy as np
from bson import ObjectId
from otx.api.entities.annotation import Annotation
from otx.api.entities.dataset_item import DatasetItemEntity
from otx.api.entities.id import ID
from otx.api.entities.label import LabelEntity
from otx.api.entities.scored_label import ScoredLabel
from otx.api.entities.shapes.polygon import Point, Polygon
from otx.api.utils.shape_factory import ShapeFactory

def mask_from_dataset_item(dataset_item: DatasetItemEntity, labels: List[LabelEntity]) -> np.ndarray:
    """Creates a mask from dataset item.

    The mask will be two dimensional, and the value of each pixel matches the class index with offset 1. The background
    class index is zero. labels[0] matches pixel value 1, etc. The class index is
    determined based on the order of 'labels'.

    Args:
        dataset_item: Item to make mask for
        labels: The labels to use for creating the mask. The order of
            the labels determines the class index.

    Returns:
        Numpy array of mask
    """
    mask = mask_from_annotation(dataset_item.get_annotations(), labels, dataset_item.width, dataset_item.height)
    return mask

def mask_from_annotation(annotations: List[Annotation], labels: List[LabelEntity], width: int, height: int) -> np.ndarray:
    """Generate a segmentation mask of a numpy image, and a list of shapes.

    The mask is will be two dimensional and the value of each pixel matches the class
    index with offset 1. The background class index is zero. labels[0] matches pixel
    value 1, etc. The class index is determined based on the order of `labels`:

    Args:
        annotations: List of annotations to plot in mask
        labels: List of labels. The index position of the label
            determines the class number in the segmentation mask.
        width: Width of the mask
        height: Height of the mask

    Returns:
        2d numpy array of mask
    """
    labels = sorted(labels)
    mask = np.zeros(shape=(height, width), dtype=np.uint8)
    for annotation in annotations:
        shape = annotation.shape
        if not isinstance(shape, Polygon):
            shape = ShapeFactory.shape_as_polygon(annotation.shape)
        known_labels = [label for label in annotation.get_labels() if isinstance(label, ScoredLabel) and label.get_label() in labels]
        if len(known_labels) == 0:
            continue
        label_to_compare = known_labels[0].get_label()
        class_idx = labels.index(label_to_compare) + 1
        contour = []
        for point in shape.points:
            contour.append([int(point.x * width), int(point.y * height)])
        mask = cv2.drawContours(mask, np.asarray([contour]), 0, (class_idx, class_idx, class_idx), -1)
    mask = np.expand_dims(mask, axis=2)
    return mask

def create_hard_prediction_from_soft_prediction(soft_prediction: np.ndarray, soft_threshold: float, blur_strength: int=5) -> np.ndarray:
    """Creates a hard prediction containing the final label index per pixel.

    Args:
        soft_prediction: Output from segmentation network. Assumes
            floating point values, between 0.0 and 1.0. Can be a
            2d-array of shape (height, width) or per-class segmentation
            logits of shape (height, width, num_classes)
        soft_threshold: minimum class confidence for each pixel. The
            higher the value, the more strict the segmentation is
            (usually set to 0.5)
        blur_strength: The higher the value, the smoother the
            segmentation output will be, but less accurate

    Returns:
        Numpy array of the hard prediction
    """
    soft_prediction_blurred = cv2.blur(soft_prediction, (blur_strength, blur_strength))
    if len(soft_prediction.shape) == 3:
        soft_prediction_blurred[soft_prediction_blurred < soft_threshold] = 0
        hard_prediction = np.argmax(soft_prediction_blurred, axis=2)
    elif len(soft_prediction.shape) == 2:
        hard_prediction = soft_prediction_blurred > soft_threshold
    else:
        raise ValueError(f'Invalid prediction input of shape {soft_prediction.shape}. Expected either a 2D or 3D array.')
    return hard_prediction
Contour = List[Tuple[float, float]]

def get_subcontours(contour: Contour) -> List[Contour]:
    """Splits contour into subcontours that do not have self intersections."""
    ContourInternal = List[Optional[Tuple[float, float]]]

    def find_loops(points: ContourInternal) -> List[Sequence[int]]:
        """For each consecutive pair of equivalent rows in the input matrix returns their indices."""
        (_, inverse, count) = np.unique(points, axis=0, return_inverse=True, return_counts=True)
        duplicates = np.where(count > 1)[0]
        indices = []
        for x in duplicates:
            y = np.nonzero(inverse == x)[0]
            for (i, _) in enumerate(y[:-1]):
                indices.append(y[i:i + 2])
        return indices
    base_contour = cast(ContourInternal, copy(contour))
    if not np.array_equal(base_contour[0], base_contour[-1]):
        base_contour.append(base_contour[0])
    subcontours: List[Contour] = []
    loops = sorted(find_loops(base_contour), key=lambda x: x[0], reverse=True)
    for loop in loops:
        (i, j) = loop
        subcontour = base_contour[i:j]
        subcontour = list((x for x in subcontour if x is not None))
        subcontours.append(cast(Contour, subcontour))
        base_contour[i:j] = [None] * (j - i)
    subcontours = [i for i in subcontours if len(i) > 2]
    return subcontours

def create_annotation_from_segmentation_map(hard_prediction: np.ndarray, soft_prediction: np.ndarray, label_map: dict) -> List[Annotation]:
    """Creates polygons from the soft predictions.

    Background label will be ignored and not be converted to polygons.

    Args:
        hard_prediction: hard prediction containing the final label
            index per pixel. See function
            `create_hard_prediction_from_soft_prediction`.
        soft_prediction: soft prediction with shape H x W x N_labels,
            where soft_prediction[:, :, 0] is the soft prediction for
            background. If soft_prediction is of H x W shape, it is
            assumed that this soft prediction will be applied for all
            labels.
        label_map: dictionary mapping labels to an index. It is assumed
            that the first item in the dictionary corresponds to the
            background label and will therefore be ignored.

    Returns:
        List of shapes
    """
    (height, width) = hard_prediction.shape[:2]
    img_class = hard_prediction.swapaxes(0, 1)
    annotations: List[Annotation] = []
    for (label_index, label) in label_map.items():
        if label_index == 0:
            continue
        if len(soft_prediction.shape) == 3:
            current_label_soft_prediction = soft_prediction[:, :, label_index]
        else:
            current_label_soft_prediction = soft_prediction
        obj_group = img_class == label_index
        label_index_map = (obj_group.T.astype(int) * 255).astype(np.uint8)
        (contours, hierarchies) = cv2.findContours(label_index_map, cv2.RETR_CCOMP, cv2.CHAIN_APPROX_NONE)
        if hierarchies is not None:
            for (contour, hierarchy) in zip(contours, hierarchies[0]):
                if hierarchy[3] == -1:
                    contour = list(((point[0][0], point[0][1]) for point in contour))
                    subcontours = get_subcontours(contour)
                    for subcontour in subcontours:
                        mask = np.zeros(hard_prediction.shape, dtype=np.uint8)
                        cv2.drawContours(mask, np.asarray([[[x, y]] for (x, y) in subcontour]), contourIdx=-1, color=1, thickness=-1)
                        probability = cv2.mean(current_label_soft_prediction, mask)[0]
                        points = [Point(x=x / width, y=y / height) for (x, y) in subcontour]
                        polygon = Polygon(points=points)
                        if polygon.get_area() > 0:
                            annotations.append(Annotation(shape=polygon, labels=[ScoredLabel(label, probability)], id=ID(ObjectId())))
                        else:
                            warnings.warn('The geometry of the segmentation map you are converting is not fully supported. Polygons with a area of zero will be removed.', UserWarning)
                else:
                    warnings.warn('The geometry of the segmentation map you are converting is not fully supported. A hole was found and will be filled.', UserWarning)
    return annotations