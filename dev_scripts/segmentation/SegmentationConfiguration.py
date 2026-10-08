import json
import logging
import pathlib
from dataclasses import dataclass
from typing import Optional


@dataclass
class TrainingParameters:
    batch_size: int
    epochs: int
    learning_rate: float


@dataclass
class SegmentationConfiguration:
    base_repo_name: str
    dataset_repo_name: str
    pretrained_mlm_repo_name: str
    cache_dir: pathlib.Path
    max_token_length: int
    dataset_percentage: int
    mlm_training_parameters: TrainingParameters
    segmentation_training_parameters: TrainingParameters

    @property
    def tokenizer_repo_name(self):
        return self.base_repo_name + "-tokenizer"

    @property
    def tokenizer_json_path(self):
        return self.cache_dir / "tokenizers" / self.tokenizer_repo_name / "tokenizer.json"

    @property
    def tokenized_dataset_repo_name(self):
        return self.dataset_repo_name + "-tokenized"

    @property
    def tokenized_dataset_dir(self):
        return self.cache_dir / "datasets" / self.tokenized_dataset_repo_name

    @property
    def mlm_repo_name(self):
        return self.base_repo_name + "-mlm"

    @property
    def mlm_dir(self):
        return self.cache_dir / "models" / self.mlm_repo_name

    @property
    def segmenter_repo_name(self):
        return self.base_repo_name + "-segmenter"

    @property
    def segmenter_dir(self):
        return self.cache_dir / "models" / self.segmenter_repo_name

    @property
    def dataset_dir(self):
        return self.cache_dir / "datasets" / self.dataset_repo_name

    def __post_init__(self):
        self.cache_dir = pathlib.Path(self.cache_dir)


def parse_segmentation_config_json(json_file_path: pathlib.Path, logger: Optional[logging.Logger] = None) -> SegmentationConfiguration:
    if not json_file_path.exists():
        raise FileNotFoundError(f"{json_file_path} does not exist")

    if logger:
        logger.info(f"Loading model description from {json_file_path}...")

    with json_file_path.open() as json_file:
        segmentation_config_dict = json.load(json_file)

    segmentation_config_dict["mlm_training_parameters"] = TrainingParameters(**segmentation_config_dict["mlm_training_parameters"])
    segmentation_config_dict["segmentation_training_parameters"] = TrainingParameters(**segmentation_config_dict["segmentation_training_parameters"])
    return SegmentationConfiguration(**segmentation_config_dict)
