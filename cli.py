import requests
from bs4 import BeautifulSoup
from library import fetchd
from thefuzz import fuzz as difflib
from tabulate import tabulate
from tqdm import tqdm

r = requests.get('https://knowyourmeme.com/memes/',
headers={'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.101 Safari/537.36'})
s = BeautifulSoup(r.text, 'html.parser')

class color:
   PURPLE = '\033[95m'
   CYAN = '\033[96m'
   DARKCYAN = '\033[36m'
   BLUE = '\033[94m'
   GREEN = '\033[92m'
   YELLOW = '\033[93m'
   RED = '\033[91m'
   BOLD = '\033[1m'
   UNDERLINE = '\033[4m'
   END = '\033[0m'

while True:
  try:
    m = [a['href'] for a in s.find('tbody').find_all('a', href=True) if a['href'].startswith('/memes/')]
  except AttributeError:
    input(color.RED+'Uh oh! This script failed! You may be banned from knowyourmemes.com. Press any key to print out the document and exit... '+color.END)
    print(r.text)
    exit(0)
  m = list(set(m))
  x = input(color.BOLD+color.BLUE+'Enter a meme (Enter ? for meme links) > '+color.END)

  if x == '?':
    print('\n'.join(m))
    continue

  y = int(input(color.BOLD+color.YELLOW+'How many memes should I fetch? (current amount to fetch is {}) '.format(len(m))+color.END))

  memes = []
  for en in tqdm(m[:y]):
      memes.append(fetchd(en))
  keys = [list(d.keys())[0] for d in memes[:10]]
  resp = {}

  for t in keys:
      ratio = difflib.token_set_ratio(x, t)
      resp[str(ratio)] = t

  val = resp[str(max([int(k) for k in resp.keys()]))]
  json = next(item for item in memes if list(item.keys())[0] == val)

  print(color.BOLD+color.GREEN+val+'\n'+color.END+tabulate(json[val]))
