def scatter(input, devices, streams=None):
    """Scatters tensor across multiple GPUs.
    """
    if streams is None:
        streams = [None] * len(devices)
    if isinstance(input, list):
        chunk_size = (len(input) - 1) // len(devices) + 1
        outputs = [scatter(input[i], [devices[i // chunk_size]], [streams[i // chunk_size]]) for i in range(len(input))]
        return outputs
    elif isinstance(input, torch.Tensor):
        output = input.contiguous()
        stream = streams[0] if output.numel() > 0 else None
        with torch.cuda.device(devices[0]), torch.cuda.stream(stream):
            output = output.cuda(devices[0], non_blocking=True)
        return output
    else:
        raise Exception('Unknown type {}.'.format(type(input)))