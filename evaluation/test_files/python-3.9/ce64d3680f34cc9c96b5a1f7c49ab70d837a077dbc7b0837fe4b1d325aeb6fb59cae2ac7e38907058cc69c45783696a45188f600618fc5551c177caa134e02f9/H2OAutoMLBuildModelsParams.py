from pyspark.ml.param import *
from ai.h2o.sparkling.ml.params.H2OTypeConverters import H2OTypeConverters

class H2OAutoMLBuildModelsParams(Params):
    excludeAlgos = Param(Params._dummy(), 'excludeAlgos', 'A list of algorithms to skip during the model-building phase.', H2OTypeConverters.toNullableListEnumString('ai.h2o.automl.Algo'))
    includeAlgos = Param(Params._dummy(), 'includeAlgos', 'A list of algorithms to restrict to during the model-building phase.', H2OTypeConverters.toListEnumString('ai.h2o.automl.Algo'))
    exploitationRatio = Param(Params._dummy(), 'exploitationRatio', 'The budget ratio (between 0 and 1) dedicated to the exploitation (vs exploration) phase.', H2OTypeConverters.toFloat())

    def getExcludeAlgos(self):
        return self.getOrDefault(self.excludeAlgos)

    def getIncludeAlgos(self):
        return self.getOrDefault(self.includeAlgos)

    def getExploitationRatio(self):
        return self.getOrDefault(self.exploitationRatio)

    def setExcludeAlgos(self, value):
        return self._set(excludeAlgos=value)

    def setIncludeAlgos(self, value):
        return self._set(includeAlgos=value)

    def setExploitationRatio(self, value):
        return self._set(exploitationRatio=value)