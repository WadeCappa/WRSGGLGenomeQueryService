from typing import Container
from flask import render_template, request
from genomesearch.forms import SearchForm
from genomesearch.models import Genome
from genomesearch import app

import uuid
import json
from datetime import datetime
import time, sched

class Output():


    schedule = sched.scheduler(time.time, time.sleep)
    def writeToCSV(queryOutput, cultures, targetCultivar = ""):

        fileName = str(uuid.uuid4())
        pathToFile = "genomesearch/static/exitFiles/" + fileName + ".csv"
        outfile = open(f'{pathToFile}', 'w')

        rows = queryOutput
        excludedColumns = []

        columnNames = "SNPId,name,chrom,cM,AAFreq,ABFreq,BBFreq,SNP,alleleA,alleleB,sourceSeq,samples".split(',')
        
        for columnName in excludedColumns:
            columnNames.pop(columnNames.index(columnName))

        columnNames += cultures.split(',')

        writtenNames = columnNames
        writtenNames.pop(writtenNames.index("samples"))  
        csvInf = ", ".join(writtenNames) + "\n"

        for row in rows:
            for columnName in columnNames:
                if columnName not in rows[0].__dict__:
                    pass
                elif columnName not in excludedColumns:
                    data = str(row.__dict__[columnName])
                    csvInf += data + ","

            data = str(row.__dict__["samples"])

            for cultureName in cultures.split(','):
                data = data.replace(cultureName, '', 1)

            csvInf += data + ","   
            csvInf += "\n"

        csvInf = csvInf.replace(' ','')
        outfile.write(csvInf)
        outfile.close()
        return(fileName)



    def writeToJson(queryOutput, cultures, targetCultivar = ""):
        if queryOutput == []:
            return 'No matching data', 400

        fileName = str(uuid.uuid4())
        pathToFile = "genomesearch/static/exitFiles/" + fileName + ".json"
        outfile = open(f'{pathToFile}', 'w')

        rows = queryOutput
        excludedColumns = []
        excludedColumns.append("_sa_instance_state")
        excludedColumns.append("id")
        excludedColumns.append("samples")

        columnNames = [i for i in rows[0].__dict__]
        
        for columnName in excludedColumns:
            columnNames.pop(columnNames.index(columnName))

        columnNames.sort()
        columnNames += [i for i in cultures]

        jsonInf = '{'
        for row in rows:
            jsonInf += '"' + str(row.__dict__["SNPId"]) + '":\n{\n'
            for columnName in columnNames:
                if columnName not in rows[0].__dict__:
                    pass
                elif columnName not in excludedColumns:
                    data = str(row.__dict__[columnName])
                    jsonInf += '"' + columnName + '"' +  ":" + '"' + data + '",\n'

            culturesSTR = str(row.__dict__["samples"])

            jsonInf += '"Samples":\n{'
            samplesSTR = ''
            strContant = [x for x in culturesSTR.split(',')]
            strContantIncrement = 0
            for cultureName in cultures.split(','):
                samplesSTR += '     "' + cultureName + '":"' + strContant[strContantIncrement].replace(cultureName, '', 1) + '",\n'
                strContantIncrement += 1

            samplesSTR = samplesSTR[:-2]
            jsonInf += samplesSTR + "\n}\n"   
            jsonInf += "},\n"

        jsonInf = jsonInf.replace(' ','')
        jsonInf = jsonInf[:-6]
        jsonInf += '\n}\n}\n}'
        outfile.write(jsonInf)
        outfile.close()

        outfile = open(f'{pathToFile}', 'r')
        data = json.load(outfile)

        return(data)