from __future__ import annotations
from tcsoa.gen.BusinessObjects import BusinessObject
from typing import Dict, List
from tcsoa.gen.Server import ServiceData
from tcsoa.base import TcBaseObj
from dataclasses import dataclass

@dataclass
class PrintSubmitRequestInfo(TcBaseObj):
    """
    The input values needed to submit the print request.
    
    :var clientId: A unique string supplied by the caller. This ID is used to identify return data elements and partial
    errors associated with this input structure.
    :var printObjs: A list of objects that will get printed.
    :var collate: When two or more copies are printed, this specifies whether the printed pages are collated.
    :var printToScale: Specifies the scaling factor.
    :var orientation: Specifies the paper orientation of best fit, portrait or landscape.
    :var bannerPage: Specifies whether to print a page including the defined stamps and listing additional data as
    specified by the VVCP setup.
    :var extraInfo: The placeholder for extra name value pair information.
    :var printerConfigurationName: The PrintConfiguration object name.
    :var printerName: The printer name.
    :var colorMode: The print color mode.
    :var userStamp: Specifies text for a user stamp to be applied in addition to any existing system stamp
    configuration.
    :var paperSize: The print paper size.
    :var printStamp: Specify whether the print stamp applies to the first page, the banner page, or all pages.
    :var pageRange: Specifies a range of pages to print.
    :var numberCopies: The number of copies.
    """
    clientId: str = ''
    printObjs: List[BusinessObject] = ()
    collate: bool = False
    printToScale: str = ''
    orientation: str = ''
    bannerPage: str = ''
    extraInfo: AttributeMap = None
    printerConfigurationName: str = ''
    printerName: str = ''
    colorMode: str = ''
    userStamp: str = ''
    paperSize: str = ''
    printStamp: str = ''
    pageRange: str = ''
    numberCopies: str = ''

@dataclass
class PrinterDefinitionOutput(TcBaseObj):
    """
    Printer definition output, this information will be used for the printSubmitRequest operation.
    
    :var printerConfigurationName: The PrintConfiguration object name.
    :var printerName: The printer name.
    :var paperSizes: List of paper sizes.
    :var supportStamp: Support stamp or not.
    :var printableDatasetTypeNames: The printable dataset type names.
    """
    printerConfigurationName: str = ''
    printerName: str = ''
    paperSizes: List[str] = ()
    supportStamp: bool = False
    printableDatasetTypeNames: List[str] = ()

@dataclass
class PrinterDefinitionResponse(TcBaseObj):
    """
    The return list of PrinterDefinitionOutput structures.
    
    :var outputs: List of PrinterDefinitionOutput.
    :var serviceData: Standard return; includes any error information.
    """
    outputs: List[PrinterDefinitionOutput] = ()
    serviceData: ServiceData = None

@dataclass
class RenderSubmitRequestInfo(TcBaseObj):
    """
    The input values needed to submit the render request.
    
    :var clientId: A unique string supplied by the caller. This ID is used to identify return data elements and partial
    errors associated with this input structure.
    :var renderObjs: A list of objects that will get rendered.
    :var preserve: If true preserve the previous rendered dataset, otherwise replace the rendered dataset.
    :var extraInfo: The placeholder for extra name value pair information.
    """
    clientId: str = ''
    renderObjs: List[BusinessObject] = ()
    preserve: bool = False
    extraInfo: AttributeMap = None

@dataclass
class SubmitRequestOutput(TcBaseObj):
    """
    The structure contains the created request object.
    
    :var clientId: The unmodified value from the PrintSubmitRequestInfo.clientId. This can be used by the caller to
    identify this data structure with the source input data.
    :var requestObject: The request object created.
    """
    clientId: str = ''
    requestObject: BusinessObject = None

@dataclass
class SubmitRequestResponse(TcBaseObj):
    """
    The structure contains a list of SubmitRequestOutput.
    
    :var outputs: List of SubmitPrintRequestOutput.
    :var serviceData: Standard return; includes any error information.
    """
    outputs: List[SubmitRequestOutput] = ()
    serviceData: ServiceData = None
'\nString to string map, it is extra information for the request\n'
AttributeMap = Dict[str, str]