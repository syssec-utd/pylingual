from typing import TYPE_CHECKING
from .lazy import lazy_import

if TYPE_CHECKING:
    import transformers
else:
    lazy_import("transformers")

SEGMENTATION_STEP = "Segmentation"
TRANSLATION_STEP = "Translation"
CFLOW_STEP = "Control Flow"
CORRECTION_STEP = "Error Correction"


class TrackedList:
    """
    List-like class that calls self.progress on each element access
    Used to display progress bars when PyLingual is run as a script, does nothing otherwise
    """

    def __init__(self, name: str, x: list, check_timeout: callable = None):
        self.name = name
        self.x = x
        self.i = 0
        self.check_timeout = check_timeout
        self.init()

    # overwritten when run as script
    def init(self):
        pass

    def __getitem__(self, i):
        if self.check_timeout:
            self.check_timeout()
        if isinstance(i, slice):
            # batched access: advance progress by the batch size
            items = self.x[i]
            self.progress(len(items))
            return items
        self.progress(i - self.i)
        self.i = i
        return self.x[i]

    def __len__(self):
        return len(self.x)

    def __iter__(self):
        return self

    def __next__(self):
        if self.check_timeout:
            self.check_timeout()
        try:
            n = self.x[self.i]
        except:
            raise StopIteration()
        self.progress(1)
        self.i += 1
        return n

    # overwritten when run as script
    def progress(self, i: int):
        pass


class TrackedDataset(TrackedList):
    """
    Like TrackedList, but inherits from Dataset
    """

    def __init__(self, name: str, x: list, check_timeout: callable = None):
        super().__init__(name, x, check_timeout)
        TrackedDataset.__bases__ = (TrackedList, transformers.pipelines.base.Dataset)
