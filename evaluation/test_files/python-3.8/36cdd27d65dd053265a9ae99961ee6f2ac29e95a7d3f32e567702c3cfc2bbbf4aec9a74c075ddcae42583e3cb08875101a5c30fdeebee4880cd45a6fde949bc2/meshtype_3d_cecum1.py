"""
Generates a 3-D cecum mesh along the central line, with variable
numbers of elements around, along and through wall, with
variable radius and thickness along.
"""
import copy
import math
from opencmiss.zinc.field import Field
from opencmiss.zinc.node import Node
from scaffoldmaker.annotation.annotationgroup import AnnotationGroup
from scaffoldmaker.annotation.colon_terms import get_colon_term
from scaffoldmaker.meshtypes.meshtype_1d_path1 import MeshType_1d_path1, extractPathParametersFromRegion
from scaffoldmaker.meshtypes.meshtype_3d_colonsegment1 import ColonSegmentTubeMeshInnerPoints, getFullProfileFromHalfHaustrum, getTeniaColi, createNodesAndElementsTeniaColi
from scaffoldmaker.meshtypes.meshtype_3d_ostium1 import MeshType_3d_ostium1, generateOstiumMesh
from scaffoldmaker.meshtypes.scaffold_base import Scaffold_base
from scaffoldmaker.scaffoldpackage import ScaffoldPackage
from scaffoldmaker.utils import interpolation as interp
from scaffoldmaker.utils import matrix
from scaffoldmaker.utils import tubemesh
from scaffoldmaker.utils import vector
from scaffoldmaker.utils.annulusmesh import createAnnulusMesh3d
from scaffoldmaker.utils.tracksurface import TrackSurface, TrackSurfacePosition
from scaffoldmaker.utils.zinc_utils import exnodeStringFromNodeValues, mesh_destroy_elements_and_nodes_by_identifiers

class MeshType_3d_cecum1(Scaffold_base):
    """
    Generates a 3-D cecum mesh with variable numbers
    of elements around, along the central line, and through wall.
    The cecum is created by a function that generates a cecum
    segment and uses tubemesh to map the segment along a central
    line profile. The proximal end of the cecum is closed up with
    an apex plate. An ostium is included to generate the
    ileo-cecal junction.
    """
    centralPathDefaultScaffoldPackages = {'Pig 1': ScaffoldPackage(MeshType_1d_path1, {'scaffoldSettings': {'Coordinate dimensions': 3, 'D2 derivatives': True, 'Length': 120.0, 'Number of elements': 3}, 'meshEdits': exnodeStringFromNodeValues([Node.VALUE_LABEL_VALUE, Node.VALUE_LABEL_D_DS1, Node.VALUE_LABEL_D_DS2, Node.VALUE_LABEL_D2_DS1DS2], [[[0.0, 0.0, 0.0], [0.0, 0.0, 60.0], [1.0, 0.0, 0.0], [0.0, 0.0, 0.0]], [[0.0, 0.0, 60.0], [0.0, 0.0, 60.0], [1.0, 0.0, 0.0], [0.0, 0.0, 0.0]], [[0.0, 0.0, 120.0], [0.0, 0.0, 60.0], [1.0, 0.0, 0.0], [0.0, 0.0, 0.0]], [[0.0, 0.0, 180.0], [0.0, 0.0, 60.0], [1.0, 0.0, 0.0], [0.0, 0.0, 0.0]]])})}
    ostiumDefaultScaffoldPackages = {'Pig 1': ScaffoldPackage(MeshType_3d_ostium1, {'scaffoldSettings': {'Number of vessels': 1, 'Number of elements across common': 2, 'Number of elements around ostium': 8, 'Number of elements along': 2, 'Number of elements through wall': 1, 'Unit scale': 1.0, 'Outlet': False, 'Ostium diameter': 20.0, 'Ostium length': 10.0, 'Ostium wall thickness': 2.0, 'Ostium inter-vessel distance': 0.0, 'Ostium inter-vessel height': 0.0, 'Use linear through ostium wall': True, 'Vessel end length factor': 1.0, 'Vessel inner diameter': 10.0, 'Vessel wall thickness': 2.0, 'Vessel angle 1 degrees': 0.0, 'Vessel angle 1 spread degrees': 0.0, 'Vessel angle 2 degrees': 0.0, 'Use linear through vessel wall': True, 'Use cross derivatives': False, 'Refine': False, 'Refine number of elements around': 4, 'Refine number of elements along': 4, 'Refine number of elements through wall': 1}})}

    @staticmethod
    def getName():
        return '3D Cecum 1'

    @staticmethod
    def getParameterSetNames():
        return ['Default', 'Pig 1']

    @classmethod
    def getDefaultOptions(cls, parameterSetName='Default'):
        centralPathOption = cls.centralPathDefaultScaffoldPackages['Pig 1']
        ostiumOption = cls.ostiumDefaultScaffoldPackages['Pig 1']
        options = {'Central path': copy.deepcopy(centralPathOption), 'Number of segments': 5, 'Number of elements around tenia coli': 2, 'Number of elements around haustrum': 8, 'Number of elements along segment': 8, 'Number of elements through wall': 1, 'Start inner radius': 35.0, 'Start inner radius derivative': 3.0, 'End inner radius': 38.0, 'End inner radius derivative': 3.0, 'Corner inner radius factor': 0.5, 'Haustrum inner radius factor': 0.25, 'Segment length end derivative factor': 1.0, 'Segment length mid derivative factor': 4.0, 'Number of tenia coli': 3, 'Start tenia coli width': 5.0, 'Start tenia coli width derivative': 0.0, 'End tenia coli width': 5.0, 'End tenia coli width derivative': 0.0, 'Tenia coli thickness': 0.5, 'Wall thickness': 2.0, 'Ileocecal junction': copy.deepcopy(ostiumOption), 'Ileocecal junction angular position degrees': 60.0, 'Ileocecal junction position along factor': 0.5, 'Use cross derivatives': False, 'Use linear through wall': True, 'Refine': False, 'Refine number of elements around': 1, 'Refine number of elements along': 1, 'Refine number of elements through wall': 1}
        cls.updateSubScaffoldOptions(options)
        return options

    @staticmethod
    def getOrderedOptionNames():
        return ['Central path', 'Number of segments', 'Number of elements around tenia coli', 'Number of elements around haustrum', 'Number of elements along segment', 'Number of elements through wall', 'Start inner radius', 'Start inner radius derivative', 'End inner radius', 'End inner radius derivative', 'Corner inner radius factor', 'Haustrum inner radius factor', 'Segment length end derivative factor', 'Segment length mid derivative factor', 'Number of tenia coli', 'Start tenia coli width', 'Start tenia coli width derivative', 'End tenia coli width', 'End tenia coli width derivative', 'Tenia coli thickness', 'Wall thickness', 'Ileocecal junction', 'Ileocecal junction angular position degrees', 'Ileocecal junction position along factor', 'Use cross derivatives', 'Use linear through wall', 'Refine', 'Refine number of elements around', 'Refine number of elements along', 'Refine number of elements through wall']

    @classmethod
    def getOptionValidScaffoldTypes(cls, optionName):
        if optionName == 'Central path':
            return [MeshType_1d_path1]
        if optionName == 'Ileocecal junction':
            return [MeshType_3d_ostium1]
        return []

    @classmethod
    def getOptionScaffoldTypeParameterSetNames(cls, optionName, scaffoldType):
        if optionName == 'Central path':
            return list(cls.centralPathDefaultScaffoldPackages.keys())
        if optionName == 'Ileocecal junction':
            return list(cls.ostiumDefaultScaffoldPackages.keys())
        assert scaffoldType in cls.getOptionValidScaffoldTypes(optionName), cls.__name__ + '.getOptionScaffoldTypeParameterSetNames.  ' + "Invalid option '" + optionName + "' scaffold type " + scaffoldType.getName()
        return scaffoldType.getParameterSetNames()

    @classmethod
    def getOptionScaffoldPackage(cls, optionName, scaffoldType, parameterSetName=None):
        """
        :param parameterSetName:  Name of valid parameter set for option Scaffold, or None for default.
        :return: ScaffoldPackage.
        """
        if parameterSetName:
            assert parameterSetName in cls.getOptionScaffoldTypeParameterSetNames(optionName, scaffoldType), 'Invalid parameter set ' + str(parameterSetName) + ' for scaffold ' + str(scaffoldType.getName()) + ' in option ' + str(optionName) + ' of scaffold ' + cls.getName()
        if optionName == 'Central path':
            if not parameterSetName:
                parameterSetName = list(cls.centralPathDefaultScaffoldPackages.keys())[0]
            return copy.deepcopy(cls.centralPathDefaultScaffoldPackages[parameterSetName])
        if optionName == 'Ileocecal junction':
            if not parameterSetName:
                parameterSetName = list(cls.ostiumDefaultScaffoldPackages.keys())[0]
            return copy.deepcopy(cls.ostiumDefaultScaffoldPackages[parameterSetName])
        assert False, cls.__name__ + '.getOptionScaffoldPackage:  Option ' + optionName + ' is not a scaffold'

    @classmethod
    def checkOptions(cls, options):
        if not options['Central path'].getScaffoldType() in cls.getOptionValidScaffoldTypes('Central path'):
            options['Central path'] = cls.getOptionScaffoldPackage('Central path', MeshType_1d_path1)
        if not options['Ileocecal junction'].getScaffoldType() in cls.getOptionValidScaffoldTypes('Ileocecal junction'):
            options['Ileocecal junction'] = cls.getOptionScaffoldPackage('Ileocecal junction', MeshType_3d_ostium1)
        for key in ['Number of segments', 'Refine number of elements around', 'Refine number of elements along', 'Refine number of elements through wall']:
            if options[key] < 1:
                options[key] = 1
        for key in ['Number of elements around tenia coli', 'Number of elements around haustrum', 'Number of elements along segment', 'Start inner radius', 'Start inner radius derivative', 'End inner radius', 'End inner radius derivative', 'Corner inner radius factor', 'Haustrum inner radius factor', 'Segment length end derivative factor', 'Segment length mid derivative factor', 'Number of tenia coli', 'Start tenia coli width', 'Start tenia coli width derivative', 'End tenia coli width', 'End tenia coli width derivative', 'Ileocecal junction angular position degrees', 'Ileocecal junction position along factor', 'Tenia coli thickness', 'Wall thickness']:
            if options[key] < 0.0:
                options[key] = 0.0
            if options['Number of elements through wall'] != 1:
                options['Number of elements through wall'] = 1
        cls.updateSubScaffoldOptions(options)

    @classmethod
    def updateSubScaffoldOptions(cls, options):
        """
        Update ostium sub-scaffold options which depend on parent options.
        """
        wallThickness = options['Wall thickness']
        ostiumOptions = options['Ileocecal junction']
        ostiumSettings = ostiumOptions.getScaffoldSettings()
        ostiumSettings['Ostium wall thickness'] = wallThickness

    @classmethod
    def generateBaseMesh(cls, region, options):
        """
        Generate the base tricubic Hermite mesh.
        :param region: Zinc region to define model in. Must be empty.
        :param options: Dict containing options. See getDefaultOptions().
        :return: annotationGroups
        """
        cls.updateSubScaffoldOptions(options)
        centralPath = options['Central path']
        segmentCount = options['Number of segments']
        startPhase = 0.0
        elementsCountAroundTC = options['Number of elements around tenia coli']
        elementsCountAroundHaustrum = options['Number of elements around haustrum']
        elementsCountAlongSegment = options['Number of elements along segment']
        elementsCountThroughWall = options['Number of elements through wall']
        startInnerRadius = options['Start inner radius']
        startInnerRadiusDerivative = options['Start inner radius derivative']
        endInnerRadius = options['End inner radius']
        endInnerRadiusDerivative = options['End inner radius derivative']
        cornerInnerRadiusFactor = options['Corner inner radius factor']
        haustrumInnerRadiusFactor = options['Haustrum inner radius factor']
        segmentLengthEndDerivativeFactor = options['Segment length end derivative factor']
        segmentLengthMidDerivativeFactor = options['Segment length mid derivative factor']
        tcCount = options['Number of tenia coli']
        startTCWidth = options['Start tenia coli width']
        startTCWidthDerivative = options['Start tenia coli width derivative']
        endTCWidth = options['End tenia coli width']
        endTCWidthDerivative = options['End tenia coli width derivative']
        tcThickness = options['Tenia coli thickness']
        wallThickness = options['Wall thickness']
        useCrossDerivatives = options['Use cross derivatives']
        useCubicHermiteThroughWall = not options['Use linear through wall']
        elementsCountAlong = int(elementsCountAlongSegment * segmentCount)
        elementsCountAround = (elementsCountAroundTC + elementsCountAroundHaustrum) * tcCount
        ostiumPositionAngleAround = math.radians(options['Ileocecal junction angular position degrees'])
        ostiumPositionAlongFactor = options['Ileocecal junction position along factor']
        ostiumOptions = options['Ileocecal junction']
        ostiumSettings = ostiumOptions.getScaffoldSettings()
        ostiumDiameter = ostiumSettings['Ostium diameter']
        firstNodeIdentifier = 1
        firstElementIdentifier = 1
        tmpRegion = region.createRegion()
        centralPath.generate(tmpRegion)
        (cx, cd1, cd2, cd12) = extractPathParametersFromRegion(tmpRegion, [Node.VALUE_LABEL_VALUE, Node.VALUE_LABEL_D_DS1, Node.VALUE_LABEL_D_DS2, Node.VALUE_LABEL_D2_DS1DS2])
        del tmpRegion
        cecumLength = 0.0
        elementsCountIn = len(cx) - 1
        sd1 = interp.smoothCubicHermiteDerivativesLine(cx, cd1, fixAllDirections=True, magnitudeScalingMode=interp.DerivativeScalingMode.HARMONIC_MEAN)
        for e in range(elementsCountIn):
            arcLength = interp.getCubicHermiteArcLength(cx[e], sd1[e], cx[e + 1], sd1[e + 1])
            cecumLength += arcLength
        smoothd1 = interp.smoothCubicHermiteDerivativesLine(cx, cd1, magnitudeScalingMode=interp.DerivativeScalingMode.HARMONIC_MEAN)
        (sxCecum, sd1Cecum, se, sxi, ssf) = interp.sampleCubicHermiteCurves(cx, smoothd1, elementsCountAlong)
        (sd2Cecum, sd12Cecum) = interp.interpolateSampleCubicHermite(cd2, cd12, se, sxi, ssf)
        segmentLength = cecumLength / segmentCount
        innerRadiusAlongCecum = []
        dInnerRadiusAlongCecum = []
        tcWidthAlongCecum = []
        closedProximalEnd = True
        for n2 in range(elementsCountAlongSegment * segmentCount + 1):
            xi = 1 / (elementsCountAlongSegment * segmentCount) * n2
            radius = interp.interpolateCubicHermite([startInnerRadius], [startInnerRadiusDerivative], [endInnerRadius], [endInnerRadiusDerivative], xi)[0]
            innerRadiusAlongCecum.append(radius)
            dRadius = interp.interpolateCubicHermiteDerivative([startInnerRadius], [startInnerRadiusDerivative], [endInnerRadius], [endInnerRadiusDerivative], xi)[0]
            dInnerRadiusAlongCecum.append(dRadius)
            tcWidth = interp.interpolateCubicHermite([startTCWidth], [startTCWidthDerivative], [endTCWidth], [endTCWidthDerivative], xi)[0]
            tcWidthAlongCecum.append(tcWidth)
        haustrumInnerRadiusFactorAlongCecum = [haustrumInnerRadiusFactor] * (elementsCountAlong + 1)
        xToSample = []
        d1ToSample = []
        d2ToSample = []
        elementsCountAroundHalfHaustrum = int((elementsCountAroundTC + elementsCountAroundHaustrum) * 0.5)
        colonSegmentTubeMeshInnerPoints = ColonSegmentTubeMeshInnerPoints(region, elementsCountAroundTC, elementsCountAroundHaustrum, elementsCountAlongSegment, tcCount, segmentLengthEndDerivativeFactor, segmentLengthMidDerivativeFactor, segmentLength, wallThickness, cornerInnerRadiusFactor, haustrumInnerRadiusFactorAlongCecum, innerRadiusAlongCecum, dInnerRadiusAlongCecum, tcWidthAlongCecum, startPhase)
        cecumGroup = AnnotationGroup(region, get_colon_term('caecum'))
        annotationGroupsAlong = []
        for i in range(elementsCountAlong):
            annotationGroupsAlong.append([cecumGroup])
        annotationGroupsThroughWall = []
        for i in range(elementsCountThroughWall):
            annotationGroupsThroughWall.append([])
        for nSegment in range(segmentCount):
            (xInner, d1Inner, d2Inner, transitElementList, segmentAxis, annotationGroupsAround) = colonSegmentTubeMeshInnerPoints.getColonSegmentTubeMeshInnerPoints(nSegment)
            if nSegment == 0:
                (xFirstSegmentSampled, d1FirstSegmentSampled, d2FirstSegmentSampled, d1FirstDirectionVector) = getApexSegmentForCecum(xInner, d1Inner, d2Inner, elementsCountAroundHalfHaustrum, elementsCountAroundTC, elementsCountAround, elementsCountAlongSegment, tcCount)
                xToSample += xFirstSegmentSampled
                d1ToSample += d1FirstSegmentSampled
                d2ToSample += d2FirstSegmentSampled
            else:
                xInnerExtrude = []
                for n in range(len(xInner)):
                    xInnerExtrude.append([xInner[n][0], xInner[n][1], xInner[n][2] + segmentLength * nSegment])
                xToSample += xInnerExtrude[elementsCountAround:]
                d1ToSample += d1Inner[elementsCountAround:]
                d2ToSample += d2Inner[elementsCountAround:]
        (xToWarp, d1ToWarp, d2ToWarp) = sampleCecumAlongLength(xToSample, d1ToSample, d2ToSample, d1FirstDirectionVector, elementsCountAroundHalfHaustrum, elementsCountAroundTC, elementsCountAround, elementsCountAlong, tcCount)
        minZ = xToWarp[0][2]
        for n2 in range(elementsCountAlong + 1):
            zFirstNodeAlong = xToWarp[n2 * elementsCountAround][2]
            if zFirstNodeAlong < minZ:
                minZ = zFirstNodeAlong
        for n in range(len(xToWarp)):
            xToWarp[n][2] = xToWarp[n][2] - minZ
        (sxRefList, sd1RefList, sd2ProjectedListRef, zRefList) = tubemesh.getPlaneProjectionOnCentralPath(xToWarp, elementsCountAround, elementsCountAlong, cecumLength, sxCecum, sd1Cecum, sd2Cecum, sd12Cecum)
        (xWarpedList, d1WarpedList, d2WarpedList, d3WarpedUnitList) = tubemesh.warpSegmentPoints(xToWarp, d1ToWarp, d2ToWarp, segmentAxis, sxRefList, sd1RefList, sd2ProjectedListRef, elementsCountAround, elementsCountAlong, zRefList, innerRadiusAlongCecum, closedProximalEnd)
        wallThicknessList = [wallThickness] * (elementsCountAlong + 1)
        relativeThicknessList = []
        (xList, d1List, d2List, d3List, curvatureList) = tubemesh.getCoordinatesFromInner(xWarpedList, d1WarpedList, d2WarpedList, d3WarpedUnitList, wallThicknessList, relativeThicknessList, elementsCountAround, elementsCountAlong, elementsCountThroughWall, transitElementList)
        xApexInner = xList[0]
        mag = interp.getCubicHermiteArcLength(xList[0], d2List[0], xList[elementsCountAround * 2], d2List[elementsCountAround * 2])
        d2ApexInner = vector.setMagnitude(sd2Cecum[0], mag)
        d1ApexInner = vector.crossproduct3(sd1Cecum[0], d2ApexInner)
        d1ApexInner = vector.setMagnitude(d1ApexInner, mag)
        d3ApexUnit = vector.normalise(vector.crossproduct3(vector.normalise(d1ApexInner), vector.normalise(d2ApexInner)))
        d3ApexInner = [d3ApexUnit[c] * wallThickness / elementsCountThroughWall for c in range(3)]
        xCecum = []
        d1Cecum = []
        d2Cecum = []
        d3Cecum = []
        for n3 in range(elementsCountThroughWall + 1):
            xApex = [xApexInner[c] + d3ApexUnit[c] * wallThickness / elementsCountThroughWall * n3 for c in range(3)]
            xCecum.append(xApex)
            d1Cecum.append(d1ApexInner)
            d2Cecum.append(d2ApexInner)
            d3Cecum.append(d3ApexInner)
        xCecum += xList[(elementsCountThroughWall + 1) * elementsCountAround:]
        d1Cecum += d1List[(elementsCountThroughWall + 1) * elementsCountAround:]
        d2Cecum += d2List[(elementsCountThroughWall + 1) * elementsCountAround:]
        d3Cecum += d3List[(elementsCountThroughWall + 1) * elementsCountAround:]
        xFlat = d1Flat = d2Flat = []
        xOrgan = d1Organ = d2Organ = []
        if tcThickness > 0:
            tubeTCWidthList = colonSegmentTubeMeshInnerPoints.getTubeTCWidthList()
            (xCecum, d1Cecum, d2Cecum, d3Cecum, annotationGroupsAround) = getTeniaColi(region, xCecum, d1Cecum, d2Cecum, d3Cecum, curvatureList, tcCount, elementsCountAroundTC, elementsCountAroundHaustrum, elementsCountAlong, elementsCountThroughWall, tubeTCWidthList, tcThickness, sxRefList, annotationGroupsAround, closedProximalEnd)
            (nextNodeIdentifier, nextElementIdentifier, annotationGroups) = createNodesAndElementsTeniaColi(region, xCecum, d1Cecum, d2Cecum, d3Cecum, xFlat, d1Flat, d2Flat, xOrgan, d1Organ, d2Organ, None, elementsCountAroundTC, elementsCountAroundHaustrum, elementsCountAlong, elementsCountThroughWall, tcCount, annotationGroupsAround, annotationGroupsAlong, annotationGroupsThroughWall, firstNodeIdentifier, firstElementIdentifier, useCubicHermiteThroughWall, useCrossDerivatives, closedProximalEnd)
        else:
            (nextNodeIdentifier, nextElementIdentifier, annotationGroups) = tubemesh.createNodesAndElements(region, xCecum, d1Cecum, d2Cecum, d3Cecum, xFlat, d1Flat, d2Flat, xOrgan, d1Organ, d2Organ, None, elementsCountAround, elementsCountAlong, elementsCountThroughWall, annotationGroupsAround, annotationGroupsAlong, annotationGroupsThroughWall, firstNodeIdentifier, firstElementIdentifier, useCubicHermiteThroughWall, useCrossDerivatives, closedProximalEnd)
        elementsAroundTrackSurface = elementsCountAroundHaustrum
        elementsAlongTrackSurface = elementsCountAlongSegment
        sectorIdx = ostiumPositionAngleAround // (2 * math.pi / tcCount)
        startIdxElementsAround = int((elementsCountAroundHaustrum + elementsCountAroundTC) * sectorIdx + elementsCountAroundTC * 0.5)
        baseNodesIdx = elementsCountThroughWall + 1 + +(elementsCountAround * (elementsCountThroughWall + 1) + ((elementsCountAroundTC - 1) * tcCount if tcThickness > 0.0 else 0)) * (elementsCountAlongSegment * (segmentCount - 1) - 1) + elementsCountAround
        xTrackSurface = []
        d1TrackSurface = []
        d2TrackSurface = []
        for n2 in range(elementsCountAlongSegment + 1):
            for n1 in range(elementsCountAroundHaustrum + 1):
                idx = baseNodesIdx + (elementsCountAround * (elementsCountThroughWall + 1) + ((elementsCountAroundTC - 1) * tcCount if tcThickness > 0.0 else 0)) * n2 + startIdxElementsAround + n1
                xTrackSurface.append(xCecum[idx])
                d1TrackSurface.append(d1Cecum[idx])
                d2TrackSurface.append(d2Cecum[idx])
        trackSurfaceOstium = TrackSurface(elementsAroundTrackSurface, elementsAlongTrackSurface, xTrackSurface, d1TrackSurface, d2TrackSurface)
        v1 = xList[0]
        v2 = xList[int(elementsCountAroundTC * 0.5)]
        d1 = d1List[0]
        d2 = d1List[int(elementsCountAroundTC * 0.5)]
        arcLengthTC = interp.getCubicHermiteArcLength(v1, d1, v2, d2)
        angleToTCEdge = arcLengthTC / startInnerRadius
        angleOstium = ostiumDiameter / startInnerRadius
        dAngle = (2 * math.pi / tcCount - 2 * angleToTCEdge) / elementsCountAroundHaustrum
        angleAroundInSector = ostiumPositionAngleAround % (2 * math.pi / tcCount)
        assert angleAroundInSector > angleToTCEdge + angleOstium * 0.5 and angleAroundInSector < 2 * math.pi / tcCount - angleToTCEdge - angleOstium * 0.5, 'Ileocecal junction cannot sit on tenia coli'
        ei1Centre = int((angleAroundInSector - angleToTCEdge) // dAngle)
        xi1 = (angleAroundInSector - angleToTCEdge - dAngle * ei1Centre) / dAngle
        ostiumDistanceFromCecumDistal = segmentLength * ostiumPositionAlongFactor
        arcLength = interp.getCubicHermiteArcLength(sxRefList[-1], sd1RefList[-1], sxRefList[-2], sd1RefList[-2])
        distance = arcLength
        for e in range(len(sxRefList) - 2, 0, -1):
            if ostiumDistanceFromCecumDistal > distance:
                arcLength = interp.getCubicHermiteArcLength(sxRefList[e - 1], sd1RefList[e - 1], sxRefList[e], sd1RefList[e])
                distance += arcLength
            else:
                ei2Centre = e - elementsCountAlongSegment * (segmentCount - 1)
                xi2 = (distance - ostiumDistanceFromCecumDistal) / arcLength
                break
        centrePosition = TrackSurfacePosition(ei1Centre, ei2Centre, xi1, xi2)
        (xCentre, d1Centre, d2Centre) = trackSurfaceOstium.evaluateCoordinates(centrePosition, derivatives=True)
        axis1 = d1Centre
        (ei1Left, ei1Right, ei2Bottom, ei2Top) = getElementIdxOfOstiumBoundary(centrePosition, trackSurfaceOstium, ostiumDiameter)
        ei1Left -= 1
        ei1Right += 1
        ei2Bottom -= 1
        ei2Top += 1
        assert ei1Left >= 0 and ei1Right < elementsAroundTrackSurface and (ei2Bottom >= 0) and (ei2Top < elementsAlongTrackSurface), 'cecum1.py: Insufficient elements around ostium on tracksurface to make annulus mesh.'
        nodeStart = int(baseNodesIdx + ei2Bottom * (elementsCountAround * (elementsCountThroughWall + 1) + ((elementsCountAroundTC - 1) * tcCount if tcThickness > 0.0 else 0)) + ei1Centre + sectorIdx * (elementsCountAroundHaustrum + elementsCountAroundTC) + elementsCountAroundTC * 0.5) - elementsCountAround + 1
        deleteElementsCountAcross = ei1Right - ei1Left + 1
        deleteElementsCountAlong = ei2Top - ei2Bottom + 1
        deleteElementIdxStart = int((elementsCountAround * elementsCountThroughWall + (elementsCountAroundTC * tcCount if tcThickness > 0.0 else 0.0)) * (elementsCountAlong - elementsCountAlongSegment + ei2Bottom) + elementsCountAroundTC * 0.5 + (elementsCountAroundTC + elementsCountAroundHaustrum) * sectorIdx + ei1Left + 1)
        deleteElementIdentifier = []
        for n2 in range(deleteElementsCountAlong):
            for n1 in range(deleteElementsCountAcross):
                elementIdx = deleteElementIdxStart + n1 + n2 * (elementsCountAround + (int(elementsCountAroundTC * tcCount) if tcThickness > 0.0 else 0))
                deleteElementIdentifier.append(elementIdx)
        deleteNodeIdxStart = nodeStart - int(deleteElementsCountAcross * 0.5)
        deleteNodeIdentifier = []
        for n2 in range(deleteElementsCountAlong + 1):
            for n3 in range(elementsCountThroughWall + 1):
                for n1 in range(deleteElementsCountAcross + 1):
                    nodeIdx = deleteNodeIdxStart + n1 + elementsCountAround * n3 + n2 * (elementsCountAround * (elementsCountThroughWall + 1) + ((elementsCountAroundTC - 1) * tcCount if tcThickness > 0.0 else 0))
                    deleteNodeIdentifier.append(nodeIdx)
        innerEndPoints_Id = []
        endProportions = []
        for n1 in range(ei1Centre - ei1Left + 1):
            idx = nodeStart - n1
            innerEndPoints_Id.append(idx)
            endProportions.append([(ei1Centre - n1) / elementsAroundTrackSurface, ei2Bottom / elementsAlongTrackSurface])
        for n2 in range(ei2Top - ei2Bottom + 1):
            idx = idx + 2 * elementsCountAround + ((elementsCountAroundTC - 1) * tcCount if tcThickness > 0.0 else 0)
            innerEndPoints_Id.append(idx)
            endProportions.append([ei1Left / elementsAroundTrackSurface, (ei2Bottom + n2 + 1) / elementsAlongTrackSurface])
        for n1 in range(1, ei1Right - ei1Left + 2):
            idx = idx + 1
            innerEndPoints_Id.append(idx)
            endProportions.append([(ei1Left + n1) / elementsAroundTrackSurface, (ei2Top + 1) / elementsAlongTrackSurface])
        for n2 in range(ei2Top - ei2Bottom + 1):
            idx = idx - 2 * elementsCountAround - ((elementsCountAroundTC - 1) * tcCount if tcThickness > 0.0 else 0)
            innerEndPoints_Id.append(idx)
            endProportions.append([(ei1Right + 1) / elementsAroundTrackSurface, (ei2Top - n2) / elementsAlongTrackSurface])
        for n1 in range(ei1Right - ei1Centre):
            idx = idx - 1
            innerEndPoints_Id.append(idx)
            endProportions.append([(ei1Right - n1) / elementsAroundTrackSurface, ei2Bottom / elementsAlongTrackSurface])
        innerEndPoints_x = []
        innerEndPoints_d1 = []
        innerEndPoints_d2 = []
        outerEndPoints_Id = []
        outerEndPoints_x = []
        outerEndPoints_d1 = []
        outerEndPoints_d2 = []
        for i in range(len(innerEndPoints_Id)):
            innerNode = innerEndPoints_Id[i]
            innerEndPoints_x.append(xCecum[innerNode - 1])
            innerEndPoints_d1.append(d1Cecum[innerNode - 1])
            innerEndPoints_d2.append(d2Cecum[innerNode - 1])
            outerNode = innerNode + elementsCountAround
            outerEndPoints_Id.append(outerNode)
            outerEndPoints_x.append(xCecum[outerNode - 1])
            outerEndPoints_d1.append(d1Cecum[outerNode - 1])
            outerEndPoints_d2.append(d2Cecum[outerNode - 1])
        endPoints_Id = [innerEndPoints_Id, outerEndPoints_Id]
        endPoints_x = [innerEndPoints_x, outerEndPoints_x]
        endPoints_d1 = [innerEndPoints_d1, outerEndPoints_d1]
        endPoints_d2 = [innerEndPoints_d2, outerEndPoints_d2]
        endDerivativesMap = [[None] * len(innerEndPoints_Id), [None] * len(innerEndPoints_Id)]
        count = 0
        for n1 in range(ei1Centre - ei1Left):
            endDerivativesMap[0][count] = endDerivativesMap[1][count] = ((-1, 0, 0), (0, -1, 0), None)
            count += 1
        endDerivativesMap[0][count] = endDerivativesMap[1][count] = ((-1, 0, 0), (-1, -1, 0), None, (0, 1, 0))
        count += 1
        for n2 in range(ei2Top - ei2Bottom):
            endDerivativesMap[0][count] = endDerivativesMap[1][count] = ((0, 1, 0), (-1, 0, 0), None)
            count += 1
        endDerivativesMap[0][count] = endDerivativesMap[1][count] = ((0, 1, 0), (-1, 1, 0), None, (1, 0, 0))
        count += 1
        for n1 in range(1, ei1Right - ei1Left + 1):
            endDerivativesMap[0][count] = endDerivativesMap[1][count] = ((1, 0, 0), (0, 1, 0), None)
            count += 1
        endDerivativesMap[0][count] = endDerivativesMap[1][count] = ((1, 0, 0), (1, 1, 0), None, (0, -1, 0))
        count += 1
        for n2 in range(1, ei2Top - ei2Bottom + 1):
            endDerivativesMap[0][count] = endDerivativesMap[1][count] = ((0, -1, 0), (1, 0, 0), None)
            count += 1
        endDerivativesMap[0][count] = endDerivativesMap[1][count] = ((0, -1, 0), (1, -1, 0), None, (-1, 0, 0))
        count += 1
        for n1 in range(ei1Right - ei1Centre):
            endDerivativesMap[0][count] = endDerivativesMap[1][count] = ((-1, 0, 0), (0, -1, 0), None)
            count += 1
        ostiumSettings['Number of elements around ostium'] = len(innerEndPoints_Id)
        fm = region.getFieldmodule()
        mesh = fm.findMeshByDimension(3)
        nodes = fm.findNodesetByFieldDomainType(Field.DOMAIN_TYPE_NODES)
        cecumMeshGroup = cecumGroup.getMeshGroup(mesh)
        (nextNodeIdentifier, nextElementIdentifier, (o1_x, o1_d1, o1_d2, o1_d3, o1_NodeId, o1_Positions)) = generateOstiumMesh(region, ostiumSettings, trackSurfaceOstium, centrePosition, axis1, nextNodeIdentifier, nextElementIdentifier, ostiumMeshGroups=[cecumMeshGroup])
        startProportions = []
        for n in range(len(innerEndPoints_Id)):
            startProportions.append(trackSurfaceOstium.getProportion(o1_Positions[n]))
        (nextNodeIdentifier, nextElementIdentifier) = createAnnulusMesh3d(nodes, mesh, nextNodeIdentifier, nextElementIdentifier, o1_x, o1_d1, o1_d2, None, o1_NodeId, None, endPoints_x, endPoints_d1, endPoints_d2, None, endPoints_Id, endDerivativesMap, elementsCountRadial=2, meshGroups=[cecumMeshGroup], tracksurface=trackSurfaceOstium, startProportions=startProportions, endProportions=endProportions)
        mesh_destroy_elements_and_nodes_by_identifiers(mesh, deleteElementIdentifier)
        return annotationGroups

    @classmethod
    def refineMesh(cls, meshrefinement, options):
        """
        Refine source mesh into separate region, with change of basis.
        :param meshrefinement: MeshRefinement, which knows source and target region.
        :param options: Dict containing options. See getDefaultOptions().
        """
        refineElementsCountAround = options['Refine number of elements around']
        refineElementsCountAlong = options['Refine number of elements along']
        refineElementsCountThroughWall = options['Refine number of elements through wall']
        meshrefinement.refineAllElementsCubeStandard3d(refineElementsCountAround, refineElementsCountAlong, refineElementsCountThroughWall)
        return

def getApexSegmentForCecum(xInner, d1Inner, d2Inner, elementsCountAroundHalfHaustrum, elementsCountAroundTC, elementsCountAround, elementsCountAlongSegment, tcCount):
    """
    Generates the inner coordinates and derivatives for a cecum segment on the closed end.
    The closed end is a single node and segment is created by sampling curves between the
    point on closed end with nodes on the length along second half of a colon segment.
    :param xInner: coordinates of a colon segment.
    :param d1Inner: derivative around colon segment.
    :param d2Inner: derivative along colon segment.
    :param elementsCountAroundHalfHaustrum: half of total number of elements in haustrum and tenia coli.
    :param elementsCountAroundTC: number of elements around a tenia coli.
    :param elementsCountAround: number of elements around a cecum.
    :param elementsCountAlongSegment: number of elements along a segment of cecum.
    :param tcCount: number of tenia coli.
    :return: coordinates and derivatives around and along closed segment of cecum, and directional derivative for node
    on middle of tenia coli.
    """
    xFirstSegment = [[0.0, 0.0, 0.0] for c in range(elementsCountAround)]
    xFirstSegment += xInner[elementsCountAround * int(elementsCountAlongSegment * 0.5):]
    d1FirstDirectionVector = vector.normalise(d1Inner[elementsCountAround])
    d2Vector = xInner[elementsCountAround * int(elementsCountAlongSegment * 0.5):elementsCountAround * (int(elementsCountAlongSegment * 0.5) + 1)]
    d2FirstSegment = []
    for c in range(elementsCountAround):
        d2 = [d2Vector[c][0], d2Vector[c][1], 0.0]
        d2FirstSegment.append(d2)
    d2FirstSegment += d2Inner[elementsCountAround * int(elementsCountAlongSegment * 0.5):]
    xFirstSegmentSampledRaw = []
    d2FirstSegmentSampledRaw = []
    xFirstSegmentSampled = []
    d1FirstSegmentSampled = []
    d2FirstSegmentSampled = []
    for n1 in range(elementsCountAround):
        xForSamplingAlong = []
        d2ForSamplingAlong = []
        for n2 in range(1 + elementsCountAlongSegment - int(elementsCountAlongSegment * 0.5) + 1):
            idx = elementsCountAround * n2 + n1
            xForSamplingAlong.append(xFirstSegment[idx])
            d2ForSamplingAlong.append(d2FirstSegment[idx])
        (xResampled, d1Resampled, se, sxi, _) = interp.sampleCubicHermiteCurves(xForSamplingAlong, d2ForSamplingAlong, elementsCountAlongSegment, arcLengthDerivatives=True)
        xFirstSegmentSampledRaw.append(xResampled)
        d2FirstSegmentSampledRaw.append(d1Resampled)
    for n2 in range(elementsCountAlongSegment + 1):
        xAround = []
        for n1 in range(elementsCountAround):
            x = xFirstSegmentSampledRaw[n1][n2]
            d2 = d2FirstSegmentSampledRaw[n1][n2]
            if n1 < elementsCountAroundHalfHaustrum + 1:
                xAround.append(x)
            xFirstSegmentSampled.append(x)
            d2FirstSegmentSampled.append(d2)
            if n2 == 0:
                d1 = matrix.rotateAboutZAxis(d2, math.pi * 0.5)
                d1FirstSegmentSampled.append(d1)
        if n2 > 0:
            d1Around = []
            for n1 in range(elementsCountAroundHalfHaustrum):
                v1 = xAround[n1]
                v2 = xAround[n1 + 1]
                d1 = d1FirstDirectionVector if n1 == 0 else [v2[c] - v1[c] for c in range(3)]
                d2 = [v2[c] - v1[c] for c in range(3)]
                arcLengthAround = interp.computeCubicHermiteArcLength(v1, d1, v2, d2, True)
                dx_ds1 = [c * arcLengthAround for c in vector.normalise(d1)]
                d1Around.append(dx_ds1)
            d1 = vector.normalise([xAround[elementsCountAroundHalfHaustrum][c] - xAround[elementsCountAroundHalfHaustrum - 1][c] for c in range(3)])
            dx_ds1 = [c * arcLengthAround for c in d1]
            d1Around.append(dx_ds1)
            d1Smoothed = interp.smoothCubicHermiteDerivativesLine(xAround, d1Around, fixStartDerivative=True)
            d1TCEdge = vector.setMagnitude(d1Smoothed[int(elementsCountAroundTC * 0.5)], vector.magnitude(d1Smoothed[int(elementsCountAroundTC * 0.5 - 1)]))
            d1Transition = vector.setMagnitude(d1Smoothed[int(elementsCountAroundTC * 0.5 + 1)], vector.magnitude(d1Smoothed[int(elementsCountAroundTC * 0.5 + 2)]))
            d1Corrected = []
            d1Corrected = d1Corrected + d1Smoothed[:int(elementsCountAroundTC * 0.5)]
            d1Corrected.append(d1TCEdge)
            d1Corrected.append(d1Transition)
            d1Corrected = d1Corrected + d1Smoothed[int(elementsCountAroundTC * 0.5 + 2):]
            d1Full = getD1ForFullProfileFromHalfHaustrum(d1Corrected, tcCount)
            d1FirstSegmentSampled += d1Full
    return (xFirstSegmentSampled, d1FirstSegmentSampled, d2FirstSegmentSampled, d1FirstDirectionVector)

def getD1ForFullProfileFromHalfHaustrum(d1HaustrumHalfSet, tcCount):
    """
    Get full profile from half haustrum
    :param d1HaustrumHalfSet:
    :param tcCount:
    :return:
    """
    d1HaustrumHalfSet2 = []
    d1Haustra = []
    rotAng = 2 * math.pi / tcCount
    for n in range(1, len(d1HaustrumHalfSet)):
        idx = -n + len(d1HaustrumHalfSet) - 1
        d1 = d1HaustrumHalfSet[idx]
        d1Reflect = [d1[0], -d1[1], d1[2]]
        d1Rot = [-(d1Reflect[0] * math.cos(rotAng) - d1Reflect[1] * math.sin(rotAng)), -(d1Reflect[0] * math.sin(rotAng) + d1Reflect[1] * math.cos(rotAng)), -d1Reflect[2]]
        d1HaustrumHalfSet2.append(d1Rot)
    d1Haustrum = d1HaustrumHalfSet + d1HaustrumHalfSet2
    d1Haustra = d1Haustra + d1Haustrum[:-1]
    ang = [2 / 3 * math.pi, -2 / 3 * math.pi] if tcCount == 3 else [math.pi]
    for i in range(tcCount - 1):
        rotAng = ang[i]
        cosRotAng = math.cos(rotAng)
        sinRotAng = math.sin(rotAng)
        for n in range(len(d1Haustrum) - 1):
            d1 = d1Haustrum[n]
            dx_ds1 = [d1[0] * cosRotAng - d1[1] * sinRotAng, d1[0] * sinRotAng + d1[1] * cosRotAng, d1[2]]
            d1Haustra.append(dx_ds1)
    return d1Haustra

def sampleCecumAlongLength(xToSample, d1ToSample, d2ToSample, d1FirstDirectionVector, elementsCountAroundHalfHaustrum, elementsCountAroundTC, elementsCountAround, elementsCountAlong, tcCount):
    """
    Get systematically spaced points and derivatives over cubic Hermite interpolated curves along the
    length of the cecum.
    :param xToSample: coordinates of nodes.
    :param d1ToSample: derivative around elements.
    :param d2ToSample: derivative along cecum length.
    :param d1FirstDirectionVector: directional vector of derivative around for node on the middle of the tenia coli.
    :param elementsCountAroundHalfHaustrum:half the total number of elements around tenia coli and haustrum.
    :param elementsCountAroundTC: number of elements around tenia coli.
    :param elementsCountAround: number of elements around cecum.
    :param elementsCountAlong: number of elements along cecum length.
    :param tcCount: number of tenia coli.
    :return: nodes and derivatives for equally spaced points.
    """
    xInnerRaw = []
    d2InnerRaw = []
    xSampledAlongLength = []
    d1SampledAlongLength = []
    d2SampledAlongLength = []
    for n1 in range(elementsCountAroundHalfHaustrum + 1):
        xForSamplingAlong = []
        d2ForSamplingAlong = []
        for n2 in range(elementsCountAlong + 1):
            idx = n2 * elementsCountAround + n1
            xForSamplingAlong.append(xToSample[idx])
            d2ForSamplingAlong.append(d2ToSample[idx])
        (xSampled, d2Sampled, se, sxi, _) = interp.sampleCubicHermiteCurves(xForSamplingAlong, d2ForSamplingAlong, elementsCountAlong, arcLengthDerivatives=True)
        xInnerRaw.append(xSampled)
        d2InnerRaw.append(d2Sampled)
    for n2 in range(elementsCountAlong + 1):
        xAround = []
        d2Around = []
        for n1 in range(elementsCountAroundHalfHaustrum + 1):
            x = xInnerRaw[n1][n2]
            d2 = d2InnerRaw[n1][n2]
            xAround.append(x)
            d2Around.append(d2)
        d1InnerAroundList = []
        if n2 == 0:
            d1Corrected = d1ToSample[:elementsCountAroundHalfHaustrum + 1]
        else:
            for n1 in range(elementsCountAroundHalfHaustrum):
                v1 = xAround[n1]
                v2 = xAround[n1 + 1]
                d1 = d1FirstDirectionVector if n1 == 0 else [v2[c] - v1[c] for c in range(3)]
                d2 = [v2[c] - v1[c] for c in range(3)]
                arcLengthAround = interp.computeCubicHermiteArcLength(v1, d1, v2, d2, True)
                dx_ds1 = [c * arcLengthAround for c in vector.normalise(d1)]
                d1InnerAroundList.append(dx_ds1)
            d1 = vector.normalise([xAround[elementsCountAroundHalfHaustrum][c] - xAround[elementsCountAroundHalfHaustrum - 1][c] for c in range(3)])
            dx_ds1 = [c * arcLengthAround for c in d1]
            d1InnerAroundList.append(dx_ds1)
        if d1InnerAroundList:
            d1Smoothed = interp.smoothCubicHermiteDerivativesLine(xAround, d1InnerAroundList, fixStartDerivative=True)
            d1TCEdge = vector.setMagnitude(d1Smoothed[int(elementsCountAroundTC * 0.5)], vector.magnitude(d1Smoothed[int(elementsCountAroundTC * 0.5 - 1)]))
            d1Transition = vector.setMagnitude(d1Smoothed[int(elementsCountAroundTC * 0.5 + 1)], vector.magnitude(d1Smoothed[int(elementsCountAroundTC * 0.5 + 2)]))
            d1Corrected = []
            d1Corrected = d1Corrected + d1Smoothed[:int(elementsCountAroundTC * 0.5)]
            d1Corrected.append(d1TCEdge)
            d1Corrected.append(d1Transition)
            d1Corrected = d1Corrected + d1Smoothed[int(elementsCountAroundTC * 0.5 + 2):]
        (xAlongList, d1AlongList, d2AlongList) = getFullProfileFromHalfHaustrum(xAround, d1Corrected, d2Around, tcCount)
        xSampledAlongLength += xAlongList
        d1SampledAlongLength += d1AlongList
        d2SampledAlongLength += d2AlongList
    return (xSampledAlongLength, d1SampledAlongLength, d2SampledAlongLength)

def getElementIdxOfOstiumBoundary(centrePosition, trackSurfaceOstium, ostiumDiameter):
    """
    Finds the element indices of the boundaries of elements on tracksurface that surround
    the ostium. Indices based on numbering for elements around and along tracksurface.
    Boundary lies on xi=0 of elements on left and bottom boundaries and xi = 1 for right and
    top boundaries.
    :param centrePosition: surface description for centre of ostium.
    :param trackSurfaceOstium: surface description for tracksurface.
    :param ostiumDiameter: Diameter of ostium.
    :return: element indices on the left, right, bottom and top boundaries around tracksurface.
    """
    elementsAroundTrackSurface = trackSurfaceOstium.elementsCount1
    elementsAlongTrackSurface = trackSurfaceOstium.elementsCount2
    ei1 = centrePosition.e1
    ei2 = centrePosition.e2
    xi1 = centrePosition.xi1
    xi2 = centrePosition.xi2
    (xCentre, d1Centre, d2Centre) = trackSurfaceOstium.evaluateCoordinates(centrePosition, derivatives=True)
    leftPositionOfCentreElement = TrackSurfacePosition(ei1, ei2, 0, xi2)
    (xLeft, d1Left, _) = trackSurfaceOstium.evaluateCoordinates(leftPositionOfCentreElement, derivatives=True)
    distxLeftToxCentre = interp.computeCubicHermiteArcLength(xLeft, d1Left, xCentre, d1Centre, False)
    remainingLength = ostiumDiameter * 0.5 - distxLeftToxCentre
    xCurrent = xLeft
    d1Current = d1Left
    for n1 in range(ei1, -1, -1):
        if remainingLength > 0.0:
            prevPosition = TrackSurfacePosition(n1 - 1, ei2, 0, xi2)
            (xPrev, d1Prev, _) = trackSurfaceOstium.evaluateCoordinates(prevPosition, derivatives=True)
            distPrevToxCurrent = interp.computeCubicHermiteArcLength(xPrev, d1Prev, xCurrent, d1Current, False)
            remainingLength -= distPrevToxCurrent
            xCurrent = xPrev
            d1Current = d1Prev
        else:
            ei1Left = n1
            break
    rightPositionOfCentreElement = TrackSurfacePosition(ei1, ei2, 1.0, xi2)
    (xRight, d1Right, _) = trackSurfaceOstium.evaluateCoordinates(rightPositionOfCentreElement, derivatives=True)
    distxCentreToxRight = interp.computeCubicHermiteArcLength(xCentre, d1Centre, xRight, d1Right, False)
    remainingLength = ostiumDiameter * 0.5 - distxCentreToxRight
    xCurrent = xRight
    d1Current = d1Right
    for n1 in range(ei1, elementsAroundTrackSurface):
        if remainingLength > 0.0:
            nextPosition = TrackSurfacePosition(n1 + 1, ei2, 1.0, xi2)
            (xNext, d1Next, _) = trackSurfaceOstium.evaluateCoordinates(nextPosition, derivatives=True)
            distxCurrentToxNext = interp.computeCubicHermiteArcLength(xCurrent, d1Current, xNext, d1Next, False)
            remainingLength -= distxCurrentToxNext
            xCurrent = xNext
            d1Current = d1Next
        else:
            ei1Right = n1
            break
    bottomPositionOfCentreElement = TrackSurfacePosition(ei1, ei2, xi1, 0)
    (xBottom, _, d2Bottom) = trackSurfaceOstium.evaluateCoordinates(bottomPositionOfCentreElement, derivatives=True)
    distxBottomToxCentre = interp.computeCubicHermiteArcLength(xBottom, d2Bottom, xCentre, d2Centre, False)
    remainingLength = ostiumDiameter * 0.5 - distxBottomToxCentre
    xCurrent = xBottom
    d2Current = d2Bottom
    for n2 in range(ei2, -1, -1):
        if remainingLength > 0.0:
            prevPosition = TrackSurfacePosition(ei1, n2 - 1, xi1, 0)
            (xPrev, _, d2Prev) = trackSurfaceOstium.evaluateCoordinates(prevPosition, derivatives=True)
            distPrevToxCurrent = interp.computeCubicHermiteArcLength(xPrev, d2Prev, xCurrent, d2Current, False)
            remainingLength -= distPrevToxCurrent
            xCurrent = xPrev
            d2Current = d2Prev
        else:
            ei2Bottom = n2
            break
    topPositionOfCentreElement = TrackSurfacePosition(ei1, ei2, xi1, 1.0)
    (xTop, _, d2Top) = trackSurfaceOstium.evaluateCoordinates(topPositionOfCentreElement, derivatives=True)
    distxCentreToxTop = interp.computeCubicHermiteArcLength(xCentre, d2Centre, xTop, d2Top, False)
    remainingLength = ostiumDiameter * 0.5 - distxCentreToxTop
    xCurrent = xTop
    d2Current = d2Top
    for n2 in range(ei2, elementsAlongTrackSurface):
        if remainingLength > 0.0:
            nextPosition = TrackSurfacePosition(ei1, n2 + 1, xi1, 1.0)
            (xNext, _, d2Next) = trackSurfaceOstium.evaluateCoordinates(nextPosition, derivatives=True)
            distxCurrentToxNext = interp.computeCubicHermiteArcLength(xCurrent, d2Current, xNext, d2Next, False)
            remainingLength -= distxCurrentToxNext
            xCurrent = xNext
            d2Current = d2Next
        else:
            ei2Top = n2
            break
    return (ei1Left, ei1Right, ei2Bottom, ei2Top)