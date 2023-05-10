from urllib import response
from django.http import Http404, HttpResponse, JsonResponse
from django.shortcuts import redirect, render
from datetime import date, datetime
import pytz
import requests
import json
from urllib3 import HTTPResponse
from .models import Database

def imfAPI(database, frequency, countries, indicators, startPeriod, endPeriod):
    url = 'http://dataservices.imf.org/REST/SDMX_JSON.svc/CompactData/'+database+'/' + \
        frequency+'.'+countries+'.'+indicators + \
        '?startPeriod='+startPeriod+'&endPeriod='+endPeriod
    print(url)
    responseIMF = requests.get(url).json()
    jsonData = responseIMF
    series = jsonData['CompactData']['DataSet']['Series']
    # if(database=="FAS" and indicators=="FCLODCG_GDP_PT"):
    #     with open('datax.json', 'w') as jsonfile:
    #         json.dump(series, jsonfile)
    extData = []
    for s in series:
        newSeries = []
        countryCode = s['@REF_AREA']
        indicatorCode = s['@INDICATOR']
        timeSeries = []
        for i in s['Obs']:
            try:
                timeSeries.append(
                    dict({"time": i['@TIME_PERIOD'], "value": i['@OBS_VALUE']}))
            except KeyError:
                pass
        newSeries.append(dict(
            {"countryCode": countryCode, "indicatorCode": indicatorCode, "timeSeries": timeSeries}))
        extData.append(newSeries)
    # with open('data.json', 'w') as jsonfile:
    #     json.dump(series, jsonfile)

    return extData #returns a python list

def wbAPI(database, frequency, countries, indicators, startPeriod, endPeriod):
    url = "http://api.worldbank.org/"+database+"/country/"+countries+"/indicator/"+indicators + \
        "?format=json"+"&date="+startPeriod+":"+endPeriod + \
        "&frequency="+frequency+"&per_page=1000"
    print(url)
    responseWB = requests.get(url).json()
    extData = []
    for s in responseWB[1]:
        try:
            extData.append(dict(
                {"countryCode": s["countryiso3code"], "indicatorCode": s["indicator"]["id"], "time": s["date"], "value": s["value"]}))
        except KeyError:
            pass
    # with open('data.json', 'w') as jsonfile:
    #     json.dump(extData, jsonfile)
    return extData#returns a python list

def insertDummyDataintoDatabase():
    if(len(Database.objects.all())==0):
        datetime_india = datetime.now(pytz.timezone('Asia/Kolkata'))
        data = "{'foo': 'bar'}"
        dummy_data = Database(database=data, database_refresh_date=datetime_india)
        dummy_data.save()

def showDatabase(request):
    insertDummyDataintoDatabase()
    database = Database.objects.all()[0].database
    response = json.dumps(database)
    return JsonResponse(response, safe=False)
    
def refreshDatabase(request):
    currentYear = date.today().year

    extData15 = wbAPI("v2", "A", "BRA;IDN;IND;MEX;TUR;ZAF;WLD", "NY.GDP.MKTP.KD", str(currentYear-22), str(currentYear-2))
    extData1 = wbAPI("v2", "A", "BRA;IDN;IND;MEX;TUR;ZAF", "NY.GDP.PCAP.PP.KD", str(currentYear-22), str(currentYear-2))
    extData8 = wbAPI("v2", "A", "BRA;IDN;IND;MEX;TUR;ZAF", "CM.MKT.LCAP.GD.ZS", str(currentYear-22), str(currentYear-2))
    extData7 = imfAPI('FM', 'A', 'BR+ID+IN+MX+TR+ZA', 'GGXCNL_G01_GDP_PT', str(currentYear-12), str(currentYear-1))
    extData9 = imfAPI('FM', 'A', 'BR+ID+IN+MX+TR+ZA', 'G_XWDG_G01_GDP_PT', str(currentYear-12), str(currentYear-1))
    extData6 = imfAPI('CPI', 'M', 'BR+ID+IN+MX+ZA', 'PCPI_PC_CP_A_PT',str(currentYear-12), str(currentYear-1))
    extData4 = wbAPI("v2", "A", "BRA;IDN;IND;MEX;TUR;ZAF", "NE.EXP.GNFS.ZS", str(currentYear-12), str(currentYear-2))
    extData11 = imfAPI('FAS', 'A', 'BR+ID+IN+MX+TR+ZA', 'FCLODCG_GDP_PT',str(currentYear-12), str(currentYear-2))
    extData17 = wbAPI("v2", "A", "BRA;IDN;IND;MEX;TUR;ZAF", "FS.AST.PRVT.GD.ZS", str(currentYear-15), str(currentYear-2))
    extData13 = imfAPI('FAS', 'A', 'BR+ID+IN+MX+TR+ZA', 'FCBODCA_NUM',str(currentYear-15), str(currentYear-2))

    # json loads -> returns an object from a string representing a json object.
    # json dumps -> returns a string representing a json object from an (list) object.
    # load and dump -> read/write from/to file instead of string


    #converts the list object (extData1) to string object representing JSON(extDataJson1)
    extDataJson1 = json.dumps(extData1)
    extDataJson4 = json.dumps(extData4)
    extDataJson6 = json.dumps(extData6)
    extDataJson7 = json.dumps(extData7)
    extDataJson8 = json.dumps(extData8)
    extDataJson9 = json.dumps(extData9)
    extDataJson11 = json.dumps(extData11)
    extDataJson13 = json.dumps(extData13)
    extDataJson15 = json.dumps(extData15)
    extDataJson17 = json.dumps(extData17)


    #creates a dict
    extResponse = {
        'extDataJson1': extDataJson1,
        'extDataJson4': extDataJson4,
        'extDataJson6': extDataJson6,
        'extDataJson7': extDataJson7,
        'extDataJson8': extDataJson8,
        'extDataJson9': extDataJson9,
        'extDataJson11': extDataJson11,
        'extDataJson13': extDataJson13,
        'extDataJson15': extDataJson15,
        'extDataJson17': extDataJson17,
    }

    #creates a string representing JSON
    response = json.dumps(extResponse)

    #add dummy data to database if it is empty
    insertDummyDataintoDatabase()

    #saving the fetched data to the database
    database = Database.objects.all()[0]
    database.database_refresh_date = datetime.now(pytz.timezone('Asia/Kolkata'))
    database.database = response
    database.save()

    return HttpResponse("database refreshed")



def data(request):
    database = Database.objects.all()[0].database
    return JsonResponse(database, safe=False)

def lastDatabaseRefreshDate(request):
    latest_refresh_date = Database.objects.all()[0].database_refresh_date
    return HttpResponse(latest_refresh_date)
    
def dashboard(request):
    return render(request, 'emer_econ_app/dashboard.html', {"activeHome": "active"})

def refreshPage(request):
    return render(request, 'emer_econ_app/refreshPage.html', {})

def errorPage(request):
    return render(request, 'emer_econ_app/errorPage.html', {})
