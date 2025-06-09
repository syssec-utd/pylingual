from cwrap import BaseCClass
from ecl import EclPrototype

class WellSegment(BaseCClass):
    TYPE_NAME = 'well_segment'
    _active = EclPrototype('bool well_segment_active(well_segment)')
    _main_stem = EclPrototype('bool well_segment_main_stem(well_segment)')
    _nearest_wellhead = EclPrototype('bool well_segment_nearest_wellhead(well_segment)')
    _id = EclPrototype('int well_segment_get_id(well_segment)')
    _link_count = EclPrototype('int well_segment_get_link_count(well_segment)')
    _branch_id = EclPrototype('int well_segment_get_branch_id(well_segment)')
    _outlet_id = EclPrototype('int well_segment_get_outlet_id(well_segment)')
    _depth = EclPrototype('double well_segment_get_depth(well_segment)')
    _length = EclPrototype('double well_segment_get_length(well_segment)')
    _total_length = EclPrototype('double well_segment_get_total_length(well_segment)')
    _diameter = EclPrototype('double well_segment_get_diameter(well_segment)')

    def __init__(self):
        raise NotImplementedError('Class can not be instantiated directly')

    def free(self):
        pass

    def __repr__(self):
        return 'WellSegment(%s) at 0x%x' % (str(self), self._address())

    def __str__(self):
        return '{Segment ID:%d   BranchID:%d  Length:%g}' % (self.id(), self.branchId(), self.length())

    def id(self):
        """@rtype: int"""
        return self._id()

    def linkCount(self):
        """@rtype: int"""
        return self._link_count()

    def branchId(self):
        """@rtype: int"""
        return self._branch_id()

    def outletId(self):
        """@rtype: int"""
        return self._outlet_id()

    def isActive(self):
        """@rtype: bool"""
        return self._active()

    def isMainStem(self):
        """@rtype: bool"""
        return self._main_stem()

    def isNearestWellHead(self):
        """@rtype: bool"""
        return self._nearest_wellhead()

    def depth(self):
        """@rtype: float"""
        return self._depth()

    def __len__(self):
        return self.length()

    def length(self):
        """@rtype: float"""
        return self._length()

    def totalLength(self):
        """@rtype: float"""
        return self._total_length()

    def diameter(self):
        """@rtype: float"""
        return self._diameter()