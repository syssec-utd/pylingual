"""JDE model for human detection and tracking."""
import logging
from typing import Any, Dict, List, Tuple
import numpy as np
from peekingduck.pipeline.nodes.base import ThresholdCheckerMixin, WeightsDownloaderMixin
from peekingduck.pipeline.nodes.model.jdev1.jde_files.tracker import Tracker

class JDEModel(ThresholdCheckerMixin, WeightsDownloaderMixin):
    """JDE Model with model types: 576x320, 865x480, and 1088x608.

    Args:
        config (Dict[str, Any]): Model configuration options.
        frame_rate (float): The frame rate of the current video sequence,
            used for computing the size of track buffer.

    Raises:
        ValueError: `iou_threshold` is beyond [0, 1].
        ValueError: `nms_threshold` is beyond [0, 1].
        ValueError: `score_threshold` is beyond [0, 1].
    """

    def __init__(self, config: Dict[str, Any], frame_rate: float) -> None:
        self.config = config
        self.logger = logging.getLogger(__name__)
        self.check_bounds(['iou_threshold', 'nms_threshold', 'score_threshold'], '[0, 1]')
        model_dir = self.download_weights()
        self.tracker = Tracker(model_dir, frame_rate, self.config['model_type'], self.weights['model_file'], self.weights['config_file'], self.config['min_box_area'], self.config['track_buffer'], self.config['iou_threshold'], self.config['nms_threshold'], self.config['score_threshold'])

    def predict(self, image: np.ndarray) -> Tuple[List[np.ndarray], List[float], List[int]]:
        """Track objects from image.

        Args:
            image (np.ndarray): Image in numpy array.

        Returns:
            (Tuple[List[np.ndarray], List[float], List[int]]): A tuple of
            - Numpy array of detected bounding boxes.
            - List of detection confidence scores.
            - List of track IDs.

        Raises:
            TypeError: The provided `image` is not a numpy array.
        """
        if not isinstance(image, np.ndarray):
            raise TypeError('image must be a np.ndarray')
        (bboxes, track_ids, bbox_scores) = self.tracker.track_objects_from_image(image)
        return (bboxes, bbox_scores, track_ids)