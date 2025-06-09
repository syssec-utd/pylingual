import numpy as np
from onnx.reference.op_run import OpRun

class Tile(OpRun):

    def _run(self, x, repeats):
        return (np.tile(x, repeats),)