supported_tuples = [(3, x) for x in range(6, 16)]
version_str = {f"{x[0]}{x[1]}": x for x in supported_tuples} | {
    f"{x[0]}.{x[1]}": x for x in supported_tuples
}


class PythonVersion:
    major: int
    minor: int
    _t: tuple[int, int]

    @staticmethod
    def normalize(x) -> tuple[int, int] | None:
        if isinstance(x, PythonVersion):
            return x._t
        if isinstance(x, float):
            if x == 3.1:
                x = "3.10"
            x = str(x)
        if isinstance(x, str):
            x = version_str.get(".".join(map(str.strip, x.split(".")[:2])))
        if isinstance(x, int):
            x = (3, x)
        if isinstance(x, tuple):
            if len(x) >= 2 and isinstance(x[0], int) and isinstance(x[1], int):
                return x[:2]

    def is_supported(self) -> bool:
        return self.as_tuple() in supported_tuples

    def __init__(self, x):
        v = PythonVersion.normalize(x)
        if v is None:
            raise ValueError(f"version {x} is invalid")
        self.major, self.minor = v
        self._t = v

    def __str__(self):
        return f"{self.major}.{self.minor}"

    def __eq__(self, o):
        return PythonVersion.normalize(o) == self._t

    def __ne__(self, o):
        norm = PythonVersion.normalize(o)
        return norm is not None and self._t != norm

    def __ge__(self, o):
        norm = PythonVersion.normalize(o)
        return norm is not None and self._t >= norm

    def __le__(self, o):
        norm = PythonVersion.normalize(o)
        return norm is not None and self._t <= norm

    def __gt__(self, o):
        norm = PythonVersion.normalize(o)
        return norm is not None and self._t > norm

    def __lt__(self, o):
        norm = PythonVersion.normalize(o)
        return norm is not None and self._t < norm

    def __hash__(self):
        return hash(self._t)

    def __getitem__(self, i):
        return self._t[i]

    def as_str(self):
        return str(self)

    def as_float(self):
        return float(str(self))

    def as_tuple(self):
        return self._t


supported_versions = list(map(PythonVersion, supported_tuples))
