from refinery.units import Arg, Unit

class group(Unit):
    """
    Group incoming chunks into frames of the given size.
    """

    def __init__(self, size: Arg.Number(help='Size of each group; must be at least 2.', bound=(2, None))):
        super().__init__(size=size)

    def process(self, data):
        members = data.temp or ()
        if len(members) >= self.args.size:
            raise RuntimeError(f'received {len(members) + 1} items in group')
        yield data
        yield from members

    def filter(self, chunks):
        members = []
        header = None
        for chunk in chunks:
            if not chunk.visible:
                yield chunk
                continue
            if len(members) > self.args.size - 2:
                yield header
                header = None
            if header is None:
                chunk.temp = members
                header = chunk
                members.clear()
            else:
                members.append(chunk)
        if header is not None:
            yield header