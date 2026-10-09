# PyLingual - Python Decompiler for 3.6+

PyLingual is a CPython bytecode decompiler supporting all released Python versions since 3.6. For information about the design and implementation of PyLingual, please refer to our [research paper](https://www.computer.org/csdl/proceedings-article/sp/2025/223600a052/21B7QZB86cg).

PyLingual can be run through our [web service](https://pylingual.io) or run locally.

This codebase is optimized for readability and future extension, so there may initially be some control flow accuracy regression compared to the version hosted on the web service.

## Requirements

- `uv` Python package manager ([installation](https://docs.astral.sh/uv/getting-started/installation/)), used for project dependencies and managed Python versions.

### Decompiling End-Of-Life Python Versions

To verify decompilation correctness and produce model training sets, PyLingual requires the ability to compile Python in the target version.

For current Python versions (3.8-3.15), PyLingual uses `uv`'s managed installations, but for Python 3.6 and 3.7, PyLingual uses [pyenv](https://github.com/pyenv/pyenv) ([pyenv-win](https://github.com/pyenv-win/pyenv-win) for Windows).

## Setup

Install from source, using [uv](https://docs.astral.sh/uv/):

```sh
git clone https://github.com/syssec-utd/pylingual
uv tool install ./pylingual
```

### Redis translation cache (optional)

The CLI can reuse translation-model predictions across files and runs using Redis,
with the same cache used by [the dataset evaluator](https://github.com/syssec-utd/pylingual_eval_dataset).
Entries are keyed by Python version and normalized bytecode. Repeated statements can
skip translation-model inference; the first uncached translation still runs the model,
and segmentation and model loading are not cached by Redis.

With Docker and Docker Compose installed, start Redis from the cloned repository:

```sh
cd pylingual
docker compose up -d redis
```

The bundled service listens on `127.0.0.1:6379`. If Redis is already running there
(for example, for the dataset evaluator), reuse it instead of starting another service.
Enable caching with:

```sh
pylingual --redis-host 127.0.0.1 example.pyc
```

Alternatively, set `PYLINGUAL_REDIS_HOST`: `export PYLINGUAL_REDIS_HOST=127.0.0.1`
in a POSIX shell, or `$env:PYLINGUAL_REDIS_HOST = '127.0.0.1'` in PowerShell.
Without a host, Redis caching remains disabled. Use `--redis-port` or
`PYLINGUAL_REDIS_PORT` for a different port; the CLI defaults to `6379`.
Command-line settings override their environment variables.

Cache keys do not include the translation model revision. Use a separate Redis
instance when switching translation models to avoid reusing predictions from another model.

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
  -r, --redis-host HOST  Redis translation cache host; defaults to
                         $PYLINGUAL_REDIS_HOST. Unset disables caching.
  --redis-port PORT      Redis port; defaults to $PYLINGUAL_REDIS_PORT
                         or 6379.
  -q, --quiet             Suppress console output.
  --trust-lnotab          Use the lnotab for segmentation instead of the
                          segmentation model.
  --init-pyenv            Install pyenv before decompiling.
  -h, --help              Show this message and exit.
```

## Demo

![demo gif](demo.gif)

## Support

If you have any issues for installing and using PyLingual, please create an issue or send your message via our support email at pylingual.io@gmail.com.
