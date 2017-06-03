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
from ocr import printed_text, find_dict, find_list, handwritten_text
from chat import get_answer

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
                               verbs=result[2],
                               freqs=sorted(result[3].items(),key=operator.itemgetter(1), reverse = True),
                               data=result[3])
    return render_template('pos.html', data=defaultdict(int))

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
                               data={id1: count1, id2: count2},
                               intersect=', '.join([str(x) for x in intersect]), id1=id1, id2=id2,
                               after_post=True, closed_1=closed_1, closed_2=closed_2, error_1=error_1, error_2=error_2)
    return render_template('groups.html', data=defaultdict(int))

@app.route('/ocr', methods=['get', 'post'])
def ocr_me():
    if request.form:
        url_of_pic = request.form['url']

        if request.form['option'] == 'printed':
            result = printed_text(url_of_pic)
            return render_template('ocr.html', url_of_pic = url_of_pic, result = result, after_post = True)

        elif request.form['option'] == 'written':
            result = handwritten_text(url_of_pic)
            return render_template('ocr.html', url_of_pic=url_of_pic, result=result, after_post=True)

    return render_template('ocr.html')


@app.route('/chat', methods=['get', 'post'])
def lets_chat():
    if request.form:
        message = request.form['mess']
        answer = get_answer(message)
        return render_template('chat.html', answer = answer, after_post = True)

    return render_template('chat.html')

if __name__ == '__main__':
    app.run(debug=True)