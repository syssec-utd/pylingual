import copy
import os
import re
from .sqlparse import SQLFormatWithPrefix
from .apiparse import APIRequestObjectFormatWithPrefix
from .commands.assertExpression import evalExpression
from .testcliexception import TestCliException

def sortresult(result):
    """
        数组排序

        不能用sorted函数，需要考虑None出现在列表中特定元素的问题
        排序遵循空值最大原则
    """
    for i in range(len(result) - 1, 0, -1):
        for j in range(i - 1, -1, -1):
            bNeedExchange = False
            for k in range(0, len(result[i])):
                if len(result[i]) != len(result[j]):
                    return
                if result[i][k] is None and result[j][k] is None:
                    continue
                if result[i][k] is None and result[j][k] is not None:
                    break
                if result[j][k] is None and result[i][k] is not None:
                    bNeedExchange = True
                    break
                if not isinstance(result[i][k], type(result[j][k])):
                    if str(result[i][k]) < str(result[j][k]):
                        bNeedExchange = True
                        break
                    if str(result[i][k]) > str(result[j][k]):
                        break
                else:
                    if result[i][k] < result[j][k]:
                        bNeedExchange = True
                        break
                    if result[i][k] > result[j][k]:
                        break
            if bNeedExchange:
                (result[j], result[i]) = (result[i], result[j])

def rewriteStatement(cls, statement: str, commandScriptFile: str):
    while True:
        match_obj = re.search('{{(.*?)}}', statement, re.IGNORECASE | re.DOTALL)
        if match_obj:
            beforeRewriteStatement = statement
            searchResult = str(match_obj.group(0))
            varName = str(match_obj.group(1)).strip()
            mappingResult = cls.cmdMappingHandler.RewriteWord(commandScriptFile, varName)
            if varName != mappingResult:
                statement = statement.replace(searchResult, str(mappingResult))
            try:
                evalResult = evalExpression(cls, varName)
                if varName != evalResult:
                    statement = statement.replace(searchResult, str(evalResult))
            except NameError:
                pass
            except Exception as ex:
                if 'TESTCLI_DEBUG' in os.environ:
                    raise TestCliException('evalExpression Error [' + varName + ']: [' + repr(ex) + '].')
            if varName in os.environ:
                statement = statement.replace(searchResult, os.environ[varName])
            if statement == beforeRewriteStatement:
                break
        else:
            break
    return statement

def rewriteHintStatement(cls, statement: str, commandScriptFile: str):
    rewrotedCommandHistory = []
    rawStatement = statement
    statement = rewriteStatement(cls=cls, statement=statement, commandScriptFile=commandScriptFile)
    if rawStatement != statement:
        rewrotedCommandHistory.append(statement)
    return (statement, rewrotedCommandHistory)

def rewriteSQLStatement(cls, statement: str, commandScriptFile: str):
    rewrotedCommandHistory = []
    rawStatement = statement
    statement = rewriteStatement(cls=cls, statement=statement, commandScriptFile=commandScriptFile)
    if rawStatement != statement:
        rewrotedCommandHistory.append(SQLFormatWithPrefix('Your SQL has been changed to:\n' + statement, 'REWROTED '))
    return (statement, rewrotedCommandHistory)

def rewriteConnectRequest(cls, connectRequestObject, commandScriptFile: str):
    rewrotedRequestObjects = []
    rawConnectRequestObject = copy.copy(connectRequestObject)
    for keyword in ['username', 'password', 'driver', 'driverSchema', 'driverType', 'host', 'port', 'service']:
        if keyword in connectRequestObject:
            oldType = type(connectRequestObject[keyword])
            newValue = rewriteStatement(cls=cls, statement=str(connectRequestObject[keyword]), commandScriptFile=commandScriptFile)
            newValue = oldType(newValue)
            connectRequestObject[keyword] = newValue
    if rawConnectRequestObject != connectRequestObject:
        statement = '_CONNECT '
        if 'username' in connectRequestObject:
            statement = statement + connectRequestObject['username']
        if 'password' in connectRequestObject:
            statement = statement + '/' + str(connectRequestObject['password'])
        if 'driver' in connectRequestObject:
            statement = statement + '@' + str(connectRequestObject['driver'])
        if 'driverSchema' in connectRequestObject:
            statement = statement + ':' + str(connectRequestObject['driverSchema'])
        if 'driverType' in connectRequestObject:
            statement = statement + ':' + str(connectRequestObject['driverType'])
        if 'host' in connectRequestObject:
            statement = statement + '//' + str(connectRequestObject['host'])
        if 'port' in connectRequestObject:
            statement = statement + ':' + str(connectRequestObject['port'])
        if 'service' in connectRequestObject:
            statement = statement + '/' + str(connectRequestObject['service'])
        rewrotedRequestObjects.append(SQLFormatWithPrefix('Your CONNECT has been changed to :\n' + statement, "REWROTED '"))
    return (connectRequestObject, rewrotedRequestObjects)

def rewriteAPIStatement(cls, requestObject: [], commandScriptFile: str):
    rewrotedRequestObjects = []
    rawRequestObject = copy.copy(requestObject)
    httpRequestTarget = rewriteStatement(cls=cls, statement=rawRequestObject['httpRequestTarget'], commandScriptFile=commandScriptFile)
    if 'contents' in rawRequestObject:
        httpRequestContents = copy.copy(rawRequestObject['contents'])
        for nPos in range(0, len(httpRequestContents)):
            newHttpRequestContent = rewriteStatement(cls=cls, statement=httpRequestContents[nPos], commandScriptFile=commandScriptFile)
            if newHttpRequestContent == httpRequestContents[nPos]:
                break
            else:
                httpRequestContents[nPos] = newHttpRequestContent
    else:
        httpRequestContents = None
    if 'httpFields' in rawRequestObject:
        httpRequestFields = copy.copy(rawRequestObject['httpFields'])
        for (key, value) in httpRequestFields.items():
            originFieldName = key
            key = rewriteStatement(cls=cls, statement=originFieldName, commandScriptFile=commandScriptFile)
            if originFieldName != key:
                del httpRequestFields[originFieldName]
            value = rewriteStatement(cls=cls, statement=value, commandScriptFile=commandScriptFile)
            httpRequestFields[key] = value
    else:
        httpRequestFields = None
    if 'operate' in rawRequestObject:
        operateList = []
        for operate in rawRequestObject['operate']:
            content = operate['content']
            content = rewriteStatement(cls=cls, statement=content, commandScriptFile=commandScriptFile)
            operateList.append({'operator': operate['operator'], 'content': content})
        requestObject['operate'] = operateList
    else:
        requestObject['operate'] = None
    requestObject['httpRequestTarget'] = httpRequestTarget
    if httpRequestContents is not None:
        requestObject['contents'] = httpRequestContents
    if httpRequestFields is not None:
        requestObject['httpFields'] = httpRequestFields
    if rawRequestObject != requestObject:
        rewrotedRequestObjects.append(APIRequestObjectFormatWithPrefix(headerPrefix='Your API has been changed to:\n', requestObject=requestObject, outputPrefix='REWROTED '))
    return (requestObject, rewrotedRequestObjects)

def parseSQLHints(commandHints: list):
    commandHintList = {}
    for commandHint in commandHints:
        match_obj = re.match('^Scenario:(.*)', commandHint, re.IGNORECASE | re.DOTALL)
        if match_obj:
            senario = match_obj.group(1).strip()
            if len(senario.split(':')) == 2:
                scenarioSplitList = senario.split(':')
                commandHintList['ScenarioId'] = scenarioSplitList[0].strip()
                commandHintList['ScenarioName'] = scenarioSplitList[1].strip()
                continue
            else:
                commandHintList['ScenarioId'] = 'N/A'
                commandHintList['ScenarioName'] = senario
                continue
        match_obj = re.search('^order', commandHint, re.IGNORECASE | re.DOTALL)
        if match_obj:
            commandHintList['Order'] = True
            continue
        match_obj = re.search('^LogFilter(\\s+)(.*)', commandHint, re.IGNORECASE | re.DOTALL)
        if match_obj:
            sqlFilter = match_obj.group(2).strip()
            if 'LogFilter' in commandHintList:
                commandHintList['LogFilter'].append(sqlFilter)
            else:
                commandHintList['LogFilter'] = [sqlFilter]
            continue
        match_obj = re.search('^LogMask(\\s+)(.*)', commandHint, re.IGNORECASE | re.DOTALL)
        if match_obj:
            sqlMask = match_obj.group(2).strip()
            if 'LogMask' in commandHintList:
                commandHintList['LogMask'].append(sqlMask)
            else:
                commandHintList['LogMask'] = [sqlMask]
            continue
        match_obj = re.search('^SQL_DIRECT', commandHint, re.IGNORECASE | re.DOTALL)
        if match_obj:
            commandHintList['SQL_DIRECT'] = True
            continue
        match_obj = re.search('^SQL_PREPARE', commandHint, re.IGNORECASE | re.DOTALL)
        if match_obj:
            commandHintList['SQL_PREPARE'] = True
            continue
    return commandHintList

def parseAPIHints(commandHints: list):
    commandHintList = {}
    for commandHint in commandHints:
        match_obj = re.match('^Scenario:(.*)', commandHint, re.IGNORECASE | re.DOTALL)
        if match_obj:
            senario = match_obj.group(1).strip()
            if len(senario.split(':')) == 2:
                scenarioSplitList = senario.split(':')
                commandHintList['ScenarioId'] = scenarioSplitList[0].strip()
                commandHintList['ScenarioName'] = scenarioSplitList[1].strip()
                continue
            else:
                commandHintList['ScenarioId'] = 'N/A'
                commandHintList['ScenarioName'] = senario
                continue
        match_obj = re.search('^LogFilter(\\s+)(.*)', commandHint, re.IGNORECASE | re.DOTALL)
        if match_obj:
            sqlFilter = match_obj.group(2).strip()
            if 'LogFilter' in commandHintList:
                commandHintList['LogFilter'].append(sqlFilter)
            else:
                commandHintList['LogFilter'] = [sqlFilter]
            continue
        match_obj = re.search('^LogMask(\\s+)(.*)', commandHint, re.IGNORECASE | re.DOTALL)
        if match_obj:
            sqlMask = match_obj.group(2).strip()
            if 'LogMask' in commandHintList:
                commandHintList['LogMask'].append(sqlMask)
            else:
                commandHintList['LogMask'] = [sqlMask]
            continue
        match_obj = re.search('^JsonFilter(\\s+)(.*)', commandHint, re.IGNORECASE | re.DOTALL)
        if match_obj:
            sqlMask = match_obj.group(2).strip()
            if 'JsonFilter' in commandHintList:
                commandHintList['JsonFilter'].append(sqlMask)
            else:
                commandHintList['JsonFilter'] = [sqlMask]
            continue
    return commandHintList