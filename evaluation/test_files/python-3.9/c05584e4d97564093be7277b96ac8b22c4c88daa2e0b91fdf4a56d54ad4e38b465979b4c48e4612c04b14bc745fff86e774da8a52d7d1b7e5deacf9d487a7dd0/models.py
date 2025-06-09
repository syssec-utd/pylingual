"""Models and schema for SpatialData."""
from __future__ import annotations
import warnings
from collections.abc import Mapping, Sequence
from functools import singledispatchmethod
from pathlib import Path
from typing import Any, Literal, Optional, Union
import dask.dataframe as dd
import numpy as np
import pandas as pd
from anndata import AnnData
from dask.array.core import Array as DaskArray
from dask.array.core import from_array
from dask.dataframe.core import DataFrame as DaskDataFrame
from geopandas import GeoDataFrame, GeoSeries
from multiscale_spatial_image import to_multiscale
from multiscale_spatial_image.multiscale_spatial_image import MultiscaleSpatialImage
from multiscale_spatial_image.to_multiscale.to_multiscale import Methods
from pandas.api.types import is_categorical_dtype
from shapely._geometry import GeometryType
from shapely.geometry import MultiPolygon, Point, Polygon
from shapely.geometry.collection import GeometryCollection
from shapely.io import from_geojson, from_ragged_array
from spatial_image import SpatialImage, to_spatial_image
from xarray import DataArray
from xarray_schema.components import ArrayTypeSchema, AttrSchema, AttrsSchema, DimsSchema
from xarray_schema.dataarray import DataArraySchema
from spatialdata._logging import logger
from spatialdata._types import ArrayLike
from spatialdata.models import C, X, Y, Z, get_axes_names
from spatialdata.models._utils import DEFAULT_COORDINATE_SYSTEM, TRANSFORM_KEY, MappingToCoordinateSystem_t, SpatialElement, _validate_mapping_to_coordinate_system_type
from spatialdata.transformations._utils import _get_transformations, _set_transformations, compute_coordinates
from spatialdata.transformations.transformations import BaseTransformation, Identity
Chunks_t = Union[int, tuple[int, ...], tuple[tuple[int, ...], ...], Mapping[Any, Union[None, int, tuple[int, ...]]]]
ScaleFactors_t = Sequence[Union[dict[str, int], int]]
Transform_s = AttrSchema(BaseTransformation, None)

def _parse_transformations(element: SpatialElement, transformations: Optional[MappingToCoordinateSystem_t]=None) -> None:
    _validate_mapping_to_coordinate_system_type(transformations)
    transformations_in_element = _get_transformations(element)
    if transformations_in_element is not None and len(transformations_in_element) > 0 and (transformations is not None) and (len(transformations) > 0):
        raise ValueError('Transformations are both specified for the element and also passed as an argument to the parser. Please specify the transformations only once.')
    if transformations_in_element is not None and len(transformations_in_element) > 0:
        parsed_transformations = transformations_in_element
    elif transformations is not None and len(transformations) > 0:
        parsed_transformations = transformations
    else:
        parsed_transformations = {DEFAULT_COORDINATE_SYSTEM: Identity()}
    _set_transformations(element, parsed_transformations)

class RasterSchema(DataArraySchema):
    """Base schema for raster data."""

    @classmethod
    def parse(cls, data: Union[ArrayLike, DataArray, DaskArray], dims: Optional[Sequence[str]]=None, transformations: Optional[MappingToCoordinateSystem_t]=None, scale_factors: Optional[ScaleFactors_t]=None, method: Optional[Methods]=None, chunks: Optional[Chunks_t]=None, **kwargs: Any) -> Union[SpatialImage, MultiscaleSpatialImage]:
        """
        Validate (or parse) raster data.

        Parameters
        ----------
        data
            Data to validate.
        dims
            Dimensions of the data.
        transformations
            Transformations to apply to the data.
        scale_factors
            Scale factors to apply for multiscale.
            If not None, a :class:`multiscale_spatial_image.MultiscaleSpatialImage` is returned.
        method
            Method to use for multiscale.
        chunks
            Chunks to use for dask array.

        Returns
        -------
        :class:`spatial_image.SpatialImage` or
        :class:`multiscale_spatial_image.MultiscaleSpatialImage`.
        """
        if 'name' in kwargs:
            raise ValueError('The `name` argument is not (yet) supported for raster data.')
        if isinstance(data, (DataArray, SpatialImage)):
            if not isinstance(data.data, DaskArray):
                data.data = from_array(data.data)
            if dims is not None:
                if set(dims).symmetric_difference(data.dims):
                    raise ValueError(f'`dims`: {dims} does not match `data.dims`: {data.dims}, please specify the dims only once.')
                logger.info('`dims` is specified redundantly: found also inside `data`.')
            else:
                dims = data.dims
            if set(dims).symmetric_difference(cls.dims.dims):
                raise ValueError(f'Wrong `dims`: {dims}. Expected {cls.dims.dims}.')
            _reindex = lambda d: d
        elif isinstance(data, (np.ndarray, DaskArray)):
            if not isinstance(data, DaskArray):
                data = from_array(data)
            if dims is None:
                dims = cls.dims.dims
                logger.info(f'no axes information specified in the object, setting `dims` to: {dims}')
            elif len(set(dims).symmetric_difference(cls.dims.dims)) > 0:
                raise ValueError(f'Wrong `dims`: {dims}. Expected {cls.dims.dims}.')
            _reindex = lambda d: dims.index(d)
        else:
            raise ValueError(f'Unsupported data type: {type(data)}.')
        if tuple(dims) != cls.dims.dims:
            try:
                if isinstance(data, DataArray):
                    data = data.transpose(*list(cls.dims.dims))
                elif isinstance(data, DaskArray):
                    data = data.transpose(*[_reindex(d) for d in cls.dims.dims])
                else:
                    raise ValueError(f'Unsupported data type: {type(data)}.')
                logger.info(f'Transposing `data` of type: {type(data)} to {cls.dims.dims}.')
            except ValueError as e:
                raise ValueError(f'Cannot transpose arrays to match `dims`: {dims}.', 'Try to reshape `data` or `dims`.') from e
        data = to_spatial_image(array_like=data, dims=cls.dims.dims, **kwargs)
        _parse_transformations(data, transformations)
        if scale_factors is not None:
            parsed_transform = _get_transformations(data)
            del data.attrs['transform']
            data = to_multiscale(data, scale_factors=scale_factors, method=method, chunks=chunks)
            _parse_transformations(data, parsed_transform)
        data = compute_coordinates(data)
        return data

    @singledispatchmethod
    def validate(self, data: Any) -> None:
        """
        Validate data.

        Parameters
        ----------
        data
            Data to validate.

        Raises
        ------
        ValueError
            If data is not valid.
        """
        raise ValueError(f'Unsupported data type: {type(data)}.')

    @validate.register(SpatialImage)
    def _(self, data: SpatialImage) -> None:
        super().validate(data)

    @validate.register(MultiscaleSpatialImage)
    def _(self, data: MultiscaleSpatialImage) -> None:
        for (j, k) in zip(data.keys(), [f'scale{i}' for i in np.arange(len(data.keys()))]):
            if j != k:
                raise ValueError(f'Wrong key for multiscale data, found: `{j}`, expected: `{k}`.')
        name = {list(data[i].data_vars.keys())[0] for i in data}
        if len(name) > 1:
            raise ValueError(f'Wrong name for datatree: `{name}`.')
        name = list(name)[0]
        for d in data:
            super().validate(data[d][name])

class Labels2DModel(RasterSchema):
    dims = DimsSchema((Y, X))
    array_type = ArrayTypeSchema(DaskArray)
    attrs = AttrsSchema({'transform': Transform_s})

    def __init__(self, *args: Any, **kwargs: Any) -> None:
        super().__init__(*args, dims=self.dims, array_type=self.array_type, attrs=self.attrs, **kwargs)

class Labels3DModel(RasterSchema):
    dims = DimsSchema((Z, Y, X))
    array_type = ArrayTypeSchema(DaskArray)
    attrs = AttrsSchema({'transform': Transform_s})

    def __init__(self, *args: Any, **kwargs: Any) -> None:
        super().__init__(*args, dims=self.dims, array_type=self.array_type, attrs=self.attrs, **kwargs)

class Image2DModel(RasterSchema):
    dims = DimsSchema((C, Y, X))
    array_type = ArrayTypeSchema(DaskArray)
    attrs = AttrsSchema({'transform': Transform_s})

    def __init__(self, *args: Any, **kwargs: Any) -> None:
        super().__init__(*args, dims=self.dims, array_type=self.array_type, attrs=self.attrs, **kwargs)

class Image3DModel(RasterSchema):
    dims = DimsSchema((C, Z, Y, X))
    array_type = ArrayTypeSchema(DaskArray)
    attrs = AttrsSchema({'transform': Transform_s})

    def __init__(self, *args: Any, **kwargs: Any) -> None:
        super().__init__(*args, dims=self.dims, array_type=self.array_type, attrs=self.attrs, **kwargs)

class ShapesModel:
    GEOMETRY_KEY = 'geometry'
    ATTRS_KEY = 'spatialdata_attrs'
    GEOS_KEY = 'geos'
    TYPE_KEY = 'type'
    NAME_KEY = 'name'
    RADIUS_KEY = 'radius'
    TRANSFORM_KEY = 'transform'

    @classmethod
    def validate(cls, data: GeoDataFrame) -> None:
        """
        Validate data.

        Parameters
        ----------
        data
            :class:`geopandas.GeoDataFrame` to validate.

        Returns
        -------
        None
        """
        if cls.GEOMETRY_KEY not in data:
            raise KeyError(f'GeoDataFrame must have a column named `{cls.GEOMETRY_KEY}`.')
        if not isinstance(data[cls.GEOMETRY_KEY], GeoSeries):
            raise ValueError(f'Column `{cls.GEOMETRY_KEY}` must be a GeoSeries.')
        if len(data[cls.GEOMETRY_KEY]) == 0:
            raise ValueError(f'Column `{cls.GEOMETRY_KEY}` is empty.')
        geom_ = data[cls.GEOMETRY_KEY].values[0]
        if not isinstance(geom_, (Polygon, MultiPolygon, Point)):
            raise ValueError(f'Column `{cls.GEOMETRY_KEY}` can only contain `Point`, `Polygon` or `MultiPolygon` shapes,but it contains {type(geom_)}.')
        if isinstance(geom_, Point) and cls.RADIUS_KEY not in data.columns:
            raise ValueError(f'Column `{cls.RADIUS_KEY}` not found.')
        if cls.TRANSFORM_KEY not in data.attrs:
            raise ValueError(f':class:`geopandas.GeoDataFrame` does not contain `{TRANSFORM_KEY}`.')

    @singledispatchmethod
    @classmethod
    def parse(cls, data: Any, **kwargs: Any) -> GeoDataFrame:
        """
        Parse shapes data.

        Parameters
        ----------
        data
            Data to parse:

                - If :class:`numpy.ndarray`, it assumes the shapes are parsed as
                  ragged arrays, in case of (Multi)`Polygons`.
                  Therefore additional arguments `offsets` and `geometry` must be provided
                - if `Path` or `str`, it's read as a GeoJSON file.
                - If :class:`geopandas.GeoDataFrame`, it's validated.

        geometry
            Geometry type of the shapes. The following geometries are supported:

                - 0: `Circles`
                - 3: `Polygon`
                - 6: `MultiPolygon`

        offsets
            In the case of (Multi)`Polygons` shapes, the offsets of the polygons must be provided.
        radius
            Size of the `Circles`. It must be provided if the shapes are `Circles`.
        index
            Index of the shapes, must be of type `str`. If None, it's generated automatically.
        transform
            Transform of points.
        kwargs
            Additional arguments for GeoJSON reader.

        Returns
        -------
        :class:`geopandas.GeoDataFrame`
        """
        raise NotImplementedError()

    @parse.register(np.ndarray)
    @classmethod
    def _(cls, data: np.ndarray, geometry: Literal[0, 3, 6], offsets: Optional[tuple[ArrayLike, ...]]=None, radius: Optional[Union[float, ArrayLike]]=None, index: Optional[ArrayLike]=None, transformations: Optional[MappingToCoordinateSystem_t]=None) -> GeoDataFrame:
        geometry = GeometryType(geometry)
        data = from_ragged_array(geometry_type=geometry, coords=data, offsets=offsets)
        geo_df = GeoDataFrame({'geometry': data})
        if GeometryType(geometry).name == 'POINT':
            if radius is None:
                raise ValueError('If `geometry` is `Circles`, `radius` must be provided.')
            geo_df[cls.RADIUS_KEY] = radius
        if index is not None:
            geo_df.index = index
        _parse_transformations(geo_df, transformations)
        cls.validate(geo_df)
        return geo_df

    @parse.register(str)
    @parse.register(Path)
    @classmethod
    def _(cls, data: Union[str, Path], radius: Optional[Union[float, ArrayLike]]=None, index: Optional[ArrayLike]=None, transformations: Optional[Any]=None, **kwargs: Any) -> GeoDataFrame:
        data = Path(data) if isinstance(data, str) else data
        gc: GeometryCollection = from_geojson(data.read_bytes(), **kwargs)
        if not isinstance(gc, GeometryCollection):
            raise ValueError(f'`{data}` does not contain a `GeometryCollection`.')
        geo_df = GeoDataFrame({'geometry': gc.geoms})
        if isinstance(geo_df['geometry'].iloc[0], Point):
            if radius is None:
                raise ValueError('If `geometry` is `Circles`, `radius` must be provided.')
            geo_df[cls.RADIUS_KEY] = radius
        if index is not None:
            geo_df.index = index
        _parse_transformations(geo_df, transformations)
        cls.validate(geo_df)
        return geo_df

    @parse.register(GeoDataFrame)
    @classmethod
    def _(cls, data: GeoDataFrame, transformations: Optional[MappingToCoordinateSystem_t]=None) -> GeoDataFrame:
        if 'geometry' not in data.columns:
            raise ValueError('`geometry` column not found in `GeoDataFrame`.')
        if isinstance(data['geometry'].iloc[0], Point) and cls.RADIUS_KEY not in data.columns:
            raise ValueError(f'Column `{cls.RADIUS_KEY}` not found.')
        _parse_transformations(data, transformations)
        cls.validate(data)
        return data

class PointsModel:
    ATTRS_KEY = 'spatialdata_attrs'
    INSTANCE_KEY = 'instance_key'
    FEATURE_KEY = 'feature_key'
    TRANSFORM_KEY = 'transform'
    NPARTITIONS = 1

    @classmethod
    def validate(cls, data: DaskDataFrame) -> None:
        """
        Validate data.

        Parameters
        ----------
        data
            :class:`dask.dataframe.core.DataFrame` to validate.

        Returns
        -------
        None
        """
        for ax in [X, Y, Z]:
            if ax in data.columns:
                assert data[ax].dtype in [np.float32, np.float64, np.int64]
        if cls.TRANSFORM_KEY not in data.attrs:
            raise ValueError(f':attr:`dask.dataframe.core.DataFrame.attrs` does not contain `{cls.TRANSFORM_KEY}`.')
        if cls.ATTRS_KEY in data.attrs and 'feature_key' in data.attrs[cls.ATTRS_KEY]:
            feature_key = data.attrs[cls.ATTRS_KEY][cls.FEATURE_KEY]
            if not is_categorical_dtype(data[feature_key]):
                logger.info(f'Feature key `{feature_key}`could be of type `pd.Categorical`. Consider casting it.')

    @singledispatchmethod
    @classmethod
    def parse(cls, data: Any, **kwargs: Any) -> DaskDataFrame:
        """
        Validate (or parse) points data.

        Parameters
        ----------
        data
            Data to parse:

                - If :class:`numpy.ndarray`, an `annotation` :class:`pandas.DataFrame`
                  must be provided, as well as the `feature_key` in the `annotation`. Furthermore,
                  :class:`numpy.ndarray` is assumed to have shape `(n_points, axes)`, with `axes` being
                  "x", "y" and optionally "z".
                - If :class:`pandas.DataFrame`, a `coordinates` mapping must be provided
                  with key as *valid axes* and value as column names in dataframe.

        annotation
            Annotation dataframe. Only if `data` is :class:`numpy.ndarray`.
        coordinates
            Mapping of axes names to column names in `data`. Only if `data` is :class:`pandas.DataFrame`.
        feature_key
            Feature key in `annotation` or `data`.
        instance_key
            Instance key in `annotation` or `data`.
        transformations
            Transformations of points.
        kwargs
            Additional arguments for :func:`dask.dataframe.from_array`.

        Returns
        -------
        :class:`dask.dataframe.core.DataFrame`
        """
        raise NotImplementedError()

    @parse.register(np.ndarray)
    @classmethod
    def _(cls, data: np.ndarray, annotation: Optional[pd.DataFrame]=None, feature_key: Optional[str]=None, instance_key: Optional[str]=None, transformations: Optional[MappingToCoordinateSystem_t]=None, **kwargs: Any) -> DaskDataFrame:
        if 'npartitions' not in kwargs and 'chunksize' not in kwargs:
            kwargs['npartitions'] = cls.NPARTITIONS
        assert len(data.shape) == 2
        ndim = data.shape[1]
        axes = [X, Y, Z][:ndim]
        table: DaskDataFrame = dd.from_pandas(pd.DataFrame(data, columns=axes), **kwargs)
        if annotation is not None:
            if feature_key is not None:
                feature_categ = dd.from_pandas(annotation[feature_key].astype(str).astype('category'), **kwargs)
                table[feature_key] = feature_categ
            if instance_key is not None:
                table[instance_key] = annotation[instance_key]
            for c in set(annotation.columns) - {feature_key, instance_key}:
                table[c] = dd.from_pandas(annotation[c], **kwargs)
            return cls._add_metadata_and_validate(table, feature_key=feature_key, instance_key=instance_key, transformations=transformations)
        return cls._add_metadata_and_validate(table, transformations=transformations)

    @parse.register(pd.DataFrame)
    @parse.register(DaskDataFrame)
    @classmethod
    def _(cls, data: pd.DataFrame, coordinates: Mapping[str, str], feature_key: Optional[str]=None, instance_key: Optional[str]=None, transformations: Optional[MappingToCoordinateSystem_t]=None, **kwargs: Any) -> DaskDataFrame:
        if 'npartitions' not in kwargs and 'chunksize' not in kwargs:
            kwargs['npartitions'] = cls.NPARTITIONS
        ndim = len(coordinates)
        axes = [X, Y, Z][:ndim]
        if isinstance(data, pd.DataFrame):
            table: DaskDataFrame = dd.from_pandas(pd.DataFrame(data[[coordinates[ax] for ax in axes]].to_numpy(), columns=axes), **kwargs)
            if feature_key is not None:
                feature_categ = dd.from_pandas(data[feature_key].astype(str).astype('category'), **kwargs)
                table[feature_key] = feature_categ
        elif isinstance(data, dd.DataFrame):
            table = data[[coordinates[ax] for ax in axes]]
            table.columns = axes
            if feature_key is not None and data[feature_key].dtype.name != 'category':
                table[feature_key] = data[feature_key].astype(str).astype('category')
        if instance_key is not None:
            table[instance_key] = data[instance_key]
        for c in set(data.columns) - {feature_key, instance_key, *coordinates.values()}:
            table[c] = data[c]
        return cls._add_metadata_and_validate(table, feature_key=feature_key, instance_key=instance_key, transformations=transformations)

    @classmethod
    def _add_metadata_and_validate(cls, data: DaskDataFrame, feature_key: Optional[str]=None, instance_key: Optional[str]=None, transformations: Optional[MappingToCoordinateSystem_t]=None) -> DaskDataFrame:
        assert isinstance(data, dd.DataFrame)
        if feature_key is not None or instance_key is not None:
            data.attrs[cls.ATTRS_KEY] = {}
        if feature_key is not None:
            assert feature_key in data.columns
            data.attrs[cls.ATTRS_KEY][cls.FEATURE_KEY] = feature_key
        if instance_key is not None:
            assert instance_key in data.columns
            data.attrs[cls.ATTRS_KEY][cls.INSTANCE_KEY] = instance_key
        for c in data.columns:
            if is_categorical_dtype(data[c]) and (not data[c].cat.known):
                try:
                    data[c] = data[c].cat.set_categories(data[c].head(1).cat.categories)
                except ValueError:
                    logger.info(f'Column `{c}` contains unknown categories. Consider casting it.')
        _parse_transformations(data, transformations)
        cls.validate(data)
        return data

class TableModel:
    ATTRS_KEY = 'spatialdata_attrs'
    REGION_KEY = 'region'
    REGION_KEY_KEY = 'region_key'
    INSTANCE_KEY = 'instance_key'

    def validate(self, data: AnnData) -> AnnData:
        """
        Validate the data.

        Parameters
        ----------
        data
            The data to validate.

        Returns
        -------
        The validated data.
        """
        if self.ATTRS_KEY not in data.uns:
            raise ValueError(f'`{self.ATTRS_KEY}` not found in `adata.uns`.')
        attr = data.uns[self.ATTRS_KEY]
        if 'region' not in attr:
            raise ValueError(f"`region` not found in `adata.uns['{self.ATTRS_KEY}']`.")
        if 'region_key' not in attr:
            raise ValueError(f"`region_key` not found in `adata.uns['{self.ATTRS_KEY}']`.")
        if 'instance_key' not in attr:
            raise ValueError(f"`instance_key` not found in `adata.uns['{self.ATTRS_KEY}']`.")
        if attr[self.REGION_KEY_KEY] not in data.obs:
            raise ValueError(f'`{attr[self.REGION_KEY_KEY]}` not found in `adata.obs`.')
        if attr[self.INSTANCE_KEY] not in data.obs:
            raise ValueError(f'`{attr[self.INSTANCE_KEY]}` not found in `adata.obs`.')
        expected_regions = attr[self.REGION_KEY] if isinstance(attr[self.REGION_KEY], list) else [attr[self.REGION_KEY]]
        found_regions = data.obs[attr[self.REGION_KEY_KEY]].unique().tolist()
        if len(set(expected_regions).symmetric_difference(set(found_regions))) > 0:
            raise ValueError(f'Regions in the AnnData object and `{attr[self.REGION_KEY_KEY]}` do not match.')
        return data

    @classmethod
    def parse(cls, adata: AnnData, region: Optional[Union[str, list[str]]]=None, region_key: Optional[str]=None, instance_key: Optional[str]=None) -> AnnData:
        """
        Parse the :class:`anndata.AnnData` to be compatible with the model.

        Parameters
        ----------
        adata
            The AnnData object.
        region
            Region(s) to be used.
        region_key
            Key in `adata.obs` that specifies the region.
        instance_key
            Key in `adata.obs` that specifies the instance.

        Returns
        -------
        :class:`anndata.AnnData`.
        """
        n_args = sum([region is not None, region_key is not None, instance_key is not None])
        if n_args > 0:
            if cls.ATTRS_KEY in adata.uns:
                raise ValueError(f'Either pass `{cls.REGION_KEY}`, `{cls.REGION_KEY_KEY}` and `{cls.INSTANCE_KEY}`as arguments or have them in `adata.uns[{cls.ATTRS_KEY!r}]`.')
        elif cls.ATTRS_KEY in adata.uns:
            attr = adata.uns[cls.ATTRS_KEY]
            region = attr[cls.REGION_KEY]
            region_key = attr[cls.REGION_KEY_KEY]
            instance_key = attr[cls.INSTANCE_KEY]
        if region_key is None:
            raise ValueError(f'`{cls.REGION_KEY_KEY}` must be provided.')
        if isinstance(region, np.ndarray):
            region = region.tolist()
        if region is None:
            raise ValueError(f'`{cls.REGION_KEY}` must be provided.')
        region_: list[str] = region if isinstance(region, list) else [region]
        if not adata.obs[region_key].isin(region_).all():
            raise ValueError(f'`adata.obs[{region_key}]` values do not match with `{cls.REGION_KEY}` values.')
        if not is_categorical_dtype(adata.obs[region_key]):
            warnings.warn(f'Converting `{cls.REGION_KEY_KEY}: {region_key}` to categorical dtype.', UserWarning, stacklevel=2)
            adata.obs[region_key] = pd.Categorical(adata.obs[region_key])
        if instance_key is None:
            raise ValueError('`instance_key` must be provided.')
        attr = {'region': region, 'region_key': region_key, 'instance_key': instance_key}
        adata.uns[cls.ATTRS_KEY] = attr
        return adata
Schema_t = Union[type[Image2DModel], type[Image3DModel], type[Labels2DModel], type[Labels3DModel], type[PointsModel], type[ShapesModel], type[TableModel]]

def get_model(e: SpatialElement) -> Schema_t:
    """
    Get the model for the given element.

    Parameters
    ----------
    e
        The element.

    Returns
    -------
    The SpatialData model.
    """

    def _validate_and_return(schema: Schema_t, e: SpatialElement) -> Schema_t:
        schema().validate(e)
        return schema
    if isinstance(e, (SpatialImage, MultiscaleSpatialImage)):
        axes = get_axes_names(e)
        if 'c' in axes:
            if 'z' in axes:
                return _validate_and_return(Image3DModel, e)
            return _validate_and_return(Image2DModel, e)
        if 'z' in axes:
            return _validate_and_return(Labels3DModel, e)
        return _validate_and_return(Labels2DModel, e)
    if isinstance(e, GeoDataFrame):
        return _validate_and_return(ShapesModel, e)
    if isinstance(e, DaskDataFrame):
        return _validate_and_return(PointsModel, e)
    if isinstance(e, AnnData):
        return _validate_and_return(TableModel, e)
    raise TypeError(f'Unsupported type {type(e)}')