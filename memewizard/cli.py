#!/usr/bin/env python3

'''The command line functions'''

from memewizard.helpers import *
from memewizard.visual import *
import memewizard

from bs4 import BeautifulSoup
from tabulate import tabulate

import PyInquirer
import webbrowser
import traceback
import tqdm

def predict_meme() -> None:
  '''Nearly deprecated CLI interface for directing fetching KnowYourMeme data'''

  r = requests.get('https://knowyourmeme.com/memes/',
  headers={'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.101 Safari/537.36'})
  s = BeautifulSoup(r.text, 'html.parser')

  try:
    m = s.find('tbody', {'class':['entry-grid-body', 'infinite']}).text.split('    ')

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
  except AttributeError:
    print(color.RED+'Uh oh! This script failed! You may be banned from knowyourmemes.com.'+color.END)
    open('error.log','w').write(r.text)
    exit(0)
  m = list(set(m))
  l = ['/memes/'+e.lower().replace(' ', '-') for e in m]
  x = input(color.BOLD+color.BLUE+'Enter a meme (Enter ? for memes) > '+color.END)

  if x == '?':
    print('▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬\n'+'\n'.join([color.BOLD+h.strip()+color.END for h in m]), '\n▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬')
    predict_meme()

  y = int(input(color.BOLD+color.YELLOW+'How many memes should I fetch? (current amount to fetch is {}) '.format(len(m))+color.END))

  memes = []
  for en in tqdm(l[:y]):
      memes.append(memewizard.meme_object.fetch_meme_info('https://knowyourmeme.com/memes'+en))
  print(memes)

  keys = [list(d.keys())[0] for d in memes[:10]]
  resp = {}

  for t in keys:
      ratio = difflib.token_set_ratio(x, t)
      resp[str(ratio)] = t

  val = resp[str(max([int(k) for k in resp.keys()]))]
  json = next(item for item in memes if list(item.keys())[0] == val)

  print(color.BOLD+color.GREEN+val+'\n'+color.END+tabulate(json[val]))
  show = input(color.BOLD+color.BLUE+'Would you like to view the trend history for this meme ({}) [Y/n] ? '.format(val)+color.END)

  if show == 'n' or show == 'N':
    exit(0)
  else:
    print(color.BOLD+'Saving trend history to "figure.png"...'+color.END)
    memewizard.predict(val)
    exit(0)

def main() -> None:
  '''The cool CLI function that you definitely use'''

  print( '\x1b[32m\x1b[1m',
  '''
  . * .
     .  *                                 _                  _
   . *. * .                              (_)                | |
   _ __ ___   ___ _ __ ___   _____      ___ ______ _ _ __ __| |
  | '_ ` _ \ / _ \ '_ ` _ \ / _ \ \ /\ / / |_  / _` | '__/ _` |
  | | | | | |  __/ | | | | |  __/\ V  V /| |/ / (_| | | | (_| |
  |_| |_| |_|\___|_| |_| |_|\___| \_/\_/ |_/___\__,_|_|  \__,_|
  ▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬
  version 0.0.4
  ''',
  '\x1b[0m' )
  prompt = PyInquirer.prompt([
    {
        'type':'list',
        'name':'choice',
        'message':'What do you want to do?',
        'choices':[
            'Create a meme popularity pie chart',
            'Fetch information for a single meme',
            'Exit'
        ]
    }
  ])

  if prompt['choice'] == 'Create a meme popularity pie chart':
    prompt = PyInquirer.prompt([
      {
          'type':'list',
          'name':'choice',
          'message':'What kind of pie do you want to make?',
          'choices':[
              'Make a single pie for current information',
              'Make multiple pies going back 30 days',
          ]
      }
    ])
    if prompt['choice'] == 'Make a single pie for current information':
      make_pie()
      exit(0)
    else:
      make_trackback_pie(serve=True)
  elif prompt['choice'] == 'Fetch information for a single meme':
    prompt_ = PyInquirer.prompt([
      {
          'type':'list',
          'name':'choice',
          'message':'Where do you want to fetch memes?',
          'choices':[
              'KnowYourMeme',
              'YouTube (recommended)'
          ]
      }
    ])

    if prompt_['choice'] == 'YouTube (recommended)':
      memesyt, historyyt = memewizard.meme_object_yt.fetch_memes(), memewizard.meme_object_yt.fetch_meme_dates()
      memesyt = [meme.strip() for meme in memesyt if not memewizard.nsfw_regex.search(meme)]

      print('▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬\n'+'\n'.join(['{}. {}{}{}  {}{}{}'.format(i, color.BOLD,a,color.END,color.GREY,b,color.END) for i, (a,b) in enumerate(zip(memesyt, historyyt))])+'\n▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬')
      while True:
        x = input(color.BOLD+color.BLUE+'Select a meme by its number (add ? after number for meme images) > '+color.END)
        try:
          if x.endswith('?') and x.count('?') == 1:
            try:
              x = int(x.replace('?', ''))
              webbrowser.open('https://duckduckgo.com/?q={}'.format(memesyt[x]))
            except ValueError:
              print(color.RED+'Not a number. Please use a real number that is in range.'+color.END)
          else:
              doc = requests.get('https://www.google.com/search?q={}&surl=1&safe=active&ssui=on'.format(str(memesyt[int(x)]+' know your meme').replace(' ', '+')))
              soup = BeautifulSoup(doc.text, 'html.parser')

              search = [link['href'] for link in soup.find_all('a', href=True) if 'knowyourmeme.com' in link['href'] and link['href'].find('cultures') == -1][0]

              data = memewizard.meme_object.fetch_meme_info(search.split('url?q=')[1].split('&sa')[0].replace('25',''))
              key = list(data.keys())[0]
              if memewizard.invalids.NOTFOUND in key or memewizard.invalids.GALLERY in key:
                print(color.RED+'What!? That meme does not exist in the KnowYourMeme database.'+color.END)
              else:
                if len(data[key]) < 5:
                  print(color.YELLOW+'It looks like there is limited data for this meme. You may encounter errors.'+color.END)
                print(color.BOLD+'Most related meme'+color.END+'\n'+tabulate(data[key]))
                y = input(color.BOLD+color.BLUE+'Would you like to view the Google Search trend history for this meme ({}) [Y/n] ? '.format(key)+color.END)
                if y == 'n' or y == 'N':
                  pass
                else:
                  try:
                    print(color.BOLD+'Saving trend history to "figure.png"...'+color.END,end='',flush=True)
                    predict(key)
                    print('\r'+color.BOLD+'Saving trend history to "figure.png"...'+color.END+' Finished\n',end='',flush=True)
                  except Exception as e:
                    print('\n'+color.BOLD+color.RED+'An error has occurred. The stack trace has been logged for further details.\n\n'+traceback.format_exc()+color.END)
                  exit(0)
        except ValueError:
          print(color.RED+'Not a number. Please use a real number that is in range.'+color.END)
    elif prompt_['choice'] == 'KnowYourMeme':
      predict_meme()
  else:
    exit(0)
