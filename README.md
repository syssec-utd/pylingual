# PyLingual - Python Decompiler for 3.6+

PyLingual is a CPython bytecode decompiler supporting all released Python versions since 3.6. For information about the design and implementation of PyLingual, please refer to our [research paper](https://www.computer.org/csdl/proceedings-article/sp/2025/223600a052/21B7QZB86cg).

PyLingual can be run through our [web service](https://pylingual.io) or run locally.

This codebase is optimized for readability and future extension, so there may initially be some control flow accuracy regression compared to the version hosted on the web service.

## Requirements

- Python 3.11 or higher

### Compiling bytecode

Some parts of PyLingual require the ability to compile bytecode in a different Python version (equivalence check and model training). For this, you will need the following:

- [pyenv](https://github.com/pyenv/pyenv) with all Python versions you want to compile to
- Unix-like operating system (pyenv does not support Windows)

## Setup

Install from source, using [Poetry](https://python-poetry.org/):

```sh
git clone https://github.com/syssec-utd/pylingual
cd pylingual
python -m venv venv
source venv/bin/activate
pip install poetry==2.1.1
poetry install
```

## Usage

```
Usage: pylingual [OPTIONS] [FILES]...

  End to end pipeline to decompile Python bytecode into source code.

Options:
  -o, --out-dir PATH      The directory to export results to.
  -c, --config-file PATH  Config file for model information.
  -v, --version VERSION   Python version of the .pyc, default is auto
                          detection.
  -k, --top-k INT         Maximum number of additional segmentations to
                          consider.
  -q, --quiet             Suppress console output.
  --trust-lnotab          Use the lnotab for segmentation instead of the
                          segmentation model.
  --init-pyenv            Install pyenv before decompiling.
  -h, --help              Show this message and exit.
```

## Demo

![demo gif](demo.gif)

## Support

If you have any issues for installing and using PyLingual, please create an issue or send your message via our support email at pylingual@gmail.com.
