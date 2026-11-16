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

## Control flow model

The control flow model predicts how the translated statements of a code object nest, as a skeleton such as `<s0> { <s1> } else { <s2> }`. It (`pylingual/control_flow_reconstruction/transition.py`) encodes the statements and writes the skeleton one grammar action at a time, pointing at statements instead of naming them. Every skeleton must fit the block grammar (`pylingual/control_flow_reconstruction/block_grammar.py`), Python's block structure as a pushdown automaton, so the source rendered from it compiles.

One model serves every version. Build a control flow dataset for each version from a normal dataset JSON (`sample_jsons/py312-sample-control-flow-data.json`); the `cflow` stage keeps the code objects whose gold skeleton recompiles to equivalent bytecode:

```
uv run prepare_dataset.py sample_jsons/py312-sample-control-flow-data.json --stage generate --stage compile --stage cflow
```

Then train on every version's `cflow` dir (`dataset_dirs` in `sample_jsons/sample-control-flow-transition-unified.json`, the config of the released model; `--seed` sets the seed, 42 by default):

```
uv run control_flow/train_transition.py sample_jsons/sample-control-flow-transition-unified.json
```

The released model was trained on the 150k sources of the translation models' corpus, 15k per version (13,500 PyPI, 1,500 CodeSearchNet), each source compiled for one version only. Batches hold up to `batch_size` rows, fewer for large code objects, so a 2048 statement code object fits in memory.

To compare models on the [PyLingual evaluation dataset](https://github.com/syssec-utd/pylingual_eval_dataset) v1 (`git clone --branch v1.1.0 --depth 1`), or on a dataset's compiled test split, with the gold segmentation and lines:

```
uv run bench_cflow.py <eval dataset>/python-3.12 --model <HuggingFace repo or directory> --out bench.json
uv run bench_cflow.py <eval dataset>/python-3.12 --baseline
```

The decompiler's model is the `CONTROL_FLOW_MODEL` (`REPO`, `REVISION`) at the top level of `decompiler_config.yaml`, which a version's own entry overrides. Changing the output of `pylingual/control_flow_reconstruction/model_view.py` needs new models.
