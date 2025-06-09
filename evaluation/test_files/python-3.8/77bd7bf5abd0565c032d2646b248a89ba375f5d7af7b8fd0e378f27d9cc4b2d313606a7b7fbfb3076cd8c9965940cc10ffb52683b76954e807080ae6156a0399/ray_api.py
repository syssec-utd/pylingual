def create_ray_multiprocessing_backend():
    from bigdl.nano.deps.ray.ray_backend import RayBackend
    return RayBackend()

def create_ray_strategy(*args, **kwargs):
    """Create ray strategy."""
    from .ray_distributed import RayStrategy
    return RayStrategy(*args, **kwargs)

def distributed_ray(*args, **kwargs):
    from bigdl.nano.utils.common import invalidInputError
    invalidInputError(False, 'bigdl-nano no longer support ray backend when using pytorch lightning 1.4, please upgrade your pytorch lightning to 1.6.4')