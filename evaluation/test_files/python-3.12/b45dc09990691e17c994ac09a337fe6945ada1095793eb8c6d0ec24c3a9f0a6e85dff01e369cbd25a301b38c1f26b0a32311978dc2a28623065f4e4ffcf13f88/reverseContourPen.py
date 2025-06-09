from fontTools.misc.arrayTools import pairwise
from fontTools.pens.filterPen import ContourFilterPen
__all__ = ['reversedContour', 'ReverseContourPen']

class ReverseContourPen(ContourFilterPen):
    """Filter pen that passes outline data to another pen, but reversing
    the winding direction of all contours. Components are simply passed
    through unchanged.

    Closed contours are reversed in such a way that the first point remains
    the first point.
    """

    def filterContour(self, contour):
        return reversedContour(contour)

def reversedContour(contour):
    """ Generator that takes a list of pen's (operator, operands) tuples,
    and yields them with the winding direction reversed.
    """
    if not contour:
        return
    assert len(contour) > 1, 'invalid contour'
    contourType = contour.pop()[0]
    assert contourType in ('endPath', 'closePath')
    closed = contourType == 'closePath'
    firstType, firstPts = contour.pop(0)
    assert firstType in ('moveTo', 'qCurveTo'), 'invalid initial segment type: %r' % firstType
    firstOnCurve = firstPts[-1]
    if firstType == 'qCurveTo':
        assert firstOnCurve is None, "off-curve only paths must end with 'None'"
        assert not contour, 'only one qCurveTo allowed per off-curve path'
        firstPts = (firstPts[0],) + tuple(reversed(firstPts[1:-1])) + (None,)
    if not contour:
        if firstType == 'moveTo':
            closed = False
        else:
            closed = True
        yield (firstType, firstPts)
    else:
        lastType, lastPts = contour[-1]
        lastOnCurve = lastPts[-1]
        if closed:
            yield (firstType, firstPts)
            if firstOnCurve != lastOnCurve:
                yield ('lineTo', (lastOnCurve,))
                contour[-1] = (lastType, tuple(lastPts[:-1]) + (firstOnCurve,))
            if len(contour) > 1:
                secondType, secondPts = contour[0]
            else:
                secondType, secondPts = (lastType, lastPts)
            if secondType == 'lineTo' and firstPts != secondPts:
                del contour[0]
                if contour:
                    contour[-1] = (lastType, tuple(lastPts[:-1]) + secondPts)
        else:
            yield (firstType, (lastOnCurve,))
            contour[-1] = (lastType, tuple(lastPts[:-1]) + (firstOnCurve,))
        for (curType, curPts), (_, nextPts) in pairwise(contour, reverse=True):
            yield (curType, tuple(reversed(curPts[:-1])) + (nextPts[-1],))
    yield ('closePath' if closed else 'endPath', ())