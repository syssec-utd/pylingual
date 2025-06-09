from ....Internal.Core import Core
from ....Internal.CommandsGroup import CommandsGroup
from ....Internal.Types import DataType
from ....Internal.StructBase import StructBase
from ....Internal.ArgStruct import ArgStruct
from ....Internal.ArgSingleList import ArgSingleList
from ....Internal.ArgSingle import ArgSingle
from .... import repcap

class TfactorCls:
    """Tfactor commands group definition. 1 total commands, 0 Subgroups, 1 group commands"""

    def __init__(self, core: Core, parent):
        self._core = core
        self._cmd_group = CommandsGroup('tfactor', core, parent)

    def set(self, filename: str, transd_name: str, store=repcap.Store.Default) -> None:
        """SCPI: MMEMory:STORe<n>:TFACtor 

		Snippet: driver.massMemory.store.tfactor.set(filename = '1', transd_name = '1', store = repcap.Store.Default) 

		This command exports transducer factor data to an ASCII (CSV) file. For details on the file format see 'Reference:
		transducer factor file format'. 

			:param filename: Name of the transducer factor to be exported.
			:param transd_name: Name of the transducer factor to be exported.
			:param store: optional repeated capability selector. Default value: Pos1 (settable in the interface 'Store')
		"""
        param = ArgSingleList().compose_cmd_string(ArgSingle('filename', filename, DataType.String), ArgSingle('transd_name', transd_name, DataType.String))
        store_cmd_val = self._cmd_group.get_repcap_cmd_value(store, repcap.Store)
        self._core.io.write(f'MMEMory:STORe{store_cmd_val}:TFACtor {param}'.rstrip())

    class TfactorStruct(StructBase):
        """Response structure. Fields: 

			- Filename: str: Name of the transducer factor to be exported.
			- Transd_Name: str: Name of the transducer factor to be exported."""
        __meta_args_list = [ArgStruct.scalar_str('Filename'), ArgStruct.scalar_str('Transd_Name')]

        def __init__(self):
            StructBase.__init__(self, self)
            self.Filename: str = None
            self.Transd_Name: str = None

    def get(self, store=repcap.Store.Default) -> TfactorStruct:
        """SCPI: MMEMory:STORe<n>:TFACtor 

		Snippet: value: TfactorStruct = driver.massMemory.store.tfactor.get(store = repcap.Store.Default) 

		This command exports transducer factor data to an ASCII (CSV) file. For details on the file format see 'Reference:
		transducer factor file format'. 

			:param store: optional repeated capability selector. Default value: Pos1 (settable in the interface 'Store')
			:return: structure: for return value, see the help for TfactorStruct structure arguments."""
        store_cmd_val = self._cmd_group.get_repcap_cmd_value(store, repcap.Store)
        return self._core.io.query_struct(f'MMEMory:STORe{store_cmd_val}:TFACtor?', self.__class__.TfactorStruct())