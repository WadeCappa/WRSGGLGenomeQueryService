# expecting filenames HitCounts.txt and SNPreport.txt
# expecting files: fixedHitCounts.txt and fixedSNPreport.txt

import csv
#Psy1.D1_48

def trimEndNumber(name):
    i = len(name) - 1
    while i >= 0:
        if name[i] == "_":
            name = name[0:i]
            return name
        i -= 1
    return name

errorDictionary = {}
averageDictionary = {}
keysArray = []
firstColumn = []
fileObject = open('fixedHitCounts.txt', 'w')
fileObject.truncate(0)
f = open('HitCounts.txt')
fileObject.write(f.readline())
f.close()
fileObject.close()
outputArray = []
with open('HitCounts.txt') as csvfile:
    csvreader = csv.reader(csvfile, delimiter='\t')
    lineCount = 0
    lineSum = 0
    for row in csvreader:
        #FIRST RUN THROUGH START
        
        i = 1
        while i < len(row):

            if row[i] != '':
                outputArray.append(row[i])
                if lineCount > 1:
                    lineSum += int(row[i])
            i += 1
        
        outputArray.insert(0, row[0])
        if lineCount == 0:
            keysArray = outputArray
        else:
            if row[0] not in errorDictionary:
                errorDictionary[row[0]] = {}
            averageDictionary[row[0]] = lineSum
            firstColumn.append(row[0])

        lineCount += 1
        
        print(lineSum)
        lineSum = 0
        #FIRST RUN THROUGH END

        #SECOND RUN THROUGH START
        outputArray = []
        i = 1
        if lineCount > 1:
            while i < len(row):

                if row[i] != '':
                    if lineCount > 1 and int(row[i]) < (averageDictionary[row[0]]/ (len(row) - 1 ) * .01): # len(row)-1 should be NumberOfSamples (DOUBLE CHECK THIS)
                        outputArray.append(0)
                        errorDictionary[row[0]][keysArray[i]] = 0
                    else:
                        outputArray.append(int(row[i]))

                i += 1

            fileObject = open('fixedHitCounts.txt', 'a')
            
            fileObject.write(row[0])
            for i in range(len(outputArray)):
                fileObject.write("\t" + str(outputArray[i]))
            
            fileObject.write("\n")
            fileObject.close()

fileObject = open('fixedSNPreport.txt', 'w')
fileObject.truncate(0)
f = open('SNPreport.txt')
fileObject.write(f.readline())
f.close()
fileObject.close()
outputArray = []
with open('SNPreport.txt') as csvfile:
    csvreader = csv.reader(csvfile, delimiter='\t')
    lineCount = 0
    lineSum = 0
    #print(keysArray)
    for row in csvreader:
        #print(row)
        if lineCount > 0:
            i = 1
            while i < len(row):

                if row[i] != '':
                    if lineCount > 0:
                        #print(row[0])
                        #print(errorDictionary)
                        savedStr = trimEndNumber(row[0])
                        
                        if savedStr in errorDictionary:
                            #print(errorDictionary[row[0]])
                            if keysArray[i] in errorDictionary[savedStr]: #errorDictionary[row[0]]
                                outputArray.append("-")
                            else:
                                outputArray.append(row[i])
                        else:
                            outputArray.append(row[i])
                i += 1
        
        fileObject = open('fixedSNPreport.txt', 'a')
        if lineCount > 0:
            fileObject.write(row[0])

            for i in range(len(outputArray)):
                fileObject.write("\t" + outputArray[i])
            
            fileObject.write("\n")
        fileObject.close()

        lineCount += 1
        outputArray = []
        
    

