import datetime

from flask import Flask
from flask import url_for, render_template, request, redirect
from collections import defaultdict

import operator
from collections import defaultdict
from flask import Flask
from flask import url_for, render_template, request, redirect
from pymystem3 import Mystem
from vk_groups import get_groups
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

@app.route('/pos', methods=['get', 'post'])
def pos():
    if request.form:
        text = request.form['text']
        result = add_POS(text)
        return render_template('pos.html', input=text, text=result, dict_vid = result[0], dict_trans = result[1],
                               verbs=result[2], freqs =
                            sorted(result[3].items(),key=operator.itemgetter(1), reverse = True))
    return render_template('pos.html')

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/groups', methods=['get', 'post'])
def groups():
    if request.form:
        id1 = request.form['id1']
        id2 = request.form['id2']
        count1, count2, intersect, closed_1, closed_2, error_1, error_2 = get_groups(id1, id2)
        return render_template('groups.html', count1=count1, count2=count2,
                               intersect=', '.join([str(x) for x in intersect]), id1=id1, id2=id2,
                               after_post=True, closed_1=closed_1, closed_2=closed_2, error_1=error_1, error_2=error_2)
    return render_template('groups.html')

if __name__ == '__main__':
    app.run(debug=True)