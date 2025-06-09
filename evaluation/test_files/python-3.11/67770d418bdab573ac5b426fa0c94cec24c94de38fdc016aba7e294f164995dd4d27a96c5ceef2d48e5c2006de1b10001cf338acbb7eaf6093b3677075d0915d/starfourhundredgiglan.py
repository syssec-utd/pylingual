import sys
from ixnetwork_restpy.base import Base
from ixnetwork_restpy.files import Files
if sys.version_info >= (3, 5):
    from typing import List, Any, Union

class StarFourHundredGigLan(Base):
    """
    The StarFourHundredGigLan class encapsulates a required starFourHundredGigLan resource which will be retrieved from the server every time the property is accessed.
    """
    __slots__ = ()
    _SDM_NAME = 'starFourHundredGigLan'
    _SDM_ATT_MAP = {'AutoInstrumentation': 'autoInstrumentation', 'AutonegotiationPreset': 'autonegotiationPreset', 'AvailableSpeeds': 'availableSpeeds', 'BadBlocksNumber': 'badBlocksNumber', 'CanModifySpeed': 'canModifySpeed', 'CanSetMultipleSpeeds': 'canSetMultipleSpeeds', 'EnableAutoNegotiation': 'enableAutoNegotiation', 'EnablePPM': 'enablePPM', 'EnableRsFec': 'enableRsFec', 'EnableRsFecStats': 'enableRsFecStats', 'EnabledFlowControl': 'enabledFlowControl', 'FirecodeAdvertise': 'firecodeAdvertise', 'FirecodeForceOff': 'firecodeForceOff', 'FirecodeForceOn': 'firecodeForceOn', 'FirecodeRequest': 'firecodeRequest', 'FlowControlDirectedAddress': 'flowControlDirectedAddress', 'ForceDisableFEC': 'forceDisableFEC', 'GoodBlocksNumber': 'goodBlocksNumber', 'IeeeL1Defaults': 'ieeeL1Defaults', 'LaserOn': 'laserOn', 'LinkTraining': 'linkTraining', 'LoopContinuously': 'loopContinuously', 'LoopCountNumber': 'loopCountNumber', 'Loopback': 'loopback', 'LoopbackMode': 'loopbackMode', 'Ppm': 'ppm', 'RsFecAdvertise': 'rsFecAdvertise', 'RsFecForceOn': 'rsFecForceOn', 'RsFecRequest': 'rsFecRequest', 'SelectedSpeeds': 'selectedSpeeds', 'SendSetsMode': 'sendSetsMode', 'Speed': 'speed', 'StartErrorInsertion': 'startErrorInsertion', 'TxIgnoreRxLinkFaults': 'txIgnoreRxLinkFaults', 'TypeAOrderedSets': 'typeAOrderedSets', 'TypeBOrderedSets': 'typeBOrderedSets', 'UseANResults': 'useANResults'}
    _SDM_ENUM_MAP = {'autoInstrumentation': ['endOfFrame', 'floating'], 'autonegotiationPreset': ['default', 'alternate1', 'alternate2', 'alternate3', 'alternate4'], 'loopbackMode': ['none', 'internalLoopback'], 'sendSetsMode': ['alternate', 'typeAOnly', 'typeBOnly'], 'speed': ['speed100g', 'speed10g', 'speed200g', 'speed25g', 'speed400g', 'speed40g', 'speed50g'], 'typeAOrderedSets': ['localFault', 'remoteFault'], 'typeBOrderedSets': ['localFault', 'remoteFault']}

    def __init__(self, parent, list_op=False):
        super(StarFourHundredGigLan, self).__init__(parent, list_op)

    @property
    def Fcoe(self):
        """
        Returns
        -------
        - obj(ixnetwork_restpy.testplatform.sessions.ixnetwork.vport.l1config.starfourhundredgiglan.fcoe.fcoe.Fcoe): An instance of the Fcoe class

        Raises
        ------
        - ServerError: The server has encountered an uncategorized error condition
        """
        from ixnetwork_restpy.testplatform.sessions.ixnetwork.vport.l1config.starfourhundredgiglan.fcoe.fcoe import Fcoe
        if len(self._object_properties) > 0:
            if self._properties.get('Fcoe', None) is not None:
                return self._properties.get('Fcoe')
        return Fcoe(self)._select()

    @property
    def AutoInstrumentation(self):
        """
        Returns
        -------
        - str(endOfFrame | floating): The auto instrumentation mode.
        """
        return self._get_attribute(self._SDM_ATT_MAP['AutoInstrumentation'])

    @AutoInstrumentation.setter
    def AutoInstrumentation(self, value):
        self._set_attribute(self._SDM_ATT_MAP['AutoInstrumentation'], value)

    @property
    def AutonegotiationPreset(self):
        """
        Returns
        -------
        - str(default | alternate1 | alternate2 | alternate3 | alternate4): Defines auto-negotiation preset options.
        """
        return self._get_attribute(self._SDM_ATT_MAP['AutonegotiationPreset'])

    @AutonegotiationPreset.setter
    def AutonegotiationPreset(self, value):
        self._set_attribute(self._SDM_ATT_MAP['AutonegotiationPreset'], value)

    @property
    def AvailableSpeeds(self):
        """
        Returns
        -------
        - list(str[speed100g | speed25g | speed50g | speed200g | speed400g | speed10g | speed40g]): Which speeds are available for the current media and AN settings.
        """
        return self._get_attribute(self._SDM_ATT_MAP['AvailableSpeeds'])

    @property
    def BadBlocksNumber(self):
        """
        Returns
        -------
        - number:
        """
        return self._get_attribute(self._SDM_ATT_MAP['BadBlocksNumber'])

    @BadBlocksNumber.setter
    def BadBlocksNumber(self, value):
        self._set_attribute(self._SDM_ATT_MAP['BadBlocksNumber'], value)

    @property
    def CanModifySpeed(self):
        """
        Returns
        -------
        - bool: Returns true/false depending upon if the port can change speed for the current media and AN settings.
        """
        return self._get_attribute(self._SDM_ATT_MAP['CanModifySpeed'])

    @property
    def CanSetMultipleSpeeds(self):
        """
        Returns
        -------
        - bool: Can this port selectmultiple speeds for the current media and AN settings.
        """
        return self._get_attribute(self._SDM_ATT_MAP['CanSetMultipleSpeeds'])

    @property
    def EnableAutoNegotiation(self):
        """
        Returns
        -------
        - bool:
        """
        return self._get_attribute(self._SDM_ATT_MAP['EnableAutoNegotiation'])

    @EnableAutoNegotiation.setter
    def EnableAutoNegotiation(self, value):
        self._set_attribute(self._SDM_ATT_MAP['EnableAutoNegotiation'], value)

    @property
    def EnablePPM(self):
        """
        Returns
        -------
        - bool: If true, enables the portsppm.
        """
        return self._get_attribute(self._SDM_ATT_MAP['EnablePPM'])

    @EnablePPM.setter
    def EnablePPM(self, value):
        self._set_attribute(self._SDM_ATT_MAP['EnablePPM'], value)

    @property
    def EnableRsFec(self):
        """
        Returns
        -------
        - bool:
        """
        return self._get_attribute(self._SDM_ATT_MAP['EnableRsFec'])

    @EnableRsFec.setter
    def EnableRsFec(self, value):
        self._set_attribute(self._SDM_ATT_MAP['EnableRsFec'], value)

    @property
    def EnableRsFecStats(self):
        """
        Returns
        -------
        - bool:
        """
        return self._get_attribute(self._SDM_ATT_MAP['EnableRsFecStats'])

    @EnableRsFecStats.setter
    def EnableRsFecStats(self, value):
        self._set_attribute(self._SDM_ATT_MAP['EnableRsFecStats'], value)

    @property
    def EnabledFlowControl(self):
        """
        Returns
        -------
        - bool: If true, enables the port's MAC flow control mechanisms to listen for a directed address pause message.
        """
        return self._get_attribute(self._SDM_ATT_MAP['EnabledFlowControl'])

    @EnabledFlowControl.setter
    def EnabledFlowControl(self, value):
        self._set_attribute(self._SDM_ATT_MAP['EnabledFlowControl'], value)

    @property
    def FirecodeAdvertise(self):
        """
        Returns
        -------
        - bool:
        """
        return self._get_attribute(self._SDM_ATT_MAP['FirecodeAdvertise'])

    @FirecodeAdvertise.setter
    def FirecodeAdvertise(self, value):
        self._set_attribute(self._SDM_ATT_MAP['FirecodeAdvertise'], value)

    @property
    def FirecodeForceOff(self):
        """DEPRECATED
        Returns
        -------
        - bool:
        """
        return self._get_attribute(self._SDM_ATT_MAP['FirecodeForceOff'])

    @FirecodeForceOff.setter
    def FirecodeForceOff(self, value):
        self._set_attribute(self._SDM_ATT_MAP['FirecodeForceOff'], value)

    @property
    def FirecodeForceOn(self):
        """
        Returns
        -------
        - bool:
        """
        return self._get_attribute(self._SDM_ATT_MAP['FirecodeForceOn'])

    @FirecodeForceOn.setter
    def FirecodeForceOn(self, value):
        self._set_attribute(self._SDM_ATT_MAP['FirecodeForceOn'], value)

    @property
    def FirecodeRequest(self):
        """
        Returns
        -------
        - bool:
        """
        return self._get_attribute(self._SDM_ATT_MAP['FirecodeRequest'])

    @FirecodeRequest.setter
    def FirecodeRequest(self, value):
        self._set_attribute(self._SDM_ATT_MAP['FirecodeRequest'], value)

    @property
    def FlowControlDirectedAddress(self):
        """
        Returns
        -------
        - str: The 48-bit MAC address that the port listens on for a directed pause.
        """
        return self._get_attribute(self._SDM_ATT_MAP['FlowControlDirectedAddress'])

    @FlowControlDirectedAddress.setter
    def FlowControlDirectedAddress(self, value):
        self._set_attribute(self._SDM_ATT_MAP['FlowControlDirectedAddress'], value)

    @property
    def ForceDisableFEC(self):
        """
        Returns
        -------
        - bool:
        """
        return self._get_attribute(self._SDM_ATT_MAP['ForceDisableFEC'])

    @ForceDisableFEC.setter
    def ForceDisableFEC(self, value):
        self._set_attribute(self._SDM_ATT_MAP['ForceDisableFEC'], value)

    @property
    def GoodBlocksNumber(self):
        """
        Returns
        -------
        - number:
        """
        return self._get_attribute(self._SDM_ATT_MAP['GoodBlocksNumber'])

    @GoodBlocksNumber.setter
    def GoodBlocksNumber(self, value):
        self._set_attribute(self._SDM_ATT_MAP['GoodBlocksNumber'], value)

    @property
    def IeeeL1Defaults(self):
        """
        Returns
        -------
        - bool:
        """
        return self._get_attribute(self._SDM_ATT_MAP['IeeeL1Defaults'])

    @IeeeL1Defaults.setter
    def IeeeL1Defaults(self, value):
        self._set_attribute(self._SDM_ATT_MAP['IeeeL1Defaults'], value)

    @property
    def LaserOn(self):
        """
        Returns
        -------
        - bool:
        """
        return self._get_attribute(self._SDM_ATT_MAP['LaserOn'])

    @LaserOn.setter
    def LaserOn(self, value):
        self._set_attribute(self._SDM_ATT_MAP['LaserOn'], value)

    @property
    def LinkTraining(self):
        """
        Returns
        -------
        - bool:
        """
        return self._get_attribute(self._SDM_ATT_MAP['LinkTraining'])

    @LinkTraining.setter
    def LinkTraining(self, value):
        self._set_attribute(self._SDM_ATT_MAP['LinkTraining'], value)

    @property
    def LoopContinuously(self):
        """
        Returns
        -------
        - bool:
        """
        return self._get_attribute(self._SDM_ATT_MAP['LoopContinuously'])

    @LoopContinuously.setter
    def LoopContinuously(self, value):
        self._set_attribute(self._SDM_ATT_MAP['LoopContinuously'], value)

    @property
    def LoopCountNumber(self):
        """
        Returns
        -------
        - number:
        """
        return self._get_attribute(self._SDM_ATT_MAP['LoopCountNumber'])

    @LoopCountNumber.setter
    def LoopCountNumber(self, value):
        self._set_attribute(self._SDM_ATT_MAP['LoopCountNumber'], value)

    @property
    def Loopback(self):
        """
        Returns
        -------
        - bool: If enabled, the port is set to internally loopback from transmit to receive.
        """
        return self._get_attribute(self._SDM_ATT_MAP['Loopback'])

    @Loopback.setter
    def Loopback(self, value):
        self._set_attribute(self._SDM_ATT_MAP['Loopback'], value)

    @property
    def LoopbackMode(self):
        """
        Returns
        -------
        - str(none | internalLoopback):
        """
        return self._get_attribute(self._SDM_ATT_MAP['LoopbackMode'])

    @LoopbackMode.setter
    def LoopbackMode(self, value):
        self._set_attribute(self._SDM_ATT_MAP['LoopbackMode'], value)

    @property
    def Ppm(self):
        """
        Returns
        -------
        - number: Indicates the value that needs to be adjusted for the line transmit frequency.
        """
        return self._get_attribute(self._SDM_ATT_MAP['Ppm'])

    @Ppm.setter
    def Ppm(self, value):
        self._set_attribute(self._SDM_ATT_MAP['Ppm'], value)

    @property
    def RsFecAdvertise(self):
        """
        Returns
        -------
        - bool:
        """
        return self._get_attribute(self._SDM_ATT_MAP['RsFecAdvertise'])

    @RsFecAdvertise.setter
    def RsFecAdvertise(self, value):
        self._set_attribute(self._SDM_ATT_MAP['RsFecAdvertise'], value)

    @property
    def RsFecForceOn(self):
        """
        Returns
        -------
        - bool:
        """
        return self._get_attribute(self._SDM_ATT_MAP['RsFecForceOn'])

    @RsFecForceOn.setter
    def RsFecForceOn(self, value):
        self._set_attribute(self._SDM_ATT_MAP['RsFecForceOn'], value)

    @property
    def RsFecRequest(self):
        """
        Returns
        -------
        - bool:
        """
        return self._get_attribute(self._SDM_ATT_MAP['RsFecRequest'])

    @RsFecRequest.setter
    def RsFecRequest(self, value):
        self._set_attribute(self._SDM_ATT_MAP['RsFecRequest'], value)

    @property
    def SelectedSpeeds(self):
        """
        Returns
        -------
        - list(str[speed100g | speed25g | speed50g | speed200g | speed400g | speed10g | speed40g]): Which speeds are selected for the current media and AN settings.
        """
        return self._get_attribute(self._SDM_ATT_MAP['SelectedSpeeds'])

    @SelectedSpeeds.setter
    def SelectedSpeeds(self, value):
        self._set_attribute(self._SDM_ATT_MAP['SelectedSpeeds'], value)

    @property
    def SendSetsMode(self):
        """
        Returns
        -------
        - str(alternate | typeAOnly | typeBOnly):
        """
        return self._get_attribute(self._SDM_ATT_MAP['SendSetsMode'])

    @SendSetsMode.setter
    def SendSetsMode(self, value):
        self._set_attribute(self._SDM_ATT_MAP['SendSetsMode'], value)

    @property
    def Speed(self):
        """
        Returns
        -------
        - str(speed100g | speed10g | speed200g | speed25g | speed400g | speed40g | speed50g):
        """
        return self._get_attribute(self._SDM_ATT_MAP['Speed'])

    @Speed.setter
    def Speed(self, value):
        self._set_attribute(self._SDM_ATT_MAP['Speed'], value)

    @property
    def StartErrorInsertion(self):
        """
        Returns
        -------
        - bool:
        """
        return self._get_attribute(self._SDM_ATT_MAP['StartErrorInsertion'])

    @StartErrorInsertion.setter
    def StartErrorInsertion(self, value):
        self._set_attribute(self._SDM_ATT_MAP['StartErrorInsertion'], value)

    @property
    def TxIgnoreRxLinkFaults(self):
        """
        Returns
        -------
        - bool: If enabled, will allow transmission of packets even if the receive link is down.
        """
        return self._get_attribute(self._SDM_ATT_MAP['TxIgnoreRxLinkFaults'])

    @TxIgnoreRxLinkFaults.setter
    def TxIgnoreRxLinkFaults(self, value):
        self._set_attribute(self._SDM_ATT_MAP['TxIgnoreRxLinkFaults'], value)

    @property
    def TypeAOrderedSets(self):
        """
        Returns
        -------
        - str(localFault | remoteFault):
        """
        return self._get_attribute(self._SDM_ATT_MAP['TypeAOrderedSets'])

    @TypeAOrderedSets.setter
    def TypeAOrderedSets(self, value):
        self._set_attribute(self._SDM_ATT_MAP['TypeAOrderedSets'], value)

    @property
    def TypeBOrderedSets(self):
        """
        Returns
        -------
        - str(localFault | remoteFault):
        """
        return self._get_attribute(self._SDM_ATT_MAP['TypeBOrderedSets'])

    @TypeBOrderedSets.setter
    def TypeBOrderedSets(self, value):
        self._set_attribute(self._SDM_ATT_MAP['TypeBOrderedSets'], value)

    @property
    def UseANResults(self):
        """
        Returns
        -------
        - bool:
        """
        return self._get_attribute(self._SDM_ATT_MAP['UseANResults'])

    @UseANResults.setter
    def UseANResults(self, value):
        self._set_attribute(self._SDM_ATT_MAP['UseANResults'], value)

    def update(self, AutoInstrumentation=None, AutonegotiationPreset=None, BadBlocksNumber=None, EnableAutoNegotiation=None, EnablePPM=None, EnableRsFec=None, EnableRsFecStats=None, EnabledFlowControl=None, FirecodeAdvertise=None, FirecodeForceOff=None, FirecodeForceOn=None, FirecodeRequest=None, FlowControlDirectedAddress=None, ForceDisableFEC=None, GoodBlocksNumber=None, IeeeL1Defaults=None, LaserOn=None, LinkTraining=None, LoopContinuously=None, LoopCountNumber=None, Loopback=None, LoopbackMode=None, Ppm=None, RsFecAdvertise=None, RsFecForceOn=None, RsFecRequest=None, SelectedSpeeds=None, SendSetsMode=None, Speed=None, StartErrorInsertion=None, TxIgnoreRxLinkFaults=None, TypeAOrderedSets=None, TypeBOrderedSets=None, UseANResults=None):
        """Updates starFourHundredGigLan resource on the server.

        Args
        ----
        - AutoInstrumentation (str(endOfFrame | floating)): The auto instrumentation mode.
        - AutonegotiationPreset (str(default | alternate1 | alternate2 | alternate3 | alternate4)): Defines auto-negotiation preset options.
        - BadBlocksNumber (number):
        - EnableAutoNegotiation (bool):
        - EnablePPM (bool): If true, enables the portsppm.
        - EnableRsFec (bool):
        - EnableRsFecStats (bool):
        - EnabledFlowControl (bool): If true, enables the port's MAC flow control mechanisms to listen for a directed address pause message.
        - FirecodeAdvertise (bool):
        - FirecodeForceOff (bool):
        - FirecodeForceOn (bool):
        - FirecodeRequest (bool):
        - FlowControlDirectedAddress (str): The 48-bit MAC address that the port listens on for a directed pause.
        - ForceDisableFEC (bool):
        - GoodBlocksNumber (number):
        - IeeeL1Defaults (bool):
        - LaserOn (bool):
        - LinkTraining (bool):
        - LoopContinuously (bool):
        - LoopCountNumber (number):
        - Loopback (bool): If enabled, the port is set to internally loopback from transmit to receive.
        - LoopbackMode (str(none | internalLoopback)):
        - Ppm (number): Indicates the value that needs to be adjusted for the line transmit frequency.
        - RsFecAdvertise (bool):
        - RsFecForceOn (bool):
        - RsFecRequest (bool):
        - SelectedSpeeds (list(str[speed100g | speed25g | speed50g | speed200g | speed400g | speed10g | speed40g])): Which speeds are selected for the current media and AN settings.
        - SendSetsMode (str(alternate | typeAOnly | typeBOnly)):
        - Speed (str(speed100g | speed10g | speed200g | speed25g | speed400g | speed40g | speed50g)):
        - StartErrorInsertion (bool):
        - TxIgnoreRxLinkFaults (bool): If enabled, will allow transmission of packets even if the receive link is down.
        - TypeAOrderedSets (str(localFault | remoteFault)):
        - TypeBOrderedSets (str(localFault | remoteFault)):
        - UseANResults (bool):

        Raises
        ------
        - ServerError: The server has encountered an uncategorized error condition
        """
        return self._update(self._map_locals(self._SDM_ATT_MAP, locals()))

    def find(self, AutoInstrumentation=None, AutonegotiationPreset=None, AvailableSpeeds=None, BadBlocksNumber=None, CanModifySpeed=None, CanSetMultipleSpeeds=None, EnableAutoNegotiation=None, EnablePPM=None, EnableRsFec=None, EnableRsFecStats=None, EnabledFlowControl=None, FirecodeAdvertise=None, FirecodeForceOff=None, FirecodeForceOn=None, FirecodeRequest=None, FlowControlDirectedAddress=None, ForceDisableFEC=None, GoodBlocksNumber=None, IeeeL1Defaults=None, LaserOn=None, LinkTraining=None, LoopContinuously=None, LoopCountNumber=None, Loopback=None, LoopbackMode=None, Ppm=None, RsFecAdvertise=None, RsFecForceOn=None, RsFecRequest=None, SelectedSpeeds=None, SendSetsMode=None, Speed=None, StartErrorInsertion=None, TxIgnoreRxLinkFaults=None, TypeAOrderedSets=None, TypeBOrderedSets=None, UseANResults=None):
        """Finds and retrieves starFourHundredGigLan resources from the server.

        All named parameters are evaluated on the server using regex. The named parameters can be used to selectively retrieve starFourHundredGigLan resources from the server.
        To retrieve an exact match ensure the parameter value starts with ^ and ends with $
        By default the find method takes no parameters and will retrieve all starFourHundredGigLan resources from the server.

        Args
        ----
        - AutoInstrumentation (str(endOfFrame | floating)): The auto instrumentation mode.
        - AutonegotiationPreset (str(default | alternate1 | alternate2 | alternate3 | alternate4)): Defines auto-negotiation preset options.
        - AvailableSpeeds (list(str[speed100g | speed25g | speed50g | speed200g | speed400g | speed10g | speed40g])): Which speeds are available for the current media and AN settings.
        - BadBlocksNumber (number):
        - CanModifySpeed (bool): Returns true/false depending upon if the port can change speed for the current media and AN settings.
        - CanSetMultipleSpeeds (bool): Can this port selectmultiple speeds for the current media and AN settings.
        - EnableAutoNegotiation (bool):
        - EnablePPM (bool): If true, enables the portsppm.
        - EnableRsFec (bool):
        - EnableRsFecStats (bool):
        - EnabledFlowControl (bool): If true, enables the port's MAC flow control mechanisms to listen for a directed address pause message.
        - FirecodeAdvertise (bool):
        - FirecodeForceOff (bool):
        - FirecodeForceOn (bool):
        - FirecodeRequest (bool):
        - FlowControlDirectedAddress (str): The 48-bit MAC address that the port listens on for a directed pause.
        - ForceDisableFEC (bool):
        - GoodBlocksNumber (number):
        - IeeeL1Defaults (bool):
        - LaserOn (bool):
        - LinkTraining (bool):
        - LoopContinuously (bool):
        - LoopCountNumber (number):
        - Loopback (bool): If enabled, the port is set to internally loopback from transmit to receive.
        - LoopbackMode (str(none | internalLoopback)):
        - Ppm (number): Indicates the value that needs to be adjusted for the line transmit frequency.
        - RsFecAdvertise (bool):
        - RsFecForceOn (bool):
        - RsFecRequest (bool):
        - SelectedSpeeds (list(str[speed100g | speed25g | speed50g | speed200g | speed400g | speed10g | speed40g])): Which speeds are selected for the current media and AN settings.
        - SendSetsMode (str(alternate | typeAOnly | typeBOnly)):
        - Speed (str(speed100g | speed10g | speed200g | speed25g | speed400g | speed40g | speed50g)):
        - StartErrorInsertion (bool):
        - TxIgnoreRxLinkFaults (bool): If enabled, will allow transmission of packets even if the receive link is down.
        - TypeAOrderedSets (str(localFault | remoteFault)):
        - TypeBOrderedSets (str(localFault | remoteFault)):
        - UseANResults (bool):

        Returns
        -------
        - self: This instance with matching starFourHundredGigLan resources retrieved from the server available through an iterator or index

        Raises
        ------
        - ServerError: The server has encountered an uncategorized error condition
        """
        return self._select(self._map_locals(self._SDM_ATT_MAP, locals()))

    def read(self, href):
        """Retrieves a single instance of starFourHundredGigLan data from the server.

        Args
        ----
        - href (str): An href to the instance to be retrieved

        Returns
        -------
        - self: This instance with the starFourHundredGigLan resources from the server available through an iterator or index

        Raises
        ------
        - NotFoundError: The requested resource does not exist on the server
        - ServerError: The server has encountered an uncategorized error condition
        """
        return self._read(href)