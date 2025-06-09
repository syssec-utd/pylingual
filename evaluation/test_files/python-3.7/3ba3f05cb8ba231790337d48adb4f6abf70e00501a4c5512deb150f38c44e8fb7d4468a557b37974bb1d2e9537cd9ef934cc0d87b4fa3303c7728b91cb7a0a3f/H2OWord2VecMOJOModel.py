from ai.h2o.sparkling.ml.models.H2OWord2VecMOJOBase import H2OWord2VecMOJOBase
from pyspark.ml.util import _jvm
from py4j.java_gateway import JavaObject
from ai.h2o.sparkling.Initializer import Initializer
from ai.h2o.sparkling.ml.models.H2OMOJOSettings import H2OMOJOSettings
from ai.h2o.sparkling.ml.params.H2OTypeConverters import H2OTypeConverters

class H2OWord2VecMOJOModel(H2OWord2VecMOJOBase):

    @staticmethod
    def createFromMojo(pathToMojo, settings=H2OMOJOSettings.default()):
        Initializer.load_sparkling_jar()
        javaModel = _jvm().ai.h2o.sparkling.ml.models.H2OWord2VecMOJOModel.createFromMojo(pathToMojo, settings.toJavaObject())
        return H2OWord2VecMOJOModel(javaModel)

    def getCrossValidationModels(self):
        cvModels = self._java_obj.getCrossValidationModelsAsArray()
        if cvModels is None:
            return None
        elif isinstance(cvModels, JavaObject):
            return [H2OWord2VecMOJOModel(v) for v in cvModels]
        else:
            raise TypeError('Invalid type.')

    def getVecSize(self):
        value = self._java_obj.getVecSize()
        return value

    def getWindowSize(self):
        value = self._java_obj.getWindowSize()
        return value

    def getSentSampleRate(self):
        value = self._java_obj.getSentSampleRate()
        return value

    def getNormModel(self):
        value = self._java_obj.getNormModel()
        return value

    def getEpochs(self):
        value = self._java_obj.getEpochs()
        return value

    def getMinWordFreq(self):
        value = self._java_obj.getMinWordFreq()
        return value

    def getInitLearningRate(self):
        value = self._java_obj.getInitLearningRate()
        return value

    def getWordModel(self):
        value = self._java_obj.getWordModel()
        return value

    def getMaxRuntimeSecs(self):
        value = self._java_obj.getMaxRuntimeSecs()
        return value

    def getExportCheckpointsDir(self):
        value = self._java_obj.getExportCheckpointsDir()
        return value