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

        fileName = "exitFiles/" + str(uuid.uuid4())
        pathToFile = "genomesearch/static/" + fileName + ".csv"
        outfile = open(f'{pathToFile}', 'w')

        rows = queryOutput
        excludedColumns = []

        columnNames = "SNPId,name,chrom,cM,AAFreq,ABFreq,BBFreq,SNP,alleleA,alleleB,sourceSeq,samples".split(',')
        
        for columnName in excludedColumns:
            columnNames.pop(columnNames.index(columnName))

        columnNames += cultures

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
            dataArr = data.split(',')
            data = ""

            cultureIncrement = 0
            while cultureIncrement < len(cultures):   
                data += dataArr[cultureIncrement].replace(cultures[cultureIncrement], '', 1) + ','           
                cultureIncrement += 1                

            csvInf += data
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
            dataArr = culturesSTR.split(',')
            data = ""

            jsonInf += '"Samples":\n{'

            dataIncrement = 0
            while (dataIncrement < len(dataArr)):
                data += '"' + cultures[dataIncrement] + '":"' + dataArr[dataIncrement].replace(cultures[dataIncrement], '', 1) + '",\n'
                dataIncrement += 1

            data = data[:-2]
            jsonInf += data + "\n}\n"   
            jsonInf += "},\n"

        jsonInf = jsonInf.replace(' ','')
        jsonInf = jsonInf[:-6]
        jsonInf += '\n}\n}\n}'

        outfile.write(jsonInf)
        outfile.close()

        outfile = open(f'{pathToFile}', 'r')
        data = json.load(outfile)

        return(data)

        