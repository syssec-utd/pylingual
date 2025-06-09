from pyspark.ml.param import *
from ai.h2o.sparkling.ml.params.H2OTypeConverters import H2OTypeConverters
from ai.h2o.sparkling.ml.metrics.H2OCommonMetrics import H2OCommonMetrics

class H2OGLRMMetrics(H2OCommonMetrics):

    def __init__(self, java_obj):
        self._java_obj = java_obj

    def getNumErr(self):
        """
        Sum of Squared Error (Numeric Cols).
        """
        value = self._java_obj.getNumErr()
        return value

    def getCatErr(self):
        """
        Misclassification Error (Categorical Cols).
        """
        value = self._java_obj.getCatErr()
        return value

    def getNumCnt(self):
        """
        Number of Non-Missing Numeric Values.
        """
        value = self._java_obj.getNumCnt()
        return value

    def getCatCnt(self):
        """
        Number of Non-Missing Categorical Values.
        """
        value = self._java_obj.getCatCnt()
        return value