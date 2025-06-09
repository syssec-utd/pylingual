from ...gmpv208 import Gmpv208TestCase
from .trashcan import GmpEmptyTrashcanTestMixin, GmpRestoreFromTrashcanTestMixin

class Gmpv208EmptyTrashcanTestCase(GmpEmptyTrashcanTestMixin, Gmpv208TestCase):
    pass

class Gmpv208RestoreFromTrashcanTestCase(GmpRestoreFromTrashcanTestMixin, Gmpv208TestCase):
    pass