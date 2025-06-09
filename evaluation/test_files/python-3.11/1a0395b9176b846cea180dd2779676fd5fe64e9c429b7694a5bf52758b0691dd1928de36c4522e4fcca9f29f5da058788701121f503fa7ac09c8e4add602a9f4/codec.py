import base64
import pickle
import cloudpickle

def loads_base64(encoded):
    decoded = base64.b64decode(encoded)
    return cloudpickle.loads(decoded)

def dumps_base64(obj, to_ascii=True):
    serialized = cloudpickle.dumps(obj, protocol=pickle.HIGHEST_PROTOCOL)
    encoded = base64.b64encode(serialized)
    return encoded.decode('ascii') if to_ascii else encoded