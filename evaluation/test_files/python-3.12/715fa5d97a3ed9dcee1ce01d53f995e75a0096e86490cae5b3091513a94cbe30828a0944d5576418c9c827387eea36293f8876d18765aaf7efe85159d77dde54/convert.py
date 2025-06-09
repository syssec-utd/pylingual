"""
This module contains converter functions that will serve to:
1. Write from base classes to Xmipp specific files
2. Read from Xmipp files to base classes
"""
import os
from os.path import join, exists
from collections import OrderedDict
try:
    from itertools import izip
except ImportError:
    izip = zip
import numpy as np
from pyworkflow.utils import replaceBaseExt
from pyworkflow.utils.path import cleanPath
from pyworkflow.object import ObjectWrap, String, Float, Integer, Object
from pwem.constants import NO_INDEX, ALIGN_NONE, ALIGN_PROJ, ALIGN_2D, ALIGN_3D
from pwem.objects import Angles, Coordinate, Micrograph, Volume, Particle, MovieParticle, CTFModel, Acquisition, SetOfParticles, Class3D, SetOfVolumes, Transform
from pwem.emlib.image import ImageHandler
import pwem.emlib.metadata as md
from xmipp3.base import getLabelPythonType, iterMdRows
from pwem import emlib

def prefixAttribute(attribute):
    return '_xmipp_%s' % attribute
if not getattr(emlib, 'GHOST_ACTIVATED', False):
    ' Some of MDL may not exist when Ghost is activated\n    '
    ACQUISITION_DICT = OrderedDict([('_amplitudeContrast', emlib.MDL_CTF_Q0), ('_sphericalAberration', emlib.MDL_CTF_CS), ('_voltage', emlib.MDL_CTF_VOLTAGE)])
    COOR_DICT = OrderedDict([('_x', emlib.MDL_XCOOR), ('_y', emlib.MDL_YCOOR)])
    COOR_EXTRA_LABELS = [md.RLN_PARTICLE_AUTOPICK_FOM, md.RLN_PARTICLE_CLASS, md.RLN_ORIENT_PSI, emlib.MDL_GOOD_REGION_SCORE]
    CTF_DICT = OrderedDict([('_defocusU', emlib.MDL_CTF_DEFOCUSU), ('_defocusV', emlib.MDL_CTF_DEFOCUSV), ('_defocusAngle', emlib.MDL_CTF_DEFOCUS_ANGLE), ('_resolution', emlib.MDL_CTF_CRIT_MAXFREQ), ('_fitQuality', emlib.MDL_CTF_CRIT_FITTINGSCORE)])
    CTF_DICT_NORESOLUTION = OrderedDict([('_defocusU', emlib.MDL_CTF_DEFOCUSU), ('_defocusV', emlib.MDL_CTF_DEFOCUSV), ('_defocusAngle', emlib.MDL_CTF_DEFOCUS_ANGLE)])
    CTF_PSD_DICT = OrderedDict([('_psdFile', emlib.MDL_PSD), (prefixAttribute('enhanced_psd'), emlib.MDL_PSD_ENHANCED), (prefixAttribute('ctfmodel_quadrant'), emlib.MDL_IMAGE1), (prefixAttribute('ctfmodel_halfplane'), emlib.MDL_IMAGE1)])
    CTF_EXTRA_LABELS = [emlib.MDL_CTF_CA, emlib.MDL_CTF_ENERGY_LOSS, emlib.MDL_CTF_LENS_STABILITY, emlib.MDL_CTF_CONVERGENCE_CONE, emlib.MDL_CTF_LONGITUDINAL_DISPLACEMENT, emlib.MDL_CTF_TRANSVERSAL_DISPLACEMENT, emlib.MDL_CTF_K, emlib.MDL_CTF_BG_GAUSSIAN_K, emlib.MDL_CTF_BG_GAUSSIAN_SIGMAU, emlib.MDL_CTF_BG_GAUSSIAN_SIGMAV, emlib.MDL_CTF_BG_GAUSSIAN_CU, emlib.MDL_CTF_BG_GAUSSIAN_CV, emlib.MDL_CTF_BG_SQRT_K, emlib.MDL_CTF_BG_SQRT_U, emlib.MDL_CTF_BG_SQRT_V, emlib.MDL_CTF_BG_SQRT_ANGLE, emlib.MDL_CTF_BG_BASELINE, emlib.MDL_CTF_BG_GAUSSIAN2_K, emlib.MDL_CTF_BG_GAUSSIAN2_SIGMAU, emlib.MDL_CTF_BG_GAUSSIAN2_SIGMAV, emlib.MDL_CTF_BG_GAUSSIAN2_CU, emlib.MDL_CTF_BG_GAUSSIAN2_CV, emlib.MDL_CTF_BG_GAUSSIAN2_ANGLE, emlib.MDL_CTF_CRIT_FITTINGCORR13, emlib.MDL_CTF_CRIT_ICENESS, emlib.MDL_CTF_VPP_RADIUS, emlib.MDL_CTF_DOWNSAMPLE_PERFORMED, emlib.MDL_CTF_CRIT_PSDVARIANCE, emlib.MDL_CTF_CRIT_PSDPCA1VARIANCE, emlib.MDL_CTF_CRIT_PSDPCARUNSTEST, emlib.MDL_CTF_CRIT_FIRSTZEROAVG, emlib.MDL_CTF_CRIT_DAMPING, emlib.MDL_CTF_CRIT_FIRSTZERORATIO, emlib.MDL_CTF_CRIT_PSDCORRELATION90, emlib.MDL_CTF_CRIT_PSDRADIALINTEGRAL, emlib.MDL_CTF_CRIT_NORMALITY, emlib.MDL_CTF_Q0, emlib.MDL_CTF_CS, emlib.MDL_CTF_VOLTAGE, emlib.MDL_CTF_SAMPLING_RATE]
    CTF_EXTRA_LABELS_PLUS_RESOLUTION = [emlib.MDL_CTF_CA, emlib.MDL_CTF_ENERGY_LOSS, emlib.MDL_CTF_LENS_STABILITY, emlib.MDL_CTF_CONVERGENCE_CONE, emlib.MDL_CTF_LONGITUDINAL_DISPLACEMENT, emlib.MDL_CTF_TRANSVERSAL_DISPLACEMENT, emlib.MDL_CTF_K, emlib.MDL_CTF_BG_GAUSSIAN_K, emlib.MDL_CTF_BG_GAUSSIAN_SIGMAU, emlib.MDL_CTF_BG_GAUSSIAN_SIGMAV, emlib.MDL_CTF_BG_GAUSSIAN_CU, emlib.MDL_CTF_BG_GAUSSIAN_CV, emlib.MDL_CTF_BG_SQRT_K, emlib.MDL_CTF_BG_SQRT_U, emlib.MDL_CTF_BG_SQRT_V, emlib.MDL_CTF_BG_SQRT_ANGLE, emlib.MDL_CTF_BG_BASELINE, emlib.MDL_CTF_BG_GAUSSIAN2_K, emlib.MDL_CTF_BG_GAUSSIAN2_SIGMAU, emlib.MDL_CTF_BG_GAUSSIAN2_SIGMAV, emlib.MDL_CTF_BG_GAUSSIAN2_CU, emlib.MDL_CTF_BG_GAUSSIAN2_CV, emlib.MDL_CTF_BG_GAUSSIAN2_ANGLE, emlib.MDL_CTF_CRIT_MAXFREQ, emlib.MDL_CTF_CRIT_FITTINGSCORE, emlib.MDL_CTF_CRIT_FITTINGCORR13, emlib.MDL_CTF_CRIT_ICENESS, emlib.MDL_CTF_DOWNSAMPLE_PERFORMED, emlib.MDL_CTF_CRIT_PSDVARIANCE, emlib.MDL_CTF_CRIT_PSDPCA1VARIANCE, emlib.MDL_CTF_CRIT_PSDPCARUNSTEST, emlib.MDL_CTF_CRIT_FIRSTZEROAVG, emlib.MDL_CTF_CRIT_DAMPING, emlib.MDL_CTF_CRIT_FIRSTZERORATIO, emlib.MDL_CTF_CRIT_PSDCORRELATION90, emlib.MDL_CTF_CRIT_PSDRADIALINTEGRAL, emlib.MDL_CTF_CRIT_NORMALITY, emlib.MDL_CTF_Q0, emlib.MDL_CTF_CS, emlib.MDL_CTF_VOLTAGE, emlib.MDL_CTF_SAMPLING_RATE, emlib.MDL_CTF_VPP_RADIUS]
    IMAGE_EXTRA_LABELS = [emlib.MDL_ZSCORE, emlib.MDL_ZSCORE_HISTOGRAM, emlib.MDL_ZSCORE_RESMEAN, emlib.MDL_ZSCORE_RESVAR, emlib.MDL_ZSCORE_RESCOV, emlib.MDL_ZSCORE_SHAPE1, emlib.MDL_ZSCORE_SHAPE2, emlib.MDL_ZSCORE_SNR1, emlib.MDL_ZSCORE_SNR2, emlib.MDL_CUMULATIVE_SSNR, emlib.MDL_PARTICLE_ID, emlib.MDL_FRAME_ID, emlib.MDL_SCORE_BY_VAR, emlib.MDL_SCORE_BY_GINI, emlib.MDL_ZSCORE_DEEPLEARNING1]
    ANGLES_DICT = OrderedDict([('_angleY', emlib.MDL_ANGLE_Y), ('_angleY2', emlib.MDL_ANGLE_Y2), ('_angleTilt', emlib.MDL_ANGLE_TILT)])
    ALIGNMENT_DICT = OrderedDict([(prefixAttribute('shiftX'), emlib.MDL_SHIFT_X), (prefixAttribute('shiftY'), emlib.MDL_SHIFT_Y), (prefixAttribute('shiftZ'), emlib.MDL_SHIFT_Z), (prefixAttribute('flip'), emlib.MDL_FLIP), (prefixAttribute('anglePsi'), emlib.MDL_ANGLE_PSI), (prefixAttribute('angleRot'), emlib.MDL_ANGLE_ROT), (prefixAttribute('angleTilt'), emlib.MDL_ANGLE_TILT)])

def objectToRow(obj, row, attrDict, extraLabels=[]):
    """ This function will convert an EMObject into a Row.
    Params:
        obj: the EMObject instance (input)
        row: the Row instance (output)  -see emlib.metadata.utils.Row()-
        attrDict: dictionary with the map between obj attributes(keys) and
            row MDLabels in Xmipp (values).
        extraLabels: a list with extra labels that could be included
            as _xmipp_labelName
    """
    if obj.isEnabled():
        enabled = 1
    else:
        enabled = -1
    row.setValue(emlib.MDL_ENABLED, enabled)
    for attr, label in attrDict.items():
        if hasattr(obj, attr):
            valueType = getLabelPythonType(label)
            value = getattr(obj, attr).get()
            try:
                row.setValue(label, valueType(value))
            except Exception as e:
                print(e)
                print('Problems found converting metadata: ')
                print('Label id = %s' % label)
                print('Attribute = %s' % attr)
                print('Value = %s' % value)
                print('Value type = %s' % valueType)
                raise e
            row.setValue(label, valueType(getattr(obj, attr).get()))
    attrLabels = attrDict.values()
    for label in extraLabels:
        attrName = prefixAttribute(emlib.label2Str(label))
        if label not in attrLabels and hasattr(obj, attrName):
            value = obj.getAttributeValue(attrName)
            row.setValue(label, value)

def rowToObject(row, obj, attrDict, extraLabels=[]):
    """ This function will convert from a Row to an EMObject.
    Params:
        row: the Row instance (input)  -see emlib.metadata.utils.Row()-
        obj: the EMObject instance (output)
        attrDict: dictionary with the map between obj attributes(keys) and
            row MDLabels in Xmipp (values).
        extraLabels: a list with extra labels that could be included
            as _xmipp_labelName
    """
    obj.setEnabled(row.getValue(emlib.MDL_ENABLED, 1) > 0)
    for attr, label in attrDict.items():
        value = row.getValue(label)
        if not hasattr(obj, attr):
            setattr(obj, attr, ObjectWrap(value))
        else:
            getattr(obj, attr).set(value)
    attrLabels = attrDict.values()
    for label in extraLabels:
        if label not in attrLabels and row.hasLabel(label):
            labelStr = emlib.label2Str(label)
            setattr(obj, prefixAttribute(labelStr), row.getValueAsObject(label))

def setXmippAttributes(obj, objRow, *labels, **kwargs):
    """ Set the labels attribute(s) to obj from a objRow
        (those not basic ones).
        More than one label can be set
        and default can also be a list of same number of entries.
        The new attribute will be named _xmipp_LabelName
        and the datatype will be set correctly.
        If obj doesn't contain a label and a default value is in kwargs,
        it's set in its corresponding Scipion datatype.
    """
    defaults = kwargs.get('default', None)
    for idx, label in enumerate(labels):
        if objRow.containsLabel(label):
            value = objRow.getValueAsObject(label)
        else:
            if isinstance(defaults, list):
                value = defaults[idx]
            else:
                value = defaults
            value = getScipionObj(value)
        if value is not None:
            setXmippAttribute(obj, label, value)

def getScipionObj(value):
    if isinstance(value, Object):
        return value
    elif isinstance(value, int):
        return Integer(value)
    elif isinstance(value, float):
        return Float(value)
    elif isinstance(value, str):
        return String(value)
    else:
        return None

def setXmippAttribute(obj, label, value):
    """ Sets an attribute of an object prefixing it with xmipp"""
    setattr(obj, prefixAttribute(emlib.label2Str(label)), value)

def getXmippAttribute(obj, label, default=None):
    """ Sets an attribute of an object prefixing it with xmipp"""
    return getattr(obj, prefixAttribute(emlib.label2Str(label)), default)

def rowFromMd(mdIn, objId):
    row = md.Row()
    row.readFromMd(mdIn, objId)
    return row

def _containsAll(row, labels):
    """ Check if the labels (values) in labelsDict
    are present in the row.
    """
    values = labels.values() if isinstance(labels, dict) else labels
    return all((row.containsLabel(l) for l in values))

def _containsAny(row, labels):
    """ Check if the labels (values) in labelsDict
    are present in the row.
    """
    values = labels.values() if isinstance(labels, dict) else labels
    return any((row.containsLabel(l) for l in values))

def _rowToObjectFunc(obj):
    """ From a given object, return the function rowTo{OBJECT_CLASS_NAME}. """
    return globals()['rowTo' + obj.getClassName()]

def _readSetFunc(obj):
    """ From a given object, return the function read{OBJECT_CLASS_NAME}. """
    return globals()['read' + obj.getClassName()]

def locationToXmipp(index, filename):
    """ Convert an index and filename location
    to a string with @ as expected in Xmipp.
    """
    return ImageHandler.locationToXmipp((index, filename))

def fixVolumeFileName(image):
    """ This method will add :mrc to .mrc volumes
    because for mrc format is not possible to distinguish
    between 3D volumes and 2D stacks.
    """
    return ImageHandler.fixXmippVolumeFileName(image)

def getMovieFileName(movie):
    """ Add the :mrcs or :ems extensions to movie files to be
    recognized by Xmipp as proper stack files.
    """
    fn = movie.getFileName()
    if fn.endswith('.mrc'):
        fn += ':mrcs'
    elif fn.endswith('.em'):
        fn += ':ems'
    return fn

def getImageLocation(image):
    return ImageHandler.locationToXmipp(image)

def xmippToLocation(xmippFilename):
    """ Return a location (index, filename) given
    a Xmipp filename with the index@filename structure. """
    if '@' in xmippFilename:
        return emlib.FileName(xmippFilename).decompose()
    else:
        return (NO_INDEX, str(xmippFilename))

def setObjId(obj, mdRow, label=emlib.MDL_ITEM_ID):
    if mdRow.containsLabel(label):
        obj.setObjId(mdRow.getValue(label))
    else:
        obj.setObjId(None)

def setRowId(mdRow, obj, label=emlib.MDL_ITEM_ID):
    mdRow.setValue(label, int(obj.getObjId()))

def micrographToCTFParam(mic, ctfparam):
    """ This function is used to convert a Micrograph object
    to the .ctfparam metadata needed by some Xmipp programs.
    If the micrograph already comes from xmipp, the ctfparam
    will be returned, if not, the new file.
    """
    ctf = mic.getCTF()
    if hasattr(ctf, '_xmippMd'):
        return ctf._xmippMd.get()
    mdCtf = emlib.MetaData()
    mdCtf.setColumnFormat(False)
    row = md.Row()
    ctfModelToRow(ctf, row)
    acquisitionToRow(mic.getAcquisition(), row)
    row.writeToMd(mdCtf, mdCtf.addObject())
    mdCtf.write(ctfparam)
    return ctfparam

def imageToRow(img, imgRow, imgLabel, **kwargs):
    preprocessImageRow = kwargs.get('preprocessImageRow', None)
    if preprocessImageRow:
        preprocessImageRow(img, imgRow)
    setRowId(imgRow, img)
    index, filename = img.getLocation()
    fn = locationToXmipp(index, filename)
    imgRow.setValue(imgLabel, fn)
    if kwargs.get('writeCtf', True) and img.hasCTF():
        ctfModelToRow(img.getCTF(), imgRow)
    alignType = kwargs.get('alignType')
    if alignType != ALIGN_NONE:
        alignmentToRow(img.getTransform(), imgRow, alignType)
    if kwargs.get('writeAcquisition', True) and img.hasAcquisition():
        acquisitionToRow(img.getAcquisition(), imgRow)
    objectToRow(img, imgRow, {}, extraLabels=IMAGE_EXTRA_LABELS)
    postprocessImageRow = kwargs.get('postprocessImageRow', None)
    if postprocessImageRow:
        postprocessImageRow(img, imgRow)

def rowToImage(imgRow, imgLabel, imgClass, **kwargs):
    """ Create an Image from a row of a metadata. """
    img = imgClass()
    preprocessImageRow = kwargs.get('preprocessImageRow', None)
    if preprocessImageRow:
        preprocessImageRow(img, imgRow)
    index, filename = xmippToLocation(imgRow.getValue(imgLabel))
    img.setLocation(index, filename)
    if imgRow.containsLabel(emlib.MDL_REF):
        img.setClassId(imgRow.getValue(emlib.MDL_REF))
    elif imgRow.containsLabel(emlib.MDL_REF3D):
        img.setClassId(imgRow.getValue(emlib.MDL_REF3D))
    if kwargs.get('readCtf', True):
        img.setCTF(rowToCtfModel(imgRow))
    alignType = kwargs.get('alignType')
    if alignType != ALIGN_NONE:
        img.setTransform(rowToAlignment(imgRow, alignType))
    if kwargs.get('readAcquisition', True):
        img.setAcquisition(rowToAcquisition(imgRow))
    if kwargs.get('magnification', None):
        img.getAcquisition().setMagnification(kwargs.get('magnification'))
    setObjId(img, imgRow)
    rowToObject(imgRow, img, {}, extraLabels=IMAGE_EXTRA_LABELS + kwargs.get('extraLabels', []))
    postprocessImageRow = kwargs.get('postprocessImageRow', None)
    if postprocessImageRow:
        postprocessImageRow(img, imgRow)
    return img

def micrographToRow(mic, micRow, **kwargs):
    """ Set labels values from Micrograph mic to md row. """
    imageToRow(mic, micRow, imgLabel=emlib.MDL_MICROGRAPH, **kwargs)

def rowToMicrograph(micRow, **kwargs):
    """ Create a Micrograph object from a row of Xmipp metadata. """
    return rowToImage(micRow, emlib.MDL_MICROGRAPH, Micrograph, **kwargs)

def volumeToRow(vol, volRow, **kwargs):
    """ Set labels values from Micrograph mic to md row. """
    imageToRow(vol, volRow, imgLabel=emlib.MDL_IMAGE, writeAcquisition=False, **kwargs)

def rowToVolume(volRow, **kwargs):
    """ Create a Volume object from a row of Xmipp metadata. """
    return rowToImage(volRow, emlib.MDL_IMAGE, Volume, **kwargs)

def coordinateToRow(coord, coordRow, copyId=True):
    """ Set labels values from Coordinate coord to md row. """
    if copyId:
        setRowId(coordRow, coord)
    objectToRow(coord, coordRow, COOR_DICT, extraLabels=COOR_EXTRA_LABELS)
    if coord.getMicId():
        coordRow.setValue(emlib.MDL_MICROGRAPH, str(coord.getMicId()))

def rowToCoordinate(coordRow):
    """ Create a Coordinate from a row of a metadata. """
    if _containsAll(coordRow, COOR_DICT):
        coord = Coordinate()
        rowToObject(coordRow, coord, COOR_DICT, extraLabels=COOR_EXTRA_LABELS)
        try:
            coord.setMicId(int(coordRow.getValue(emlib.MDL_MICROGRAPH_ID)))
        except Exception:
            pass
    else:
        coord = None
    return coord

def _rowToParticle(partRow, particleClass, **kwargs):
    """ Create a Particle from a row of a metadata. """
    postprocessImageRow = kwargs.get('postprocessImageRow', None)
    if postprocessImageRow:
        del kwargs['postprocessImageRow']
    img = rowToImage(partRow, emlib.MDL_IMAGE, particleClass, **kwargs)
    img.setCoordinate(rowToCoordinate(partRow))
    try:
        if partRow.hasLabel(emlib.MDL_MICROGRAPH_ID):
            img.setMicId(partRow.getValue(emlib.MDL_MICROGRAPH_ID))
    except Exception as e:
        print('Warning:', e.message)
    if postprocessImageRow:
        postprocessImageRow(img, partRow)
    return img

def rowToParticle(partRow, **kwargs):
    return _rowToParticle(partRow, Particle, **kwargs)

def rowToMovieParticle(partRow, **kwargs):
    return _rowToParticle(partRow, MovieParticle, **kwargs)

def particleToRow(part, partRow, **kwargs):
    """ Set labels values from Particle to md row. """
    imageToRow(part, partRow, emlib.MDL_IMAGE, **kwargs)
    coord = part.getCoordinate()
    if coord is not None:
        coordinateToRow(coord, partRow, copyId=False)
    if part.hasMicId():
        partRow.setValue(emlib.MDL_MICROGRAPH_ID, int(part.getMicId()))
        partRow.setValue(emlib.MDL_MICROGRAPH, str(part.getMicId()))

def rowToClass(classRow, classItem):
    """ Method base to create a class2D, class3D or classVol from
    a row of a metadata
    """
    setObjId(classItem, classRow, label=emlib.MDL_REF)
    if classRow.containsLabel(emlib.MDL_IMAGE):
        index, filename = xmippToLocation(classRow.getValue(emlib.MDL_IMAGE))
        img = classItem.REP_TYPE()
        img.setLocation(index, filename)
        img.setSamplingRate(classItem.getSamplingRate())
        classItem.setRepresentative(img)
    return classItem

def class2DToRow(class2D, classRow):
    """ Set labels values from Class2D to md row. """
    if class2D.hasRepresentative():
        index, filename = class2D.getRepresentative().getLocation()
        fn = locationToXmipp(index, filename)
        classRow.setValue(emlib.MDL_IMAGE, fn)
    n = int(len(class2D))
    classRow.setValue(emlib.MDL_CLASS_COUNT, n)
    classRow.setValue(emlib.MDL_REF, int(class2D.getObjId()))
    classRow.setValue(emlib.MDL_ITEM_ID, int(class2D.getObjId()))

def ctfModelToRow(ctfModel, ctfRow):
    """ Set labels values from ctfModel to md row. """
    if ctfModel.hasResolution():
        objectToRow(ctfModel, ctfRow, CTF_DICT, extraLabels=CTF_EXTRA_LABELS)
        if ctfModel.hasPhaseShift():
            ctfRow.setValue(emlib.MDL_CTF_PHASE_SHIFT, ctfModel.getPhaseShift())
    else:
        objectToRow(ctfModel, ctfRow, CTF_DICT_NORESOLUTION, extraLabels=CTF_EXTRA_LABELS)

def defocusGroupSetToRow(defocusGroup, defocusGroupRow):
    """ Set labels values from ctfModel to md row. """
    objectToRow(defocusGroup, defocusGroupRow, CTF_DICT)

def setPsdFiles(ctfModel, ctfRow):
    """ Set the PSD files of CTF estimation related
    to this ctfModel. The values will be read from
    the ctfRow if present.
    """
    for attr, label in CTF_PSD_DICT.items():
        if ctfRow.containsLabel(label):
            setattr(ctfModel, attr, String(ctfRow.getValue(label)))

def rowToCtfModel(ctfRow):
    """ Create a CTFModel from a row of a metadata. """
    if _containsAll(ctfRow, CTF_DICT_NORESOLUTION):
        ctfModel = CTFModel()
        if ctfRow.hasLabel(md.MDL_CTF_PHASE_SHIFT):
            ctfModel.setPhaseShift(ctfRow.getValue(md.MDL_CTF_PHASE_SHIFT, 0))
        if ctfRow.containsLabel(emlib.label2Str(emlib.MDL_CTF_CRIT_MAXFREQ)):
            rowToObject(ctfRow, ctfModel, CTF_DICT, extraLabels=CTF_EXTRA_LABELS)
        else:
            rowToObject(ctfRow, ctfModel, CTF_DICT_NORESOLUTION, extraLabels=CTF_EXTRA_LABELS_PLUS_RESOLUTION)
        ctfModel.standardize()
        setPsdFiles(ctfModel, ctfRow)
    else:
        ctfModel = None
    return ctfModel

def acquisitionToRow(acquisition, ctfRow):
    """ Set labels values from acquisition to md row. """
    objectToRow(acquisition, ctfRow, ACQUISITION_DICT)

def rowToAcquisition(acquisitionRow):
    """ Create an acquisition from a row of a metadata. """
    if _containsAll(acquisitionRow, ACQUISITION_DICT):
        acquisition = Acquisition()
        rowToObject(acquisitionRow, acquisition, ACQUISITION_DICT)
    else:
        acquisition = None
    return acquisition

def readSetOfMicrographs(filename, micSet, **kwargs):
    readSetOfImages(filename, micSet, rowToMicrograph, **kwargs)

def writeSetOfMicrographs(micSet, filename, blockName='Micrographs', **kwargs):
    writeSetOfImages(micSet, filename, micrographToRow, blockName, **kwargs)

def readSetOfVolumes(filename, volSet, **kwargs):
    readSetOfImages(filename, volSet, rowToVolume, **kwargs)

def writeSetOfVolumes(volSet, filename, blockName='Volumes', **kwargs):
    writeSetOfImages(volSet, filename, volumeToRow, blockName, **kwargs)

def mdToCTFModel(mdIn, mic):
    ctfRow = rowFromMd(mdIn, mdIn.firstObject())
    ctfObj = rowToCtfModel(ctfRow)
    setXmippAttributes(ctfObj, ctfRow, emlib.MDL_CTF_CRIT_NONASTIGMATICVALIDITY, emlib.MDL_CTF_CRIT_FIRSTMINIMUM_FIRSTZERO_DIFF_RATIO)
    ctfObj.setMicrograph(mic)
    return ctfObj

def readCTFModel(filename, mic):
    """ Read from Xmipp .ctfparam and create a CTFModel object. """
    mdCtf = emlib.MetaData(filename)
    return mdToCTFModel(mdCtf, mic)

def openMd(fn, state='Manual'):
    f = open(fn, 'w')
    ismanual = state == 'Manual'
    block = 'data_particles' if ismanual else 'data_particles_auto'
    s = '# XMIPP_STAR_1 *\n#\ndata_header\nloop_\n _pickingMicrographState\n%s\n%s\nloop_\n _itemId\n _enabled\n _xcoor\n _ycoor\n _cost\n _micrographId\n' % (state, block)
    f.write(s)
    return f

def writeSetOfCoordinates(posDir, coordSet, ismanual=True, scale=1):
    state = 'Manual' if ismanual else 'Supervised'
    writeSetOfCoordinatesWithState(posDir, coordSet, state, scale)

def writeSetOfCoordinatesWithState(posDir, coordSet, state, scale=1):
    """ Write a pos file on metadata format for each micrograph
    on the coordSet.
    Params:
        posDir: the directory where the .pos files will be written.
        coordSet: the SetOfCoordinates that will be read.
    """
    boxSize = coordSet.getBoxSize() or 100
    posDict = {}
    for mic in coordSet.iterMicrographs():
        micIndex, micFileName = mic.getLocation()
        micName = os.path.basename(micFileName)
        if micIndex != NO_INDEX:
            micName = '%06d_at_%s' % (micIndex, micName)
        posFn = join(posDir, replaceBaseExt(micName, 'pos'))
        posDict[mic.getObjId()] = posFn
    f = None
    lastMicId = None
    c = 0
    for coord in coordSet.iterItems(orderBy='_micId'):
        micId = coord.getMicId()
        if micId != lastMicId:
            if f:
                f.close()
                c = 0
            f = openMd(posDict[micId], state)
            lastMicId = micId
        c += 1
        if scale != 1:
            x = coord.getX() * scale
            y = coord.getY() * scale
        else:
            x = coord.getX()
            y = coord.getY()
        f.write(' %06d   1   %d  %d  %d   %06d\n' % (coord.getObjId(), x, y, 1, micId))
    if f:
        f.close()
    configFn = join(posDir, 'config.xmd')
    writeCoordsConfig(configFn, int(boxSize), state)
    return posDict.values()

def writeCoordsConfig(configFn, boxSize, state):
    """ Write the config.xmd file needed for Xmipp picker.
    Params:
        configFn: The filename were to store the configuration.
        boxSize: the box size in pixels for extraction.
        state: picker state
    """
    print('writeCoordsConfig: state=', state)
    mdCoord = emlib.MetaData()
    objId = mdCoord.addObject()
    mdCoord.setValue(emlib.MDL_PICKING_PARTICLE_SIZE, int(boxSize), objId)
    mdCoord.setValue(emlib.MDL_PICKING_STATE, state, objId)
    mdCoord.write('properties@%s' % configFn)

def writeMicCoordinates(mic, coordList, outputFn, isManual=True, getPosFunc=None):
    """ Write the pos file as expected by Xmipp with the coordinates
    of a given micrograph.
    Params:
        mic: input micrograph.
        coordList: list of (x, y) pairs of the mic coordinates.
        outputFn: output filename for the pos file .
        isManual: if the coordinates are 'Manual' or 'Supervised'
        getPosFunc: a function to get the positions from the coordinate,
            it can be useful for scaling the coordinates if needed.
    """
    if getPosFunc is None:
        getPosFunc = lambda coord: coord.getPosition()
    state = 'Manual' if isManual else 'Supervised'
    f = openMd(outputFn, state)
    for coord in coordList:
        x, y = getPosFunc(coord)
        f.write(' %06d   1   %d  %d  %d   %06d \n' % (coord.getObjId(), x, y, 1, mic.getObjId()))
    f.close()

def readSetOfCoordinates(outputDir, micSet, coordSet, readDiscarded=False, scale=1):
    """ Read from Xmipp .pos files.
    Params:
        outputDir: the directory where the .pos files are.
            It is also expected a file named: config.xmd
            in this directory where the box size can be read.
        micSet: the SetOfMicrographs to associate the .pos, which
            name should be the same of the micrographs.
        coordSet: the SetOfCoordinates that will be populated.
        readDiscarded: read only the coordinates with the MDL_ENABLE set at -1
        scale: Factor to scale ONLY x,y coordinates, you are supposed to use an appropiate boxsize (you created the set)
    """
    configfile = join(outputDir, 'config.xmd')
    if exists(configfile):
        mdCoords = emlib.MetaData('properties@' + join(outputDir, 'config.xmd'))
        boxSize = mdCoords.getValue(emlib.MDL_PICKING_PARTICLE_SIZE, mdCoords.firstObject())
        coordSet.setBoxSize(int(boxSize))
    for mic in micSet:
        posFile = join(outputDir, replaceBaseExt(mic.getFileName(), 'pos'))
        readCoordinates(mic, posFile, coordSet, outputDir, readDiscarded, scale=scale)
    coordSet._xmippMd = String(outputDir)

def readCoordinates(mic, fileName, coordsSet, outputDir, readDiscarded=False, scale=1):
    posMd = readPosCoordinates(fileName, readDiscarded)
    posMd.addLabel(md.MDL_ITEM_ID)
    for objId in posMd:
        if posMd.getValue(md.MDL_ENABLED, objId) == 0:
            posMd.setValue(md.MDL_ENABLED, 1, objId)
        coord = rowToCoordinate(rowFromMd(posMd, objId))
        coord.setMicrograph(mic)
        coord.setX(int(coord.getX() * scale))
        coord.setY(int(coord.getY() * scale))
        coordsSet.append(coord)
        posMd.setValue(md.MDL_ITEM_ID, int(coord.getObjId()), objId)

def readPosCoordinates(posFile, readDiscarded=False):
    """ Read the coordinates in .pos file and return corresponding metadata.
    There are two possible blocks with particles:
    particles: with manual/supervised particles
    particles_auto: with automatically picked particles.
    If posFile doesn't exist, the metadata will be empty
    readDiscarded: read only the coordinates in the particles_auto DB
                   with the MDL_ENABLE set at -1 and a positive cost
    """
    mData = md.MetaData()
    if exists(posFile):
        blocks = md.getBlocksInMetaDataFile(posFile)
        blocksToRead = ['particles_auto'] if readDiscarded else ['particles', 'particles_auto']
        for b in blocksToRead:
            if b in blocks:
                mdAux = md.MetaData('%(b)s@%(posFile)s' % locals())
                mData.unionAll(mdAux)
        if readDiscarded:
            for objId in mData:
                if mData.getValue(md.MDL_COST, objId) > 0:
                    enabled = mData.getValue(md.MDL_ENABLED, objId)
                    mData.setValue(md.MDL_ENABLED, -1 * enabled, objId)
        mData.removeDisabled()
    return mData

def readSetOfImages(filename, imgSet, rowToFunc, **kwargs):
    """read from Xmipp image metadata.
        filename: The metadata filename where the image are.
        imgSet: the SetOfParticles that will be populated.
        rowToFunc: this function will be used to convert the row to Object
    """
    imgMd = emlib.MetaData(filename)
    if kwargs.get('removeDisabled', True):
        imgMd.removeDisabled()
    if 'alignType' not in kwargs:
        imgRow = rowFromMd(imgMd, imgMd.firstObject())
        if _containsAny(imgRow, ALIGNMENT_DICT):
            if imgRow.containsLabel(emlib.MDL_ANGLE_TILT):
                kwargs['alignType'] = ALIGN_PROJ
            else:
                kwargs['alignType'] = ALIGN_2D
        else:
            kwargs['alignType'] = ALIGN_NONE
    if imgMd.size() > 0:
        for objId in imgMd:
            imgRow = rowFromMd(imgMd, objId)
            img = rowToFunc(imgRow, **kwargs)
            imgSet.append(img)
        imgSet.setHasCTF(img.hasCTF())
        imgSet.setAlignment(kwargs['alignType'])

def setOfImagesToMd(imgSet, mdIn, imgToFunc, **kwargs):
    """ This function will fill Xmipp metadata from a SetOfMicrographs
    Params:
        imgSet: the set of images to be converted to metadata
        mdIn: metadata to be filled
        rowFunc: this function can be used to setup the row before
            adding to metadata.
    """
    if 'alignType' not in kwargs:
        kwargs['alignType'] = imgSet.getAlignment()
    if 'where' in kwargs:
        where = kwargs['where']
        for img in imgSet.iterItems(where=where):
            objId = mdIn.addObject()
            imgRow = md.Row()
            imgToFunc(img, imgRow, **kwargs)
            imgRow.writeToMd(mdIn, objId)
    else:
        for img in imgSet:
            objId = mdIn.addObject()
            imgRow = md.Row()
            imgToFunc(img, imgRow, **kwargs)
            imgRow.writeToMd(mdIn, objId)

def readAnglesFromMicrographs(micFile, anglesSet):
    """ Read the angles from a micrographs Metadata.
    """
    micMd = emlib.MetaData(micFile)
    for objId in micMd:
        angles = Angles()
        row = rowFromMd(micMd, objId)
        rowToObject(row, angles, ANGLES_DICT)
        angles.setObjId(micMd.getValue(emlib.MDL_ITEM_ID, objId))
        anglesSet.append(angles)

def writeSetOfImages(imgSet, filename, imgToFunc, blockName='Images', **kwargs):
    """ This function will write a SetOfImages as a Xmipp metadata.
    Params:
        imgSet: the set of images to be written (particles,
        micrographs or volumes)
        filename: the filename where to write the metadata.
        rowFunc: this function can be used to setup the row before
            adding to metadata.
    """
    mdSet = emlib.MetaData()
    setOfImagesToMd(imgSet, mdSet, imgToFunc, **kwargs)
    mdSet.write('%s@%s' % (blockName, filename))

def readSetOfParticles(filename, partSet, **kwargs):
    readSetOfImages(filename, partSet, rowToParticle, **kwargs)

def readSetOfMovieParticles(filename, partSet, **kwargs):
    readSetOfImages(filename, partSet, rowToMovieParticle, **kwargs)

def setOfParticlesToMd(imgSet, mdParts, **kwargs):
    setOfImagesToMd(imgSet, mdParts, particleToRow, **kwargs)

def setOfMicrographsToMd(imgSet, mdMics, **kwargs):
    setOfImagesToMd(imgSet, mdMics, micrographToRow, **kwargs)

def writeSetOfParticles(imgSet, filename, blockName='Particles', **kwargs):
    writeSetOfImages(imgSet, filename, particleToRow, blockName, **kwargs)

def writeCTFModel(ctfModel, ctfFile):
    """ Given a CTFModel object write as Xmipp ctfparam
    """
    mdCtf = emlib.MetaData()
    objId = mdCtf.addObject()
    ctfRow = md.Row()
    ctfModelToRow(ctfModel, ctfRow)
    ctfRow.writeToMd(mdCtf, objId)
    mdCtf.setColumnFormat(False)
    mdCtf.write(ctfFile)

def writeSetOfCTFs(ctfSet, mdCTF):
    """ Write a ctfSet on metadata format.
    Params:
        ctfSet: the SetOfCTF that will be read.
        mdCTF: The file where metadata should be written.
    """
    mdCtf = emlib.MetaData()
    for ctfModel in ctfSet:
        objId = mdCtf.addObject()
        ctfRow = md.Row()
        ctfRow.setValue(emlib.MDL_MICROGRAPH, ctfModel.getMicFile())
        if ctfModel.getPsdFile():
            ctfRow.setValue(emlib.MDL_PSD, ctfModel.getPsdFile())
        ctfModelToRow(ctfModel, ctfRow)
        ctfRow.writeToMd(mdCtf, objId)
    mdCtf.write(mdCTF)
    ctfSet._xmippMd = String(mdCTF)

def writeSetOfDefocusGroups(defocusGroupSet, fnDefocusGroup):
    """ Write a defocuGroupSet on metadata format.
    Params:
        defocusGroupSet: the SetOfDefocus that will be read.
        fnDefocusGroup: The file where defocusGroup should be written.
    """
    mdDefGr = emlib.MetaData()
    for defocusGroup in defocusGroupSet:
        objId = mdDefGr.addObject()
        defocusGroupRow = md.Row()
        defocusGroupSetToRow(defocusGroup, defocusGroupRow)
        defocusGroupRow.setValue(emlib.MDL_CTF_GROUP, defocusGroup.getObjId())
        defocusGroupRow.setValue(emlib.MDL_MIN, defocusGroup.getDefocusMin())
        defocusGroupRow.setValue(emlib.MDL_MAX, defocusGroup.getDefocusMax())
        defocusGroupRow.setValue(emlib.MDL_AVG, defocusGroup.getDefocusAvg())
        defocusGroupRow.writeToMd(mdDefGr, objId)
    mdDefGr.write(fnDefocusGroup)
    defocusGroupSet._xmippMd = String(fnDefocusGroup)

def writeSetOfClasses2D(classes2DSet, filename, classesBlock='classes', writeParticles=True):
    """ This function will write a SetOfClasses2D as Xmipp metadata.
    Params:
        classes2DSet: the SetOfClasses2D instance.
        filename: the filename where to write the metadata.
    """
    classFn = '%s@%s' % (classesBlock, filename)
    classMd = emlib.MetaData()
    classMd.write(classFn)
    classRow = md.Row()
    for class2D in classes2DSet:
        class2DToRow(class2D, classRow)
        classRow.writeToMd(classMd, classMd.addObject())
        if writeParticles:
            ref = class2D.getObjId()
            imagesFn = 'class%06d_images@%s' % (ref, filename)
            imagesMd = emlib.MetaData()
            imgRow = md.Row()
            if class2D.getSize() > 0:
                for img in class2D:
                    particleToRow(img, imgRow)
                    imgRow.writeToMd(imagesMd, imagesMd.addObject())
            imagesMd.write(imagesFn, emlib.MD_APPEND)
    classMd.write(classFn, emlib.MD_APPEND)

def writeSetOfMicrographsPairs(uSet, tSet, filename):
    """ This function will write a MicrographsTiltPair as Xmipp metadata.
    Params:
        uSet: the untilted set of micrographs to be written
        tSet: the tilted set of micrographs to be written
        filename: the filename where to write the metadata.
    """
    mdMics = emlib.MetaData()
    for micU, micT in izip(uSet, tSet):
        objId = mdMics.addObject()
        pairRow = md.Row()
        pairRow.setValue(emlib.MDL_ITEM_ID, int(micU.getObjId()))
        pairRow.setValue(emlib.MDL_MICROGRAPH, micU.getFileName())
        pairRow.setValue(emlib.MDL_MICROGRAPH_TILTED, micT.getFileName())
        pairRow.writeToMd(mdMics, objId)
    mdMics.write(filename)

def __readSetOfClasses(classBaseSet, readSetFunc, classesSet, filename, classesBlock='classes', **kwargs):
    """ Read a set of classes from an Xmipp metadata with the given
    convention of a block for classes and another block for each set of
    images assigned to each class.
    Params:
        classesSet: the SetOfClasses object that will be populated.
        filename: the file path where to read the Xmipp metadata.
        classesBlock (by default 'classes'):
            the block name of the classes group in the metadata.
    """
    blocks = emlib.getBlocksInMetaDataFile(filename)
    classesMd = emlib.MetaData('%s@%s' % (classesBlock, filename))
    preprocessClass = kwargs.get('preprocessClass', None)
    postprocessClass = kwargs.get('postprocessClass', None)
    for objId in classesMd:
        classItem = classesSet.ITEM_TYPE()
        classRow = rowFromMd(classesMd, objId)
        classItem = rowToClass(classRow, classItem)
        classBaseSet.copyInfo(classItem, classesSet.getImages())
        if preprocessClass:
            preprocessClass(classItem, classRow)
        classesSet.append(classItem)
        ref = classItem.getObjId()
        b = 'class%06d_images' % ref
        if b in blocks:
            readSetFunc('%s@%s' % (b, filename), classItem, **kwargs)
        if postprocessClass:
            postprocessClass(classItem, classRow)
        classesSet.update(classItem)

def readSetOfClasses(classesSet, filename, classesBlock='classes', **kwargs):
    __readSetOfClasses(SetOfParticles, readSetOfParticles, classesSet, filename, classesBlock, **kwargs)

def readSetOfClasses2D(classes2DSet, filename, classesBlock='classes', **kwargs):
    """ Just a wrapper to readSetOfClasses. """
    readSetOfClasses(classes2DSet, filename, classesBlock, **kwargs)

def readSetOfClasses3D(classes3DSet, filename, classesBlock='classes', **kwargs):
    """ Just a wrapper to readSetOfClasses. """
    readSetOfClasses(classes3DSet, filename, classesBlock, **kwargs)

def writeSetOfClassesVol(classesVolSet, filename, classesBlock='classes'):
    """ This function will write a SetOfClassesVol as Xmipp metadata.
    Params:
        classesVolSet: the SetOfClassesVol instance.
        filename: the filename where to write the metadata.
    """
    classFn = '%s@%s' % (classesBlock, filename)
    classMd = emlib.MetaData()
    classMd.write(classFn)
    classRow = md.Row()
    for classVol in classesVolSet:
        classVolToRow(classVol, classRow)
        classRow.writeToMd(classMd, classMd.addObject())
        ref = Class3D.getObjId()
        imagesFn = 'class%06d_images@%s' % (ref, filename)
        imagesMd = emlib.MetaData()
        imgRow = md.Row()
        for vol in classVol:
            volumeToRow(vol, imgRow)
            imgRow.writeToMd(imagesMd, imagesMd.addObject())
        imagesMd.write(imagesFn, emlib.MD_APPEND)
    classMd.write(classFn, emlib.MD_APPEND)

def readSetOfClassesVol(classesVolSet, filename, classesBlock='classes', **kwargs):
    """read from Xmipp image metadata.
        fnImages: The metadata filename where the particles properties are.
        imgSet: the SetOfParticles that will be populated.
        hasCtf: is True if the ctf information exists.
    """
    __readSetOfClasses(SetOfVolumes, readSetOfVolumes, classesVolSet, filename, classesBlock, **kwargs)

def writeSetOfMovies(moviesSet, filename, moviesBlock='movies'):
    """ This function will write a SetOfMovies as Xmipp metadata.
    Params:
        moviesSet: the SetOfMovies instance.
        filename: the filename where to write the metadata.
    """
    for movie in moviesSet:
        ref = movie.getObjId()
        micrographsFn = 'movie%06d_micrographs@%s' % (ref, filename)
        micrographsMd = emlib.MetaData()
        micRow = md.Row()
        for mic in movie:
            micrographToRow(mic, micRow)
            micRow.writeToMd(micrographsMd, micrographsMd.addObject())
        micrographsMd.write(micrographsFn, emlib.MD_APPEND)

def geometryFromMatrix(matrix, inverseTransform):
    from pwem.convert.transformations import translation_from_matrix, euler_from_matrix
    if inverseTransform:
        matrix = np.linalg.inv(matrix)
        shifts = -translation_from_matrix(matrix)
    else:
        shifts = translation_from_matrix(matrix)
    angles = -np.rad2deg(euler_from_matrix(matrix, axes='szyz'))
    return (shifts, angles)

def matrixFromGeometry(shifts, angles, inverseTransform):
    """ Create the transformation matrix from a given
    2D shifts in X and Y...and the 3 euler angles.
    """
    from pwem.convert import euler_matrix
    radAngles = -np.deg2rad(angles)
    M = euler_matrix(radAngles[0], radAngles[1], radAngles[2], 'szyz')
    if inverseTransform:
        M[:3, 3] = -shifts[:3]
        M = np.linalg.inv(M)
    else:
        M[:3, 3] = shifts[:3]
    return M

def rowToAlignment(alignmentRow, alignType):
    """
    is2D == True-> matrix is 2D (2D images alignment)
            otherwise matrix is 3D (3D volume alignment or projection)
    invTransform == True  -> for xmipp implies projection
        """
    is2D = alignType == ALIGN_2D
    inverseTransform = alignType == ALIGN_PROJ
    if _containsAny(alignmentRow, ALIGNMENT_DICT):
        alignment = Transform()
        angles = np.zeros(3)
        shifts = np.zeros(3)
        flip = alignmentRow.getValue(emlib.MDL_FLIP)
        shifts[0] = alignmentRow.getValue(emlib.MDL_SHIFT_X, 0.0)
        shifts[1] = alignmentRow.getValue(emlib.MDL_SHIFT_Y, 0.0)
        if not is2D:
            angles[0] = alignmentRow.getValue(emlib.MDL_ANGLE_ROT, 0.0)
            angles[1] = alignmentRow.getValue(emlib.MDL_ANGLE_TILT, 0.0)
            shifts[2] = alignmentRow.getValue(emlib.MDL_SHIFT_Z, 0.0)
            angles[2] = alignmentRow.getValue(emlib.MDL_ANGLE_PSI, 0.0)
            if flip:
                angles[1] = angles[1] + 180
                angles[2] = -angles[2]
                shifts[0] = -shifts[0]
        else:
            psi = alignmentRow.getValue(emlib.MDL_ANGLE_PSI, 0.0)
            rot = alignmentRow.getValue(emlib.MDL_ANGLE_ROT, 0.0)
            if rot != 0.0 and psi != 0:
                print('HORROR rot and psi are different from zero in 2D case')
            angles[0] = alignmentRow.getValue(emlib.MDL_ANGLE_PSI, 0.0) + alignmentRow.getValue(emlib.MDL_ANGLE_ROT, 0.0)
        matrix = matrixFromGeometry(shifts, angles, inverseTransform)
        if flip:
            if alignType == ALIGN_2D:
                matrix[0, :2] *= -1.0
                matrix[2, 2] = -1.0
            elif alignType == ALIGN_3D:
                matrix[0, :3] *= -1.0
                matrix[3, 3] *= -1.0
            elif alignType == ALIGN_PROJ:
                pass
        alignment.setMatrix(matrix)
    else:
        alignment = None
    return alignment

def alignmentToRow(alignment, alignmentRow, alignType):
    """
    is2D == True-> matrix is 2D (2D images alignment)
            otherwise matrix is 3D (3D volume alignment or projection)
    invTransform == True  -> for xmipp implies projection
                          -> for xmipp implies alignment
    """
    if alignment is None:
        return
    is2D = alignType == ALIGN_2D
    inverseTransform = alignType == ALIGN_PROJ
    flip = False
    matrix = alignment.getMatrix()
    if alignType == ALIGN_2D:
        flip = bool(np.linalg.det(matrix[0:2, 0:2]) < 0)
        if flip:
            matrix[0, :2] *= -1.0
            matrix[2, 2] = 1.0
        else:
            pass
    elif alignType == ALIGN_3D:
        flip = bool(np.linalg.det(matrix[0:3, 0:3]) < 0)
        if flip:
            matrix[0, :4] *= -1.0
            matrix[3, 3] = 1.0
        else:
            pass
    else:
        flip = bool(np.linalg.det(matrix[0:3, 0:3]) < 0)
        if flip:
            raise Exception('the det of the transformation matrix is negative. This is not a valid transformation matrix for Scipion.')
    shifts, angles = geometryFromMatrix(matrix, inverseTransform)
    alignmentRow.setValue(emlib.MDL_SHIFT_X, shifts[0])
    alignmentRow.setValue(emlib.MDL_SHIFT_Y, shifts[1])
    if is2D:
        angle = angles[0] + angles[2]
        alignmentRow.setValue(emlib.MDL_ANGLE_PSI, angle)
    else:
        alignmentRow.setValue(emlib.MDL_SHIFT_Z, shifts[2])
        alignmentRow.setValue(emlib.MDL_ANGLE_ROT, angles[0])
        alignmentRow.setValue(emlib.MDL_ANGLE_TILT, angles[1])
        alignmentRow.setValue(emlib.MDL_ANGLE_PSI, angles[2])
    alignmentRow.setValue(emlib.MDL_FLIP, flip)

def fillClasses(clsSet, updateClassCallback=None):
    """ Give an empty SetOfClasses (either 2D or 3D).
    Iterate over the input images and append to the corresponding class.
    It is important that each image has the classId properly set.
    """
    clsDict = {}
    inputImages = clsSet.getImages()
    for img in inputImages:
        ref = img.getClassId()
        if ref is None:
            raise Exception('Particle classId is None!!!')
        if ref not in clsDict:
            classItem = clsSet.ITEM_TYPE(objId=ref)
            rep = clsSet.REP_TYPE()
            classItem.setRepresentative(rep)
            clsDict[ref] = classItem
            classItem.copyInfo(inputImages)
            classItem.setAcquisition(inputImages.getAcquisition())
            if updateClassCallback is not None:
                updateClassCallback(classItem)
            clsSet.append(classItem)
        else:
            classItem = clsDict[ref]
        classItem.append(img)
    for classItem in clsDict.values():
        clsSet.update(classItem)

def createClassesFromImages2(inputImages, inputMd, classesFn, ClassType, classLabel, alignType, getClassFn=None, preprocessImageRow=None):
    """ From an intermediate X.xmd file produced by xmipp, create
    the set of classes in which those images are classified.
    Params:
        inputImages: the SetOfImages that were initially classified by relion.
        inputMd: the filename metadata.
        classesFn: filename where to write the classes.
        ClassType: the output type of the classes set ( usually SetOfClass2D or
        3D )
        classLabel: label that is the class reference.
        classFnTemplate: the template to get the classes averages filenames
        iter: the iteration number, just used in Class template
    """
    mdIter = iterMdRows(inputMd)
    clsDict = {}
    clsSet = ClassType(filename=classesFn)
    clsSet.setImages(inputImages)
    hasCtf = inputImages.hasCTF()
    sampling = inputImages.getSamplingRate()
    for img, row in izip(inputImages, mdIter):
        ref = row.getValue(emlib.MDL_REF)
        if ref is None:
            raise Exception('MDL_REF not found in metadata: %s' % inputMd)
        if ref not in clsDict:
            classItem = clsSet.ITEM_TYPE(objId=ref)
            if getClassFn is None:
                refFn = ''
            else:
                refFn = getClassFn(ref)
            refLocation = xmippToLocation(refFn)
            rep = clsSet.REP_TYPE()
            rep.setLocation(refLocation)
            rep.setSamplingRate(sampling)
            classItem.setRepresentative(rep)
            clsDict[ref] = classItem
            classItem.copyInfo(inputImages)
            classItem.setAlignment(alignType)
            classItem.setAcquisition(inputImages.getAcquisition())
            clsSet.append(classItem)
        else:
            classItem = clsDict[ref]
        img.setTransform(rowToAlignment(row, alignType))
        classItem.append(img)
    for classItem in clsDict.values():
        clsSet.update(classItem)
    clsSet.write()
    return clsSet

def createClassesFromImages(inputImages, inputMd, classesFn, ClassType, classLabel, classFnTemplate, alignType, iter, preprocessImageRow=None):
    """ From an intermediate X.xmd file produced by xmipp, create
    the set of classes in which those images are classified.
    Params:
        inputImages: the SetOfImages that were initially classified by relion.
        inputMd: the filename metadata.
        classesFn: filename where to write the classes.
        ClassType: the output type of the classes set
                   (usually SetOfClass2D or 3D)
        classLabel: label that is the class reference.
        classFnTemplate: the template to get the classes averages filenames
        iter: the iteration number, just used in Class template
    """
    if '@' in inputMd:
        inputFn = inputMd.split('@')[1]
        tmpDir = os.path.dirname(inputFn)
    else:
        tmpDir = os.path.dirname(inputMd)

    def getClassFn(ref):
        args = {'rootDir': tmpDir, 'iter': iter, 'ref': ref}
        return classFnTemplate % args
    createClassesFromImages2(inputImages, inputMd, classesFn, ClassType, classLabel, alignType, getClassFn=getClassFn, preprocessImageRow=preprocessImageRow)

def createItemMatrix(item, row, align):
    item.setTransform(rowToAlignment(row, alignType=align))

def readShiftsMovieAlignment(xmdFn):
    shiftsMd = md.MetaData(xmdFn)
    shiftsMd.removeDisabled()
    return (shiftsMd.getColumnValues(md.MDL_SHIFT_X), shiftsMd.getColumnValues(md.MDL_SHIFT_Y))

def writeShiftsMovieAlignment(movie, xmdFn, s0, sN):
    movieAlignment = movie.getAlignment()
    shiftListX, shiftListY = movieAlignment.getShifts()
    a0, aN = movieAlignment.getRange()
    globalShiftsMD = emlib.MetaData()
    alFrame = a0
    if s0 < a0:
        for i in range(s0, a0):
            objId = globalShiftsMD.addObject()
            imgFn = locationToXmipp(i, getMovieFileName(movie))
            globalShiftsMD.setValue(emlib.MDL_IMAGE, imgFn, objId)
            globalShiftsMD.setValue(emlib.MDL_SHIFT_X, 0.0, objId)
            globalShiftsMD.setValue(emlib.MDL_SHIFT_Y, 0.0, objId)
    for shiftX, shiftY in izip(shiftListX, shiftListY):
        if alFrame >= s0 and alFrame <= sN:
            objId = globalShiftsMD.addObject()
            imgFn = locationToXmipp(alFrame, getMovieFileName(movie))
            globalShiftsMD.setValue(emlib.MDL_IMAGE, imgFn, objId)
            globalShiftsMD.setValue(emlib.MDL_SHIFT_X, shiftX, objId)
            globalShiftsMD.setValue(emlib.MDL_SHIFT_Y, shiftY, objId)
        alFrame += 1
    if sN > aN:
        for j in range(aN, sN):
            objId = globalShiftsMD.addObject()
            imgFn = locationToXmipp(j + 1, getMovieFileName(movie))
            globalShiftsMD.setValue(emlib.MDL_IMAGE, imgFn, objId)
            globalShiftsMD.setValue(emlib.MDL_SHIFT_X, 0.0, objId)
            globalShiftsMD.setValue(emlib.MDL_SHIFT_Y, 0.0, objId)
    globalShiftsMD.write(xmdFn)

def writeMovieMd(movie, outXmd, f1, fN, useAlignment=False):
    movieMd = md.MetaData()
    frame = movie.clone()
    firstFrame, _, frameIndex = movie.getFramesRange()
    _, _, lastFrame = movie.getDim()
    lastFrame += 1
    if lastFrame == 0:
        frames = movie.getNumberOfFrames()
        if frames is not None:
            lastFrame = frames
    if f1 < firstFrame or fN > lastFrame:
        raise Exception('Frame range could not be greater than the movie one.')
    ih = ImageHandler()
    if useAlignment:
        alignment = movie.getAlignment()
        if alignment is None:
            raise Exception('Can not write alignment for movie. ')
        a0, aN = alignment.getRange()
        if a0 < firstFrame or aN > lastFrame:
            raise Exception('Trying to write frames which have not been aligned.')
        shiftListX, shiftListY = alignment.getShifts()
    row = md.Row()
    stackIndex = frameIndex + (f1 - firstFrame)
    for i in range(f1, fN + 1):
        frame.setIndex(stackIndex)
        row.setValue(md.MDL_IMAGE, ih.locationToXmipp(frame))
        if useAlignment:
            shiftIndex = i - firstFrame
            row.setValue(emlib.MDL_SHIFT_X, shiftListX[shiftIndex])
            row.setValue(emlib.MDL_SHIFT_Y, shiftListY[shiftIndex])
        row.addToMd(movieMd)
        stackIndex += 1
    movieMd.write(outXmd)

def createParamPhantomFile(filename, dimX, partSetMd, phFlip=False, ctfCorr=False):
    f = open(filename, 'w')
    str = "# XMIPP_STAR_1 *\n#\ndata_block1\n_dimensions2D '%d %d'\n" % (dimX, dimX)
    str += '_projAngleFile %s\n' % partSetMd
    str += '_ctfPhaseFlipped %d\n_ctfCorrected %d\n' % (phFlip, ctfCorr)
    str += "_applyShift 1\n_noisePixelLevel    '0 0'\n"
    f.write(str)
    f.close()

def convertToMrc(self, fnVol, Ts, deleteVol=False):
    fnMrc = fnVol.replace('.vol', '.mrc')
    self.runJob('xmipp_image_convert', '-i %s -o %s -t vol' % (fnVol, fnMrc), numberOfMpi=1)
    self.runJob('xmipp_image_header', '-i %s --sampling_rate %f' % (fnMrc, Ts), numberOfMpi=1)
    if deleteVol:
        cleanPath(fnVol)
    return fnMrc