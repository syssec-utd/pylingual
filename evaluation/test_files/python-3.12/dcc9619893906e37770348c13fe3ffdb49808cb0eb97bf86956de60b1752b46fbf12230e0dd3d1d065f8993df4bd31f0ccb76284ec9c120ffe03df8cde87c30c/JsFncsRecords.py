"""
This module get all the functions related to the transformation of the recordset on the Javascript part.
Each of those functions are in charge of transforming a recordSet in the front end (which means that this cannot be
seen on the Python side in the scripting interface). The best way to test those changes is to use a report and set
the DEBUG flag.
"""
from abc import ABC, abstractmethod

class JsRecFunc(ABC):
    """
  This class cannot be used directly to format a record as the mandatory parameters are not defined and are set to None.

  Anyway as an interface this will give you the different information which have to be defined to create a new
  js function.

  The objective in this logic is to centralise all the js functions used in the front end in this folder in order
  to limit the use and standardise the implementation.

  ## The main parameters ##

  - alias, The alias name used in the Python layer to point to this function
  - params, The parameters name available in the Javascript function (data is always passed)
  - value, The content of the function.

  ## Javascript function ##

  A javascript function, represented as a class in the framework, is always trying to transform a data variable
  which is defined as a recordSet to a result variable which should be also a recordSet. The purpose of having this
  will ensure that functions can:

    1. Transform the recordSet in a specific manner
    2. Be shared in the different components
    3. Be put together sum(count(...))

  """
    alias = None
    params = None
    value = None

    @staticmethod
    def extendArgs(category, originParams, newCols):
        """

    :param category:
    :param originParams:
    :param newCols:
    """
        return originParams

    @staticmethod
    @abstractmethod
    def extendColumns(jsSchema, params):
        """

    :param jsSchema:
    :param params:
    """
        pass

class JsRowBuckets(JsRecFunc):

    @staticmethod
    def extendArgs(category, originParams, newCols):
        """

    :param category:
    :param originParams:
    :param newCols:
    """
        originParams[1] += newCols
        return originParams

    @staticmethod
    def extendColumns(jsSchema, params):
        """

    :param jsSchema:
    :param params:
    """
    alias = 'row-buckets'
    params = ('allGroups', 'seriesNames')
    value = "\n    var groupRowsIds = {}; var groupRows = {};\n    data.forEach(function(rec, i){\n      var inBuckets = {}; for(var g in allGroups){inBuckets[g] = null};\n      for(var g in allGroups){\n        for(var col in allGroups[g]){if(allGroups[g][col].indexOf(rec[col]) >= 0){\n          inBuckets[g] = true} else {inBuckets[g] = false; break}}}\n      for(var g in inBuckets){\n        if (inBuckets[g]) { \n            if (g in groupRowsIds) {groupRowsIds[g].push(i);groupRows[g].push(rec)} \n            else {groupRowsIds[g] = [i]; groupRows[g] = [rec]}}\n      }; result.push(rec)});\n      \n    for(var g in groupRows){\n      var row = {'_system': true}; var text = g;\n      for(var col in allGroups[g]){row[col] = text; text=''}; seriesNames.forEach(function(v){row[v] = 0}); \n      groupRows[g].forEach(function(rec){ seriesNames.forEach(function(v){row[v] += rec[v]})});\n      result.push(row)}"

class JsRowTotal(JsRecFunc):

    @staticmethod
    def extendArgs(category, originParams, newCols):
        """

    :param category:
    :param originParams:
    :param newCols:
    """
        originParams[0] += newCols
        return originParams

    @staticmethod
    def extendColumns(jsSchema, params):
        """

    :param jsSchema:
    :param params:
    """
    alias = 'row-total'
    params = ('seriesNames', 'rowDefinition')
    value = "\n    seriesNames.forEach(function(v){rowDefinition[v] = 0});\n    data.forEach(function(rec){\n      if(!rec['_system']){seriesNames.forEach(function(v){rowDefinition[v] += rec[v]})};\n      result.push(rec);\n    }); result.push(rowDefinition);\n    "

class JsAll(JsRecFunc):

    @staticmethod
    def extendColumns(jsSchema, params):
        """

    :param jsSchema:
    :param params:
    """
        if params[0] is not None and params[1] is not None:
            jsSchema['keys'] |= set(params[0])
            jsSchema['values'] |= set(params[1])
    alias = 'all'
    params = ('keys', 'values')
    value = 'result = data'

class JsSum(JsRecFunc):

    @staticmethod
    def extendColumns(jsSchema, params):
        """

    :param jsSchema:
    :param params:
    """
        if params[0] is not None and params[1] is not None:
            jsSchema['keys'] |= set(params[0])
            jsSchema['values'] |= set(params[1])
    alias = 'sum'
    params = ('keys', 'values', 'xOrder')
    value = '\n    if ((keys == null) || (values == null)){result = data}\n    else{\n      var temp = {}; var order = []; \n      if (Array.isArray(data)){\n        data.forEach( function(rec){ \n          var aggKey = []; keys.forEach(function(k){ aggKey.push(rec[k])}); \n          var newKey = aggKey.join("#"); if (!(newKey in temp)) {order.push(newKey)};\n          if (!(newKey in temp)) {temp[newKey] = {}};\n          values.forEach(function(v) {if (!(v in temp[newKey])) {temp[newKey][v] = rec[v]} else {temp[newKey][v] += rec[v]}})})}; \n      if(Array.isArray(xOrder)){order = xOrder};\n      order.forEach(function(label) {\n        var rec = {}; var splitKey = label.split("#");\n        keys.forEach(function(k, i) {rec[k] = splitKey[i];});\n        for(var v in temp[label]) {rec[v] = temp[label][v]};\n        result.push(rec)})}'

class JsPercentage(JsRecFunc):

    @staticmethod
    def extendColumns(jsSchema, params):
        """

    :param jsSchema:
    :param params:
    """
        if params[0] is not None and params[1] is not None:
            jsSchema['keys'] |= set(params[0])
            jsSchema['values'] |= set(params[1])
    alias = 'percentage'
    params = ('keys', 'values')
    value = ' \n    if ((keys == null) || (values == null)){result = data}\n    else{\n      var temp = {}; var order = []; var sumPerSeries = {};\n      data.forEach( function(rec) { \n        var aggKey = []; keys.forEach(function(k){ aggKey.push(rec[k])}); \n        var newKey = aggKey.join("#"); if (!(newKey in temp)) {order.push(newKey)};\n        if (!(newKey in temp)) {temp[newKey] = {}};\n        values.forEach(function(v) {\n          if (!(v in sumPerSeries)) {sumPerSeries[v] = rec[v]} else {sumPerSeries[v] += rec[v]};\n          if (!(v in temp[newKey])) {temp[newKey][v] = rec[v]} \n          else {temp[newKey][v] += rec[v]}})});\n      order.forEach(function(label) {\n        var rec = {}; var splitKey = label.split("#");\n        keys.forEach(function(k, i) {rec[k] = splitKey[i]});\n        for(var v in temp[label]) {rec[v] = 100 * (temp[label][v] / sumPerSeries[v])};\n        result.push(rec)})}'

class JsOperations(JsRecFunc):
    """
  This function will aggregate the different values for each series according to a shcema defined in a Python
  dictionary in the last position of the tuple.

  Usage::

    aggFnc=('aggregation', ['direction'], values, {'dn': 'sum', 'Date': 'count'}),
  """

    @staticmethod
    def extendArgs(category, originParams, newCols):
        """
    This function will update the function argument according to the mode defined by the user. Indeed some properties
    can be received to validate the accuracy of the data.
    Those data should be added to the different transformation functions and the columns should be passed to the final
    object.
    This function will ensure that by activating the mode the columns will be automatically added to the aggregated data.

    :return: The update set of columns to be considered in the Javascript function
    """
        if category == 'age':
            originParams[1] = originParams[1] + newCols
            for c in newCols:
                originParams[2][c] = 'sum'
        return originParams

    @staticmethod
    def extendColumns(jsSchema, params):
        """

    :param jsSchema:
    :param params:
    """
        if params[0] is not None and params[1] is not None:
            jsSchema['keys'] |= set(params[0])
            jsSchema['values'] |= set(params[1])
    alias = 'aggregation'
    params = ('keys', 'values', 'operations')
    value = '\n    var temp = {};\n    var order = [];\n    data.forEach( function(rec) { \n      var aggKey = []; keys.forEach(function(k){ aggKey.push( rec[k])}); var newKey = aggKey.join("#"); order.push(newKey);\n      if (!(newKey in temp)) {temp[newKey] = {}};\n      values.forEach(function(v) {\n        if (operations[v] === undefined){ if (!(v in temp[newKey])) {temp[newKey][v] = 1} else {temp[newKey][v] += 1} }\n        else if (operations[v] == \'sum\') {if (!(v in temp[newKey])) {temp[newKey][v] = rec[v]} else {temp[newKey][v] += rec[v]}}\n        else if (operations[v] == \'count\') {if (!(v in temp[newKey])) {temp[newKey][v] = 1} else {temp[newKey][v] += 1}}\n      })}); \n    order.forEach(function(label) {\n      var rec = {}; var splitKey = label.split("#");\n      keys.forEach(function(k, i) {rec[k] = splitKey[i];});\n      for(var v in temp[label]) {rec[v] = temp[label][v]};\n      result.push(rec)})'

class JsCount(JsRecFunc):
    params = ('keys', 'values')
    value = '\n    var temp = {}; var order = [];\n    data.forEach(function(rec){ \n      var aggKey = []; keys.forEach(function(k){aggKey.push(rec[k])}); var newKey = aggKey.join("#"); \n      if(!(newKey in temp)){order.push(newKey); temp[newKey] = {}};\n      values.forEach(function(v){if (!(v in temp[newKey])){\n        temp[newKey][v] = rec[v]; temp[newKey][v +"_count"] = 1} else{temp[newKey][v +"_count"] += 1}})}); \n    order.forEach(function(label){\n      var rec = {}; var splitKey = label.split("#");\n      keys.forEach(function(k, i){rec[k] = splitKey[i]});\n      for(var v in temp[label]){rec[v] = temp[label][v]};\n      result.push(rec)})'

class JsCountSum(JsRecFunc):
    params = ('keys', 'values')
    value = '\n    var temp = {}; var order = [];\n    data.forEach(function(rec){ \n      var aggKey = []; keys.forEach(function(k){aggKey.push(rec[k])}); var newKey = aggKey.join("#"); \n      if(!(newKey in temp)){order.push(newKey); temp[newKey] = {}};\n      values.forEach(function(v){\n        if (!(v in temp[newKey])){\n          temp[newKey][v] = rec[v]; temp[newKey][v +"_count"] = 1; temp[newKey][v +"_min"] = rec[v]; \n          temp[newKey][v +"_max"] = rec[v]} \n        else{\n          if(rec[v] > temp[newKey][v +"_max"]){temp[newKey][v +"_max"] = rec[v]};\n          if(rec[v] < temp[newKey][v +"_min"]){temp[newKey][v +"_min"] = rec[v]};\n          temp[newKey][v] += rec[v];temp[newKey][v +"_count"] += 1}})}); \n    order.forEach(function(label){\n      var rec = {}; var splitKey = label.split("#");\n      keys.forEach(function(k, i){rec[k] = splitKey[i]});\n      for(var v in temp[label]){rec[v] = temp[label][v]};\n      result.push(rec)})'

class JsTop:

    @staticmethod
    def extendColumns(jsSchema, params):
        pass
    alias = 'top'
    params = ('countItems', 'value', 'sortType')
    value = "\n    var tmpRec = {};\n    data.forEach(function(rec){\n      if(tmpRec[rec[value]] === undefined){ tmpRec[rec[value]] = [rec] } else {tmpRec[rec[value]].push(rec)}});\n    \n    var result = []; \n    Object.keys(tmpRec).sort().forEach(function(key){\n      tmpRec[key].forEach(function(rec){result.push(rec)})});\n    \n    if (sortType == 'desc'){ result = result.slice(-countItems)}\n    else {result = result.slice(0, countItems)}\n    "

class JsCountDistinct:
    """
  Return the distinct counts of element in a list of columns. This function will return a list of dictionaries
  with the following structure {'column': '', 'count_distinct': 0}

  :return: A new recordSet with the properties of the requested keys
  """
    params = ('keys',)
    value = "\n    var temp = {}; keys.forEach(function(k){temp[k] = {}});\n    data.forEach(function(rec){keys.forEach(function(k){temp[k][rec[k]] = 1})}); \n    for(var col in temp){\n      var dCount = Object.keys(temp[col]).length; \n      result.push({'column': col, 'count': dCount, 'distinct': true, 'values': Object.keys(temp[col])})}"

class JsCountAll:
    """
  Function to produce KPI on an original recordSet. This function will create a new recordSet based on the selected
  columns of the original data source.

  :return: A new recordSet with the properties of the requested keys
  """
    params = ('keys',)
    value = '\n    var temp = {}; var order= [];\n    data.forEach(function(rec){ \n      keys.forEach(function(k){\n        var aggKey = k +"#"+ rec[k]; if(!(aggKey in temp)){order.push(aggKey); temp[aggKey] = 1} else{temp[aggKey] += 1}})}); \n    order.forEach(function(label){\n      var keys = label.split("#"); var rec = {\'column\': keys[0], \'value\': keys[1], \'count\': temp[label], \'distinct\': false};\n      result.push(rec)})'

class JsRename:
    """
  Function to remap some columns in the recordSet. The renaming is done based on the input parameter.
  The parameter passed in this function is a dictionary with as keys the existing column names and value the new column.

  :return: The Js recordSet with the new columns in each record. The original keys will be removed
  """
    alias = 'rename'
    params = ('colsWithName',)
    value = '\n    data.forEach(function(rec){ \n      for(var col in colsWithName){rec[colsWithName[col]] = rec[col]; delete rec[col]; result.push(rec)}})'

class JsExtend:
    """
  Function to add some predefined entries to each records in the RecordSet
  The parameter passed in the function call should be a dictionary with as keys the columns to be added to the original record
  and the value {'static': {}, 'dynamic': {}}
  In case of key clashes the values will be replaced.

  :return: A new Js recordSet with the extra columns
  """
    alias = 'extend'
    params = ('values', 'recKey')
    value = '\n    if (Array.isArray(data)){\n      if(recKey == undefined){\n        data.forEach(function(rec, i){ \n          var newRec = Object.assign(rec, values.static);\n          if (i in values.dynamic) {newRec = Object.assign(newRec, values.dynamic[i])};\n          result.push(newRec)})}\n      else{\n        data.forEach(function(rec, i){ \n          var newRec = Object.assign(rec, values.static);\n          if (i in values.dynamic) {newRec = Object.assign(newRec, values.dynamic[i])};\n          result.push(newRec);\n          var subValues = rec[recKey]; result[recKey] = [];\n          subValues.forEach(function(row, j){ \n            var newRec = Object.assign(row, values.static);\n            if (i in values.dynamic) {newRec = Object.assign(newRec, values.dynamic[i])};\n            result[recKey].push(newRec)})  \n        })\n      }} \n    else {result = data}\n  '

class JsExtendDataSet:
    """
  :return: A new Js recordSet with the extra columns in the datasets section
  """
    alias = 'extend-dataset'
    params = ('values', 'recKey')
    value = '\n    var records; var recResults; \n    if(recKey == undefined){records = data; recResults = result} \n    else {records = data[recKey];result[recKey] = [];recResults = result[recKey];\n      for(var k in data) {if (k != recKey) {result[k] = data[k]}}};\n    records.forEach(function(rec, i) { \n      var newRec = Object.assign(rec, values.static);\n      if (i in values.dynamic) {newRec = Object.assign(newRec, values.dynamic[i])};\n      recResults.push(newRec)})'

class JsFilter:
    """
  Filter the different records in a recordSet from the definition given as a parameter.
  The filters definition is based on a dictionary as keys the column names. Each records should have the given columns.
  All records which do not match the rules will not be considered

  :return: A new JS dictionary with only the selected lines
  """
    pmts = ('filterCols',)
    content = " \n    filters = {};\n    filterCols.forEach(function(rec){  \n      if (filters[rec['colName']] === undefined){\n        filters[rec['colName']] = {val: [], op: rec['op'], allIfEmpty: rec['allIfEmpty']}};\n      if(Array.isArray(rec['val'])){ filters[rec['colName']].val = filters[rec['colName']].val.concat(rec['val'])}\n      else if (filters[rec['colName']].val.indexOf(rec['val']) < 0) { filters[rec['colName']].val.push(rec['val'])}});\n    data.forEach( function(rec) {  \n      var isValid = true; \n      for (var col in filters) {\n        var opType = filters[col]['op']; \n        if (opType == '='){if(filters[col].val.indexOf(rec[col]) < 0){if ( (filters[col].val != '') && filters[col].allIfEmpty ) {isValid = false; break}}}\n        else if (opType == 'in'){ \n          if(filters[col].val.indexOf(rec[col]) < 0){isValid = false; break}\n          else if ((filters[col].val.length == 0) && !filters[col].allIfEmpty) {isValid = false; break}}\n        else if (opType == 'above'){if(filters[col].val[0] > rec[col]){isValid = false; break}}\n        else if (opType == 'below'){if(filters[col].val[0] < rec[col]){isValid = false; break}}\n        else if (opType == 'between'){if((filters[col].val[0] > rec[col]) || (filters[col].val[1] < rec[col])){isValid = false; break}}\n    }; if (isValid) {result.push(rec)}})"

class JsIntensity:
    """

  """
    alias = 'intensity'
    params = ('cols',)
    value = '\n    stats = {};\n    cols.forEach(function(col){stats[col] = {min: null, max: null}});\n    data.forEach(function(rec){\n      cols.forEach(function(col){\n        if((stats[col].max == null) || (rec[col] > stats[col].max) ) { stats[col].max = rec[col]};\n        if((stats[col].min == null) || (rec[col] < stats[col].min) ) { stats[col].min = rec[col]}})});\n    data.forEach(function(rec){\n      cols.forEach(function(col){rec[col + ".intensity.min"] = stats[col].min; rec[col + ".intensity.max"] = stats[col].max});\n      result.push(rec)});\n    '

    @staticmethod
    def extendColumns(jsSchema, params):
        """

    :param jsSchema:
    :param params:
    """

class JsToUrl:
    alias = 'dictToUrl'
    value = '\n    var tmpResults = [];\n    for(var k in data["pmts"]){tmpResults.push(k +"="+ data["pmts"][k])}; \n    result = tmpResults.join("&");\n    if (typeof data["anchor"] !== \'undefined\'){result = result +"#"+ data["anchor"]}\n    '