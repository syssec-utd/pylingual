import os
from typing import Tuple, List, Dict, Union
import pandas as pd
from .data_parser import DataParser
from .json_parser import JsonParser
from .graph_parser import GraphParser
from ..graph import Graph
from ..meta_struct import MetaStruct
from ..utils import iter_csv, mp_run
DataParserCls = {'JsonParser': JsonParser}
UnionGraphParser = Union[GraphParser, Tuple[GraphParser, List[str]]]

class ParserWrapper(MetaStruct):

    def __init__(self, data_parser: Union[DataParser, List[DataParser], Dict[str, DataParser]]=None, graph_parser: Union[UnionGraphParser, List[UnionGraphParser], Dict[str, UnionGraphParser]]=None, **kwargs):
        super().__init__(**kwargs)
        self.data_parser = data_parser
        self.graph_parser = graph_parser

    @property
    def data_parser(self):
        if len(self._data_parser) == 1:
            return list(self._data_parser.values())[0]
        return self._data_parser

    @data_parser.setter
    def data_parser(self, data_parser):
        if not isinstance(data_parser, (list, dict)):
            data_parser = [data_parser]
        if isinstance(data_parser, list):
            data_parser = {str(i): parser for i, parser in enumerate(data_parser)}
        self._data_parser: Dict[str, DataParser] = data_parser

    @property
    def graph_parser(self):
        if len(self._graph_parser) == 1:
            return list(self._graph_parser.values())[0][0]
        return {k: v[0] for k, v in self._graph_parser.items()}

    @graph_parser.setter
    def graph_parser(self, graph_parser):
        if not isinstance(graph_parser, (list, dict)):
            graph_parser = [graph_parser]
        if isinstance(graph_parser, list):
            graph_parser = {str(i): parser for i, parser in enumerate(graph_parser)}
        self._graph_parser: Dict[str, Tuple[GraphParser, List[str]]] = {}
        for k, parser in graph_parser.items():
            if not isinstance(parser, (tuple, list)):
                parser = (parser, list(self._data_parser))
                self._graph_parser[k] = parser
            else:
                self._graph_parser[k] = parser

    def to_json(self) -> dict:
        outputs = super().to_json()
        outputs['data_parser'] = {k: v.to_json() for k, v in self._data_parser.items()}
        outputs['graph_parser'] = {k: [v[0].to_json(), v[1]] for k, v in self._graph_parser.items()}
        return outputs

    @classmethod
    def from_json(cls, obj: dict, data_parser_cls=None):
        data_parser_cls = data_parser_cls or DataParserCls
        obj = dict(obj)
        obj['data_parser'] = {k: data_parser_cls[v['type']].from_json(v) for k, v in obj['data_parser'].items()}
        obj['graph_parser'] = {k: (GraphParser.from_json(v[0]), v[1]) for k, v in obj['graph_parser'].items()}
        return cls(**obj)

    def call_graph_parser(self, raw_graph, key=None):
        output = {}
        for key2, (parser, key3) in self._graph_parser.items():
            if key and key not in key3:
                continue
            output[key, key2] = parser.call(raw_graph)
        return output

    def __call__(self, df: pd.DataFrame, disable=True) -> Union[Graph, Dict[Tuple[str, str], Graph]]:
        output = {}
        for k, parser in self._data_parser.items():
            raw_graph = parser(df, disable=disable)
            output.update(self.call_graph_parser(raw_graph, key=k))
        if len(output) == 1:
            output = list(output.values())[0]
        return output

    def generate(self, df: pd.DataFrame, sel_cols=None, drop_cols=None, drop_data_cols=True):
        graph = self(df, disable=True)
        if sel_cols is not None:
            df = df[sel_cols]
        drop_cols = drop_cols or set()
        if drop_data_cols:
            drop_cols = drop_cols.union([parser.data_col for parser in self._data_parser.values()])
        df = df.drop(columns=drop_cols)
        return (graph, df)

    def get_targets(self, df):
        labels = {}
        for data_parser in self._data_parser.values():
            labels.update(data_parser.get_targets(df))
        return labels

    def _save(self, inputs, sel_cols=None, drop_cols=None):
        """

        Args:
            inputs: df, path
            sel_cols:
            drop_cols:

        Returns:

        """
        df, path = inputs
        labels = self.get_targets(df)
        graph, df = self.generate(df, sel_cols=sel_cols, drop_cols=drop_cols)
        graph.save(path, labels=labels)
        df['path'] = path
        return df

    def save(self, src, dst, disable=False, chunksize=64, postfix='saving graph', processes=None, sel_cols=None, drop_cols=None, unordered=False, **kwargs):
        """
        将原始数据加工后，存储成分片的文件
        Args:
            src: 原始数据
            dst: 存储文件夹路径
            disable: 是否禁用进度条
            chunksize: 分片数据的大小
            postfix: 进度条后缀
            processes: 多进程数量
            sel_cols: 需要返回的元数据列
            drop_cols: 需要去掉的列, 只在meta_col为None时生效
            unordered: 使用Pool.imap_unordered
            **kwargs: pd.read_csv的额外参数

        Returns:
            返回一个包含路径和元数据的DataFrame
        """
        assert not os.path.exists(dst), '{} already exists'.format(dst)
        os.mkdir(dst)
        dfs = []
        inputs = ((df, os.path.join(dst, '{}.ag.graph'.format(i))) for i, df in enumerate(iter_csv(src, chunksize=chunksize, **kwargs)))
        kwds = dict(sel_cols=sel_cols, drop_cols=drop_cols)
        for df in mp_run(self._save, inputs, kwds=kwds, disable=disable, processes=processes, postfix=postfix, unordered=unordered):
            dfs.append(df)
        path_df = pd.concat(dfs)
        path_df.to_csv(os.path.abspath(dst) + '_path.csv', index=False)
        return pd.concat(dfs)

    def generator(self, src, disable=False, chunksize=64, processes=0, postfix='parsing', sel_cols=None, drop_cols=None, drop_data_cols=True, unordered=False, **kwargs):
        """
        返回一个graph生成器
        Args:
            src: dataframe 或者"list和路径的任意嵌套"
            disable: 是否禁用进度条
            chunksize: 批次处理的大小
            processes: 多进程数量
            postfix: 进度条后缀
            sel_cols: 需要返回的元数据列
            drop_cols: 需要去掉的列, 只在meta_col为None时生效
            drop_data_cols: 去掉data列
            unordered: 使用Pool.imap_unordered
            **kwargs: pd.read_csv的额外参数

        Returns:
            graph:
            df
        """
        data = iter_csv(src, chunksize=chunksize, **kwargs)
        kwds = dict(sel_cols=sel_cols, drop_cols=drop_cols, drop_data_cols=drop_data_cols)
        for output in mp_run(self.generate, data, kwds=kwds, processes=processes, disable=disable, postfix=postfix, unordered=unordered):
            yield output

    def extra_repr(self) -> str:
        return 'data_parser={}\ngraph_parser={}'.format('  \n'.join(str(self.data_parser).split('\n')), '  \n'.join(str(self.graph_parser).split('\n')))