import numpy as np
from typing import Any
from typing import List
from typing import Type
from typing import Union
try:
    from transformers import BertTokenizer
    from transformers import PreTrainedTokenizer
    from transformers import CLIPTokenizer as _CLIPTokenizer
except:
    BertTokenizer = PreTrainedTokenizer = _CLIPTokenizer = None
from .protocol import ITokenizer

class ICLIPTokenizer(ITokenizer):
    tag: str
    base: Type[PreTrainedTokenizer]

    def __init__(self, *, pad_to_max: bool=False):
        self.tokenizer = self.base.from_pretrained(self.tag)
        self.bos_token_id = self.tokenizer.bos_token_id
        self.eos_token_id = self.tokenizer.eos_token_id
        self.comma_token_id = self.tokenizer.get_vocab().get(',</w>')
        self.pad_to_max = pad_to_max

    def encode(self, texts: List[str], *, padding: Union[str, bool]=False, truncation: bool=True, add_special_tokens: bool=True, return_numpy: bool=False) -> Any:
        tokenized = self.tokenizer(texts, padding=padding, truncation=truncation, add_special_tokens=add_special_tokens)
        if not return_numpy:
            return tokenized
        return np.array(tokenized['input_ids'], np.int64)

    def tokenize(self, texts: Union[str, List[str]], **kwargs: Any) -> np.ndarray:
        if isinstance(texts, str):
            texts = [texts]
        kwargs['return_numpy'] = True
        kwargs['padding'] = 'max_length' if self.pad_to_max else True
        return self.encode(texts, **kwargs)

@ITokenizer.register('clip')
class CLIPTokenizer(ICLIPTokenizer):
    tag = 'openai/clip-vit-large-patch14'
    base = _CLIPTokenizer

@ITokenizer.register('clip.chinese')
class ChineseCLIPTokenizer(ICLIPTokenizer):
    tag = 'IDEA-CCNL/Taiyi-CLIP-Roberta-large-326M-Chinese'
    base = BertTokenizer

    def __init__(self) -> None:
        super().__init__()
        self.max_length = 512
__all__ = ['ICLIPTokenizer', 'CLIPTokenizer', 'ChineseCLIPTokenizer']