import pymorphy2
import re, pandas, random
from nltk.tokenize import word_tokenize

morph = pymorphy2.MorphAnalyzer()
wordlist = pandas.read_csv('/Users/Valeriya/Desktop/lemmas/1grams-3.csv', delimiter = '\t')

all_words = list(wordlist['и'])


def get_answer(message):
    splitted = word_tokenize(message)
    answer = []
    sent_tags = []
    for i in splitted:
        if any([char.isalpha() for char in i]):
            parsed = morph.parse(i.strip(' .?!:;-'))[0].tag
            sent_tags.append(parsed)
        else:
            sent_tags.append(i)

    for tag_w in sent_tags:
        if type(tag_w) == pymorphy2.tagset.OpencorporaTag:
            flag = 0
            while flag == 0:
                word = random.choice(all_words)
                w = morph.parse(word)[0]
                lexs = w.lexeme
                if w.tag.POS == tag_w.POS:
                    for i in lexs:
                        if i.tag == tag_w:
                            answer.append(i.word)
                            flag = 1
                            break
                else:
                    flag = 0
        else:
            answer.append(tag_w)

    fst_word = re.sub(answer[0][0], answer[0][0].upper(), answer[0])
    answer.pop(0)
    answer = [fst_word] + answer
    answer = ' '.join(answer)
    return answer