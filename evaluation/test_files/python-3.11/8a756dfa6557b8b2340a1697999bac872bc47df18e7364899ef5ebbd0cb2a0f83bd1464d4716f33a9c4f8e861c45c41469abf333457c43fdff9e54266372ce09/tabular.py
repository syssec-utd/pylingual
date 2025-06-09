"""
The pre-processing function for tabular data.
"""
import numpy as np
import pandas as pd
from .base import TransformBase, Identity
from .encode import OneHot, Ordinal, LabelEncoder
from ..data.tabular import Tabular

class TabularTransform(TransformBase):
    """
    Transforms for a ``data.tabular.Tabular`` instance.
    """

    def __init__(self, cate_transform: TransformBase=OneHot(), cont_transform: TransformBase=Identity(), target_transform: TransformBase=LabelEncoder()):
        """
        :param cate_transform: The transform for the categorical features, e.g.,
            `OneHot`, `Ordinal`.
        :param cont_transform: The transform for the continuous-valued features,
            e.g., `Identity`, `Standard`, `MinMax`, `Scale`.
        :param target_transform: The transform for the target column, e.g.,
            `Identity` for regression, `LabelEncoder` for classification.
        """
        super().__init__()
        assert cate_transform is not None, 'Transform for categorical features cannot be None.'
        assert cont_transform is not None, 'Transform for continuous-valued features cannot be None.'
        self.cate_transform = cate_transform
        self.cont_transform = cont_transform
        self.cate_shape = None
        self.cont_shape = None
        self.cate_columns = None
        self.cont_columns = None
        self.targ_column = None
        self.targ_transform = target_transform
        self.columns = None

    @staticmethod
    def _split(x: Tabular) -> (pd.DataFrame, pd.DataFrame, pd.DataFrame):
        """
        Separates the categorical features, continuous-valued features
        and target/labels column.

        :param x: A `Tabular` object.
        :return: The pandas DataFrames of the categorical features,
            the continuous-valued features and the targets/labels.
        :rtype: tuple(pd.DataFrame, pd.DataFrame, pd.DataFrame)
        """
        df = x.to_pd()
        cate_df = df[x.categorical_columns] if x.categorical_columns else None
        cont_df = df[x.continuous_columns] if x.continuous_columns else None
        targ_df = df[[x.target_column]] if x.target_column else None
        return (cate_df, cont_df, targ_df)

    def fit(self, x: Tabular):
        """
        Fits a tabular transformer.

        :param x: A `Tabular` object.
        :return: Itself.
        :rtype: TabularTransform
        """
        self.cate_columns = x.categorical_columns
        self.cont_columns = x.continuous_columns
        self.targ_column = x.target_column
        self.columns = list(x.columns)
        cate_df, cont_df, targ_df = self._split(x)
        if cate_df is not None:
            self.cate_transform.fit(cate_df)
            self.cate_shape = self.cate_transform.transform(cate_df).shape[1]
        if cont_df is not None:
            self.cont_transform.fit(cont_df)
            self.cont_shape = self.cont_transform.transform(cont_df).shape[1]
        if targ_df is not None:
            self.targ_transform.fit(targ_df)
        return self

    def transform(self, x: Tabular) -> np.ndarray:
        """
        Transforms the input tabular instance. The output data concatenates the transformed
        categorical features, continuous-valued features and targets/labels (if exist) together.

        :param x: A `Tabular` object.
        :return: The transformed data.
        :rtype: np.ndarray
        """
        values = []
        cate_df, cont_df, targ_df = self._split(x)
        if cate_df is not None:
            values.append(self.cate_transform.transform(cate_df))
        if cont_df is not None:
            values.append(self.cont_transform.transform(cont_df).astype(float))
        if targ_df is not None:
            values.append(self.targ_transform.transform(targ_df).reshape((-1, 1)))
        return np.concatenate(values, axis=1)

    def invert(self, x: np.ndarray) -> Tabular:
        """
        Converts a numpy array into a Tabular object.

        :param x: An input numpy array.
        :return: The inverse Tabular object.
        :rtype: Tabular
        """
        if x.ndim == 1:
            x = np.expand_dims(x, axis=0)
        elif x.ndim > 2:
            raise ValueError('The dimension of the data should be <= 2.')
        index = 0
        cate_array = None
        if self.cate_shape is not None:
            cate_array = x[:, :self.cate_shape]
            index = self.cate_shape
        cont_array = None
        if self.cont_shape is not None:
            cont_array = x[:, index:index + self.cont_shape]
            index += self.cont_shape
        targ_array = None
        if self.targ_column is not None:
            targ_array = x[:, index:]
            if targ_array.shape[1] == 0:
                targ_array = None
        dfs = []
        if cate_array is not None:
            dfs.append(pd.DataFrame(self.cate_transform.invert(cate_array), columns=self.cate_columns))
        if cont_array is not None:
            dfs.append(pd.DataFrame(self.cont_transform.invert(cont_array), columns=self.cont_columns))
        if targ_array is not None:
            dfs.append(pd.DataFrame(self.targ_transform.invert(targ_array.flatten()), columns=[self.targ_column]))
        df = pd.concat(dfs, axis=1)
        if len(self.columns) == len(df.columns):
            df = df[self.columns]
        else:
            df = df[[c for c in self.columns if c != self.targ_column]]
        return Tabular(df, categorical_columns=self.cate_columns, target_column=self.targ_column if targ_array is not None else None)

    def decompose(self, x: np.ndarray) -> tuple:
        """
        Decomposes the transformed data into `categorical`, `continuous` and `target`.

        :param x: An input numpy array.
        :return: A tuple of `categorical`, `continuous` and `target` data.
        :rtype: tuple
        """
        index = 0
        cate_array = None
        if self.cate_shape is not None:
            cate_array = x[:, :self.cate_shape]
            index = self.cate_shape
        cont_array = None
        if self.cont_shape is not None:
            cont_array = x[:, index:index + self.cont_shape]
            index += self.cont_shape
        targ_array = None
        if self.targ_column is not None:
            targ_array = x[:, index:]
            if targ_array.shape[1] == 0:
                targ_array = None
        return (cate_array, cont_array, targ_array)

    @property
    def categories(self):
        """
        Gets the categories for all the features.

        :return: A list of categories, i.e., ``categories[i]`` holds
            the categories expected in the ith column, or None.
        """
        if self.cate_shape is not None and isinstance(self.cate_transform, (Ordinal, OneHot)):
            return self.cate_transform.categories
        else:
            return None

    @property
    def class_names(self):
        """
        Returns the class names for a classification task.

        :return: A list of class names or None.
        """
        if self.targ_column is not None and isinstance(self.targ_transform, LabelEncoder):
            return [str(c) for c in self.targ_transform.categories]
        else:
            return None

    def get_feature_names(self):
        """
        Returns the feature names in the transformed data.
        """
        features = []
        if self.cate_columns:
            if isinstance(self.cate_transform, OneHot):
                features += list(self.cate_transform.get_feature_names(self.cate_columns))
            else:
                features += self.cate_columns
        if self.cont_columns:
            features += self.cont_columns
        return features