import datetime

from flask import Flask
from flask import url_for, render_template, request, redirect
from collections import defaultdict

import operator
from collections import defaultdict
from flask import Flask
from flask import url_for, render_template, request, redirect
from pymystem3 import Mystem

m = Mystem()
app = Flask(__name__)


def add_POS(text):
    trans_dict = defaultdict(int)
    vid_dict = defaultdict(int)
    freq_lemmas = defaultdict(int)
    ana = m.analyze(text)
    verbs = 0
    for i in ana:
        if i['text'].strip() and 'analysis' in i and i['analysis']:
            if 'V,' in i['analysis'][0]['gr']:
                verbs+=1
                lemma = i['analysis'][0]['lex']
                freq_lemmas[lemma] += 1
                if 'несов' in i['analysis'][0]['gr']:
                    vid_dict['несовершенный'] += 1
                elif 'сов' in i['analysis'][0]['gr']:
                    vid_dict['совершенный'] += 1
                if 'пе' in i['analysis'][0]['gr']:
                    trans_dict['переходный'] += 1
                elif 'не' in i['analysis'][0]['gr']:
                    trans_dict['непереходный'] += 1

    return vid_dict, trans_dict, verbs, freq_lemmas

@app.route('/', methods=['get', 'post'])
def index():
    if request.form:
        text = request.form['text']
        result = add_POS(text)
        return render_template('index.html', input=text, text=result, dict_vid = result[0], dict_trans = result[1], verbs=result[2], freqs =
                            sorted(result[3].items(),key=operator.itemgetter(1), reverse = True))
    return render_template('index.html')


if __name__ == '__main__':
    app.run(debug=True)