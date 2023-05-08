from urllib import response
from django.http import Http404, HttpResponse, JsonResponse
from django.shortcuts import redirect, render
from datetime import date
import requests
import json
from urllib3 import HTTPResponse

def index(request):
    return HttpResponse("Hello, world. You're at the emerging economies app's index.")


def hrdoAPI(countries):
    url = 'http://ec2-54-174-131-205.compute-1.amazonaws.com/API/HDRO_API.php/country_code=' + \
        countries+'/indicator_id=137506'
    print(url)
    responseIMF = requests.get(url).json()
    extData = []
    jsonDataBRA = responseIMF["indicator_value"]["BRA"]["137506"]
    jsonDataIDN = responseIMF["indicator_value"]["IDN"]["137506"]
    jsonDataIND = responseIMF["indicator_value"]["IND"]["137506"]
    jsonDataMEX = responseIMF["indicator_value"]["MEX"]["137506"]
    jsonDataTUR = responseIMF["indicator_value"]["TUR"]["137506"]
    jsonDataZAF = responseIMF["indicator_value"]["ZAF"]["137506"]
    extData.append(jsonDataBRA)
    extData.append(jsonDataIDN)
    extData.append(jsonDataIND)
    extData.append(jsonDataMEX)
    extData.append(jsonDataTUR)
    extData.append(jsonDataZAF)
    # with open('data.json', 'w') as jsonfile:
    #     json.dump(extData, jsonfile)
    return extData


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
    return extData


def imfAPIone(database, frequency, countries, indicators, startPeriod, endPeriod):
    url = 'http://dataservices.imf.org/REST/SDMX_JSON.svc/CompactData/'+database+'/' + \
        frequency+'.'+countries+'.'+indicators + \
        '?startPeriod='+startPeriod+'&endPeriod='+endPeriod
    responseIMF = requests.get(url).json()
    jsonData = responseIMF
    series = jsonData['CompactData']['DataSet']['Series']
    extData = []
    countryCode = series['@REF_AREA']
    indicatorCode = series['@INDICATOR']
    timeSeries = []
    for i in series['Obs']:
        try:
            timeSeries.append(
                dict({"time": i['@TIME_PERIOD'], "value": i['@OBS_VALUE']}))
        except KeyError:
            pass
    extData.append(dict({"countryCode": countryCode,
                   "indicatorCode": indicatorCode, "timeSeries": timeSeries}))
    # with open('data.json', 'w') as jsonfile:
    #     json.dump(extData, jsonfile)
    return extData


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
    return extData


def dashboard(request):

    currentYear = date.today().year

    extData15 = wbAPI("v2", "A", "BRA;IDN;IND;MEX;TUR;ZAF;WLD", "NY.GDP.MKTP.KD", str(currentYear-22), str(currentYear-2))  # OKK
    # extData14 = hrdoAPI('BRA,IDN,IND,MEX,TUR,ZAF')  # OKK
    extData1 = wbAPI("v2", "A", "BRA;IDN;IND;MEX;TUR;ZAF", "NY.GDP.PCAP.PP.KD", str(
        currentYear-22), str(currentYear-2))  # OKK
    extData8 = wbAPI("v2", "A", "BRA;IDN;IND;MEX;TUR;ZAF", "CM.MKT.LCAP.GD.ZS", str(
        currentYear-22), str(currentYear-2))  # OKK
    extData7 = imfAPI('FM', 'A', 'BR+ID+IN+MX+TR+ZA', 'GGXCNL_G01_GDP_PT', str(currentYear-12), str(currentYear-1))  # OKK
    extData9 = imfAPI('FM', 'A', 'BR+ID+IN+MX+TR+ZA', 'G_XWDG_G01_GDP_PT',
                      str(currentYear-12), str(currentYear-1))  # OKK
    extData6 = imfAPI('CPI', 'M', 'BR+ID+IN+MX+ZA', 'PCPI_PC_CP_A_PT',
                      str(currentYear-12), str(currentYear-1))  # OKK
    extData16 = imfAPI('IFS', 'M', 'IN+GB+U2', 'ENDA_XDC_USD_RATE',
                       str(currentYear-12), str(currentYear))  # ID+IN+TR+ZA // BR+MX
    extData4 = wbAPI("v2", "A", "BRA;IDN;IND;MEX;TUR;ZAF", "NE.EXP.GNFS.ZS", str(
        currentYear-12), str(currentYear-2))  # OKK
    extData11 = imfAPI('FAS', 'A', 'BR+ID+IN+MX+TR+ZA', 'FCLODCG_GDP_PT',
                       str(currentYear-12), str(currentYear-2))  # OKK
    extData17 = wbAPI("v2", "A", "BRA;IDN;IND;MEX;TUR;ZAF", "FS.AST.PRVT.GD.ZS", str(
        currentYear-15), str(currentYear-2))  # OKK
    extData13 = imfAPI('FAS', 'A', 'BR+ID+IN+MX+TR+ZA', 'FCBODCA_NUM',str(currentYear-15), str(currentYear-2))  # OKK

    extDataJson1 = json.dumps(extData1)
    extDataObj1 = json.loads(extDataJson1)

    extDataJson4 = json.dumps(extData4)
    extDataObj4 = json.loads(extDataJson4)

    extDataJson6 = json.dumps(extData6)
    extDataObj6 = json.loads(extDataJson6)

    extDataJson7 = json.dumps(extData7)
    extDataObj7 = json.loads(extDataJson7)

    extDataJson8 = json.dumps(extData8)
    extDataObj8 = json.loads(extDataJson8)

    extDataJson9 = json.dumps(extData9)
    extDataObj9 = json.loads(extDataJson9)

    extDataJson11 = json.dumps(extData11)
    extDataObj11 = json.loads(extDataJson11)

    extDataJson13 = json.dumps(extData13)
    extDataObj13 = json.loads(extDataJson13)

    # extDataJson14 = json.dumps(extData14)
    # extDataObj14 = json.loads(extDataJson14)

    extDataJson15 = json.dumps(extData15)
    extDataObj15 = json.loads(extDataJson15)

    extDataJson16 = json.dumps(extData16)
    extDataObj16 = json.loads(extDataJson16)

    extDataJson17 = json.dumps(extData17)
    extDataObj17 = json.loads(extDataJson17)

    extResponse = {
        'extDataJson1': extDataJson1,
        'extDataObj1': extDataObj1,
        'extDataJson4': extDataJson4,
        'extDataObj4': extDataObj4,
        'extDataJson6': extDataJson6,
        'extDataObj6': extDataObj6,
        'extDataJson7': extDataJson7,
        'extDataObj7': extDataObj7,
        'extDataJson8': extDataJson8,
        'extDataObj8': extDataObj8,
        'extDataJson9': extDataJson9,
        'extDataObj9': extDataObj9,
        'extDataJson11': extDataJson11,
        'extDataObj11': extDataObj11,
        'extDataJson13': extDataJson13,
        'extDataObj13': extDataObj13,
        # 'extDataJson14': extDataJson14,
        'extDataObj14': extDataObj14,
        'extDataJson15': extDataJson15,
        'extDataObj15': extDataObj15,
        'extDataJson16': extDataJson16,
        'extDataObj16': extDataObj16,
        'extDataJson17': extDataJson17,
        'extDataObj17': extDataObj17,
    }

    response = json.dumps(extResponse)

    return JsonResponse(response, safe=False)


def home(request):
    return render(request, 'emer_econ_app/dashboard.html', {"activeHome": "active"})


def errorPage(request):
    return render(request, 'emer_econ_app/errorPage.html', {})
