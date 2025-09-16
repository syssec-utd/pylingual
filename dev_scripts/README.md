# Model Training

PyLingual's accuracy is dependent on having accurate segmentation and statement models [^1]. The segmentation model divides a list of bytecode instructions into groups for each source instruction. The statement model transforms each group of instructions into source code. The instructions for training these models is as follows:

## Dataset generation

Create a dataset JSON file based off the sample (`sample_jsons/py36-sample-data.json`).

The dataset directory should be structured like so, with only one `.py` file per directory:

```
dataset
├── 0
│   └── file.py
├── 1
│   └── file.py
...
├── 999
│   └── file.py
└── 1000
    └── file.py
```

The names of the inner directories and files do not matter. Then create the dataset:

```
uv run prepare_dataset.py <path to JSON>
```

## Segmentation model

Create a segmentation model JSON file based off the sample (`sample_jsons/py36-sample-segmentation.json`). Then train the model:

```
uv run train_models.py --segmentation <path to JSON>
```

## Statement model

Create a statement model JSON file based off the sample (`sample_jsons/py36-sample-statement.json`). Then train the model:

```
uv run train_models.py --statement <path to JSON>
```

Once models are trained, update `../pylingual/decompiler_config.yaml` or create a separate config file by replacing the old models with the newly trained ones.

[^1]: [pylingual models](https://huggingface.co/syssec-utd).
