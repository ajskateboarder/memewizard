import requests
from bs4 import BeautifulSoup

# dumb submission statement to remove
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
    return Exception('')
  while '' in st:
    st.remove('')
  st = [_st.replace(':', '').replace('\n', '') for _st in st]
  st = list(chunkify(st, 2))

  if SENTENCE in st:
    st.remove(SENTENCE)
  return {title: st}
