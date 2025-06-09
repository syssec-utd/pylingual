"""
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
Utility functions writing revit geometry data to file.
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
"""
import Utility as util
import RevitCeilings as rCeil
import RevitRooms as rRoom
import Result as res

def ConvertDataToListJson(dataIn):
    """
    Converts lists of data classes into a single list of list of Json string representing the data class

    :param dataIn: list of data class instances
    :type dataIn: [data class]

    :return: list of list of Json string
    :rtype: [[str]]
    """
    dataJsonAll = []
    for dataList in dataIn:
        for d in dataList:
            dataRow = []
            dataRow.append(d.to_json())
            dataJsonAll.append(dataRow)
    return dataJsonAll

def WriteJsonDataToFile(doc, dataOutPutFileName):
    """
    Collects geometry data and writes it to a new json formatted file

    :param doc: Current Revit model document.
    :type doc: Autodesk.Revit.DB.Document
    :param dataOutPutFileName: Fully qualified file path to json data file.
    :type dataOutPutFileName: str

    :return: 
        Result class instance.
        
        - result.status. True if json data file was written successfully, otherwise False.
        - result.message will confirm path of json data file.
        - result.result empty list

        On exception:
        
        - result.status (bool) will be False.
        - result.message will contain exception message.
        - result.result will be empty

    :rtype: :class:`.Result`
    """
    result = res.Result()
    allRoomData = rRoom.GetAllRoomData(doc)
    allCeilingData = rCeil.GetAllCeilingData(doc)
    data = ConvertDataToListJson([allRoomData, allCeilingData])
    try:
        util.writeReportData(dataOutPutFileName, [], data)
        result.UpdateSep(True, 'Data written to file: ' + dataOutPutFileName)
    except Exception as e:
        result.UpdateSep(False, 'Failed to write data to file with exception: ' + str(e))
    return result