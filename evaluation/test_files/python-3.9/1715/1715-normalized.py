def readImages(path, sc=None, minParitions=1, bigdl_type='float'):
    """
        Read the directory of images into DataFrame from the local or remote source.
        :param path Directory to the input data files, the path can be comma separated paths as the
                list of inputs. Wildcards path are supported similarly to sc.binaryFiles(path).
        :param min_partitions A suggestion value of the minimal splitting number for input data.
        :return DataFrame with a single column "image"; Each record in the column represents one image
                record: Row (uri, height, width, channels, CvType, bytes)
        """
    df = callBigDlFunc(bigdl_type, 'dlReadImage', path, sc, minParitions)
    df._sc._jsc = sc._jsc
    return df