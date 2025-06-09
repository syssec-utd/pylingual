import pickle
import os
from pathlib import Path
from .preprocessor import Preprocessor
__all__ = ['save_pipeline', 'load_pipeline']

def save_pipeline(checkpoint_dir: str, preprocessor: Preprocessor, model):
    """Saves preprocessor and model to checkpoint_dir/linear_pipline.pickle.

    Args:
        checkpoint_dir (str): The directory to save to.
        preprocessor (Preprocessor): A Preprocessor.
        model: A model returned from one of the training functions.
    """
    Path(checkpoint_dir).mkdir(parents=True, exist_ok=True)
    checkpoint_path = os.path.join(checkpoint_dir, 'linear_pipeline.pickle')
    with open(checkpoint_path, 'wb') as f:
        pickle.dump({'preprocessor': preprocessor, 'model': model}, f)

def load_pipeline(checkpoint_path: str) -> tuple:
    """Loads preprocessor and model from checkpoint_path.

    Args:
        checkpoint_path (str): The path to a previously saved pipeline.

    Returns:
        tuple: A tuple of the preprocessor and model.
    """
    with open(checkpoint_path, 'rb') as f:
        pipeline = pickle.load(f)
    return (pipeline['preprocessor'], pipeline['model'])