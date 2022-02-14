from html2image import Html2Image
import memewizard
import statistics
import requests
import reqtest
import random
import json
import os

if not os.path.exists('bin/'):
    os.mkdir('bin')

def rgb_to_hex(rgb):
    return '#%02x%02x%02x' % rgb
def colors(amount):
    return [rgb_to_hex((random.randrange(100,255),random.randrange(100,255),random.randrange(100,255))) for _ in range(amount)]

def pies_() -> 'dict[list]':
    memes = memewizard.meme_object_yt.fetch_memes()
    resp = []
    for meme in memes:
        try:
            if not any(ele in meme.strip() for ele in memewizard.funnywords):
                resp.append([{meme.strip(): round(statistics.mean(s))} for s in list(memewizard.chunkify(reqtest.fetch_trend_history([meme])[0], 3))])
        except IndexError:
            pass
    return resp

def pies() -> 'list[dict]':
    p = pies_()
    resp = []
    for i in range(len(p)):
        timeframe = {}
        for l in p:
            try:
                timeframe[list(l[i].keys())[0]] = list(l[i].values())[0]
            except IndexError:
                pass
        resp.append(timeframe)
    return resp

data = pies()
DOC = requests.get('https://raw.githubusercontent.com/ajskateboarder/stuff/main/meme.js/trackpie.html').text
COLOR = str(colors(len(data))).replace('[','').replace(']','')

os.chdir('bin')
for i,datum in enumerate(data):
    resp = json.dumps(datum).replace('{','').replace('}','')
    open(f'chart{i}.html', 'w').write(DOC.replace('/*data*/', resp).replace('/*colors*/', COLOR))
    Html2Image(output_path='images',custom_flags=['--virtual-time-budget=5000', '--default-background-color=0']).screenshot(html_file=f'chart{i}.html', save_as=f'chart{i}.png', size=(600,600))
