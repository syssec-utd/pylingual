from io import BytesIO
from typing import Dict, List, Literal

from datasets import load_dataset
from huggingface_hub import HfApi

from .DatasetDescription import DatasetDescription

LOCAL_DATASET = Dict[Literal["train", "test", "valid"], List[str]]


def upload_single_dataset(data_files: LOCAL_DATASET, dataset_name: str, dataset_card: str, public: bool = False):
    local_datasets = load_dataset("csv", data_files=data_files)
    local_datasets.push_to_hub(dataset_name, private=not public)

    dataset_card_with_stats = dataset_card + f"\n\nDataset Statistics:\n\n```\n{local_datasets}\n```"

    api = HfApi()
    api.upload_file(
        path_or_fileobj=BytesIO(bytes(dataset_card_with_stats, "utf-8")),
        path_in_repo="README.md",
        repo_id=dataset_name,
        repo_type="dataset",
    )


def upload_dataset_to_huggingface(dataset_description: DatasetDescription, public: bool = False):
    formatted_data_requests = "\n".join(f"{str(req.source_path.resolve())}: (train: {req.num_train}, test: {req.num_test}, valid: {req.num_valid})" for req in dataset_description.data_requests)
    dataset_card = f"""
# {dataset_description.name}

Created by the Syssec team @ UTD

Dataset Composition:

```
{formatted_data_requests}
```

Python version: `{".".join(map(str, dataset_description.version))}`
"""

    splits: List[Literal["train", "test", "valid"]] = [
        "train",
        "test",
        "valid",
    ]

    # collect data files
    segmentation_data_files: LOCAL_DATASET = {}
    statement_data_files: LOCAL_DATASET = {}
    for split in splits:
        segmentation_data_files[split] = [str(path.resolve()) for path in (dataset_description.csv_dir / split / "segmentation").glob("*.csv")]
        statement_data_files[split] = [str(path.resolve()) for path in (dataset_description.csv_dir / split / "statement").glob("*.csv")]

    # upload datasets
    segmentation_dataset_name = f"{dataset_description.huggingface_user}/segmentation-{dataset_description.name}"
    upload_single_dataset(segmentation_data_files, segmentation_dataset_name, dataset_card, public)
    statement_dataset_name = f"{dataset_description.huggingface_user}/statement-{dataset_description.name}"
    upload_single_dataset(statement_data_files, statement_dataset_name, dataset_card, public)
