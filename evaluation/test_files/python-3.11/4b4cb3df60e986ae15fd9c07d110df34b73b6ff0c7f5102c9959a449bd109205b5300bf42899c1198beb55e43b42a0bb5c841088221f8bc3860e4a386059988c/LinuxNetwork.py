import logging
import time
from typing import Dict
from typing import List
from typing import Optional
from typing import Union
from jumonc import settings
from jumonc.helpers import convertNumbers
from jumonc.helpers import dicthelper
from jumonc.tasks import Plugin
from jumonc.tasks.mpi_helper import multi_node_information
from jumonc.tasks.taskSwitcher import task_switcher
logger = logging.getLogger(__name__)

class _LinuxNetworkPlugin(Plugin.Plugin):

    def __init__(self) -> None:
        super().__init__()
        self.__initial_interfaces = self._GetNetworkInfo()
        self.net_mpi_id = task_switcher.addFunction(self._getData)

    def _isWorking(self) -> bool:
        testInterfaces = _getDataDiff(newData=self._GetNetworkInfo(), oldData=self.__initial_interfaces)
        if len(testInterfaces) == 0:
            return False
        return True

    def GetNetworkInfo(self) -> List[Dict[str, Union[str, Dict[str, Union[int, float, str]]]]]:
        return _getDataDiff(newData=self._GetNetworkInfo(), oldData=self.__initial_interfaces)

    def _GetNetworkInfo(self) -> List[Dict[str, Union[str, Dict[str, Union[int, float, str]]]]]:
        interfaces: List[Dict[str, Union[str, Dict[str, Union[int, float, str]]]]] = []
        try:
            with open('/proc/net/dev', encoding='utf8') as file:
                data = file.read()
        except FileNotFoundError:
            logger.warning('Could not find the file: "/proc/net/dev"', exc_info=True)
            return []
        except PermissionError:
            logger.warning('Missing permissions for the file: "/proc/net/dev"', exc_info=True)
            return []
        lines = data.split('\n')[2:]
        for line in lines:
            if len(line.strip()) > 0:
                elements = line.split()
                interface: Dict[str, Union[str, Dict[str, Union[int, float, str]]]] = {'interface': elements[0][:len(elements[0]) - 1], 'received': {'Bytes': int(elements[1]), 'Packets': int(elements[2]), 'Errs': int(elements[3]), 'Drop': int(elements[4]), 'Fifo': int(elements[5]), 'Frame': int(elements[6]), 'Compressed': int(elements[7]), 'Multicast': int(elements[8])}, 'transmitted': {'Bytes': int(elements[9]), 'Packets': int(elements[10]), 'Errs': int(elements[11]), 'Drop': int(elements[12]), 'Fifo': int(elements[13]), 'Frame': int(elements[14]), 'Compressed': int(elements[15]), 'Multicast': int(elements[16])}}
                interfaces.append(interface)
        return interfaces

    def getAvaiableInterfaces(self) -> List[str]:
        if not hasattr(self, '_interfaces'):
            self._interfaces: List[str] = []
            netInfos = self._GetNetworkInfo()
            if netInfos is None:
                return self._interfaces
            for netInfo in netInfos:
                self._interfaces.append(str(netInfo['interface']))
            self._interfaces.append(str('total'))
        return self._interfaces

    def getAvaiableDataTypes(self) -> List[str]:
        return ['Bytes', 'Packets', 'Errs', 'Drop', 'Fifo', 'Frame', 'Compressed', 'Multicast']

    def getAvaiableDataTypesDescriptions(self) -> List[str]:
        return ['the bytes send and recieved', 'the number of packets send and recieved', 'the number of errors that occured', 'the number of dropped packets', 'fifo', 'frame', 'compressed', 'multicast']

    @multi_node_information()
    def _getData(self, dataType: str, duration: float, interface: str, overrideHumanReadableWithValue: Optional[bool]=None) -> List[Dict[str, Union[str, Dict[str, Union[int, float, str]]]]]:
        data: List[Dict[str, Union[str, Dict[str, Union[int, float, str]]]]] = self.GetNetworkInfo()
        data = _reduceInterfaces(data, interface)
        data = _reduceDataTypes(data, dataType)
        if duration >= 0.0:
            time.sleep(duration)
            newData = self.getData(dataType=dataType, duration=-1.0, interface=interface, overrideHumanReadableWithValue=False)
            oldData = data
            data = _getDataDiff(newData=newData, oldData=oldData)
            data = _divideData(data, duration, '/s')
        if overrideHumanReadableWithValue or (overrideHumanReadableWithValue is None and settings.DEFAULT_TO_HUMAN_READABLE_NUMBERS):
            data = _makeDataHumanReadable(data)
        return data

    def getData(self, dataType: str, duration: float, interface: str, overrideHumanReadableWithValue: Optional[bool]=None) -> List[Dict[str, Union[str, Dict[str, Union[int, float, str, List[int], List[float], List[str]]]]]]:
        data = self._getData(dataType=dataType, duration=duration, interface=interface, overrideHumanReadableWithValue=overrideHumanReadableWithValue, id=self.net_mpi_id)
        if isinstance(data, list) and isinstance(data[0], list):
            return _reorder_multinode(data)
        return data
plugin = _LinuxNetworkPlugin()

def _reorder_multinode(dataIn: List[List[Dict[str, Union[str, Dict[str, Union[int, float, str]]]]]]) -> List[Dict[str, Union[str, Dict[str, Union[List[int], List[float], List[str]]]]]]:
    data: List[Dict[str, Union[str, Dict[str, Union[List[int], List[float], List[str]]]]]] = []
    for i in range(len(dataIn[0])):
        interfaceData = dataIn[0][i]
        if not isinstance(interfaceData, Dict):
            logger.error('Unexpected interface data type: %s', type(interfaceData))
            interfaceData = {'interface': 'internalError'}
        divData: Dict[str, Union[str, Dict[str, Union[List[int], List[float], List[str]]]]] = {'interface': interfaceData['interface']}
        rec: Dict[str, Union[List[int], List[float], List[str]]] = {}
        trans: Dict[str, Union[List[int], List[float], List[str]]] = {}
        recData = interfaceData['received']
        transData = interfaceData['transmitted']
        if isinstance(recData, dict):
            dictkeys = recData.keys()
        for dataType in dictkeys:
            if isinstance(recData, dict):
                value = recData[dataType]
                if isinstance(value, (int, float)):
                    rec[dataType] = [dataIn[j][i]['received'][dataType] for j in range(len(dataIn))]
                else:
                    logger.warning('Unexpected data type in LinuxNetwork._reorder_multinode')
            else:
                logging.warning('Unexpected data type in LinuxNetwork._reorder_multinode')
            if isinstance(transData, dict):
                value = transData[dataType]
                if isinstance(value, (int, float)):
                    trans[dataType] = [dataIn[j][i]['transmitted'][dataType] for j in range(len(dataIn))]
                else:
                    logger.warning('Unexpected data type in LinuxNetwork._reorder_multinode')
            else:
                logger.warning('Unexpected data type in LinuxNetwork._reorder_multinode')
        divData['received'] = rec
        divData['transmitted'] = trans
        data.append(divData)
    return data

def _reduceInterfaces(data: List[Dict[str, Union[str, Dict[str, Union[int, float, str]]]]], interface: str) -> List[Dict[str, Union[str, Dict[str, Union[int, float, str]]]]]:
    if interface == 'all':
        return data
    if interface == 'total':
        total = data[0]
        del data[0]
        total['interface'] = 'total'
        for interfaceData in data:
            total['received'] = dicthelper.mergeDictionaryAndAdd(total['received'], interfaceData['received'])
            total['transmitted'] = dicthelper.mergeDictionaryAndAdd(total['transmitted'], interfaceData['transmitted'])
        return [total]
    if interface in plugin.getAvaiableInterfaces():
        dataAllInterfaces = data
        data = []
        for interfaceData in dataAllInterfaces:
            if interfaceData['interface'] == interface:
                data.append(interfaceData)
    return data

def _reduceDataTypes(data: List[Dict[str, Union[str, Dict[str, Union[int, float, str]]]]], dataType: str) -> List[Dict[str, Union[str, Dict[str, Union[int, float, str]]]]]:
    if dataType == 'all':
        return data
    if dataType in plugin.getAvaiableDataTypes():
        dataAllDataTypes = data
        data = []
        for interfaceData in dataAllDataTypes:
            strippedData: Dict[str, Union[str, Dict[str, Union[int, float, str]]]] = {'interface': interfaceData['interface']}
            recData = interfaceData['received']
            if isinstance(recData, dict):
                strippedData['received'] = {dataType: recData[dataType]}
            else:
                logger.warning('Unexpected data type in LinuxNetwork._reduceDataTypes')
            transData = interfaceData['transmitted']
            if isinstance(transData, dict):
                strippedData['transmitted'] = {dataType: transData[dataType]}
            else:
                logger.warning('Unexpected data type in LinuxNetwork._reduceDataTypes')
            data.append(strippedData)
    return data

def _getDataDiff(newData: List[Dict[str, Union[str, Dict[str, Union[int, float, str]]]]], oldData: List[Dict[str, Union[str, Dict[str, Union[int, float, str]]]]]) -> List[Dict[str, Union[str, Dict[str, Union[int, float, str]]]]]:
    data: List[Dict[str, Union[str, Dict[str, Union[int, float, str]]]]] = []
    for i, interfaceDataOld in enumerate(oldData):
        interfaceDataNew = newData[i]
        difData: Dict[str, Union[str, Dict[str, Union[int, float, str]]]] = {'interface': interfaceDataNew['interface']}
        rec: Dict[str, Union[int, float, str]] = {}
        trans: Dict[str, Union[int, float, str]] = {}
        recData = interfaceDataOld['received']
        if isinstance(recData, dict):
            dictkeys = recData.keys()
        for dataType in dictkeys:
            old = interfaceDataOld['received']
            new = interfaceDataNew['received']
            if isinstance(new, dict) and isinstance(old, dict):
                newValue = new[dataType]
                oldValue = old[dataType]
                if isinstance(newValue, (int, float)) and isinstance(oldValue, (int, float)):
                    rec[dataType] = newValue - oldValue
                else:
                    logger.warning('Unexpected data type in LinuxNetwork._getDataDiff')
            else:
                logger.warning('Unexpected data type in LinuxNetwork._getDataDiff')
            old = interfaceDataOld['transmitted']
            new = interfaceDataNew['transmitted']
            if isinstance(new, dict) and isinstance(old, dict):
                newValue = new[dataType]
                oldValue = old[dataType]
                if isinstance(newValue, (int, float)) and isinstance(oldValue, (int, float)):
                    trans[dataType] = newValue - oldValue
                else:
                    logger.warning('Unexpected data type in LinuxNetwork._getDataDiff')
            else:
                logger.warning('Unexpected data type in LinuxNetwork._getDataDiff')
        difData['received'] = rec
        difData['transmitted'] = trans
        data.append(difData)
    return data

def _divideData(dataIn: List[Dict[str, Union[str, Dict[str, Union[int, float, str]]]]], divisor: float, typeNamePostfix: str) -> List[Dict[str, Union[str, Dict[str, Union[int, float, str]]]]]:
    data: List[Dict[str, Union[str, Dict[str, Union[int, float, str]]]]] = []
    for interfaceData in dataIn:
        divData: Dict[str, Union[str, Dict[str, Union[int, float, str]]]] = {'interface': interfaceData['interface']}
        rec: Dict[str, Union[int, float, str]] = {}
        trans: Dict[str, Union[int, float, str]] = {}
        recData = interfaceData['received']
        transData = interfaceData['transmitted']
        if isinstance(recData, dict):
            dictkeys = recData.keys()
        for dataType in dictkeys:
            if isinstance(recData, dict):
                dataValue = recData[dataType]
                if isinstance(dataValue, (int, float)):
                    rec[dataType + typeNamePostfix] = dataValue / divisor
                else:
                    logger.warning('Unexpected data type in LinuxNetwork._divideData')
            else:
                logging.warning('Unexpected data type in LinuxNetwork._divideData')
            if isinstance(transData, dict):
                dataValue = transData[dataType]
                if isinstance(dataValue, (int, float)):
                    trans[dataType + typeNamePostfix] = dataValue / divisor
                else:
                    logger.warning('Unexpected data type in LinuxNetwork._divideData')
            else:
                logger.warning('Unexpected data type in LinuxNetwork._divideData')
        divData['received'] = rec
        divData['transmitted'] = trans
        data.append(divData)
    return data

def _makeDataHumanReadable(dataIn: List[Dict[str, Union[str, Dict[str, Union[int, float, str]]]]]) -> List[Dict[str, Union[str, Dict[str, Union[int, float, str]]]]]:
    data: List[Dict[str, Union[str, Dict[str, Union[int, float, str]]]]] = []
    for interfaceData in dataIn:
        divData: Dict[str, Union[str, Dict[str, Union[int, float, str]]]] = {'interface': interfaceData['interface']}
        rec: Dict[str, Union[int, float, str]] = {}
        trans: Dict[str, Union[int, float, str]] = {}
        recData = interfaceData['received']
        transData = interfaceData['transmitted']
        if isinstance(recData, dict):
            dictkeys = recData.keys()
        for dataType in dictkeys:
            if isinstance(recData, dict):
                dataValue = recData[dataType]
                if isinstance(dataValue, (int, float)):
                    value, unitPrefix = convertNumbers.convertBinaryPrefix(dataValue)
                    rec[unitPrefix + dataType] = value
                else:
                    logger.warning('Unexpected data type in LinuxNetwork._makeDataHumanReadable')
            else:
                logging.warning('Unexpected data type in LinuxNetwork._makeDataHumanReadable')
            if isinstance(transData, dict):
                dataValue = transData[dataType]
                if isinstance(dataValue, (int, float)):
                    value, unitPrefix = convertNumbers.convertBinaryPrefix(dataValue)
                    trans[unitPrefix + dataType] = value
                else:
                    logger.warning('Unexpected data type in LinuxNetwork._makeDataHumanReadable')
            else:
                logger.warning('Unexpected data type in LinuxNetwork._makeDataHumanReadable')
        divData['received'] = rec
        divData['transmitted'] = trans
        data.append(divData)
    return data