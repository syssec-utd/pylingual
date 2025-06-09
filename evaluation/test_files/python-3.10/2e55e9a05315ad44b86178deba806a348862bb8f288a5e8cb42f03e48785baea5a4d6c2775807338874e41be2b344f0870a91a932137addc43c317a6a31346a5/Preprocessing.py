from typing import Callable, List
import numpy as np
from pyPhases.util.Logger import classLogger
from pyPhasesPreprocessing.Event import Event
from pyPhasesRecordloader import ChannelsNotPresent, ParseError, RecordSignal, Signal

@classLogger
class Preprocessing:
    stepDefinition: dict = {}
    instance: 'Preprocessing' = None

    def addPreprocessingStep(self, stepName: str, stepCallable: Callable[[Signal, RecordSignal, dict], None]):
        """Add a new preprocessing step to the preprocessing pipeline

        Args:
            stepName (str): name of the step to be used in the config
            stepCallable (Callable): Callable with the signature (signal: Signal, recordSignal: RecordSignal, channelConfig: dict)
        """
        Preprocessing.stepDefinition[stepName] = stepCallable

    @classmethod
    def setup(cls, config):
        instance = Preprocessing()
        preprocessingConfig = config['preprocessing']
        instance.targetChannels = preprocessingConfig['targetChannels']
        instance.stepsByType = preprocessingConfig['stepsPerType']
        instance.forceGapBetweenEvents = preprocessingConfig['forceGapBetweenEvents']
        instance.extendEvents = preprocessingConfig['extendEvents'] if 'extendEvents' in preprocessingConfig else None
        cls.instance = instance

    @classmethod
    def get(cls) -> 'Preprocessing':
        return cls.instance

    def parseSignalSteps(self, signal: Signal, stepName, psgSignal: RecordSignal, channelConfig={}):
        signal.processHistory.append(stepName)
        if stepName == 'resampleFIR':
            signal.resample(psgSignal.targetFrequency, antialiaseFIR=True)
        elif stepName == 'resampleFIRSimple':
            signal.resample(psgSignal.targetFrequency, simple=True, antialiaseFIR=True)
        elif stepName == 'resample':
            signal.resample(psgSignal.targetFrequency, antialiaseFIR=False)
        elif stepName == 'resampleSimple':
            signal.resample(psgSignal.targetFrequency, simple=True, antialiaseFIR=False)
        elif stepName == 'normalizePercentage':
            signal.simpleNormalize(0, 100)
        elif stepName == 'normalize':
            signal.simpleNormalize()
        elif stepName == 'tanh':
            signal.tanh()
        elif stepName == 'sigmoid':
            signal.sigmoid()
        elif stepName == 'normalize01':
            signal.simpleNormalize(0, 1, cut=False)
        elif stepName == 'normalize1':
            signal.simpleNormalize(-1, 1, cut=False)
        elif stepName == 'scale':
            signal.scale()
        elif stepName == 'fftConvolutionECG':
            kernel_size = 2 * signal.frequency + 1
            signal.fftConvolution(kernel_size)
        elif stepName == 'fftConvolutionECG6':
            kernel_size = 6 * signal.frequency + 1
            signal.fftConvolution(kernel_size)
        elif stepName == 'fftConvolution':
            kernel_size = 18 * 60 * signal.frequency + 1
            signal.fftConvolution(kernel_size)
        elif stepName == 'notchFilter':
            signal.notchFilter()
        elif stepName == 'fixedSize':
            fc = channelConfig['size']
            signal.fixedSize(fc)
        elif stepName == 'positionAlice':
            uniquePositions = set(np.unique(signal.signal))
            checkValues = set(uniquePositions) - set([0, 3, 6, 9, 12])
            if len(checkValues) > 0:
                raise Exception('alice position only supports 0, 3, 6, 9, 12 as values ... fix here :-)')
            signal.signal[signal.signal == 0] = 1
            signal.signal[signal.signal == 3] = 5
            signal.signal[signal.signal == 6] = 2
            signal.signal[signal.signal == 9] = 4
            signal.signal[signal.signal == 12] = 3
        elif stepName == 'positionDomino':
            uniquePositions = set(np.unique(signal.signal))
            checkValues = set(uniquePositions) - set([1, 2, 3, 4, 5, 6])
            if len(checkValues) > 0:
                raise Exception('domino position only supports 1, 2, 3, 4, 5, 6 as values ... fix here :-)')
            signal.signal[signal.signal == 1] = 4
            signal.signal[signal.signal == 2] = 1
            signal.signal[signal.signal == 3] = 3
            signal.signal[signal.signal == 4] = 5
            signal.signal[signal.signal == 5] = 1
            signal.signal[signal.signal == 6] = 2
        elif stepName == 'positionSHHS':
            uniquePositions = set(np.unique(signal.signal))
            checkValues = set(uniquePositions) - set([0, 1, 2, 3])
            if len(checkValues) > 0:
                signal.signal[np.isin(signal.signal, list(checkValues))] = 0
                self.logError('shhs position only supports 0, 1, 2, 3 as values, conflicts: %s \n... fix here :-)' % checkValues)
            signal.signal += 10
            signal.signal[signal.signal == 10] = 5
            signal.signal[signal.signal == 11] = 3
            signal.signal[signal.signal == 12] = 2
            signal.signal[signal.signal == 13] = 4
        elif stepName == 'positionMESA':
            uniquePositions = set(np.unique(signal.signal))
            checkValues = set(uniquePositions) - set([0, 1, 2, 3, 4])
            if len(checkValues) > 0:
                raise Exception('domino position only supports 0, 1, 2, 3, 4 as values ... fix here :-)')
            signal.signal += 10
            signal.signal[signal.signal == 10] = 5
            signal.signal[signal.signal == 11] = 2
            signal.signal[signal.signal == 12] = 3
            signal.signal[signal.signal == 13] = 4
            signal.signal[signal.signal == 14] = 1
        elif stepName == 'rr2hr':
            timeseries = TimeseriesSignal(signal)
            timeseries.rr2hr()
            signal.signal = timeseries.resampleAtFrequency(signal.signal.shape[0], signal.frequency)
        elif stepName in Preprocessing.stepDefinition:
            Preprocessing.stepDefinition[stepName](signal, psgSignal, channelConfig)
        else:
            raise Exception("The Preprocessing step '%s' is not yet supported" % stepName)

    def preprocessingSignal(self, psgSignal: RecordSignal):
        self.preprocessingSignal(psgSignal, self.stepsByType)

    def preprocessSignalByType(self, psgSignal: RecordSignal, stepsByType, targetFrequency):
        psgSignal.targetFrequency = targetFrequency
        for signal in psgSignal.signals:
            cName = signal.name
            if cName in psgSignal.signalNames:
                signal = psgSignal.getSignalByName(cName)
                type = signal.typeStr
                if type in stepsByType:
                    stepNames = stepsByType[type]
                    for processStep in stepNames:
                        self.parseSignalSteps(signal, processStep, psgSignal, signal)
                elif type is not None:
                    self.logError('Signaltype %s for signal %s has no preprocessing steps (defined in preprocessing.stepsPerType.[type])' % (signal.type, signal.name))
            elif cName not in self.optionalSignals and (not signal['generated']):
                self.logError('Missing channel %s for %s' % (cName, signal.recordId))
                raise ChannelsNotPresent(cName, signal.recordId)

    def preprocessEvents(self, events: List[Event]):
        if self.extendEvents is not None:
            events = self.preprocessEventsByConfig(events, self.extendEvents)
        return events

    def preprocessEventsByConfig(self, events: List[Event], extendEventsConfig):
        extendEventMap = extendEventsConfig
        for event in events:
            if event.name in extendEventMap:
                (addBefore, addAfter) = extendEventMap[event.name]
                event.start -= addBefore
                event.duration += addAfter + addAfter
        return events