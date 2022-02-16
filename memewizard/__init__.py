from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from pytrends.request import TrendReq as UTrendReq
import matplotlib.pyplot as plt
from bs4 import BeautifulSoup
import pandas as pd
import numpy as np
import statistics
import requests
import warnings
import random
import json
import re

headers = {
    'authority': 'trends.google.com',
    'cache-control': 'max-age=0',
    'sec-ch-ua': '" Not A;Brand";v="99", "Chromium";v="96", "Google Chrome";v="96"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"Linux"',
    'upgrade-insecure-requests': '1',
    'user-agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.110 Safari/537.36',
    'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
    'x-client-data': 'CIy2yQEIprbJAQipncoBCNT5ygEI6/LLAQif+csBCOaEzAEIy4nMAQjTj8wBCJmQzAEInZHMAQ==',
    'sec-fetch-site': 'same-origin',
    'sec-fetch-mode': 'navigate',
    'sec-fetch-user': '?1',
    'sec-fetch-dest': 'document',
    'referer': 'https://trends.google.com/trends/?geo=US',
    'accept-language': 'en-US,en;q=0.9',
    'cookie': '__utma=10102256.749338736.1643927518.1644687090.1644761529.3; __utmc=10102256; __utmz=10102256.1644761529.3.2.utmcsr=google|utmccn=(organic)|utmcmd=organic|utmctr=(not%20provided); __utmt=1; __utmb=10102256.11.9.1644761625921; SID=GgjPdMu4L6IlFUCmmEQAxAUloL1sGDpBRyMP7XpaKWTnOwRne3I0mcdVPBn3l72evi6nCQ.; __Secure-1PSID=GgjPdMu4L6IlFUCmmEQAxAUloL1sGDpBRyMP7XpaKWTnOwRn3ew1xWC7wWRAeQ4G7X7aqg.; __Secure-3PSID=GgjPdMu4L6IlFUCmmEQAxAUloL1sGDpBRyMP7XpaKWTnOwRnjh72t40P-VPU7i1z6SCGtg.; HSID=A2t8uymoosCaCpneP; SSID=ASwoNBdOnMshI8AUd; APISID=A1sSy7xe2cwo4ZSb/AL7GLTTK2EpBbgRzT; SAPISID=p-Ehz1pFU7EJn5WB/AH-auG1NNxg6ITYjQ; __Secure-1PAPISID=p-Ehz1pFU7EJn5WB/AH-auG1NNxg6ITYjQ; __Secure-3PAPISID=p-Ehz1pFU7EJn5WB/AH-auG1NNxg6ITYjQ; SEARCH_SAMESITE=CgQIzpQB; OGPC=19022519-1:; 1P_JAR=2022-02-13-14; NID=511=CKJn1vvn6aE1OKvMLG6WlLir23qfmHo5j4zkdjW5Hiu88UyLKFSM-V4FnMC6uzyfnabNLJQbzD57qDvGBmaGT1w1w3VHaHW3NW8OKbCv8esnw1RUnWjQAPbHJrBJkzmw2Y0L632c_xW5CdTvDx6x-mNUBxi0gc4DdDpfZsEEUo_pbZuIzQvHOg14DF3MBnbLnuhGstZtigPsUBd29q6yMMHEeKUugktSkkaeKJAOLTod1hCR5YrVy1qVEmxGhevfQvOkPBYo7PxleoE; SIDCC=AJi4QfFkAXjP9hIIsEtGtr5Oue2mE4MjQaSseyvkbSMymsI_iWzgK237Qoso50dk8uU_ww4VSg; __Secure-3PSIDCC=AJi4QfGajfVnAMdn_0-7y02j-5Lk4Nk7XXpf5d1LHWnIGXtQ9Hj4Qe52VF5Fo3o-tt4wEXo4Bw',
}


class TrendReq(UTrendReq):
    def _get_data(self, url, method='get', trim_chars=0, **kwargs):
        return super()._get_data(url, method='get', trim_chars=trim_chars, headers=headers, **kwargs)

warnings.filterwarnings('ignore')
stopwords = ['Why Is', 'Why Does', 'Everyone', 'EVERYONE', 'Why', 'Is The', 'How', 'What Are', 'What\'s Up', 'With', '?', '.', 'Are You', 'FINISHED']
trails = ("classic", "everywhere")
funnywords = ['d*ck','Rule 34','Sex']
regex = re.compile('|'.join(map(re.escape, stopwords)))

def subjectify(text):
    _list = re.split(r'{}'.format('|'.join(trails)), ''.join(text), flags=re.IGNORECASE)
    return ''.join(_list)

class meme_object:
    def fetch_memes(page: str) -> list:
        '''
        Scrape any memes page on knowyourmemes.com
        '''

        r = requests.get(
            'https://knowyourmeme.com/memes/page/{}'
            .format(page),
            headers={'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.101 Safari/537.36'}
        ).text
        soup = BeautifulSoup(r, 'html.parser')

        # parsing perfection
        m = soup.find('tbody', {'class':['entry-grid-body', 'infinite']}).text.split('    ')

        for i, s in enumerate(m):
            m[i] = s.strip()
            if m[i] == '': del m[i]
        for i, s in enumerate(m): m[i] = s.strip()
        for i, s in enumerate(m):
            if 'NSFW' in m[i] or m[i] == 'NSFW':
                del m[i+1]
                del m[i]
        while '' in m:
            m.remove('')
        for i, s in enumerate(m):
            if 'Updated' in m[i]: del m[i]

        return m
    def fetch_meme_images(meme_list: list) -> list:
        '''
        Find relevant images for a list of memes
        '''

        meme_images = []
        for meme in meme_list:
            r = requests.get(
                'https://www.google.com/search?q={}&rlz=1CAOUAQ_enUS980&source=lnms&tbm=isch&biw=1517&bih=750&dpr=0.9&surl=1&safe=active&ssui=on#imgrc=1QhXmjkgq_MRQM'
                .format(meme)
            ).text
            soup = BeautifulSoup(r, 'html.parser')

            images = soup.find_all('img')
            meme_images.append(images[random.randrange(1, len(images))]['src'])

        return meme_images
    def fetch_trend_history(memes: list) -> list:
        '''
        Find trend history of image
        '''

        trend = TrendReq()
        trend.build_payload(memes, timeframe='today 1-m', cat='0', geo='US')

        search = trend.interest_over_time()
        trend.build_payload(memes, timeframe='today 5-y', cat='0', geo='US')

        youtube = trend.interest_over_time()

        df = pd.DataFrame(search)
        dF = pd.DataFrame(youtube)

        df.reset_index(inplace=True, drop=True)
        df = df.to_dict()
        dF.reset_index(inplace=True, drop=True)
        dF = dF.to_dict()

        meme = []
        for k in df:
            submeme = []
            v = df[k]
            for e in v:
                if not isinstance(v[e], (bool, str)):
                    submeme.append(v[e])
            meme.append(submeme)
        while [] in meme:
            meme.remove([])
        meme2 = []
        for k in df:
            submeme = []
            v = df[k]
            for e in v:
                if not isinstance(v[e], (bool, str)):
                    submeme.append(v[e])
            meme2.append(submeme)
        while [] in meme:
            meme2.remove([])

        return meme, meme2

class meme_object_yt:
    def fetch_memes() -> list:
        '''Fetches memes from LessonsInMemeCulture on YouTube and does a ton of parsing magic.'''
        r = requests.get('https://www.youtube.com/c/LessonsinMemeCulture/videos')
        big_response = json.loads(r.text.split('var ytInitialData =')[1].split(';</script>')[0])
        filtere = big_response['contents']['twoColumnBrowseResultsRenderer']['tabs'][1]['tabRenderer']['content']['sectionListRenderer']['contents'][0]['itemSectionRenderer']['contents'][0]['gridRenderer']['items']
        res = []
        for i in range(len(filtere)):
            try:
                string = filtere[i]['gridVideoRenderer']['title']['runs'][0]['text'].replace('“', '"').replace('”', '"')
                token = regex.sub('', string)
                words = re.findall('"([^"]*)"', string)
                if len(words) > 0:
                    meme = ''.join([s.split('_')[0] for s in words[0]])
                    res.append(meme)
                else:
                    res.append(subjectify(token))
            except KeyError:
                break

        return res

    def fetch_meme_dates() -> list:
        '''Fetch "meme" dates from LessonsInMemeCulture'''

        r = requests.get('https://www.youtube.com/c/LessonsinMemeCulture/videos')
        big_response = json.loads(r.text.split('var ytInitialData =')[1].split(';</script>')[0])
        filtere = big_response['contents']['twoColumnBrowseResultsRenderer']['tabs'][1]['tabRenderer']['content']['sectionListRenderer']['contents'][0]['itemSectionRenderer']['contents'][0]['gridRenderer']['items']

        dates = []

        for i in range(len(filtere)):
            try:
                if not '*' in str(filtere[i]['gridVideoRenderer']['title']['runs'][0]['text']):
                    dates.append(filtere[i]['gridVideoRenderer']['publishedTimeText']['simpleText'])
            except KeyError:
                break
        return dates

class invalids:
  RESEARCH = ['This submission is currently being researched and evaluated.',
              'You can help confirm this entry by contributing facts, media, and other evidence of notability and mutation.']
  NOTFOUND = 'Page Not Found (404) - Know Your Meme'
  GALLERY = 'Trending Videos Gallery'

def chunkify(l, n):
    for i in range(0, len(l), n):
        yield l[i:i + n]

def fetchd(url):
  r = requests.get(url,
  headers={'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.101 Safari/537.36'})
  s = BeautifulSoup(r.text, 'html.parser')
  title = s.find('title').text.split(' |')[0]

  try:
    st = s.find('div', {'class': ['details']}).text.split('\n\n')
  except AttributeError:
    st = ['']
  while '' in st:
    st.remove('')
  st = [_st.replace(':', '').replace('\n', '') for _st in st]
  st = list(chunkify(st, 2))
  st.insert(0, ['Name', title])

  if invalids.RESEARCH in st:
    st.remove(invalids.RESEARCH)
  return {title: st}

def predict(meme):
  memes = meme_object.fetch_trend_history([meme])[0][0]
  data = [[i, m] for i,m in enumerate(memes)]

  y_data = np.array(data)[:,1]

  X = np.array(range(len(y_data))).reshape(-1,1)

  X_train,X_test,y_train,y_test=train_test_split(X,y_data,test_size=0.25,random_state=0)

  logreg = LogisticRegression(solver='lbfgs', max_iter=1000)
  logreg.fit(X_train,y_train)
  y_pred=logreg.predict(X_test)

  y = [*y_train, *y_test, *y_pred]

  plt.plot(range(len(y)),y,c='black')
  plt.axvline(len(y)-len(y_pred), c='blue', alpha=0.2)
  plt.title('History for \'{}\''.format(meme))

  plt.savefig('figure.png')

def makepie(page):
    print('please wait')
    obj = meme_object_yt

    trends = {}
    for sn in obj.fetch_memes():
        s, v = obj.fetch_trend_history([sn])
        try:
            trends[sn]=statistics.mean(s[0])
        except IndexError:
            pass
    return trends
