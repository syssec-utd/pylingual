from SPMUtil import NdarrayEncoder, NdarrayDecoder, DataSerializer
import json
from enum import Enum
from datetime import datetime as dt

class cache_1d_scope(Enum):
    Output_FW_ZLine = 1
    Output_BW_ZLine = 2
    Output_FW_CurrentLine = 3
    Output_BW_CurrentLine = 4
    Custom_1DSlot1 = 5
    Custom_1DSlot2 = 6
    LineProfile = 7

class cache_2d_scope(Enum):
    FWFW_ZMap = 1
    FWBW_ZMap = 2
    BWFW_ZMap = 3
    BWBW_ZMap = 4
    FWFW_CurrentMap = 5
    FWBW_CurrentMap = 6
    BWFW_CurrentMap = 7
    BWBW_CurrentMap = 8
    FF_XArray = 9
    FF_YArray = 10
    FF_ZArray = 11
    FF_CurrentArray = 12
    FF_ReadFlagArray = 13
    Custom_2DSlot1 = 14
    Custom_2DSlot2 = 15

class JsonStringClass(object):

    def __str__(self):
        return self.to_json()

    def __init__(self):
        pass

    def to_json(self):
        return json.dumps(self.__dict__, cls=NdarrayEncoder)

    def from_json(self, json_str):
        dict = json.loads(json_str, cls=NdarrayDecoder)
        for key in dict.keys():
            if key in self.__dict__:
                self.__setattr__(key, dict[key])

    @staticmethod
    def GetKeyName() -> str:
        raise NotImplementedError

    @staticmethod
    def from_dataSerilizer(dataSerilizer: DataSerializer):
        raise NotImplementedError

class StageConfigure(JsonStringClass):

    def __init__(self):
        super().__init__()
        self.Sample_Bias = 2
        self.Tube_Scanner_Offset_X = 0
        self.Tube_Scanner_Offset_Y = 0
        self.High_Speed_Scanner_Offset_X = 0
        self.High_Speed_Scanner_Offset_Y = 0
        self.Scan_Speed = 1000
        self.XY_Scan_Option = 0
        self.Z_Scan_Option = 0
        self.setpoint = 0.01
        self.drift_x = 0.0
        self.drift_y = 0.0
        self.drift_z = 0.0
        self.z_sum_offset = 0.0
        self.sys_x_tilt = 0.0
        self.sys_y_tilt = 0.0

    @staticmethod
    def GetKeyName() -> str:
        return 'StageConfigure'

    @staticmethod
    def from_dataSerilizer(dataSerilizer: DataSerializer):
        data = StageConfigure()
        if type(dataSerilizer.data_dict[data.GetKeyName()]) == str:
            data.from_json(dataSerilizer.data_dict[data.GetKeyName()])
        else:
            data = dataSerilizer.data_dict[data.GetKeyName()]
        return data

class PythonScanParam(JsonStringClass):

    def __init__(self):
        super().__init__()
        self.Aux1Pingpong = True
        self.Aux2Pingpong = False
        self.ZRotation = 0.0
        self.Aux1MinVoltage = 0.0
        self.Aux1MaxVoltage = 0.0
        self.Aux2MinVoltage = 0.0
        self.Aux2MaxVoltage = 0.0
        self.Aux1ScanSize = 5
        self.Aux2ScanSize = 5
        self.Xtilt = 0.0
        self.Ytilt = 0.0
        self.Applytilt = False
        '\n        class AuxType(Enum):\n            X = 1\n            Y = 2\n            Z = 3\n            Current = 4\n        '
        self.Aux1Type = 'X'
        self.Aux2Type = 'Y'
        self.XOffset = 0.0
        self.YOffset = 0.0
        self.ZOffset = 0.0
        self.LinesNumPerFlag = 1
        self.ZFeedbackOn = True
        self.AQBoost = False

    @property
    def Aux1DeltaVoltage(self):
        return (self.Aux1MaxVoltage - self.Aux1MinVoltage) / self.Aux1ScanSize

    @property
    def Aux2DeltaVoltage(self):
        return (self.Aux2MaxVoltage - self.Aux2MinVoltage) / self.Aux2ScanSize

    @staticmethod
    def GetKeyName() -> str:
        return 'PythonScanParam'

    @staticmethod
    def from_dataSerilizer(dataSerilizer: DataSerializer):
        data = PythonScanParam()
        data.from_json(dataSerilizer.data_dict[data.GetKeyName()])
        return data

class ScanDataHeader(JsonStringClass):

    def __init__(self):
        super().__init__()
        self.Date = ''
        self.Time_Start_Scan = ''
        self.Time_End_Scan = ''
        self.Scan_Method = ''

    @property
    def Start_Scan_Sec(self) -> int:
        return self._time_string_to_sec(self.Time_Start_Scan)

    @property
    def End_Scan_Sec(self) -> int:
        return self._time_string_to_sec(self.Time_End_Scan)

    @property
    def Start_Scan_Timestamp(self) -> float:
        tdatetime = dt.strptime(self.Date + ' ' + self.Time_Start_Scan, '%Y-%m-%d %H:%M:%S')
        return tdatetime.timestamp()

    @property
    def End_Scan_Timestamp(self) -> float:
        tdatetime = dt.strptime(self.Date + ' ' + self.Time_End_Scan, '%Y-%m-%d %H:%M:%S')
        return tdatetime.timestamp()

    @staticmethod
    def GetKeyName() -> str:
        return 'data_main_header'

    @staticmethod
    def from_dataSerilizer(dataSerilizer: DataSerializer):
        data = ScanDataHeader()
        data.from_json(dataSerilizer.data_dict[data.GetKeyName()])
        return data

    def _time_string_to_sec(self, time_str: str):
        ftr = [3600, 60, 1]
        return sum([a * b for (a, b) in zip(ftr, map(int, time_str.split(':')))])