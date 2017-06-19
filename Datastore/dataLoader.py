from SQLiteClient import SQLiteClient
class DataLoader(SQLiteClient):

    # columns delimited with '\'    ex: 'wrong\r.Q.N.\r.Q.N.\rQN\r.Q.N.\1'
    # entries delimited with newline character
    # Note on usage: column types assumed to be strings. Must correct within
    #   this function if columns are other types.
    def loadTableFromFile(self, tableToLoad, filePath, columnNameList, unique=True):
        firstColumnValueSet = set()

        with open(filePath) as fileToLoad:
            for line in fileToLoad:
                valueDict = {}
                formattedLine = line.strip('\n').split("\\")
                for i in range(len(columnNameList)):
                    valueDict[columnNameList[i]] = formattedLine[i]
                    if i == 5:
                        valueDict[columnNameList[i]] = int(valueDict[columnNameList[i]])

                if not valueDict[columnNameList[0]] in firstColumnValueSet or not unique:
                    self.insertIntoTable(tableToLoad, valueDict)
                    firstColumnValueSet.add(valueDict[columnNameList[0]])

if(__name__ == "__main__"):
    dl = DataLoader("wordformsDB")
    # run load scripts here
