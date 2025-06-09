import pandas as pd

class createDatabase:

    def __init__(self, detected_objects, threshold):
        self.dataframe = pd.DataFrame(columns=['objects'])
        self.threshold = threshold
        self.itemList = []
        self.probabilityValuesList = []
        self.detected_objects = detected_objects
        self.itemSupport = []
        self.itemSupportSum = []
        for objectList in self.detected_objects:
            supportSum = 0
            dataDic = {}
            self.items = []
            self.values = []
            self.supports = []
            for item in objectList:
                supportSum = supportSum + 1
                if item[1] >= self.threshold:
                    if item[0] not in dataDic.keys():
                        dataDic[item[0]] = [item[1]]
                    else:
                        dataDic[item[0]].append(item[1])
            self.items = [item for item in dataDic.keys()]
            self.values = [max(value) for value in dataDic.values()]
            self.supports = [len(value) for value in dataDic.values()]
            self.itemSupportSum.append(supportSum)
            self.itemList.append(self.items)
            self.probabilityValuesList.append(self.values)
            self.itemSupport.append(self.supports)
            self.dataframe.loc[self.dataframe.shape[0], 'objects'] = dataDic.keys()

    def getDataFrame(self):
        return self.dataframe

    def saveAsTransactionalDB(self, outputFile, sep):
        writeFile = open(outputFile, 'w')
        for i in range(len(self.itemList)):
            if self.itemList[i]:
                writeLine = sep.join(map(str, self.itemList[i]))
                writeFile.write(writeLine + '\n')
        writeFile.close()

    def saveAsTemporalDB(self, outputFile, sep):
        writeFile = open(outputFile, 'w')
        for i in range(len(self.itemList)):
            if self.itemList[i]:
                writeLine = sep.join(map(str, self.itemList[i]))
                writeFile.write(str(i) + sep + writeLine + '\n')
        writeFile.close()

    def saveAsUtilityTransactionalDB(self, outputFile, sep):
        writeFile = open(outputFile, 'w')
        for i in range(len(self.itemList)):
            if self.itemList[i]:
                writeLine = sep.join(map(str, self.itemList[i]))
                writeLine2 = sep.join(map(str, self.itemSupport[i]))
                writeFile.write(writeLine + ':' + str(self.itemSupportSum[i]) + ':' + writeLine2 + '\n')
        writeFile.close()

    def saveAsUtilityTemporalDB(self, outputFile, sep):
        writeFile = open(outputFile, 'w')
        for i in range(len(self.itemList)):
            if self.itemList[i]:
                writeLine = sep.join(map(str, self.itemList[i]))
                writeLine2 = sep.join(map(str, self.itemSupport[i]))
                writeFile.write(str(i) + str(sep) + writeLine + ':' + str(self.itemSupportSum[i]) + ':' + writeLine2 + '\n')
        writeFile.close()

    def saveAsUncertainTransactionalDB(self, outputFile, sep):
        writeFile = open(outputFile, 'w')
        for i in range(len(self.itemList)):
            if self.itemList[i]:
                writeLine = sep.join(map(str, self.itemList[i]))
                writeLine2 = sep.join(map(str, self.probabilityValuesList[i]))
                writeFile.write(writeLine + ':1:' + writeLine2 + '\n')
        writeFile.close()

    def saveAsUncertainTemporalDB(self, outputFile, sep):
        writeFile = open(outputFile, 'w')
        for i in range(len(self.itemList)):
            if self.itemList[i]:
                writeLine = sep.join(map(str, self.itemList[i]))
                writeLine2 = sep.join(map(str, self.probabilityValuesList[i]))
                writeFile.write(str(i) + str(sep) + writeLine + ':1:' + writeLine2 + '\n')
        writeFile.close()