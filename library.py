from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
import matplotlib.pyplot as plt
from bs4 import BeautifulSoup
import pytrends.request
import pandas as pd
import numpy as np
import requests
import warnings
import random

warnings.filterwarnings('ignore')

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
        memes = soup.find('tbody', {'class':['entry-grid-body', 'infinite']}).text.split('    ')
        print(memes)

        for i, s in enumerate(memes):
            memes[i] = s.strip()
            if memes[i] == '': del memes[i]
        for i, s in enumerate(memes): memes[i] = s.strip()
        for i, s in enumerate(memes):
            if memes[i] == 'NSFW':
                del memes[i+1]
                del memes[i]
        for i, s in enumerate(memes):
            if memes[i] == '': del memes[i]

        return memes
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

        trend = pytrends.request.TrendReq()
        trend.build_payload(memes, timeframe='today 5-y', cat='0', geo='US')

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

SENTENCE = ['This submission is currently being researched and evaluated.',
            'You can help confirm this entry by contributing facts, media, and other evidence of notability and mutation.']

def chunkify(l, n):
    for i in range(0, len(l), n):
        yield l[i:i + n]

def fetchd(endp):
  r = requests.get('https://knowyourmeme.com{}'.format(endp),
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

  if SENTENCE in st:
    st.remove(SENTENCE)
  return {title: st}

def predict(meme):
  obje = meme_object
  memes = obje.fetch_trend_history([meme])[0][0]
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
