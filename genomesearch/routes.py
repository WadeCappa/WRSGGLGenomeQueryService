from os import error
from typing import Container
from flask import Flask, render_template, request, redirect, jsonify
from genomesearch.forms import SearchForm, RegistrationForm, LoginForm, SortForm
from genomesearch.models import Genome
from genomesearch.outputData import Output
from genomesearch import app
import re
from sqlalchemy.sql import text
from flask_restful import Resource, Api
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address

import csv
import json
import sys
import random

api = Api(app)

limiter = Limiter(
    app,
    key_func=get_remote_address,
    default_limits=["60000 per day", "20 per second"]
)

class GenomeRouting():
    allCultivars = ("A99AR 600923,Abe,Abilene,Ace,Adams,Adena,Admire,Agassiz,Agent,Agrus,Akron,Albit,Alex,Alice,Alicel,Allegiance,Alliance,Alpowa,Amidon,Anderson,Andnox,Andrews,Angus,Ankor,Antelope,Anza,Apex 83,AR 910,Arapahoe,Arcadian,Archer,Arco,Ark,Arkan,Arkansas No. 105,Arrow,Arrowsmith,ARS-Amber,ARS-Chrystal,ARS-Crescent,ARS-Selbu,Arthur,Arthur 71,Ashkof,Athena,Atlas 50,Atlas 66,ATW 270,Auburn,Augusta,Austin,Avalanche,Avoca,Awned Onas,Awnless Baart,Aztec,Baart 38,Baart 46,Bac Up,Baca,Bailey,Baker,Baldrock,Bannock,Barbee,Basin,Beau,Bennett,Bergan,Big Club 37,Bison,Blackhawk,Blackhull,Blanca,Blazer,Blizzard,Blount's Lambrigg,Blue Jacket,Blueboy,Bonanza,Brill,Bronze,Brule,Buckshot,Bulter,Caddo,Calorwa,Canawa,Capitan,Carleeds,Carlson's Fife,Carson,Cataldo,Celtic,Centennial,Cheney,Chiefkan,Claf,Clark,Clemson 201,Cloud,Coastal,Coker 47-27,Coker 61-19,Coker 68-15,Coker 762,Collin,Colorado No. 50,Colorow,Colt,Comet,Concho,Copper,Coteau,Courtney,Crew,Dalen,Dancer,Delmar,Deloris,Delta Queen,Dirkwin,DK-435,Dodge,Downy,Duke,Dutro Clipper,Dynasty,Eagle Chief,Early Blackhull,Early Defiance,Early Premium,Edwall,Edwin,Eickmeyer,Eider,Eklund,Elgin,Ellar,Elmar,Eltan,Encore,Enid,Era,Erhardt,Eric,Escondido,Escondido 41,Eureka,Excel,Exchange,Express,Extra Early Blackhull,F.S. 401,Fairfield,Faro,Federation 41,Federation 41M,Federation 67,Feland,FFR 555W,Fielder,Fieldwin,Fillmore,Fineway,Finley,Fjeld,Fletcher,Florida 302,Florida 303,Florida 304,Fortuna,Forward,Forx,Fox,Frankenmuth,Franklin,Freedom,Fremont,Frisco,Frontiersman,Fulcaster,Fulcaster 612,Fulhard,Fulhio,Fulton,Funk Seeds 7171,Funk Seeds 7172,Funk Seeds 7174,Funk W-332,Funk W-335,Funk W-433,Funk W-504,Fuzz,GA-Andy,Gage,GA-Gore,Gaines,Gasser,Gasta,GB 2148,Gene,Genro,Gent,Georgia 100,Glacier,Glenman,Glory,Glyndon,Golden,Golden 50,Golden Chief,Golden Cross,Goodstreak,Goss,GR 855,GR 876,Grandin,Grandprize,Grant,Greer,Guard 17934,Gus,Gypsum,Hadden,Hallam,Halt,Hancock,Hansel,Hard Baart,Hard Federation 31,Harding,Hardired,Harry,Hart,Harvest Queen,Hatcher,Hatton,Haven,Hawk,Hayden,Haynes Bluestem,Heglar,Henry,Hi-Line,Hill 81,Hoff,Honor,Hope,Hosar,HR 53,HR 64,Hume,Hunter,Hybrid 143,Hybrid 63,Hymar,Hyper,Idaed,Idaed 59,IDO 644,IDO 671,IDO 686,IDO 687,III,Illini Chief,Illinois No. 2,Imbler,Indian,Ingal,Inia 66R,Intrada,InW0731,Inw8832,Inw8841,Inw9244,Iobred,Iohardi,Iona,Ionia,Iowin,Irwin Dicklow,Itana,Jacmar,James,Jeff,Jefferson,Jerry,John,Joleen,Jones Fife,Jubilee,Judith,Juniper,Justin,Kancom,Kanhull,KanKing,Kanqueen,Kanred,Karmont,Kaw 61,Kawvale,Kay,Kenosha,Key,Kiowa,Kirwin,Kitt,Klasic,Kmor,Knox 62,Komar,Krona,Kruse,Lafron,Lamar,Lambert,Lancer,Lani,LaPorte,Lark,Leap,Lee,Leif,Lemhi,Lemhi 53,Lemhi 62,Lemhi 66,Len,Lenore,Lew,Lewis,Lewjain,LHS,Lincoln,Lindon,Lobred 73,LoLo,Longberry No. 1,Longhorn,Louise,Lucas,Luft,Luke,Lynn,Mace,MacVicar,Madison,Madsen,Magnum,Manning,Marberg,Marett Chancellor,Marfed,Maricopa,Marshall,Martin,Martin Amber,Marvel,Massey,Maverick,Mayview,McCall,McGuire,McKay,McNair 1587,McNair 1813,McNair 2203,McNeal,Meggie,Mercury,Meridian,Merit,Merrimac,Mesa,Michigan Amber,Michikoff,Mida 12008,Milam,Milburn,Mindoro,MinnPro,Minter,Minturki,Missouri Valley,Moking,Monon,Moran,Mosida,Nabob,Nebraska No. 28,Nebraska No. 6,Nebraska No. 60,Nebred,Neeley,Nekota,Nelson,NEO 6545,NEO1643,NEO5548,New Victory,Newana,Newark Improved Triumph,Newcaster,Newthatch,Newton,Nicoma,Niobrara,Nogal,Norak,Norana,Nordic,Nordman,Norseman,Norwesta,Norwin,Nudel,Nugaines,Nuplains,Nured,NY Batavia,Oasis,Oatka Chief,OK 101,Omaha,Omar,Omega 78,Onas 41,Onas 53,Oregon Zimmerman,Orfed,Orion,Oro,Osage,Osco,Ottawa,Oveson,Owens,Pacer,Pacfific Bluestem 37,Paha,Palala,Palo Duro,Parker,Payne,Peak,Peak 72,Peck,Pecos,Pedigreed Blackhull No. 60,Penawawa,Pennoll,Penquito,Phoenix,Pilcraw,Pilot,PL 145,Plainsman,Pogo 48,Polk,Pomerelle,Ponca,Pondera,Pontiac,Pony,Portage,Portola,Poso,Poso 41,Poso 44,Potomac,Powerclub,Prairie,Prairie Red,Premier 11940,Pride of Genesee,Probred,Prodax,Profit 75,Progress,Promontory,Prospect,Prosperity,Prospur,Protor,Prowers,Prowers 99,Purcan,Purcell,Purplestraw,Quality,R 36,Racine,Radco,Raeder,Ram,Ramona,Ramona 50,Rampart,Ranger,Rawhide,Read,Red Chief,Red Clawson,Red Jacket,Red River 68,Red Rock,Red Wave,Redhard,Redhart 4,Redhart 5,Redhull,Redland,Redwin,Regal,Regenerated Defiance,Rego,Reliance,Reliant,Rely,Rew,Rex,Richland,Rick,Ridit,Riley,Riley 67,Rio,Rio Blanco,Rival,Rocky,Rod,Roedel,Rohde,Roland,Rose,Rosen,Rosetta,Roughrider,RSI 220,Ruddy,Rulo,Rural New Yorker No. 57,Rural New Yorker No. 6,Rushmore,Russell,S 76,S 78,Saline,Salmon,Saluda,Sanford,Satanta,Sawmont,Sawtana,Sawtell,Sawyer,Scout,Scoutland,Seabreeze,Sentinel,Severn,Sharp,Shasta,Shepherd,Sheridan,Sherman,Shield,Shortana,Sibley 81,Silver Sheaf,Sioux,Siouxland,Solar,Southern Belle,Spillman,Spinkcota,Spokane Chief,Spring Field,SR 49,Stacey,Stadler,Stafford,Steele,Sterling,Stoa,Stoddard,Sturgeon,Sturgeon_1,Sullivan,Super Triumph,Surprise,Survivor,Susquehanna,Sylvan,Symphony,Syringa,TAM 106,TAM 109,TAM 200,TAM 202,TAM 300,TAM W-101,TAM W-104,Tammy,Tayland,Tayler,Taylor 49,Tecumseh,Telemar 19,Tendoy,Tenmarq,Terral 877,Teton,Texred,Thatcher,Thorne,Thunderbird,Tiber,Ticonderoga,Timstein,Timwin,Tioga,Todd,Tracey,Trailblazer,Trapper,Treasure,Triplet,Trison,Triumph,Trumbull,Twain,Twin,Tyee,Tyler,UI Lochsa,UI Pettit,UI Winchester,Union,Urquie,USU Apogee,Utac,Utah-100,Ute,V.P.I. 112,V.P.I. 131,Vahart,Valprize,Vance,Vandal,Vanguard,varname2154,varname2157,varname2158,varname2163,varname2165,varname2172,varname2369,varname2375,varname2510,varname2545,varname2551,varname2552,varname2553,varname2555,varname2566,varname2571,varname2737W,varname4555,varname4578,varname5221,varname5232,varname5411,varname5422,varname5466,varname5469,varname5630,varname711,varname715,varname751,varname771,varname775,varname7805,varname7833,varname7837,varname8232,varname830,varname835,Vermillion,Vesta,Victory,Vigal,Vigo,Virginia 565372,Vista,Voyager,W2501 516200,W2502,Waban,Waco,Wadual,Wadual 94,Wahoo,Wakanz,Wakeland,Waldron,Walera,Wampum 17691,Wanken,Wanser,Wared,Warrior,Wasatch,Wawawai,Wesbred 905R,Wesel,Westar,Westbred 911,Westbred Aim,Westbred Challenger,Westmont,Weston,Wheaton,Wheedling,Wheeler,White Federation 38,White Federation 59,White Federation 60,White Mediterranean,White Odessa,Whitebird,Wichita,Wilbur 6757,Willett,Williams,Willow Creek,Windstar,Wings,Winoka,Winridge,Wisconsin Pedigree No. 2,Wissler,World Seeds 1,World Seeds 13,World Seeds 1651,World Seeds 1809,World Seeds 1812,World Seeds 1877,World Seeds 25,World Seeds 6,Wrangler,Yamhill,Yecora Rojo,Yogo,Yolo,Yorkstar,Yorkwin,Yukon,Yumar,Palomino,Boundary,Buchanan,Bauermeister,EDDY,Farnum,MDM,NORWEST 553,Paladin,WA008118,WA008119,WA008139,WA008156,WA008157,WA008158,WA008159,WHETSTONE,coda,brubdage,Estica,Residence,Yellowstone,WA7976,WA7977,Diva,Zak,FarnumB03,NW553,ORCF 102,Hollis,Cabernet,Jedd,Azimut,Tucson,Expresso,WA8152,WA8154,WA8153,WA8064-55,WA8151,F/E-39,F/E-4,MORO,WA8137,WA8138,WEATHERFORD,ARS970161-3L (Selbu),AMBER,TUBBS06,BITTERROOT,BRUEHL,BRUNDAGE96,BRUNDAGECF,BRUNEAU,CARA,CHRYSTAL,CHUKAR,CONCEPT,CRESCENT,DUNE,FINCH,GOETZE,HILLER,LAMBERTCF,MARY,MASAMI,ORCF101,ORCF103,SALUTE,SIMON,SKILES,STEPHENS,TUBBS,XERPHA,MOHLER")
    allCultivars = allCultivars.split(',')
    chromArr = ["1A","1B","1D","2A","2B","2Dx","3A","3B","3D","4A","4B","4D", "5A","5B","5D", "6A","6B","6D", "7A","7B","7D"]

    def isFilled(data):
        if data == None:
            return False
        if data == '':
            return False
        if data == []:
            return False
        return True

    @ app.route('/')
    def home():
        return redirect("/WRSGGL-Wheat-Genome-Searcher", code=302)

    @app.errorhandler(404)
    def pageNotFound(error):
        return render_template('notFound.html'), 404

    @ app.route('/WRSGGL-Wheat-API-Documentation')
    def documentation():
        return render_template('apiDoc.html')

    @ app.route('/About-The-WRSGGL-Wheat-Search-Data')
    def explainData():
        return render_template('explainData.html')

    @ app.route('/Query', methods=['GET'])
    @limiter.limit("5 per second")
    def all_info():

        print(request.args.get('chrome'))
        print(request.args.get('SNPId'))
        print(request.args.get('lowercM'))
        print(request.args.get('highercM'))        

        inputChrome = []
        filterArr = []
        count = 0
        # if request.args.get('SNIPId'):


        if request.args.get('chrome') == None:
            print("Empty inputChrome")
        else:
            inputChrome = [x for x in request.args.get('chrome').split(',')]

            goodOutput = 0
            for inputName in inputChrome:
                for name in GenomeRouting.chromArr:
                    if inputName == name:
                        goodOutput += 1
                
            if goodOutput == len(inputChrome):              
                filterArr.append(Genome.chrom.in_(inputChrome))
                print("Chrome array = ")
                print(inputChrome)
                count += 1
            else:
                return 'Bad Request!\nIncompatible chrome.', 421

        if request.args.get('SNPId') == None:
            print("No SNPId")
        else:
            input = Genome.SNPId.contains(request.args.get('SNPId'))
            if Genome.query.filter(input).first() is not None:
                filterArr.append(input)
                count += 1
            else:
                return 'Bad Request!\nIncompatible SNPId.', 422

        if request.args.get('lowercM') == None:
            print("No lower bounds")
        else:
            try:
                lowerInput = Genome.cM >= float(request.args.get('lowercM'))
                filterArr.append(lowerInput)
                count += 1
            except:
                return 'Bad Request!\nIncompatible lowercM.', 423
            
        if request.args.get('highercM') == None:
            print("no higher bounds")
        else:
            try:       
                higherInput = Genome.cM <= float(request.args.get('highercM'))
                filterArr.append(higherInput)
                count += 1
            except:
                return 'Bad Request!\nIncompatible highercM.', 424


        print(count)
        
        if count == 0:
            messagesCount = Genome.query.all()

        elif count == 1:
            messagesCount = Genome.query.filter(filterArr[0]).all()

        elif count == 2:
            messagesCount = Genome.query.filter(filterArr[0]).filter(filterArr[1]).all()

        elif count == 3:
            messagesCount = Genome.query.filter(filterArr[0]).filter(filterArr[1]).filter(filterArr[2]).all()

        elif count == 4:
            messagesCount = Genome.query.filter(filterArr[0]).filter(filterArr[1]).filter(filterArr[2]).filter(filterArr[3]).all()
    
        # if request.args.get('Chrome'):
        #     pass
            # chromeArr = [x for x in request.args.get('Chrome').split(',')]
        return(Output.writeToJson(messagesCount, GenomeRouting.allCultivars))
        # return("Test")


    # admire
    @ app.route('/WRSGGL-Wheat-Genome-Searcher', methods=['GET', 'POST'])
    def search():

        errorCode = ''

        outFile = '../static/exit.csv'
        form = SearchForm()
        messagesResult = []
        messagesCount = []
        searchParameters = []
        
        #print(form.validate_on_submit(), file=sys.stdout)
        if request.method == 'POST' and form.validate():
            print("POST requested")
            #print(form.genomeName.data, file=sys.stdout)

            #query = query()

            #if form.genomeName.data in dataDictionary:
            #    messagesResult = [dataDictionary[form.genomeName.data]]

            checkboxArr = []
            checkboxArr.extend((
            form.chrom1A.data,form.chrom1B.data,form.chrom1D.data,
            form.chrom2A.data,form.chrom2B.data,form.chrom2D.data,
            form.chrom3A.data,form.chrom3B.data,form.chrom3D.data,
            form.chrom4A.data,form.chrom4B.data,form.chrom4D.data,
            form.chrom5A.data,form.chrom5B.data,form.chrom5D.data,
            form.chrom6A.data,form.chrom6B.data,form.chrom6D.data,
            form.chrom7A.data,form.chrom7B.data,form.chrom7D.data))
            
            print(checkboxArr)
            searchArr = []
            for i in range(len(checkboxArr)):
                if checkboxArr[i]:
                    searchArr.append(GenomeRouting.chromArr[i])

            if searchArr == []:
                searchParameters.append('E')
            #    searchParameters.append(Genome.chrom.in_(chromArr))
            else:
                searchParameters.append(Genome.chrom.in_(searchArr))


            if form.lowerCM.data == None:
                searchParameters.append('E')
            else:
                input = Genome.cM >= form.lowerCM.data
                if Genome.query.filter(input).first() is not None:
                    searchParameters.append(input)
                else:
                    errorCode = 'Invalid bound for lowercM'
                    searchParameters.append(input)

            if form.upperCM.data == None:
                searchParameters.append('E')
            else:
                input = Genome.cM <= form.upperCM.data
                if Genome.query.filter(input).first() is not None:
                    searchParameters.append(input)
                else:
                    errorCode = 'Invalid bound for upperCM'
                    searchParameters.append(input)

            if form.genomeCultivar.data == '':
                searchParameters.append('E')
            #    searchParameters.append(Genome.samples)
            else:
                cultivarOut = ""
                input = Genome.samples.contains(form.genomeCultivar.data)
                test = Genome.query.filter(input).first()
                if test is not None:
                    for cultivar in GenomeRouting.allCultivars:
                        if re.search(r'\b' + cultivar + r'\b', form.genomeCultivar.data):
                            print(cultivar)
                            cultivarOut = cultivar
                            searchParameters.append(Genome.samples.contains(cultivarOut))
                    if cultivarOut == "":
                        errorCode = 'Invalid Cultivar'
                        searchParameters.append(Genome.samples.contains("ooga booga this code is now broken"))

                else:
                    errorCode = 'Invalid Cultivar'
                    searchParameters.append(input)
            
            if form.genomeName.data == '':
                searchParameters.append('E')
            #    searchParameters.append(Genome.SNPId)
            else:
                input = Genome.SNPId.contains(form.genomeName.data)
                if Genome.query.filter(input).first() is not None:
                    searchParameters.append(input)
                else:
                    errorCode = 'Invalid SNPId'
                    searchParameters.append(input)

            searchContainer = []
            count = 0


            for increment in searchParameters:
                print(increment)
                if increment != 'E':
                    searchContainer.append(increment)

                    count += 1

            print(count)
            
            if count == 0:
                messagesCount = Genome.query.all()
                messagesResult = Genome.query.limit(1000).all()
                

            elif count == 1:
                messagesCount = Genome.query.filter(searchContainer[0]).all()
                messagesResult = Genome.query.filter(searchContainer[0]).limit(1000).all()


            elif count == 2:
                messagesCount = Genome.query.filter(searchContainer[0]).filter(searchContainer[1]).all()
                messagesResult = Genome.query.filter(searchContainer[0]).filter(searchContainer[1]).limit(1000).all()


            elif count == 3:
                messagesCount = Genome.query.filter(searchContainer[0]).filter(searchContainer[1]).filter(searchContainer[2]).all()
                messagesResult = Genome.query.filter(searchContainer[0]).filter(searchContainer[1]).filter(searchContainer[2]).limit(1000).all()


            elif count == 4:
                messagesCount = Genome.query.filter(searchContainer[0]).filter(searchContainer[1]).filter(searchContainer[2]).filter(searchContainer[3]).all()
                messagesResult = Genome.query.filter(searchContainer[0]).filter(searchContainer[1]).filter(searchContainer[2]).filter(searchContainer[3]).limit(1000).all()


            elif count == 5:
                messagesCount = Genome.query.filter(searchContainer[0]).filter(searchContainer[1]).filter(searchContainer[2]).filter(searchContainer[3]).filter(searchContainer[4]).all()
                messagesResult = Genome.query.filter(searchContainer[0]).filter(searchContainer[1]).filter(searchContainer[2]).filter(searchContainer[3]).filter(searchContainer[4]).limit(1000).all()


            if messagesCount != None and len(messagesCount) > 0 and count != 0:
                outFile = Output.writeToCSV(messagesCount, GenomeRouting.allCultivars)
            elif count == 0:
                outFile = "exit"
            else:
                if errorCode == '': 
                    errorCode = 'Search Too specific, no matching data found.'
  
        print(outFile)
        return render_template('genomeSearch.html', title='Search', form=form, messages=messagesResult, messagesCount=messagesCount, outFile = outFile, errorMessage = errorCode)