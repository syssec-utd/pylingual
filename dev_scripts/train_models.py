import logging
import os
import pathlib
import subprocess
import click

from pylingual.utils.get_logger import get_logger


def train_segmentation(segmentation_config_path: pathlib.Path, logger: logging.Logger, nnodes: int = 1, nproc_per_node: int = 1, rdzv_port: int = 29400):
    segmentation_root = pathlib.Path(__file__).parent / "segmentation"

    # train tokenizer
    logger.info("training tokenizer...")
    subprocess.run(["uv", "run", segmentation_root / "train_tokenizer.py", segmentation_config_path])

    # train mlm (single gpu to avoid conflicts with local tokenized data)
    logger.info("training masked language model...")
    subprocess.run(
        [
            "uv", "run",
            "torchrun",
            f"--nnodes={nnodes}",
            f"--nproc-per-node={nproc_per_node}",
            "--rdzv-backend=c10d",
            f"--rdzv-endpoint=localhost:{rdzv_port}",
            segmentation_root / "train_mlm.py",
            segmentation_config_path,
        ],
        env=dict(os.environ, NCCL_P2P_DISABLE="1"),
    )

    # tokenize dataset
    logger.info("tokenizing segmentation dataset...")
    subprocess.run(["uv", "run", segmentation_root / "tokenize_seg.py", segmentation_config_path])

    # train segmentation model (4 gpus)
    logger.info("training segmentation model...")
    subprocess.run(
        [
            "uv", "run",
            "torchrun",
            f"--nnodes={nnodes}",
            f"--nproc-per-node={nproc_per_node}",
            "--rdzv-backend=c10d",
            f"--rdzv-endpoint=localhost:{rdzv_port}",
            segmentation_root / "train_seg.py",
            segmentation_config_path,
        ],
        env=dict(os.environ, NCCL_P2P_DISABLE="1"),
    )


def train_statement(statement_config_path: pathlib.Path, logger: logging.Logger, nnodes: int = 1, nproc_per_node: int = 1, rdzv_port: int = 29400):
    statement_root = pathlib.Path(__file__).parent / "statement"

    # manual tokenizer
    subprocess.run(["uv", "run", statement_root / "train_tokenizer_auto.py", statement_config_path])

    # tokenize statement dataset with salesforce tokenizer
    logger.info("tokenizing statement dataset...")
    subprocess.run(["uv", "run", statement_root / "tokenize_seq2seq.py", statement_config_path])

    # train statement model (4 gpus)
    logger.info("training statement model...")
    subprocess.run(
        [
            "uv", "run",
            "torchrun",
            f"--nnodes={nnodes}",
            f"--nproc-per-node={nproc_per_node}",
            "--rdzv-backend=c10d",
            f"--rdzv-endpoint=localhost:{rdzv_port}",
            statement_root / "train_seq2seq.py",
            statement_config_path,
        ],
        env=dict(os.environ, NCCL_P2P_DISABLE="1"),
    )


@click.command(help="Full tokenization and training pipeline for the segmentation and statement translation models.")
@click.option("--segmentation", type=str, default=None, help="The path to the segmentation model description JSON file.")
@click.option("--statement", type=str, default=None, help="The path to the statement model description JSON file.")
@click.option("--nnodes", type=int, default=1, help="Torchrun nnodes arg")
@click.option("--nproc_per_node", type=int, default=1, help="Torchrun nproc_per_node arg")
@click.option("--rdzv_port", "-p", type=int, default=29400, help="Port to use for torchrun rendezvous endpoint")
def main(segmentation: str, statement: str, nnodes: int, nproc_per_node: int, rdzv_port: int):
    logger = get_logger("train-models")

    ### LOAD JSON
    logger.info("Training pipeline starting...")
    logger.info("Loading dataset description JSON files...")

    ### CONFIG_PATHS
    segmentation_config_path = pathlib.Path(segmentation).resolve() if segmentation is not None else None
    statement_config_path = pathlib.Path(statement).resolve() if statement is not None else None

    logger.info("Dataset description JSON files loaded!")

    ### TRAIN SEGMENTATION
    if segmentation_config_path is not None:
        logger.info("Segmentation model training starting...")
        train_segmentation(segmentation_config_path, logger, nnodes, nproc_per_node, rdzv_port)
        logger.info("Segmentation model training complete!")
    else:
        logger.warning("Segmentation model configuration json path not provided in --segmentation; skipping segmentation model training...")

    ### TRAIN STATEMENT
    if statement_config_path is not None:
        logger.info("Statement model training starting...")
        train_statement(statement_config_path, logger, nnodes, nproc_per_node, rdzv_port)
        logger.info("Statement model training complete!")
    else:
        logger.warning("Statement model configuration json path not provided in --statement; skipping statement model training...")

    logger.info("Training pipeline complete!")


if __name__ == "__main__":
    main()
