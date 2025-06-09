def _py2java(gateway, obj):
    """ Convert Python object into Java """
    if isinstance(obj, RDD):
        obj = _to_java_object_rdd(obj)
    elif isinstance(obj, DataFrame):
        obj = obj._jdf
    elif isinstance(obj, SparkContext):
        obj = obj._jsc
    elif isinstance(obj, (list, tuple)):
        obj = ListConverter().convert([_py2java(gateway, x) for x in obj], gateway._gateway_client)
    elif isinstance(obj, dict):
        result = {}
        for (key, value) in obj.items():
            result[key] = _py2java(gateway, value)
        obj = MapConverter().convert(result, gateway._gateway_client)
    elif isinstance(obj, JavaValue):
        obj = obj.value
    elif isinstance(obj, JavaObject):
        pass
    elif isinstance(obj, (int, long, float, bool, bytes, unicode)):
        pass
    else:
        data = bytearray(PickleSerializer().dumps(obj))
        obj = gateway.jvm.org.apache.spark.bigdl.api.python.BigDLSerDe.loads(data)
    return obj