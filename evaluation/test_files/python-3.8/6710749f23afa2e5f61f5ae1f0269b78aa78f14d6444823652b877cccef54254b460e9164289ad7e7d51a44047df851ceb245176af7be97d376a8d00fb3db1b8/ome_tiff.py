from typing import Any, Dict, Mapping, Optional, Sequence, Tuple, Union, cast
import jsonpickle as json
import numpy as np
import tifffile
from tiledb.cc import WebpInputFormat
from .axes import Axes
from .base import ImageConverter, ImageReader, ImageWriter

class OMETiffReader(ImageReader):

    def __init__(self, input_path: str, extra_tags: Sequence[Union[str, int]]=()):
        """
        OME-TIFF image reader

        :param input_path: The path to the TIFF image
        :param extra_tags: Extra tags to read, specified either by name or by int code.
        """
        self._extra_tags = extra_tags
        self._tiff = tifffile.TiffFile(input_path)
        self._series = self._tiff.series[0]
        omexml = self._tiff.ome_metadata
        self._metadata = tifffile.xml2dict(omexml) if omexml else {}

    def __exit__(self, exc_type: Any, exc_val: Any, exc_tb: Any) -> None:
        self._tiff.close()

    @property
    def axes(self) -> Axes:
        return Axes(self._series.axes.replace('S', 'C'))

    @property
    def channels(self) -> Sequence[str]:
        if self.webp_format is WebpInputFormat.WEBP_RGB:
            return ('RED', 'GREEN', 'BLUE')
        try:
            channels = self._metadata['OME']['Image'][0]['Pixels']['Channel']
            if not isinstance(channels, Sequence):
                channels = [channels]
        except KeyError:
            return ()
        return tuple((c.get('Name') or f'Channel {i}' for (i, c) in enumerate(channels)))

    @property
    def webp_format(self) -> WebpInputFormat:
        if self._series.keyframe.photometric == tifffile.PHOTOMETRIC.RGB:
            return WebpInputFormat.WEBP_RGB
        if self._original_metadata('PhotometricInterpretation') == 'RGB':
            return WebpInputFormat.WEBP_RGB
        return WebpInputFormat.WEBP_NONE

    @property
    def level_count(self) -> int:
        return len(self._series.levels)

    def level_dtype(self, level: int) -> np.dtype:
        return self._series.levels[level].dtype

    def level_shape(self, level: int) -> Tuple[int, ...]:
        return cast(Tuple[int, ...], self._series.levels[level].shape)

    def level_image(self, level: int, tile: Optional[Tuple[slice, ...]]=None) -> np.ndarray:
        if tile is None:
            return self._series.levels[level].asarray()
        try:
            import zarr
        except ImportError:
            raise ImportError('zarr required for reading a Tiff tile region')
        if not hasattr(self, '_zarr_group'):
            store = self._series.aszarr(multiscales=True)
            self._zarr_group = zarr.open(store, mode='r')
        return np.asarray(self._zarr_group[level][tile])

    def level_metadata(self, level: int) -> Dict[str, Any]:
        if level == 0:
            metadata = dict(self._metadata, axes=self._series.axes)
        else:
            metadata = None
        keyframe = self._series.levels[level].keyframe
        extratags = []
        get_tag = keyframe.tags.get
        for key in self._extra_tags:
            tag = get_tag(key)
            if tag is not None:
                extratags.append(tag.astuple())
        write_kwargs = dict(subifds=self.level_count - 1 if level == 0 else None, metadata=metadata, extratags=extratags, photometric=keyframe.photometric, planarconfig=keyframe.planarconfig, extrasamples=keyframe.extrasamples, rowsperstrip=keyframe.rowsperstrip, bitspersample=keyframe.bitspersample, compression=keyframe.compression, predictor=keyframe.predictor, subsampling=keyframe.subsampling, jpegtables=keyframe.jpegtables, colormap=keyframe.colormap, subfiletype=keyframe.subfiletype, software=keyframe.software, tile=keyframe.tile, datetime=keyframe.datetime, resolution=keyframe.resolution, resolutionunit=keyframe.resolutionunit)
        return {'json_write_kwargs': json.dumps(write_kwargs)}

    @property
    def group_metadata(self) -> Dict[str, Any]:
        writer_kwargs = dict(bigtiff=self._tiff.is_bigtiff, byteorder=self._tiff.byteorder, append=self._tiff.is_appendable, imagej=self._tiff.is_imagej, ome=self._tiff.is_ome)
        return {'json_tiffwriter_kwargs': json.dumps(writer_kwargs)}

    def _original_metadata(self, key: str, default: Any=None) -> Any:
        try:
            xmlanns = self._metadata['OME']['StructuredAnnotations']['XMLAnnotation']
            for xmlann in xmlanns:
                entry = xmlann['Value']['OriginalMetadata']
                if entry['Key'] == key:
                    return entry['Value']
        except KeyError:
            pass
        return default

class OMETiffWriter(ImageWriter):

    def __init__(self, output_path: str):
        self._output_path = output_path

    def write_group_metadata(self, metadata: Mapping[str, Any]) -> None:
        tiffwriter_kwargs = json.loads(metadata['json_tiffwriter_kwargs'])
        self._writer = tifffile.TiffWriter(self._output_path, shaped=False, **tiffwriter_kwargs)

    def write_level_image(self, level: int, image: np.ndarray, metadata: Mapping[str, Any]) -> None:
        write_kwargs = json.loads(metadata['json_write_kwargs'])
        self._writer.write(image, **write_kwargs)

    def __exit__(self, exc_type: Any, exc_val: Any, exc_tb: Any) -> None:
        self._writer.close()

class OMETiffConverter(ImageConverter):
    """Converter of Tiff-supported images to TileDB Groups of Arrays"""
    _ImageReaderType = OMETiffReader
    _ImageWriterType = OMETiffWriter