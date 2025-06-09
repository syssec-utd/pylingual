from pathlib import Path
from kdfba.model import dModel
from cobra.io import read_sbml_model
from cobra.io import load_json_model
from cobra.io import load_matlab_model
from cobra.io import load_yaml_model
from cobra import Model
from typing import IO, Match, Optional, Pattern, Tuple, Type, Union
import numpy as np

class dio:

    def transfer_model2dModel(self, model: Model) -> dModel:
        return dModel(model)

    def read_sbml_dModel(self, filename: Union[str, IO, Path], number: Type=float, **kwargs) -> dModel:
        return self.transfer_model2dModel(read_sbml_model(filename, number, **kwargs))

    def load_json_dModel(self, filename: Union[str, Path, IO]) -> Model:
        return self.transfer_model2dModel(load_json_model(filename))

    def load_matlab_dModel(self, infile_path: Union[str, Path, IO], variable_name: Optional[str]=None, inf: float=np.inf) -> Model:
        return self.transfer_model2dModel(load_matlab_model(infile_path, variable_name, inf))

    def load_yaml_dModel(self, filename: Union[str, Path]) -> Model:
        return self.transfer_model2dModel(load_yaml_model(filename))