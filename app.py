#!/usr/bin/env python3 
# -*- coding: utf-8 -*-

import re
import time
sendTime = time.time()
import datetime
import pytz 
import random
import requests
import json

import gspread
from oauth2client.service_account import ServiceAccountCredentials

from bs4 import BeautifulSoup
from imgurpython import ImgurClient
from flask import Flask, request, abort

from firebase import firebase
firebase = firebase.FirebaseApplication('https://python-f5763.firebaseio.com/',None)
queryAllKeyAndValues = firebase.get('/data',None)
quiet = firebase.get('/QuietGroup',None)
quietArr = quiet['group_id']

f = {
      "type": "service_account",
      "project_id": "groupalbum-166505",
      "private_key_id": "7e1b6365be1d48cec5716c208abbf7a7ce0f5095",
      "private_key": "-----BEGIN PRIVATE KEY-----\nMIIEvQIBADANBgkqhkiG9w0BAQEFAASCBKcwggSjAgEAAoIBAQDDhNbntwtEgks5\nL5LXIaNwVjyt76L5P5YaG5eQSkoXpNHXuLoPf73yNuT1s7kTArf7sgPwaPess2+K\nDzKPnLc9Bkq728TC5D0lL4hzEKsDe/PdBqLfvoakNySEpJxXziFh/XjlND+BtkXD\nJe15xmuLc9bLZa6uQBWJdzTIoewSStfPMOoghAwLBYDAmlMzuzkK+690SiBUisb0\nOU6Sw96wsX86MO6wKIKBvgMTuegt0I6zVTei1LMsyjQplmFMuF0AUjfuQwo0BS0r\n3Kd0zdZs8OBBTitqfujKpaEVVVm4F6jopWsDqEJkT6LaaRfXRrPZ7p1Mxuv3c3TU\nSBeHzZwhAgMBAAECggEALGm1g4dB6PsL6V6UJYg/nxoHyJ8Bz0qRZzbTU/R8JijL\nfgw5P6IN3MJ5ehKsPNRGRMdoO6ksca+E68COBK9dtGAEg+3lITxFY3gLr8+eeTkj\n6RZD0z1tSko4YmUeGpf5X0/7sV0P/AASksS/0ASxk0jqBuP/LRfjjIlmlRirDnBJ\n46tv5de9XZlH1Twy0fG6+yFJGWd4uLQQm++O8xJ5loyDu7ZdWSYcJ9Bta4Ur41fb\n96tEvk7PnQ9dvGWLs00qIuSSZOigEIk5AuCxeKaMeR3SmdsK7jPuKQ5ZX3i/qcub\n6TIeVvtiZMLcAP5u+aFkTUVOKdE1dY1MEY3xbO/SXQKBgQDyZH28y+7udVwbl6mD\nbaBiqvQFKzHBVhE+x/dyx3Frm5r8ok30MKy375SdNligiGcSbLoLOIg5UJ31BTjf\nWb9f8WblQiHtpixMBbk5PghOwXulq95IOmYDsYR7Hx15KtsVPODBCO4w56RMgFAd\nK2KQa2Cg1nqr4fCCTLKd/AKdHwKBgQDOfrXvl1grKe77Fbb61KkaWqj+/9jCl2vo\nOxyl344BgEDBoXaW+YRmv4y4HXowritVP57URlT46Gq5V6gezGL6elTv6AGXYkRd\nFJGm+QUIj6WFSiQXGVlbdb1RIJrWysb1tb3T77nbAcN8Hgp3U2A+n/dSnO5sTLLG\nzV2sZbdevwKBgQDjoL131CfQZgQWoWl+VC//GL3KMNMr1dCiHZXigyufO2TkBOOi\nAyfgICx3Kvc14oKxCcv5B6Dd+jgsRjgvf4+54PCZMW69R4Vn6yQTfo68rvSYE3vO\nZpEwvL9GBGVgSX+uRRpoDSPqZ06izQjvK7QHHd+Di4dt7OM46h//Pw+RTwKBgBc8\nvR6UKnDZDDKnM+swKUN09lWT1wG25obAuC2WZbWXiDICCIVe2N5zKdPCRXDa+Ldk\nLGx46bEE/pWS3rFwkKbdQ1eoBR3TChxrZySiG0XmXFsOh9ctnBelvUM25xXKxe76\nn70M2h5iKWx7OPRKpqcFe2CJlm8LhobGr4bp/2OjAoGAZjANDFWt8sz1x4hqzdvj\nkKUGGlo66E00II8N1dN5oOfs7mlGBgX9X8uNqCQkewA5yx4lq1YkjiNrucsk8et0\n0lhVXm2k3Bae57gKoGOJ1iSlZpnLQD9sOJCavm39crCRrVtSsiy6vIsc+B3YV+jX\nNIuqgLPiszH2b+00HQMmLi0=\n-----END PRIVATE KEY-----\n",
      "client_email": "testsheet@groupalbum-166505.iam.gserviceaccount.com",
      "client_id": "117086094069483849270",
      "auth_uri": "https://accounts.google.com/o/oauth2/auth",
      "token_uri": "https://accounts.google.com/o/oauth2/token",
      "auth_provider_x509_cert_url": "https://www.googleapis.com/oauth2/v1/certs",
      "client_x509_cert_url": "https://www.googleapis.com/robot/v1/metadata/x509/testsheet%40groupalbum-166505.iam.gserviceaccount.com"
}

from linebot import (
    LineBotApi, WebhookHandler
)
from linebot.exceptions import (
    InvalidSignatureError
)
from linebot.models import *
#from linebot.models import (
#    MessageEvent, TextMessage, TextSendMessage,TemplateSendMessage
#)

app = Flask(__name__)

line_bot_api = LineBotApi('E3V1P2J74V3qQ5VQsR0Au27E+NwBBlnh8r24mpP5vbkrogwj7PFroxNAKS9MU2iBeDMJiEFiaqe0SvKypYsoPcr70wVac/v4FJfXa1TwGPo0QeI1fkZcaejhJSz09aetC0TaMsblhNOorJaG4J/RlwdB04t89/1O/w1cDnyilFU=')
handler = WebhookHandler('f2f133f2ba43194cf0e18503586023aa')


@app.route("/callback", methods=['POST'])
def callback():
    # get X-Line-Signature header value
    signature = request.headers['X-Line-Signature']

    # get request body as text
    body = request.get_data(as_text=True)
    app.logger.info("Request body: " + body)

    # handle webhook body
    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        abort(400)

    return 'OK'

@app.route('/GGWP', methods=['GET'])
def test():
    return "Hello World!"

@app.route('/queryDB/<string:message>', methods=['GET'])
def firebaseQuery(message):
    #queryAllKeyAndValues = firebase.get('/data',None)
    global queryAllKeyAndValues
    allKeys = queryAllKeyAndValues.keys()
    for k in allKeys:
        #print(message.find(k))
        #若找不到 返回值是 -1
        if message.find(k) != -1:
            #print(queryAllKeyAndValues[k])
            queryAllValues = queryAllKeyAndValues[k]
            count = len(queryAllValues) - 1
            randomNumber = random.randint(0,count)
            result = queryAllValues[randomNumber]
            return result
    
    return 'GG'

@app.route('/insertDB/<string:key>/<string:value>', methods=['GET'])
def firebaseInsert(key,value):
    #key = '冠宏'
    #value = 'OC之神'
    getValues = firebase.get('/data',key)
    if getValues is None:
        new = dict()
        new['0'] = value
        firebase.put('data',key,new)
    else:    
        getValues.append(value)
        firebase.put('data',key,getValues)
    #寫完 停兩秒 再讀取DB一次
    time.sleep(2)
    global queryAllKeyAndValues
    queryAllKeyAndValues.clear()
    queryAllKeyAndValues = firebase.get('/data',None)
    #queryAllKeyAndValues[key] = value
    return "好的 記住了"

@app.route('/deleteDB', methods=['GET'])
def firebaseDelete(deleteKey):
    firebase.delete('/data', deleteKey)
    time.sleep(2)
    #刪除完再重新讀取一次DB
    global queryAllKeyAndValues
    queryAllKeyAndValues.clear()
    queryAllKeyAndValues = firebase.get('/data',None)
    return '好的 已經遺忘'

@app.route('/fetchDB/<string:key>', methods=['GET'])
def firebaseFetch(key):
       
    string = ''
    getValues = firebase.get('/data',key)
    if getValues is None:
        string = "沒有被寫入呢"
    else:
        for x in getValues:
            string += x + ' , '
        #刪掉最後一個逗號
        last = len(string)
        string = string[0:last]
    return string

def firebaseChatLog(content, name='', userID = ''):
    tz = pytz.timezone('Asia/Taipei')
    dd = datetime.datetime.now(tz).date()
    inputDate = "{}-{}-{}".format(dd.year,dd.month,dd.day)
    getChatLog = firebase.get('/ChatLog',inputDate)
    
    if name != '' and userID != '':
        content = name + ':' + content + '.' + userID
        
    if getChatLog is None:
        arr = []
        arr.append(content)
        firebase.put('/ChatLog',inputDate,arr)
    else:    
        getChatLog.append(content)
        firebase.put('/ChatLog',inputDate,getChatLog)

def stock(stockNumber):
    url = 'https://www.google.com.hk/finance?q='
    url += stockNumber
    header = {'User-Agent':'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/59.0.3071.115 Safari/537.36'}
    res = requests.get(url,headers=header,verify=False)
    res.encoding = 'utf-8'
    soup = BeautifulSoup(res.text,'html.parser')
    title = soup.find('h3')
    title = title.text.strip()
    #print(title)
    
    resultString = ''
    resultString += title + '\n'
    #現價
    nowPrice = ''
    for p in soup.select('.pr'):
        #print(p.text)
        nowPrice += p.text.strip()
    #漲跌
    upDown = soup.select('.chr')
    if not upDown :
        upDown = soup.select('.chg')
    uString = ''
    for u in upDown:
        #print(u.text.strip().encode('utf8'))
        uString += u.text.strip()
        #print(uString)
    
    key = []
    for k in soup.select('.key'):
        #print(k.text.strip().encode('utf8'))
        key.append(k.text.strip())
    
    val = list()
    for v in soup.select('.val'):
        #print(v.text.strip().encode('utf8'))
        val.append(v.text.strip())
    
    #現價
    resultString += '-------------' + '\n'
    resultString += '現價 ' + '\n' + nowPrice + '\n'
    resultString += '-------------' + '\n'
    #漲跌
    resultString += '漲跌' + '\n' + uString + '\n'
    resultString += '-------------' + '\n'
    #每股盈餘
    resultString += key[7] + '\n' + val[7] + '\n'
    resultString += '-------------' + '\n'
    #開盤
    resultString += key[2]+ '\n' + val[2] + '\n'
    resultString += '-------------' + '\n'
    #範圍
    resultString += key[0] + '\n' + val[0] + '\n'
    resultString += '-------------' + '\n'
    #52週
    resultString += key[1] + '\n' + val[1] + '\n'
    resultString += '-------------' + '\n'
    #股息/收益
    resultString += key[6] + '\n' + val[6] + '\n' + '-------------' + '\n' + 'From Google stock'
   
    return resultString

@app.route('/star/<string:star>', methods=['GET'])
def constellation(star):

    constellationDict = dict()
    constellationDict = {'牡羊': 'Aries', '金牛': 'Taurus', '雙子': 'Gemini','巨蟹': 'Cancer',
                         '獅子': 'Leo', '處女': 'Virgo', '天秤': 'Libra','天蠍': 'Scorpio', 
                         '射手': 'Sagittarius', '魔羯': 'Capricorn','水瓶': 'Aquarius', '雙魚': 'Pisces'}
    
    url = 'http://www.daily-zodiac.com/mobile/zodiac/{}'.format(constellationDict[star])
    res = requests.get(url,verify=False)
    res.encoding = 'utf-8'
    soup = BeautifulSoup(res.text,'html.parser')
    #print(soup)
    name = soup.find_all('p')
    #print(name)
    starAndDate = []
    for n in name:
        #print n.text.encode('utf8')
        starAndDate.append(n.text)
        #print(starAndDate)
    today = soup.select('.today')[0].text.strip('\n')
    today = today.split('\n\n')[0]
    #print today
    title = soup.find('li').text.strip()
    #print(title)
    content = soup.find('article').text.strip()
    #print content

    resultString = ''
    resultString += starAndDate[0] + ' ' + starAndDate[1] + '\n'
    resultString += today + '\n'
    resultString += content + '\n\n'
    resultString += 'from 唐立淇每日星座運勢' + '\n\n'
    resultString += '-以下是小歐星座網站-' + '\n'

    urlOrz= 'https://horoscope.dice4rich.com/?sign={}'.format(constellationDict[star])
    urlOrz = urlOrz.lower()
    res = requests.get(urlOrz)
    soup = BeautifulSoup(res.text,'html.parser')

    title = soup.select('.current .title')
    content = soup.select('.current .content')
    for i in range(len(title)+len(content)):
        if i%2 == 0:
            print(title[int(i/2)].text.strip())
            resultString += title[int(i/2)].text.strip() + '\n'
        else:
            print(content[int(i/2)].text)
            resultString += content[int(i/2)].text + '\n\n'

    return resultString

@app.route('/weather', methods=['GET'])
def weather(ChooseCity):
    cityDict = dict()
    cityDict = {'台北': 'Taipei_City', '新北': 'New_Taipei_City', '桃園': 'Taoyuan_City',
          '台中': 'Taichung_City', '台南': 'Tainan_City', '高雄': 'Kaohsiung_City',
          '基隆': 'Keelung_City', '新竹市': 'Hsinchu_City', '新竹縣': 'Hsinchu_County',
          '苗栗': 'Miaoli_County', '彰化': 'Changhua_County', '南投': 'Nantou_County',
          '雲林': 'Yunlin_County', '嘉義市': 'Chiayi_City', '嘉義縣': 'Chiayi_County',
          '屏東': 'Pingtung_County', '宜蘭': 'Yilan_County', '花蓮': 'Hualien_County',
          '台東': 'Taitung_County', '澎湖': 'Penghu_County','金門': 'Kinmen_County','連江': 'Lienchiang_County'}

    url = 'http://www.cwb.gov.tw/V7/forecast/taiwan/{}.htm'.format(cityDict[ChooseCity])
    #print(url)
    #header = {'User-Agent':'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/59.0.3071.115 Safari/537.36'}
    #res = requests.get(url,headers=header,verify=False)
    res = requests.get(url,verify=False)
    res.encoding = 'utf-8'
    soup = BeautifulSoup(res.text,'html.parser')
    #print soup
    city = soup.select('.currentPage')[0].text
    #print(city)
    time = soup.select('.Issued')[0].text
    time = time.split(': ')[1]
    time = time.split(' ')[0]
    #print(time)

    imgTitle = soup.find_all('img')

    title = []
    for i in imgTitle: 
        i = str(i).split('title="')[1]
        i = str(i).split('"/>')[0]
        #print i
        title.append(i)

    content = soup.select('td')
    data = []
    for c in content:
        c = c.text.strip('\n')
        #print(c.encode('utf8'))
        data.append(c)
    
    resultString = ''
    resultString += '🌤 ' + city + '  '  + time + '\n\n' 

    resultString += '今晚至明晨 ' + str(data[0])  + '度\n' 
    resultString += title[0] + '  下雨機率 ' + str(data[3]) + '\n\n' 

    resultString += '明日白天' + str(data[4]) + ' 度\n'
    resultString += title[1] + '  下雨機率 ' + str(data[7]) + '\n\n' 

    resultString += '明日晚上' + str(data[8]) + ' 度\n'
    resultString += title[2] + '  下雨機率 ' + str(data[11]) + '\n'

    return resultString

def get_movie_id(url):
    # e.g. "https://tw.rd.yahoo.com/referurl/movie/thisweek/info/*https://tw.movies.yahoo.com/movieinfo_main.html/id=6707"
    #      -> match.group(0): "/id=6707"
    pattern = '/id=\d+'
    match = re.search(pattern, url)
    if match is None:
        return url
    else:
        return match.group(0).replace('/id=', '')

@app.route('/movie', methods=['GET'])
def get_movies():
    Y_MOVIE_URL = 'https://tw.movies.yahoo.com/movie_thisweek.html'
    dom = requests.get(Y_MOVIE_URL)
    soup = BeautifulSoup(dom.text, 'html.parser')
    movies = []
    rows = soup.select('.release_list li')
    #rows = soup.select('#content_l li')
    Y_INTRO_URL = 'https://tw.movies.yahoo.com/movieinfo_main.html'  # 詳細資訊
    for row in rows:
        movie = dict()
        movie['ch_name'] = row.select('.release_movie_name .gabtn')[0].text.strip()
        movie['eng_name'] = row.select('.en .gabtn')[0].text.strip()
        #movie['movie_id'] = get_movie_id(row.select('.release_movie_name .gabtn')[0]['href'])
        movie['poster_url'] = row.select('img')[0]['src']
        #movie['release_date'] = get_date(row.select('.release_movie_time')[0].text)
        movie['intro'] = row.select('.release_text')[0].text.strip().replace(u'...詳全文', '').replace('\n', '')[0:15] + '...'
        #movie['info_url'] = row.select('.release_movie_name .gabtn')[0]['href']
        movie['info_url'] = Y_INTRO_URL + '/id=' + get_movie_id(row.select('.release_movie_name .gabtn')[0]['href'])
        movies.append(movie)
    return movies

def sticker(key):
    sitckerDict = dict()
    sitckerDict = {'聽歌': {'sticker_id':'103','package_id':'1'}, '想睡': {'sticker_id':'1','package_id':'1'}, 
                   '生日快樂': {'sticker_id':'427','package_id':'1'}, ' 飽': {'sticker_id':'425','package_id':'1'},
                   '騎車': {'sticker_id':'430','package_id':'1'}, '窮': {'sticker_id':'417','package_id':'1'},
                   '很忙': {'sticker_id':'411','package_id':'1'}, '翻滾': {'sticker_id':'423','package_id':'1'},
                   '冷': {'sticker_id':'29','package_id':'2'}, '喝': {'sticker_id':'28','package_id':'2'},
                   '晚安': {'sticker_id':'46','package_id':'2'}, '考試': {'sticker_id':'30','package_id':'2'},
                   '熱': {'sticker_id':'601','package_id':'4'}, '戒指': {'sticker_id':'277','package_id':'4'},
                   '鑽': {'sticker_id':'276','package_id':'4'}, '唱': {'sticker_id':'413','package_id':'1'},
                   '彩虹': {'sticker_id':'268','package_id':'4'}, '櫻': {'sticker_id':'604','package_id':'4'},
                   '累': {'sticker_id':'526','package_id':'2'}, '生氣': {'sticker_id':'527','package_id':'2'},
                   '上班': {'sticker_id':'161','package_id':'2'}, '歡迎': {'sticker_id':'247','package_id':'3'},
                   '升天': {'sticker_id':'108','package_id':'1'}, '喇叭': {'sticker_id':'414','package_id':'1'},
                   '下雨': {'sticker_id':'507','package_id':'2'}}
    
    allKeys = sitckerDict.keys()
    for k in allKeys:
        #print(message.find(k))
        #若找不到 返回值是 -1
        if key.find(k) != -1:
            return sitckerDict[k]
        
    return 'GG'

def darkAnan():
    AVGLE_LIST_COLLECTIONS_API_URL = 'https://api.avgle.com/v1/videos/{}'

    randomPagesNumber = random.randint(0,1195)
    #page 1195,有60片,其他都50
    #print randomPageNumber
    if randomPagesNumber != 1195:
        #0~49選不重複的7個數字
        randomVideoNumbers = random.sample(range(0, 49), 5)
    else:
        randomVideoNumbers = random.sample(range(0, 59), 5)

    res = requests.get(AVGLE_LIST_COLLECTIONS_API_URL.format(randomPagesNumber))
    res.encoding='utf8'
    #print(res.json())
    videos = []
    videos = res.json()['response']['videos']
    
    videoRandom = []
    for x in randomVideoNumbers:
        videoRandom.append(videos[x])
    
    return videoRandom

def darkAnanQuery(name):
    url = 'https://api.avgle.com/v1/search/{}/{}'
    res = requests.get(url.format(name,'0'))
    videos = res.json()['response']['videos']
    randomVideoNumbers = random.sample(range(0, len(videos)), 5)
    
    videoRandom = []
    for x in randomVideoNumbers:
        videoRandom.append(videos[x])
    
    return videoRandom


def aime(key):
#     client_id = '78616d0ac6840e4'
#     client_secret = 'aef2b708acb068e5f7a6262190da024cc29b9b26'
    client_id = 'c3e767d450a401e'
    client_secret = 'cdf5fb70e82bc00e65c0d1d1a4eed318ae82024c'
    client = ImgurClient(client_id,client_secret)

    if key == 'Aime' or key == 'aime': 
        album = ['hLZwL','Qt8En']
        i = random.randint(0, len(album) - 1)
        images = client.get_album_images(album[i])
        index = random.sample(range(0, len(images)),5)
    else:
        album = 'hoBxs'
        #i = random.randint(0, len(album) - 1)
        images = client.get_album_images(album)
        index = random.sample(range(0, len(images)),5)
        
    imgurResult = []
    for i in index:
        imageDict = dict()
        #imageDict['imageLink'] = images[i].link.replace('http', 'https')
        imageDict['imageLink'] = images[i].link
        description = images[i].description.split('http')[0].strip('\n')
        imageDict['title&price'] = description 
        #imageDict['title'] = description.split('$')[0].strip()
        #imageDict['price'] = '$'+ description.split('$')[1].strip()
        imageDict['shopeeLink'] = images[i].description.split('$')[1][3:].strip()
        imgurResult.append(imageDict)
       
    return imgurResult

def handsome():
    client_id = 'c3e767d450a401e'
    client_secret = 'cdf5fb70e82bc00e65c0d1d1a4eed318ae82024c'
    client = ImgurClient(client_id,client_secret)
    images = client.get_album_images('hjCtM')
    index = random.randint(0, len(images) - 1)
    
    return images[index].link

def hospital():
    tz = pytz.timezone('Asia/Taipei')
    dd = datetime.datetime.now(tz).date()
    #inputDate = "{}-{}-{}".format(dd.year,dd.month,dd.day)
    chineseYear = dd.year - 1911
    m = ''
    if dd.month < 10:
        m = '0' + str(dd.month)

    d = ''
    if dd.day <= 9 :
        d = '0' + str(dd.day)
    else :
        d = str(dd.day)

    d1 = ''
    if dd.day < 9 :
        d1 = '0' + str(dd.day + 1)
    elif dd.day == 9:
        d1 = str(dd.day + 1)
    else :
        d1 = str(dd.day + 1)
        
    url = 'http://reg.807.mnd.gov.tw/stepB1.asp'
    
    #gg = "syear=106&smonth=09&sday=05&eyear=106&emonth=09&eday=12&SectNO=14&EmpNO=0117937&isQuery=1"
    fromData = "syear={}&smonth={}&sday={}&eyear={}&emonth={}&eday={}&SectNO=&EmpNO=&isQuery=1".format(chineseYear,m,d,chineseYear,m,d1)
    header = {'Content-Type':'application/x-www-form-urlencoded'}

    res = requests.post(url ,headers= header, json = fromData)
    res.encoding = res.apparent_encoding
    #res.encoding = 'big5'
    #res.encoding = 'utf8'
    soup = BeautifulSoup(res.text,'html.parser')
    #print soup
    rows = soup.select('.tablecontent1')
    #print len(rows)
    hospitalResult = []
    for row in rows:
        hospitalResult.append(row.text.split('我要預約')[0].strip())
    
    return hospitalResult[0:4]

@app.route('/wine', methods=['GET'])
def wine():

    scope = ['https://spreadsheets.google.com/feeds', 'https://www.googleapis.com/auth/drive']
    creds = ServiceAccountCredentials.from_json_keyfile_dict(f, scope)
    client = gspread.authorize(creds)
    
    # Find a workbook by name and open the first sheet
    # Make sure you use the right name here.
    sheet = client.open("酒吧巡迴清單").sheet1
    # Extract and print all of the values
    #list_of_hashes = sheet.get_all_records()
    list_of_hashes = sheet.get_all_values()

    notYet = list()
    did = list()
    totalCount = ''
    notYetCount = ''
    didCount = ''
    for sh in range(sheet.row_count):
        #row需要 + 4
        sh = sh + 4
        #print(list_of_hashes[sh])
        if list_of_hashes[sh][2] == '':
            #店名是空就跳出
            #print(int(list_of_hashes[sh][0]) -1)
            totalCount = str(int(list_of_hashes[sh][0]) -1)
            break 
        elif list_of_hashes[sh][1] == '':
            #還沒去過
            notYet.append(list_of_hashes[sh][2] + '\n' + list_of_hashes[sh][3] + '\n' + list_of_hashes[sh][5])
        else:
            #已到訪
            did.append(list_of_hashes[sh][2] + '\n' + list_of_hashes[sh][3] + '\n' + list_of_hashes[sh][5])

    #print(notYet)
    notYetCount = str(len(notYet))
    # print(notYetCount)
    # print(random.choice(notYet))
    didCount = str(len(did))
    print(didCount)
    print(did)

    return random.choice(notYet)

@app.route('/birthday/<string:date>', methods=['GET'])
def birthday(date):


    scope = ['https://spreadsheets.google.com/feeds', 'https://www.googleapis.com/auth/drive']
    creds = ServiceAccountCredentials.from_json_keyfile_dict(f, scope)
    client = gspread.authorize(creds)

    sheet = client.open("TestList").sheet1
    list_of_hashes = sheet.get_all_values()
    dictionary = dict()

    for sh in range(sheet.row_count):
        #row需要 + 4, 前四row沒資料
        sh = sh + 4
        #print(list_of_hashes[sh])
        if list_of_hashes[sh][1] != '':
            #生日 = list_of_hashes[sh][3]
            #名字 = list_of_hashes[sh][1]
            if list_of_hashes[sh][3] != '':
                #有填生日
                if list_of_hashes[sh][3] in dictionary:
                    names = list()
                    names = dictionary[list_of_hashes[sh][3]]
                    names.append(list_of_hashes[sh][1])
                    dictionary[list_of_hashes[sh][3]] = names
                else:
                    name = list()
                    name.append(list_of_hashes[sh][1])
                    dictionary[list_of_hashes[sh][3]] = name
            else:
                #沒填生日
                if '沒填生日' in dictionary:
                    names = list()
                    names = dictionary['沒填生日']
                    names.append(list_of_hashes[sh][1])
                    dictionary['沒填生日'] = names
                else:
                    name = list()
                    name.append(list_of_hashes[sh][1])
                    dictionary['沒填生日'] = name
        else:
            #名字欄位為空則跳出
            break

    #print(dictionary)
    if date != '沒填生日':
        da = str(date)
        d = da[0] + da[1] + '/' + da[2] + da[3]
        if d in dictionary:
            memberStr = ''
            for m in dictionary[d]:
                memberStr += m + ','
            return memberStr
        else:
            return '沒資料'

    else:

        if date in dictionary:
            memberStr = ''
            for m in dictionary[date]:
                memberStr += m + ','
            return memberStr
        else:
            return '沒資料'

@app.route('/bLady/<string:name>', methods=['GET'])
def bLady(name):

    scope = ['https://spreadsheets.google.com/feeds', 'https://www.googleapis.com/auth/drive']
    creds = ServiceAccountCredentials.from_json_keyfile_dict(f, scope)
    client = gspread.authorize(creds)

    sheet = client.open("100").sheet1
    list_of_hashes = sheet.get_all_values()

    nameDictionary = dict()
    for row in list_of_hashes:
        #名字 全名 手機 認識日 生日 
        #星座 嚐好 喜歡的食 討厭的食 交往過
        # FM FH	FK	FS events
        if row[0] != '名字':
            dictionary = dict()
            for index in range(len(row)):
                
                if index == 1 and row[index] != '':
                    dictionary['全名'] = row[index]
                    
                if index == 2 and row[index] != '':
                    dictionary['手機'] = row[index]     

                if index == 3 and row[index] != '':
                    dictionary['認識日'] = row[index]

                if index == 4 and row[index] != '':
                    dictionary['生日'] = row[index]

                if index == 5 and row[index] != '':
                    dictionary['星座'] = row[index]

                if index == 6 and row[index] != '':
                    dictionary['嚐好'] = row[index]

                if index == 7 and row[index] != '':
                    dictionary['喜歡的食物'] = row[index]

                if index == 8 and row[index] != '':
                    dictionary['討厭的食物'] = row[index]

                if index == 9 and row[index] != '':
                    dictionary['交往過的對象'] = row[index]

                if index == 10 and row[index] != '':
                    dictionary['FM'] = row[index]    

                if index == 11 and row[index] != '':
                    dictionary['FH'] = row[index] 

                if index == 12 and row[index] != '':
                    dictionary['FK'] = row[index]  

                if index == 13 and row[index] != '':
                    dictionary['FS'] = row[index] 

                if index == 14 and row[index] != '':
                    eventCount = len(row)
                    if eventCount > 14:
                        events = list()
                        for x in range(14, eventCount):
                            events.append(row[x])
                            dictionary['events'] = events
                    else:    
                        dictionary['events'] = row[index]

                nameDictionary[row[0]] = dictionary

    nd = nameDictionary[name]

    finalStr = ''
    for k in nd.keys():
        if k == 'events':
            for e in nd[k]:
                #print(e)
                finalStr += e + '\n'
        else:
            #print("{}:{}".format(k,nd[k]))
            finalStr += '{}:{}'.format(k,nd[k]) + '\n'

    return finalStr

# LocationMessage
@handler.add(MessageEvent, message=LocationMessage)
def handle_message(event): 
    locationInfo = '地區:' + event.message.address[:10] + '\n\n'
    locationInfo += '經緯度: ' '(' + str(event.message.longitude)[:8] +' ,'+ str(event.message.latitude)[:8] + ' )'+ '\n\n'
    locationInfo += '向阿寶請示雄三發射許可' + '\n' +'請稍候'
    #line_bot_api.reply_message(event.reply_token,TextSendMessage(text=str(event))) 
    line_bot_api.reply_message(event.reply_token,TextSendMessage(text=locationInfo)) 
    
#@handler.add(MessageEvent, message=ImageMessage)
#def handle_message(event): 
    #image_message = ImageSendMessage(
    #    original_content_url='https://i.imgur.com/uPhBqLK.jpg',
    #    preview_image_url='https://i.imgur.com/uPhBqLK.jpg'
    #)
    #line_bot_api.reply_message(event.reply_token, image_message)
    
    #line_bot_api.reply_message(event.reply_token,TextSendMessage(text=str(event.message)))
    
@handler.add(MessageEvent, message=StickerMessage)
def handle_message(event): 
    sticker_message = StickerSendMessage(
        package_id = event.message.package_id,
        sticker_id = event.message.sticker_id
    )
    line_bot_api.reply_message(event.reply_token, sticker_message)


@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    msg = event.message.text

    #if event.source.group_id is not None:
    #    groupID = event.source.group_id 

    if msg.find('100') != -1:
        string = msg.split('100')[1]
        m = bLady(string)
        line_bot_api.reply_message(event.reply_token,TextSendMessage(text=m))

    if msg == '沒填生日':
        m = birthday(msg)
        line_bot_api.reply_message(event.reply_token,TextSendMessage(text=m))

    if msg.find('生日') != -1:
        string = msg.split('生日')[1]
        m = birthday(string)
        line_bot_api.reply_message(event.reply_token,TextSendMessage(text=m))

    if msg == '重抓':
        global queryAllKeyAndValues
        queryAllKeyAndValues.clear()
        queryAllKeyAndValues = firebase.get('/data',None)

    if msg.find('抽') != -1:
        result = handsome()
        image_message = ImageSendMessage(
            original_content_url=result,
            preview_image_url=result)
        line_bot_api.reply_message(event.reply_token, image_message)
    
    if msg.find('哪喝') != -1:
        w = wine()
        w += '\n\n這家如何呢!?'
        line_bot_api.reply_message(event.reply_token,TextSendMessage(text=w))

    if msg.find('籃球') != -1:
        video_message = VideoSendMessage(
            original_content_url='https://firebasestorage.googleapis.com/v0/b/python-f5763.appspot.com/o/Hollaback%20Girl.mp4?alt=media&token=e46a3d98-6e51-4c18-b903-61ff45f19f2a',
            preview_image_url='https://imgur.com/tCtYGfK.jpg')
        line_bot_api.reply_message(event.reply_token, video_message) 
        
    if msg.find('上車') != -1:
        video_message = VideoSendMessage(
            original_content_url='https://firebasestorage.googleapis.com/v0/b/python-f5763.appspot.com/o/89.mp4?alt=media&token=4a20b5ca-d129-496a-a0b3-1d820204a3c1',
            preview_image_url='https://firebasestorage.googleapis.com/v0/b/python-f5763.appspot.com/o/89.png?alt=media&token=c3238c0d-3207-4d6d-9867-0bfa80381263')
        line_bot_api.reply_message(event.reply_token, video_message)
        
    if msg.find('吃懶') != -1 :
        image_message = ImageSendMessage(
            original_content_url='https://imgur.com/5XILKP5.jpg',
            preview_image_url='https://imgur.com/5XILKP5.jpg')
        line_bot_api.reply_message(event.reply_token, image_message)  
        
    if msg == '好朋友' :
        image_message = ImageSendMessage(
            original_content_url='https://imgur.com/2jB4sV1.jpg',
            preview_image_url='https://imgur.com/2jB4sV1.jpg')
        line_bot_api.reply_message(event.reply_token, image_message)
        
    if msg.find('珍惜') != -1 :
        image_message = ImageSendMessage(
            #https://imgur.com/syKgMMa.jpg
            original_content_url='https://imgur.com/Htn9qxf.jpg',
            preview_image_url='https://imgur.com/Htn9qxf.jpg')
        line_bot_api.reply_message(event.reply_token, image_message)
    
    if msg.find('珍奶') != -1 :
        image_message = ImageSendMessage(
            original_content_url='https://imgur.com/3XBTU2t.jpg',
            preview_image_url='https://imgur.com/3XBTU2t.jpg')
        line_bot_api.reply_message(event.reply_token, image_message)
    
    if msg == '松山':
        rows = hospital()
        string = ''
        for row in rows:
            string += row + '\n\n'
        line_bot_api.reply_message(event.reply_token,TextSendMessage(text=string))
    
    global quiet
    global quietArr
    if msg == '安靜':
        if event.source.group_id in quietArr :
            line_bot_api.reply_message(event.reply_token,TextSendMessage(text='已經安靜哩'))       
        else:    
#             quietArr.append(event.source.group_id)
#             firebase.put('QuietGroup','group_id',quietArr)
#             #寫完讓DB重讀一次
#             time.sleep(2)
#             quiet.clear()
#             quietArr.clear()
#             quiet = firebase.get('/QuietGroup',None)
#             quietArr = quiet['group_id']
#             line_bot_api.reply_message(event.reply_token,TextSendMessage(text='好的 安靜哩'))
            quietArr.append(event.source.group_id)
            firebase.put('QuietGroup','group_id',quietArr)
            line_bot_api.reply_message(event.reply_token,TextSendMessage(text='好的 安靜哩'))
        
    if msg == '講話':
        if event.source.group_id in quietArr :
            quietArr.remove(event.source.group_id)
            firebase.put('QuietGroup','group_id',quietArr)
            #寫完讓DB重讀一次
            time.sleep(2)
            quiet.clear()
            quietArr.clear()
            quiet = firebase.get('/QuietGroup',None)
            quietArr = quiet['group_id']
            line_bot_api.reply_message(event.reply_token,TextSendMessage(text='好 我會好好講話'))

    if msg == '安安':
        menulist = 'Hello 我是安安 你可以 \n' + '\n' + '1. 教我說話 \n' + '安 你好=Hello World! \n1.1 查詢教過的關鍵字 \n查 AA\n1.2 刪除 教過的字 \n遺忘 AA \n\n'
        menulist += '2. 輸入 天氣 台北 \n\n'
        menulist += '3. 輸入 星座 天蠍\n\n'
        menulist += '4. 輸入 電影\n\n'
        menulist += '5. 輸入 股 2330 \n' + '顯示該股票代碼的即時查詢 \n'
        line_bot_api.reply_message(event.reply_token,TextSendMessage(text=menulist))
       
    if msg[0] == '股' and msg[1] == ' ' and len(msg) == 6:
        stockNumber = msg.split()[1]
        result = stock(stockNumber)
        line_bot_api.reply_message(event.reply_token,TextSendMessage(text=result))
        
    #if len(msg) > 200:
    #    line_bot_api.reply_message(event.reply_token,TextSendMessage(text='未看先猜 __文'))
    
    if msg[0] == '安' and msg[1] == ' ':
        msg =  msg.strip('~!@#$%^&*()|"')
        String = msg.split('安 ')[1]
        #print(String)
        key = String.split('=')[0]
        key = key.split()
        #print(key[0])
        #如果第一個字是空白則去除
        value = String.split('=')[1]
        if value[0] == ' ':
            #從第二個字開始算 再裝回去
            value = value[1:]
            if value == '':
                line_bot_api.reply_message(event.reply_token,TextSendMessage(text='不好意思 特殊字元會記不住呢'))
    
        insertFirebase = firebaseInsert(key[0],value)   
        
        insertResult = key[0]+ ' = ' + value + ' 嗎? \n' + insertFirebase + ' !'
        line_bot_api.reply_message(event.reply_token,TextSendMessage(text=insertResult))
        
        #if event.source.user_id != "" :
            #profile = line_bot_api.get_profile(event.source.user_id)
            #n = profile.display_name
            #insertResult = '嗨! ' + n + '說的是: \n' + key[0]+ ' = ' + value + ' 嗎? \n' + insertFirebase + ' !'
            #line_bot_api.reply_message(event.reply_token,TextSendMessage(text=insertResult))
            
        #else:
        #insertResult = key[0]+ ' = ' + value + ' 嗎? \n' + insertFirebase + ' !'
        #line_bot_api.reply_message(event.reply_token,TextSendMessage(text=insertResult))
        
    if msg[0] == '遺' and msg[1] == '忘' and msg[2] ==' ':
        string = msg.split('遺忘 ')[1]
        print(string)
        deleteFirebase = firebaseDelete(string)
        line_bot_api.reply_message(event.reply_token,TextSendMessage(text=deleteFirebase))
        
    if msg[0] == '查' and msg[1] == ' ':
        string = msg.split('查 ')[1]   
        fetchResult = firebaseFetch(string)
        result = '關鍵字 ' + string + ' 結果為: \n' + fetchResult
        line_bot_api.reply_message(event.reply_token,TextSendMessage(text=result))
    
    if msg[0] == '星' and msg[1] == '座' and msg[2] == ' ':
        star = msg.split('星座 ')[1]
        constellationResult = constellation(star)
        line_bot_api.reply_message(event.reply_token,TextSendMessage(text=constellationResult))
        
    if msg[0] == '天' and msg[1] == '氣' and msg[2] == ' ':
        ChooseCity = msg.split('天氣 ')[1]
        weatherResult = weather(ChooseCity)
        line_bot_api.reply_message(event.reply_token,TextSendMessage(text=weatherResult))
        
    if msg == '時間':
        tz = pytz.timezone('Asia/Taipei')
        dd = datetime.datetime.now(tz).date()
        dt = datetime.datetime.now(tz).time()
        queryTime = "{}-{}-{} {}:{}".format(dd.year,dd.month,dd.day,dt.hour,dt.minute)
        line_bot_api.reply_message(event.reply_token,TextSendMessage(text=queryTime))
    
    if msg== 'Id' or msg== 'id':
        #if event.source.type =='group':
        #    line_bot_api.reply_message(event.reply_token,TextSendMessage(text=event.source.group_id))
        #else: 

        profile = line_bot_api.get_profile(event.source.user_id)
        n = profile.display_name
        p = profile.picture_url
        i = profile.user_id
        m = profile.status_message
        line_bot_api.reply_message(event.reply_token,TextSendMessage(text= n))

        if not m:
            z = n + '\n \n' + p + '\n \n' + '\n \n' + event.source.user_id
            line_bot_api.reply_message(event.reply_token,TextSendMessage(text= z))
        else: 
            z = n + '\n \n' + p + '\n \n' + m + '\n \n' + event.source.user_id
            line_bot_api.reply_message(event.reply_token,TextSendMessage(text= z))

    if msg == '電影':
        if event.source.type == 'group' :
            if event.source.group_id == 'C54f882fec4c5b8dc538b6d1cee5fc31f' :
                line_bot_api.reply_message(event.reply_token,TextSendMessage(text=''))
        
        g = get_movies()
        carousel_template_message = TemplateSendMessage(
        alt_text='電影',
        template=CarouselTemplate(
            columns=[
                CarouselColumn(
                    thumbnail_image_url=g[0]['poster_url'],
                    title=g[0]['ch_name'],
                    text= g[0]['intro'],
                    actions=[
                        URITemplateAction(
                            label='查看',
                            uri=g[0]['info_url']
                        )
                    ]
                ),
                CarouselColumn(
                    thumbnail_image_url=g[1]['poster_url'],
                    title=g[1]['ch_name'],
                    text= g[1]['intro'],
                    actions=[
                        URITemplateAction(
                            label='查看',
                            uri=g[1]['info_url']
                        )
                    ]
                ),
                CarouselColumn(
                    thumbnail_image_url=g[2]['poster_url'],
                    title=g[2]['ch_name'],
                    text= g[2]['intro'],
                    actions=[
                        URITemplateAction(
                            label='查看',
                            uri=g[2]['info_url']
                        )
                    ]
                ),
                CarouselColumn(
                    thumbnail_image_url=g[3]['poster_url'],
                    title=g[3]['ch_name'],
                    text= g[3]['intro'],
                    actions=[
                        URITemplateAction(
                            label='查看',
                            uri=g[3]['info_url']
                        )
                    ]
                ),
                CarouselColumn(
                    thumbnail_image_url=g[4]['poster_url'],
                    title=g[4]['ch_name'],
                    text= g[4]['intro'],
                    actions=[
                        URITemplateAction(
                            label='查看',
                            uri=g[4]['info_url']
                        )
                    ]
                 )
              ]
           )
        )
        line_bot_api.reply_message(event.reply_token, carousel_template_message)
    
    
    if msg == '小電影' or msg == 'AV':
        if event.source.type == 'group' and event.source.group_id == 'C54f882fec4c5b8dc538b6d1cee5fc31f':
            line_bot_api.reply_message(event.reply_token,TextSendMessage(text=''))
        elif event.source.user_id == 'U2e046844ad61d32e4e091b2db7dbc53f':
            line_bot_api.reply_message(event.reply_token,TextSendMessage(text='GG WP'))
            
        avgleResult = darkAnan()
        #asd = avgleResult[4]['title'][:10] + '\n' + avgleResult[4]['preview_url'] +'\n'+ avgleResult[4]['keyword'][:10] +'\n'+ avgleResult[4]['video_url']
        #line_bot_api.reply_message(event.reply_token,TextSendMessage(text=asd))
        carousel_template_message = TemplateSendMessage(
        alt_text='小電影',
        template=CarouselTemplate(
            columns=[
                CarouselColumn(
                    thumbnail_image_url=avgleResult[0]['preview_url'],
                    title=avgleResult[0]['keyword'][:10],
                    text= avgleResult[0]['title'][:10],
                    actions=[
                        URITemplateAction(
                            label='查看',
                            uri=avgleResult[0]['video_url']
                        )
                    ]
                ),
                CarouselColumn(
                    thumbnail_image_url=avgleResult[1]['preview_url'],
                    title=avgleResult[1]['keyword'][:10],
                    text= avgleResult[1]['title'][:10],
                    actions=[
                        URITemplateAction(
                            label='查看',
                            uri=avgleResult[1]['video_url']
                        )
                    ]
                ),
                CarouselColumn(
                    thumbnail_image_url=avgleResult[2]['preview_url'],
                    title=avgleResult[2]['keyword'][:10],
                    text= avgleResult[2]['title'][:10],
                    actions=[
                        URITemplateAction(
                            label='查看',
                            uri=avgleResult[2]['video_url']
                        )
                    ]
                ),
                CarouselColumn(
                    thumbnail_image_url=avgleResult[3]['preview_url'],
                    title=avgleResult[3]['keyword'][:10],
                    text= avgleResult[3]['title'][:10],
                    actions=[
                        URITemplateAction(
                            label='查看',
                            uri=avgleResult[3]['video_url']
                        )
                    ]
                ),
                CarouselColumn(
                    thumbnail_image_url=avgleResult[4]['preview_url'],
                    title=avgleResult[4]['keyword'][:10],
                    text= avgleResult[4]['title'][:10],
                    actions=[
                        URITemplateAction(
                            label='查看',
                            uri=avgleResult[4]['video_url']
                        )
                    ]
                )
              ]
           )
        )
        line_bot_api.reply_message(event.reply_token, carousel_template_message)         
    
    
    if msg[0] == 'A' and msg[1] == 'V' and msg[2] == ' ' :
        if event.source.type == 'group' and event.source.group_id == 'C54f882fec4c5b8dc538b6d1cee5fc31f':
            line_bot_api.reply_message(event.reply_token,TextSendMessage(text=''))
        elif event.source.user_id == 'U2e046844ad61d32e4e091b2db7dbc53f':
            line_bot_api.reply_message(event.reply_token,TextSendMessage(text='GG WP'))
        # event.source.group_id == 'C54f882fec4c5b8dc538b6d1cee5fc31f'
        
        name = msg.split('AV ')[1]
        avgleResult = darkAnanQuery(name)
        #asd = avgleResult[4]['title'][:10] + '\n' + avgleResult[4]['preview_url'] +'\n'+ avgleResult[4]['keyword'][:10] +'\n'+ avgleResult[4]['video_url']
        #line_bot_api.reply_message(event.reply_token,TextSendMessage(text=asd))
        carousel_template_message = TemplateSendMessage(
        alt_text=msg,
        template=CarouselTemplate(
            columns=[
                CarouselColumn(
                    thumbnail_image_url=avgleResult[0]['preview_url'],
                    title=avgleResult[0]['keyword'][:10],
                    text= avgleResult[0]['title'][:10],
                    actions=[URITemplateAction(label='查看',uri=avgleResult[0]['video_url'])]
                ),
                CarouselColumn(
                    thumbnail_image_url=avgleResult[1]['preview_url'],
                    title=avgleResult[1]['keyword'][:10],
                    text= avgleResult[1]['title'][:10],
                    actions=[URITemplateAction(label='查看',uri=avgleResult[1]['video_url'])]
                ),
                CarouselColumn(
                    thumbnail_image_url=avgleResult[2]['preview_url'],
                    title=avgleResult[2]['keyword'][:10],
                    text= avgleResult[2]['title'][:10],
                    actions=[URITemplateAction(label='查看',uri=avgleResult[2]['video_url'])]
                ),
                CarouselColumn(
                    thumbnail_image_url=avgleResult[3]['preview_url'],
                    title=avgleResult[3]['keyword'][:10],
                    text= avgleResult[3]['title'][:10],
                    actions=[URITemplateAction(label='查看',uri=avgleResult[3]['video_url'])]
                ),
                CarouselColumn(
                    thumbnail_image_url=avgleResult[4]['preview_url'],
                    title=avgleResult[4]['keyword'][:10],
                    text= avgleResult[4]['title'][:10],
                    actions=[URITemplateAction(label='查看',uri=avgleResult[4]['video_url'])]
                )
              ]
           )
        )
        line_bot_api.reply_message(event.reply_token, carousel_template_message)
            
    if msg == 'Aime' or msg == 'aime' or msg == 'AlittleSheep' or msg == '小綿羊':
        albumResult = aime(msg)
        #album = albumResult[4]['imageLink'] + '\n' + albumResult[4]['title&price'] +'\n' + albumResult[4]['shopeeLink']
        #line_bot_api.reply_message(event.reply_token,TextSendMessage(text=album))
        carousel_template_message = TemplateSendMessage(
        alt_text=msg,
        template=CarouselTemplate(
            columns=[
                CarouselColumn(
                    thumbnail_image_url=albumResult[0]['imageLink'],
                    title=albumResult[0]['title&price'],
                    text= ' ',
                    actions=[
                        URITemplateAction(
                            label='查看',
                            uri=albumResult[0]['shopeeLink']
                        )
                    ]
                ),
                CarouselColumn(
                    thumbnail_image_url=albumResult[1]['imageLink'],
                    title=albumResult[1]['title&price'],
                    text= ' ',
                    actions=[
                        URITemplateAction(
                            label='查看',
                            uri=albumResult[1]['shopeeLink']
                        )
                    ]
                ),
                CarouselColumn(
                    thumbnail_image_url=albumResult[2]['imageLink'],
                    title=albumResult[2]['title&price'],
                    text= ' ',
                    actions=[
                        URITemplateAction(
                            label='查看',
                            uri=albumResult[2]['shopeeLink']
                        )
                    ]
                ),
                CarouselColumn(
                    thumbnail_image_url=albumResult[3]['imageLink'],
                    title=albumResult[3]['title&price'],
                    text= ' ',
                    actions=[
                        URITemplateAction(
                            label='查看',
                            uri=albumResult[3]['shopeeLink']
                        )
                    ]
                ),
                CarouselColumn(
                    thumbnail_image_url=albumResult[4]['imageLink'],
                    title=albumResult[4]['title&price'],
                    text= ' ',
                    actions=[
                        URITemplateAction(
                            label='查看',
                            uri=albumResult[4]['shopeeLink']
                        )
                    ]
                )
              ]
           )
        )
        line_bot_api.reply_message(event.reply_token, carousel_template_message)
        
    #firebaseChatLog(msg)
    #profile = line_bot_api.get_profile(event.source.user_id)
    if event.source.type =='user' :
        #直接對機器人講
        z = '單獨(user_id):' + event.source.user_id
        #firebaseChatLog(msg,profile.display_name,z)   
        firebaseChatLog(msg,'',z)
        
    elif event.source.type == 'group':
        #群組裡講
        z = '群組(group_id):' + event.source.group_id
        #firebaseChatLog(msg,profile.display_name,z)
        firebaseChatLog(msg,'',z)    
            
    if sticker(msg) != 'GG':
        if event.source.type !='group':
            sticker_message = StickerSendMessage(
            package_id = sticker(msg)['package_id'],
            sticker_id = sticker(msg)['sticker_id']
            )
            line_bot_api.reply_message(event.reply_token, sticker_message)
        
        elif not event.source.group_id in quietArr :
            sticker_message = StickerSendMessage(
            package_id = sticker(msg)['package_id'],
            sticker_id = sticker(msg)['sticker_id']
            )
            line_bot_api.reply_message(event.reply_token, sticker_message)
            
    dbResult = firebaseQuery(msg)
    if dbResult != 'GG':
        #line_bot_api.reply_message(event.reply_token,TextSendMessage(text=dbResult))
        
        #r = random.random()
        #if r > 0.05 :
        #    line_bot_api.reply_message(event.reply_token,TextSendMessage(text=dbResult))
        #else:
        #    line_bot_api.reply_message(event.reply_token,TextSendMessage(text='如果我之前回過幹話 不要生氣 去怪紹安')) 
        
        global sendTime
        sendTimeStr = str(sendTime).split('.')[0]
        s = int(sendTimeStr)
        
        now = str(time.time()).split('.')[0]
        n = int(now)

        if event.source.type != 'group':
            line_bot_api.reply_message(event.reply_token,TextSendMessage(text=dbResult))
        
        if not event.source.group_id in quietArr and (n - s) > 10:
            sendTime = time.time()
            line_bot_api.reply_message(event.reply_token,TextSendMessage(text=dbResult))

if __name__ == "__main__":
    app.run()
