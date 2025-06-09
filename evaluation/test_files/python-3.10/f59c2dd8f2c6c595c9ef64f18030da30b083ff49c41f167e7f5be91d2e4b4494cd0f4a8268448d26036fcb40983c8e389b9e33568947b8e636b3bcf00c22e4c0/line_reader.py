from typing import Dict
from deeppavlov.core.common.registry import register
from deeppavlov.core.data.dataset_reader import DatasetReader

@register('line_reader')
class LineReader(DatasetReader):
    """Read txt file by lines"""

    def read(self, data_path: str=None, *args, **kwargs) -> Dict:
        """Read lines from txt file

        Args:
            data_path: path to txt file

        Returns:
            A dictionary containing training, validation and test parts of the dataset obtainable via ``train``, ``valid`` and ``test`` keys.
        """
        with open(data_path) as f:
            content = f.readlines()
        dataset = dict()
        dataset['train'] = [(line,) for line in content]
        dataset['valid'] = []
        dataset['test'] = []
        return dataset