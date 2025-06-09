from typing import Any
from typing import Dict
from typing import List
from typing import Type
from typing import Union
from typing import Callable
from typing import Optional
from cftool.misc import check_requires
from cftool.misc import shallow_copy_dict
from cftool.types import np_dict_type
from cftool.types import tensor_dict_type
from ...bases import IDLModel
from ....data import TensorDictData
from ....types import texts_type
from ....schema import TrainerState
from ....schema import IInference
try:
    from transformers import AutoModel
    from transformers import AutoTokenizer
except:
    AutoModel = AutoTokenizer = None

@IDLModel.register('hugging_face')
class HuggingFaceModel(IDLModel):
    tokenizer_base: Type = AutoTokenizer
    model_base: Type = AutoModel
    forward_fn_name: str = 'forward'

    def __init__(self, model: str):
        if AutoModel is None:
            raise ValueError('`transformers` is needed for `HuggingFaceModel`')
        super().__init__()
        self.tokenizer = self.tokenizer_base.from_pretrained(model)
        self.model = self.model_base.from_pretrained(model)

    def model_forward(self, batch: tensor_dict_type) -> Any:
        fn = getattr(self.model, self.forward_fn_name)
        batch = shallow_copy_dict(batch)
        pop_keys = [k for k in batch.keys() if not check_requires(fn, k, False)]
        for k in pop_keys:
            batch.pop(k)
        return fn(**batch)

    def forward(self, batch_idx: int, batch: tensor_dict_type, state: Optional['TrainerState']=None, **kwargs: Any) -> tensor_dict_type:
        return self.model_forward(batch)

    def inference(self, texts: texts_type, use_tqdm: bool=True, **kwargs: Any) -> np_dict_type:
        x = self.tokenizer(texts, padding=True, return_tensors='pt')
        loader = TensorDictData(x).get_loaders()[0]
        inference = IInference(model=self)
        outputs = inference.get_outputs(loader, use_tqdm=use_tqdm, **kwargs)
        return outputs.forward_results

    def to_onnx(self, export_folder: str, sample_text: str, dynamic_axes: Optional[Union[List[int], Dict[int, str]]]=None, *, max_length: Optional[int]=None, onnx_file: str='model.onnx', opset: int=11, simplify: bool=True, forward_fn: Optional[Callable[[Dict[str, Any]], Dict[str, Any]]]=None, output_names: Optional[List[str]]=None, num_samples: Optional[int]=None, verbose: bool=True, **kwargs: Any) -> 'IDLModel':
        if max_length is None:
            input_sample = self.tokenizer(sample_text, return_tensors='pt')
        else:
            input_sample = self.tokenizer(sample_text, padding='max_length', truncation=True, max_length=max_length, return_tensors='pt')
        return super().to_onnx(export_folder, input_sample, dynamic_axes, onnx_file=onnx_file, opset=opset, simplify=simplify, forward_fn=forward_fn, output_names=output_names, num_samples=num_samples, verbose=verbose, **kwargs)
__all__ = ['HuggingFaceModel']