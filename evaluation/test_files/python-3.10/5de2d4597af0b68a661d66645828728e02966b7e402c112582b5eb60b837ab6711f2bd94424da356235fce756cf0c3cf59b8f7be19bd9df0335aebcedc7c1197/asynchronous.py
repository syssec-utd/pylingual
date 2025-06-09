"""Async executor based on ModelAPI."""
import time
from typing import Any, Tuple, Union
import numpy as np
from openvino.model_zoo.model_api.pipelines import AsyncPipeline
from otx.api.usecases.exportable_code.demo.demo_package.model_container import ModelContainer
from otx.api.usecases.exportable_code.demo.demo_package.utils import create_output_converter
from otx.api.usecases.exportable_code.streamer import get_streamer
from otx.api.usecases.exportable_code.visualizers import Visualizer
from otx.api.usecases.exportable_code.prediction_to_annotation_converter import DetectionToAnnotationConverter
from otx.api.utils.vis_utils import dump_frames

class AsyncExecutor:
    """Async inferencer.

    Args:
        model: model for inference
        visualizer: visualizer of inference results
    """

    def __init__(self, model: ModelContainer, visualizer: Visualizer) -> None:
        self.model = model.core_model
        self.visualizer = visualizer
        self.converter = create_output_converter(model.task_type, model.labels)
        self.async_pipeline = AsyncPipeline(self.model)

    def run(self, input_stream: Union[int, str], loop: bool=False) -> None:
        """Async inference for input stream (image, video stream, camera)."""
        streamer = get_streamer(input_stream, loop)
        next_frame_id = 0
        next_frame_id_to_show = 0
        stop_visualization = False
        saved_frames = []
        for frame in streamer:
            results = self.async_pipeline.get_result(next_frame_id_to_show)
            while results:
                start_time = time.perf_counter()
                output = self.render_result(results)
                next_frame_id_to_show += 1
                self.visualizer.show(output)
                if self.visualizer.output:
                    saved_frames.append(output)
                if self.visualizer.is_quit():
                    stop_visualization = True
                self.visualizer.video_delay(time.perf_counter() - start_time, streamer)
                results = self.async_pipeline.get_result(next_frame_id_to_show)
            if stop_visualization:
                break
            self.async_pipeline.submit_data(frame, next_frame_id, {'frame': frame})
            next_frame_id += 1
        self.async_pipeline.await_all()
        for next_frame_id_to_show in range(next_frame_id_to_show, next_frame_id):
            start_time = time.perf_counter()
            results = self.async_pipeline.get_result(next_frame_id_to_show)
            output = self.render_result(results)
            self.visualizer.show(output)
            if self.visualizer.output:
                saved_frames.append(output)
            self.visualizer.video_delay(time.perf_counter() - start_time, streamer)
        dump_frames(saved_frames, self.visualizer.output, input_stream, streamer)

    def render_result(self, results: Tuple[Any, dict]) -> np.ndarray:
        """Render for results of inference."""
        (predictions, frame_meta) = results
        if isinstance(self.converter, DetectionToAnnotationConverter):
            predictions = np.array([[pred.id, pred.score, *pred.get_coords()] for pred in predictions])
            predictions.shape = (len(predictions), 6)
        annotation_scene = self.converter.convert_to_annotation(predictions, frame_meta)
        current_frame = frame_meta['frame']
        output = self.visualizer.draw(current_frame, annotation_scene, frame_meta)
        return output