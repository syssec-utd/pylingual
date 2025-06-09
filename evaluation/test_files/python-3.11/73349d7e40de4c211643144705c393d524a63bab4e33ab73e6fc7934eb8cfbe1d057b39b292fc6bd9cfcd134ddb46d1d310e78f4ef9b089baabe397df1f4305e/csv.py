import io
import json
import pandas as pd
from zipfile import ZipFile
from halo import Halo
import csv
from mt import np, ctx, path, aio
csv.field_size_limit(262144)
__all__ = ['metadata', 'metadata2dtypes', 'read_csv_asyn', 'read_csv', 'to_csv_asyn', 'to_csv']

def metadata(df):
    """Extracts the metadata of a dataframe.

    Parameters
    ----------
        df : pandas.DataFrame

    Returns
    -------
        meta : json-like
            metadata describing the dataframe
    """
    meta = {}
    if list(df.index.names) != [None]:
        index_names = list(df.index.names)
        df = df.reset_index(drop=False)
    else:
        index_names = []
    meta = {}
    for x in df.dtypes.index:
        dtype = df.dtypes.loc[x]
        name = dtype.name
        if name != 'category':
            meta[x] = name
        else:
            meta[x] = ['category', df[x].cat.categories.tolist(), df[x].cat.ordered]
    meta = {'columns': meta, 'index_names': index_names}
    return meta

def metadata2dtypes(meta):
    """Creates a dictionary of dtypes from the metadata returned by metadata() function."""
    res = {}
    s = meta['columns']
    for x in s:
        y = s[x]
        if y == 'datetime64[ns]':
            y = 'object'
        elif isinstance(y, list) and y[0] == 'category':
            y = 'object'
        res[x] = np.dtype(y)
    return res

async def read_csv_asyn(filepath, show_progress=False, context_vars: dict={}, **kwargs):

    def postprocess(df):
        for key in df:
            if key.endswith('_df_nd_ravel'):
                has_ndarray = True
                break
        else:
            has_ndarray = False
        if has_ndarray:
            df = df.copy()
            fromlist = lambda x: None if x is None else np.array(json.loads(x))
            for key in df:
                if key.endswith('_df_nd_ravel'):
                    df[key] = df[key].apply(fromlist)
                elif key.endswith('_df_nd_shape'):
                    df[key] = df[key].apply(fromlist)
        return df

    def process(filepath, data1: io.StringIO, data2, show_progress=False, **kwargs):
        text = "dfloading '{}'".format(filepath)
        spinner = Halo(text=text, spinner='dots', enabled=show_progress)
        spinner.start()
        ts = pd.Timestamp.now()
        cnt = 0
        dfs = []
        for df in pd.read_csv(data1, quoting=csv.QUOTE_NONNUMERIC, chunksize=1024, **kwargs):
            dfs.append(df)
            cnt += len(df)
            td = (pd.Timestamp.now() - ts).total_seconds() + 0.001
            s = '{} rows ({} rows/sec)'.format(cnt, cnt / td)
            spinner.text = s
        df = pd.concat(dfs, sort=False)
        if data2 is None:
            text = "dfloaded {} rows from '{}'".format(cnt, filepath)
            spinner.succeed(text)
            return postprocess(df)
        try:
            index_col = kwargs.pop('index_col', None)
            dtype = kwargs.pop('dtype', None)
            spinner.text = 'loading the metadata'
            meta = None if data2 is None else json.loads(data2)
            if meta is None:
                text = "dfloaded {} rows with no metadata from '{}'".format(cnt, filepath)
                spinner.succeed(text)
                return postprocess(df)
            kwargs['dtype'] = 'object'
            if index_col is None and len(meta['index_names']) > 0:
                index_col = meta['index_names']
            s = meta['columns']
            for x in s:
                spinner.text = "checking column '{}'".format(x)
                y = s[x]
                if y == 'datetime64[ns]':
                    df[x] = pd.to_datetime(df[x])
                elif isinstance(y, list) and y[0] == 'category':
                    cat_dtype = pd.api.types.CategoricalDtype(categories=y[1], ordered=y[2])
                    df[x] = df[x].astype(cat_dtype)
                elif y == 'int64':
                    df[x] = df[x].astype(np.int64)
                elif y == 'uint8':
                    df[x] = df[x].astype(np.uint8)
                elif y == 'float64':
                    df[x] = df[x].astype(np.float64)
                elif y == 'bool':
                    df[x] = df[x].replace('True', True).replace('False', False).astype(np.bool)
                elif y == 'object':
                    pass
                else:
                    raise OSError('Unknown dtype for conversion {}'.format(y))
            if index_col is not None and len(index_col) > 0:
                df = df.set_index(index_col, drop=True)
            text = "dfloaded {} rows from '{}'".format(cnt, filepath)
            spinner.succeed(text)
        except:
            spinner.fail("dfloaded {} rows, then failed, from '{}'".format(cnt, filepath))
            raise
        return postprocess(df)
    with path.lock(filepath, to_write=False):
        if filepath.lower().endswith('.csv.zip'):
            data = await aio.read_binary(filepath, context_vars=context_vars)
            with ZipFile(io.BytesIO(data), mode='r') as myzip:
                filename = path.basename(filepath)[:-4]
                fp1 = myzip.open(filename, mode='r', force_zip64=True)
                data1 = fp1.read().decode()
                meta_filename = filename[:-4] + '.meta'
                if meta_filename in myzip.namelist():
                    data2 = myzip.open(meta_filename, mode='r').read()
                else:
                    data2 = None
                return process(filepath, data1, data2, show_progress=show_progress, **kwargs)
        else:
            fp1 = filepath
            data1 = await aio.read_text(fp1, context_vars=context_vars)
            meta_filepath = path.basename(filepath)[:-4] + '.meta'
            if path.exists(meta_filepath):
                data2 = await aio.read_text(meta_filepath, context_vars=context_vars)
            else:
                data2 = None
            return process(filepath, io.StringIO(data1), data2, show_progress=show_progress, **kwargs)
read_csv_asyn.__doc__ = "An asyn function that read a CSV file or a CSV-zipped file into a pandas.DataFrame, passing all arguments to :func:`pandas.read_csv`. Keyword argument 'show_progress' tells whether to show progress in the terminal. Keyword 'context_vars' is a dictionary of context variables within which the function runs. It must include `context_vars['async']` to tell whether to invoke the function asynchronously or not.\n" + pd.read_csv.__doc__

def read_csv(filepath, show_progress=False, **kwargs):
    return aio.srun(read_csv_asyn, filepath, show_progress=show_progress, **kwargs)
read_csv.__doc__ = "Read a CSV file or a CSV-zipped file into a pandas.DataFrame, passing all arguments to :func:`pandas.read_csv`. Keyword argument 'show_progress' tells whether to show progress in the terminal.\n" + pd.read_csv.__doc__

async def to_csv_asyn(df, filepath, index='auto', file_mode: int=436, show_progress=False, context_vars: dict={}, file_write_delayed: bool=False, **kwargs):
    for key in df:
        if key.endswith('_df_nd_ravel'):
            has_ndarray = True
            break
    else:
        has_ndarray = False
    if has_ndarray:
        df = df.copy()
        tolist = lambda x: None if x is None else json.dumps(x.tolist())
        for key in df:
            if key.endswith('_df_nd_ravel'):
                df[key] = df[key].apply(tolist)
            elif key.endswith('_df_nd_shape'):
                df[key] = df[key].apply(tolist)
    spinner = Halo(text="dfsaving '{}'".format(filepath), spinner='dots') if show_progress else ctx.nullcontext()
    with spinner:
        try:
            if index == 'auto':
                index = bool(df.index.name)
            with path.lock(filepath, to_write=True):
                if filepath.lower().endswith('.csv.zip'):
                    filepath2 = filepath + '.tmp.zip'
                    dirpath = path.dirname(filepath)
                    if dirpath:
                        path.make_dirs(dirpath)
                    if not path.exists(dirpath):
                        await aio.sleep(1, context_vars=context_vars)
                    zipdata = io.BytesIO()
                    with ZipFile(zipdata, mode='w') as myzip:
                        filename = path.basename(filepath)[:-4]
                        with myzip.open(filename, mode='w', force_zip64=True) as f:
                            data = df.to_csv(None, index=index, quoting=csv.QUOTE_NONNUMERIC, **kwargs)
                            f.write(data.encode())
                        if show_progress:
                            spinner.text = 'saved CSV content'
                        with myzip.open(filename[:-4] + '.meta', mode='w') as f:
                            data = json.dumps(metadata(df))
                            f.write(data.encode())
                    res = await aio.write_binary(filepath2, zipdata.getvalue(), file_mode=file_mode, context_vars=context_vars, file_write_delayed=file_write_delayed)
                    if show_progress:
                        spinner.text = 'saved metadata'
                else:
                    filepath2 = filepath + '.tmp.csv'
                    dirpath = path.dirname(filepath)
                    if dirpath:
                        path.make_dirs(dirpath)
                    if not path.exists(dirpath):
                        await aio.sleep(1, context_vars=context_vars)
                    data = df.to_csv(None, index=index, quoting=csv.QUOTE_NONNUMERIC, **kwargs)
                    res = await aio.write_text(filepath2, data, file_mode=file_mode, context_vars=context_vars, file_write_delayed=file_write_delayed)
                    if show_progress:
                        spinner.text = 'saved CSV content'
                    filepath3 = filepath[:-4] + '.meta'
                    await aio.json_save(filepath3, metadata(df), file_mode=file_mode, context_vars=context_vars)
                    if show_progress:
                        spinner.text = 'saved metadata'
                await path.remove_asyn(filepath, context_vars=context_vars)
                if path.exists(filepath) or not path.exists(filepath2):
                    await aio.sleep(1, context_vars=context_vars)
                await path.rename_asyn(filepath2, filepath, context_vars=context_vars)
                if isinstance(spinner, Halo):
                    spinner.succeed("dfsaved '{}'".format(filepath))
                return res
        except:
            if isinstance(spinner, Halo):
                spinner.succeed("failed to dfsave '{}'".format(filepath))
            raise
to_csv_asyn.__doc__ = "An asyn function that writes DataFrame to a comma-separated values (.csv) file or a CSV-zipped (.csv.zip) file. If keyword 'index' is 'auto' (default), the index column is written if and only if it has a name. Keyword argument 'show_progress' tells whether to show progress in the terminal. Keyword 'file_mode' specifies the file mode when writing (passed directly to os.chmod if not None). Keyword 'context_vars' is a dictionary of context variables within which the function runs. Keyword 'file_write_delayed' (see :func:`mt.base.aio.files.write_binary`) is now acceptable. It must include `context_vars['async']` to tell whether to invoke the function asynchronously or not. The remaining arguments and keywords are passed directly to :func:`DataFrame.to_csv`.\n" + pd.DataFrame.to_csv.__doc__

def to_csv(df, filepath, index='auto', file_mode=436, show_progress=False, **kwargs):
    return aio.srun(to_csv_asyn, df, filepath, index=index, file_mode=file_mode, show_progress=show_progress, **kwargs)
to_csv.__doc__ = "Write DataFrame to a comma-separated values (.csv) file or a CSV-zipped (.csv.zip) file. If keyword 'index' is 'auto' (default), the index column is written if and only if it has a name. Keyword 'file_mode' specifies the file mode when writing (passed directly to os.chmod if not None). Keyword argument 'show_progress' tells whether to show progress in the terminal. Keyword 'file_write_delayed' (see :func:`mt.base.aio.files.write_binary`) is now acceptable. The remaining arguments and keywords are passed directly to :func:`DataFrame.to_csv`.\n" + pd.DataFrame.to_csv.__doc__