from vortex.handler.TupleActionProcessor import TupleActionProcessor
from peek_core_device._private.PluginNames import deviceActionProcessorName
from peek_core_device._private.PluginNames import deviceFilt
from .controller.MainController import MainController

def makeTupleActionProcessorHandler(mainController: MainController):
    processor = TupleActionProcessor(tupleActionProcessorName=deviceActionProcessorName, additionalFilt=deviceFilt, defaultDelegate=mainController)
    return processor