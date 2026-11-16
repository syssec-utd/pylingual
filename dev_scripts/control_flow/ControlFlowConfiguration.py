from dataclasses import dataclass

import pathlib
import json
import logging


@dataclass
class ModelParameters:
    d_model: int = 256
    layers: int = 4
    heads: int = 8
    d_ff: int = 1024


@dataclass
class TrainingParameters:
    batch_size: int
    epochs: int
    learning_rate: float


@dataclass
class ControlFlowConfiguration:
    base_repo_name: str
    dataset_dirs: list[pathlib.Path]
    cache_dir: pathlib.Path
    model_parameters: ModelParameters
    training_parameters: TrainingParameters
    max_stmts: int = 512
    max_input_tokens: int = 2048
    push_to_hub: bool = False

    @property
    def model_repo_name(self):
        return self.base_repo_name + "-cflow"

    @property
    def model_dir(self):
        return self.cache_dir / "models" / self.model_repo_name

    def __post_init__(self):
        self.cache_dir = pathlib.Path(self.cache_dir)
        self.dataset_dirs = [pathlib.Path(d) for d in self.dataset_dirs]


def parse_control_flow_config_json(json_file_path: pathlib.Path, logger: logging.Logger = None) -> ControlFlowConfiguration:
    if not json_file_path.exists():
        raise FileNotFoundError(f"{json_file_path} does not exist")

    if logger:
        logger.info(f"Loading model description from {json_file_path}...")

    with json_file_path.open() as json_file:
        config_dict = json.load(json_file)

    config_dict["model_parameters"] = ModelParameters(**config_dict.get("model_parameters", {}))
    config_dict["training_parameters"] = TrainingParameters(**config_dict["training_parameters"])
    return ControlFlowConfiguration(**config_dict)
