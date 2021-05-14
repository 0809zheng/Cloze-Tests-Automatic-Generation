import os
import nltk
import random
from nltk.parse import stanford
from nltk.corpus import (gutenberg, genesis, inaugural,
                         nps_chat, webtext, treebank, wordnet)


os.environ['STANFORD_PARSER'] = 'E:/stanfordParser/jars/stanford-parser.jar'
os.environ['STANFORD_MODELS'] = 'E:/stanfordParser/jars/stanford-parser-3.9.1-models.jar'
parser = stanford.StanfordParser(model_path="E:\stanfordParser\englishPCFG.ser.gz")


def get_synonym(w):
    synonym_set = []
    word_syn_set = wordnet.synsets(w)
    for word_syn in word_syn_set:
        word_names = word_syn.lemma_names()
        synonym_set += word_names
    synonym_set = list(set(synonym_set))
    return synonym_set


def get_sentences(w):
    sens = []
    count = 0
    word_syn_set = wordnet.synsets(w)
    for word_syn in word_syn_set:
        count += 1
        examples = word_syn.examples()
        count_example = 0
        for example in examples:
            count_example += 1
            if w in example:
                sens.append(example)
    return sens


def get_complexity_score(sens):
    ss = []
    for sen in sens:
        score_complexity = 1
        parse = parser.raw_parse(sen)
        tree = list(parse)[0]
        for tr in tree.subtrees():
            if tr.label() == 'S':
                score_complexity += 1
        ss.append(score_complexity)
    return ss


# 还没写
def get_context_score(sens):
    ss = []
    for sen in sens:
        ss.append(1)
    return ss


def search_noun(pos, index):
    left = index - 1
    right = index + 1
    while left >= 0 or right < len(pos):
        if left >= 0 and (pos[left][1] == 'NN' or pos[left][1] == 'NNS'):
            return pos[left][0]
        if right < len(pos) and (pos[right][1] == 'NN' or pos[right][1] == 'NNS'):
            return pos[right][0]
        left -= 1
        right += 1
    return None


def count_frequency(n, w):
    fre = 0
    for corpus_set in (gutenberg, webtext):  # , genesis, inaugural, nps_chat, treebank, wordnet):
        for fileid in corpus_set.fileids():
            try:
                corpus = gutenberg.sents(fileid)
            except OSError:
                corpus = []
            for sent in corpus:
                if w in sent and n in sent:
                    fre += 1
    return fre


def get_grammar_score(sens, w):
    ss = []
    for sen in sens:
        score_grammar = []
        parse = parser.raw_parse(sen)
        tree = list(parse)[0]
        pos = tree.pos()  # [('the', 'D'), ('dog', 'N'), ('chased', 'V'), ('the', 'D'), ('cat', 'N')]
        # print(pos)
        indexes = [i for i in range(len(pos)) if pos[i][0] == w]
        # print(w, indexes)
        for index in indexes:
            n = search_noun(pos, index)
            # print(n)
            if n is not None:
                fre = count_frequency(n, w)
                score_grammar.append(fre)
        if not score_grammar:
            ss.append(1)
        else:
            ss.append(max(max(score_grammar), 2))
    return ss


def get_length_score(sens):
    ss = []
    for sen in sens:
        length = len(sen.split())
        ss.append(length)
    return ss


def search_adv(pos, index):
    left = index - 1
    right = index + 1
    while left >= 0 or right < len(pos):
        if left >= 0 and (pos[left][1] == 'RB'):
            return pos[left][0]
        if right < len(pos) and (pos[right][1] == 'RB'):
            return pos[right][0]
        left -= 1
        right += 1
    return None


def get_frequent_words(n):
    frequent_words_fre = {}
    for corpus_set in [gutenberg]:  # , webtext, genesis, inaugural, nps_chat, treebank, wordnet]:
        for fileid in corpus_set.fileids():
            try:
                corpus = gutenberg.sents(fileid)
            except OSError:
                corpus = []
            for sent in corpus:
                if n in sent:
                    word_tag = nltk.pos_tag(sent)
                    indexes = [i for i in range(len(word_tag)) if word_tag[i][0] == n]
                    for index in indexes:
                        adv = search_adv(word_tag, index)
                        if adv in frequent_words_fre:
                            frequent_words_fre[adv] += 1
                        else:
                            frequent_words_fre[adv] = 1
    result = sorted(frequent_words_fre.items(), key=lambda item: item[1], reverse=True)
    return result


def get_distracts(sen, w):
    words_fre = []
    temp = sen.split(" ")
    word_tag = dict(nltk.pos_tag(temp))
    temp.remove(w)
    for n in temp:
        if word_tag[n] in ['RB', 'NN', 'NNS', 'VB', 'VBG']:
            words_fre += get_frequent_words(n)
    # print("words_fre:", [x[0] for x in words_fre])
    words_fre = sorted(words_fre, key=lambda item: item[1], reverse=True)
    words_fre = [words_fre[x] for x in range(min(100, len(words_fre)), len(words_fre))]  # remove stopwords 不是很成功
    random.shuffle(words_fre)
    return [words_fre[x][0] for x in range(0, min(3, len(words_fre)))]  # return the maximum 3 distractors


if __name__ == '__main__':
    word = "regularly"
    sentences = get_sentences(word)
    print("The number of sentences:", len(sentences))
    scores = [0 for i in sentences]
    complexity_scores = get_complexity_score(sentences)
    context_scores = get_context_score(sentences)
    grammar_scores = get_grammar_score(sentences, word)
    length_scores = get_length_score(sentences)
    print("complexity_scores:", complexity_scores)
    print("context_scores:", context_scores)
    print("grammar_scores:", grammar_scores)
    print("length_scores:", length_scores)
    for i in range(len(scores)):
        scores[i] += (complexity_scores[i] / max(complexity_scores)) * \
                     (context_scores[i] / max(context_scores)) * \
                     (grammar_scores[i] / max(grammar_scores)) * \
                     (length_scores[i] / max(length_scores))
    for i in range(len(scores)):
        print(round(scores[i], 10), end=": ")
        print(sentences[i])

    sentence = sentences[scores.index(max(scores))]
    distracts = [word]
    synonym = get_synonym(word)
    print("sentence:", sentence, " word:", word)
    distracts += get_distracts(sentence, word)
    distracts = [x.lower() for x in distracts]
    print("distracts:", distracts)
    random.shuffle(distracts)
    sentence = sentence.replace(word, '_____')
    print("\n" + sentence + "\n\n")
    count = 0
    for d in distracts:
        count += 1
        print(str(count) + ". " + d + "   ")
    print("\n\nCorrect answer: " + word)


