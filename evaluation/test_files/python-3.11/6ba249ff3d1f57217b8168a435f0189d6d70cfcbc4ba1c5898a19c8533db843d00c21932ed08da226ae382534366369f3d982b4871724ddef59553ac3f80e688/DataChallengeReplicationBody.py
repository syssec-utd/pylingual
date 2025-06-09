from DIRAC.RequestManagementSystem.Client.Request import Request
from DIRAC.RequestManagementSystem.Client.Operation import Operation
from DIRAC.RequestManagementSystem.Client.File import File
from DIRAC.TransformationSystem.Client.BodyPlugin.BaseBody import BaseBody

class DataChallengeReplicationBody(BaseBody):
    """
    This body is to be used for the Data challenge, and will be
    changed regularly

    * The file is originally in CERN-DAQ-EXPORT
    * We replicate it to CERN-DC-RAW (waiting for the file to be archived)
    * We then replicate to the chosen Tier 1 disk (DataChallenge shares).
    * We replicate it from the Tier1-disk to the Tier1-Tape
    * Finally, we remove the replica on the Tier1-Disk
    """
    _attrToSerialize = []

    @staticmethod
    def _createOperation(operationType, lfns, targetSE, sourceSE=None):
        """
        Generate an Operation object of the given Type, with the
        specified targetSE and sourceSE. Associate to it File objects
        from the lfns list

        :param str operationType: Type of the operation (RemoveReplica, ReplicateAndRegister, etc)
        :param list lfns: list of LFNs on which to perform the operation
        :param str targetSE: SE name(s) targeted by the ops
        :param str sourceSE: SE name of the source
        """
        newOp = Operation()
        newOp.Type = operationType
        newOp.TargetSE = targetSE
        if sourceSE:
            newOp.SourceSE = sourceSE
        for lfn in lfns:
            opFile = File()
            opFile.LFN = lfn
            newOp.addFile(opFile)
        return newOp

    def taskToRequest(self, taskID, task, transID):
        """
        Create the request object from the task Dict


        """
        if isinstance(task['InputData'], list):
            lfns = task['InputData']
        elif isinstance(task['InputData'], str):
            lfns = task['InputData'].split(';')
        req = Request()
        repCernRAW = self._createOperation('ReplicateAndRegister', lfns, 'CERN-DC-RAW')
        req.addOperation(repCernRAW)
        targetSEs = task['TargetSE'].split(',')
        bufferSE, rawSE = sorted(targetSEs, key=lambda se: '-BUFFER' in se, reverse=True)
        repBuffer = self._createOperation('ReplicateAndRegister', lfns, bufferSE)
        req.addOperation(repBuffer)
        repTape = self._createOperation('ReplicateAndRegister', lfns, rawSE, sourceSE=bufferSE)
        req.addOperation(repTape)
        daqExportRemoval = self._createOperation('RemoveReplica', lfns, bufferSE)
        req.addOperation(daqExportRemoval)
        return req