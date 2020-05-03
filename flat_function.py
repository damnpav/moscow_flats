import pandas as pd
from bs4 import BeautifulSoup
import requests
import re

flatDf = pd.read_excel("flat_pattern.xlsx")
meinLink = flatDf['Ссылка'][5]


def get_my_flat(link):
    subways = pd.read_excel('subways.xlsx')
    
    meinLink = link
    metro = list(subways['Station'])
    
    r = requests.get(meinLink)
    soup = BeautifulSoup(''.join(r.text))
    bsResult = soup.findAll(text=True)  # retrieve all text
    
    # цена
    mydivs = soup.findAll('div', {'class': 'Offer__price'})
    priceStr = re.findall(r'>.*<', str(mydivs[0]))[0][1:-1]
    price = re.sub('\D', '', priceStr)
    
    # какие станции
    ourStations = []
    for i in range(len(metro)):
        if metro[i] in r.text:
            ourStations.append(metro[i])
    ourStations = list(set(ourStations))
    
    # площадь
    flag = 0
    i = 0
    space = 'Not found'
    while i <= len(bsResult) and flag == 0:
        if str(bsResult[i]).find('space') != -1:
            space = str(str(bsResult[i]))
            flag = 1
        i += 1
    spaceStr = re.findall(r'"space":"\d+"', space)[0]
    space = spaceStr.split(":")[1].replace('"', "")
    
    # ближайшая станция
    metroLinks = soup.findAll('a', {'class': 'metro__link'})
    stationDict = {}
    for i in range(len(metroLinks)):
        if 'pedestrian' in str(metroLinks[i]):
            station = re.findall(r'title="[\w ]+"', str(metroLinks[i]))[0].split('=')[1].replace('"', '')
            rawTime = re.findall(r'~[\d ]+мин', str(metroLinks[i]))[0]
            myTime = int(re.sub('\D', '', rawTime))
            stationDict[station] = myTime
    
    closestStation = min(stationDict, key=stationDict.get)
    closestTime = stationDict[closestStation]
    
    # посудомойка
    mydivs = soup.findAll('li', {'class': 'Offer__featuresItem Offer__featuresItem--disabled'})
    dishwasher = 1
    balcony = 1
    for i in range(len(mydivs)):
        if 'Посудомоечная машина' in str(mydivs[i]):
            dishwasher = 0
        if 'Балкон' in str(mydivs[i]):
            balcony = 0

    # этаж
    mydivs = soup.findAll('div', {'class': 'Offer__detailsValue'})
    for i in range(len(mydivs)):
        if len(re.findall(r'/\d', str(mydivs[i]))) > 0:
            floors = re.findall(r'\d', str(mydivs[i]))
    floorString = str(min(floors)) + '/' + str(max(floors))

    # комиссия
    comissionRaw = re.findall(r'комиссия \d+%', r.text)[0]
    comission = re.sub(r'\D', '', comissionRaw)
    
    returnDict = {'Все станции: ': str(ourStations), 'Ближайшее метро: ': str(closestStation),
                  'Удаленность от метро (мин): ': str(closestTime), 'Площадь (м2): ': str(space),
                  'Посудомойка: ': str(dishwasher), 'Балкон: ': str(balcony), 'Этаж: ': str(floorString),
                  'Стоимость: ': str(price), 'Комиссия %': str(comission)}

    return returnDict


