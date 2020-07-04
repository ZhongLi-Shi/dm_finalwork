#!/usr/bin/python2.7
# -*- coding: utf-8 -*-

import pickle
import jieba.posseg as pseg
import codecs, sys, os
import imp

imp.reload(sys)


# sys.setdefaultencoding('utf-8')

def loadPkl(loadPath):
    print("Loading FreaItems:", loadPath)
    loadfile = open(loadPath, 'rb')
    Dat = pickle.load(loadfile, encoding='utf-8')
    loadfile.close()
    return Dat


module_dir = os.path.dirname(__file__)  # get current directory
file_path = os.path.join(module_dir, 'datasets', 'cut_stopword.txt')
stopkey = [w.strip() for w in codecs.open(file_path, 'r', encoding='utf-8').readlines()]
goodfreqItems = loadPkl(os.path.join(module_dir, "GoodResultItems.pkl"))
badfreqItems = loadPkl(os.path.join(module_dir, "BadResultItems.pkl"))
extreme_dict = loadPkl(os.path.join(module_dir, "extreme_dict.pkl"))
more_dict = loadPkl(os.path.join(module_dir, "more_dict.pkl"))
very_dict = loadPkl(os.path.join(module_dir, "very_dict.pkl"))


def splitWord(words):
    print("Spliting word...")
    split_word = []
    for i in range(len(words)):
        results = []
        word = pseg.cut(words[i])
        for w in word:
            results.append(str(w.word) + "/" + str(w.flag))
            # print str(w.word) +"/"+str(w.flag)
        split_word.append(results)
    # print split_word
    return split_word


def delstopword(words, stopkey):
    sentence = []
    for wordlist in words:
        pure_word_list = []
        for word in wordlist:
            pure_word = word[:word.index("/")]
            if pure_word not in stopkey and (word[-2:] in ["/d", "/a", "/v"] \
                                             or word[-3:] in ["/zg"]):
                pure_word_list.append(word)
                # print word
    sentence.append(pure_word_list)
    return sentence


def get_single_sentence_group(sentence, freqItems):
    sentence_table = []
    # for w in sentence:
    #     print w
    # Initial list
    sentence_table.append(sentence)
    sentence_table.append(list(range(len(sentence))))
    sentence_table.append([0] * len(sentence))
    for i in range(len(sentence_table[0])):
        # print freqItems[frozenset([sentence_table[0][i]])]
        if frozenset([sentence_table[0][i]]) in freqItems:
            sentence_table[2][i] = freqItems[frozenset([sentence_table[0][i]])]
    # print sentence_table

    for i in range(len(sentence)):
        temp = [sentence_table[0][i]]
        for j in range(len(sentence)):
            if sentence_table[1][i] == sentence_table[1][j] and i != j:
                temp.append(sentence_table[0][j])

        flag = 0
        for j in [1, 2]:
            if i + j < len(sentence_table[0]):
                if sentence_table[1][i] != sentence_table[1][i + j] and sentence_table[2][i + j] != 0:
                    temp.append(sentence_table[0][i + j])
                    flag = i + j
                    break
        # print temp
        #############################
        if frozenset(temp) in freqItems and flag != 0:
            # print "\n"
            # print frozenset(temp)
            # for w in temp:
            #     print w
            sentence_table[1][flag] = sentence_table[1][i]
            sentence_table[2][flag] = 0
        else:
            del temp
    # print sentence_table

    sentence_group = [[], []]
    for i in range(len(sentence_table[0])):
        items_cont = []
        items_freq = 0
        for j in range(len(sentence_table[0])):
            if sentence_table[1][j] == i:
                items_cont.append(sentence_table[0][j])
                items_freq = 0
        # print items_cont
        if len(items_cont) != 0:
            sentence_group[0].append(items_cont)
            sentence_group[1].append(items_freq)

    for i in range(len(sentence_group[0])):
        sentence_group[1][i] = freqItems.get(frozenset(sentence_group[0][i]), 0)
        # print temp

    return sentence_group


def get_sentence_split(sentence):
    split_word = splitWord([sentence])
    pure_sentence = delstopword(split_word, stopkey)
    # return splitWord([sentence])[0]
    return pure_sentence[0]


if __name__ == "__main__":
    with open('datasets\\pos_lzq.txt') as f:
    # with open('datasets\\neg_lzq.txt') as f:
        for line in f:
            split_result = get_sentence_split(line)
            with open('datasets\\lzq_split_good.txt', 'a') as result:
                result.write(' '.join(split_result))
                result.write('\n')


