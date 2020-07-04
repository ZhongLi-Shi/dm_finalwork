#!/usr/bin/python2.7
# -*- coding: utf-8 -*- 

import pickle
import jieba.posseg as pseg
import codecs,sys,os
import imp
imp.reload(sys)
#sys.setdefaultencoding('utf-8')

def loadPkl(loadPath):
    print("Loading FreaItems:", loadPath)
    loadfile = open(loadPath, 'rb')
    Dat = pickle.load(loadfile,encoding='utf-8')
    loadfile.close()
    return Dat

module_dir = os.path.dirname(__file__)  # get current directory
file_path = os.path.join(module_dir,'datasets','cut_stopword.txt')
stopkey = [w.strip() for w in codecs.open(file_path, 'r', encoding='utf-8').readlines()]
goodfreqItems = loadPkl(os.path.join(module_dir,"GoodResultItems_lzq.pkl"))
badfreqItems = loadPkl(os.path.join(module_dir,"BadResultItems_lzq.pkl"))
extreme_dict = loadPkl(os.path.join(module_dir,"extreme_dict.pkl"))
more_dict = loadPkl(os.path.join(module_dir,"more_dict.pkl"))
very_dict = loadPkl(os.path.join(module_dir,"very_dict.pkl"))

def splitWord(words):
    print("Spliting word...")
    split_word = []
    for i in range(len(words)):
        results = []
        word = pseg.cut(words[i])
        for w in word:
            results.append(str(w.word) +"/"+str(w.flag))
            # print str(w.word) +"/"+str(w.flag)
        split_word.append(results)
    # print split_word
    return split_word

def delstopword(words,stopkey):
    sentence = []
    for wordlist in words:
        pure_word_list = []
        for word in wordlist:
            pure_word = word[:word.index("/")]
            if pure_word not in stopkey and (word[-2:] in ["/d", "/a", "/v"]\
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
    sentence_table.append([0]*len(sentence))
    for i in range(len(sentence_table[0])):
        # print freqItems[frozenset([sentence_table[0][i]])]
        if frozenset([sentence_table[0][i]]) in freqItems:
            sentence_table[2][i] = freqItems[frozenset([sentence_table[0][i]])]
    # print sentence_table

    for i in range(len(sentence)):
        temp = [sentence_table[0][i]]
        for j in range(len(sentence)):
            if sentence_table[1][i]==sentence_table[1][j] and i!=j:
                temp.append(sentence_table[0][j])

        flag = 0
        for j in [1, 2]:
            if i+j < len(sentence_table[0]):
                if sentence_table[1][i]!=sentence_table[1][i+j] and sentence_table[2][i+j]!=0:
                    temp.append(sentence_table[0][i+j])
                    flag = i+j
                    break
        # print temp
                    #############################
        if frozenset(temp) in freqItems and flag!=0:
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
        if len(items_cont)!=0:
            sentence_group[0].append(items_cont)
            sentence_group[1].append(items_freq)
    
    for i in range(len(sentence_group[0])):
        sentence_group[1][i] = freqItems.get(frozenset(sentence_group[0][i]), 0)
        # print temp

    return sentence_group

def get_sentence_split(sentence):
    return splitWord([sentence])[0]


def get_emotion_grade(sentence,freqItems):

    # grade = 0
    split_word = splitWord([sentence])
    pure_sentence = delstopword(split_word, stopkey)
    sentence_group = get_single_sentence_group(pure_sentence[0], freqItems)
    # sentence_group = get_single_sentence_group(pure_sentence[0], goodfreqItems)
    for i in range(len(sentence_group[0])):
        for j in range(len(sentence_group[0][i])):
            print(sentence_group[0][i][j])
        print(sentence_group[1][i])
    
    sentence_grade = [0]*len(sentence_group[0])
    # Calculate grades
    for i in range(len(sentence_group[0])):
        for w in ['/a', '/v', '/d', '/zg']:
            for j in range(len(sentence_group[0][i])):
                    if w in sentence_group[0][i][j] and w in ['/a']:
                        sentence_grade[i] += sentence_group[1][i]*len(sentence_group[0][i])
                    elif w in sentence_group[0][i][j] and w in ['/v'] and sentence_group[1][i]<=0.2:
                        sentence_grade[i] += sentence_group[1][i]*len(sentence_group[0][i])
                    elif w in sentence_group[0][i][j] and w in ['/d']:
                        if sentence_group[0][i][j][:-2] in extreme_dict:
                            sentence_grade[i] *= 2.5
                        elif sentence_group[0][i][j][:-2] in very_dict:
                            sentence_grade[i] *= 1.5
                        elif sentence_group[0][i][j][:-2] in more_dict:
                            sentence_grade[i] *= 0.5
                    elif w in sentence_group[0][i][j] and w in ['/zg']:
                        if sentence_group[0][i][j][:-3] in extreme_dict:
                            sentence_grade[i] *= 2.5
                        elif sentence_group[0][i][j][:-3] in very_dict:
                            sentence_grade[i] *= 1.5
                        elif sentence_group[0][i][j][:-3] in more_dict:
                            sentence_grade[i] *= 0.5
    print(sentence_grade, sum(sentence_grade))
            
    
    return sum(sentence_grade)

def get_single_sentence_grade(sentence):
    positive_grade = get_emotion_grade(sentence, goodfreqItems)
    negative_grade = get_emotion_grade(sentence, badfreqItems)
    print(positive_grade, negative_grade, positive_grade-negative_grade)
    grade = positive_grade-negative_grade
    if grade >= 0.1 :
        grade = 10
    elif grade>=0 and grade<0.1:
        grade = 50*(grade+0.1)
    elif grade>-0.1 and grade<0:
        grade = -50*grade
    elif grade<=-0.1:
        grade = 0
    return int(grade)

def get_sentence_grade(sentence):
    positive_grade = get_emotion_grade(sentence, goodfreqItems)
    print("positive_grade:",positive_grade)
    negative_grade = get_emotion_grade(sentence, badfreqItems)
    print("positive_grade:", positive_grade)
    print(positive_grade, negative_grade, positive_grade-negative_grade)
    grade = positive_grade-negative_grade
    if grade >= 0.1 :
        grade = 10
    elif grade>=0 and grade<0.1:
        grade = 50*(grade+0.1)
    elif grade>-0.1 and grade<0:
        grade = -50*grade
    elif grade<=-0.1:
        grade = 0
    return int(grade)

def get_douban_grade(sentence_list):

    grade = []
    weight = {'积极': 100, '消极': 0}
    value = {'1-2分': 0, '3-4分': 0, '5-6分': 0, '7-8分': 0, '9-10分': 0}
    for sentence in sentence_list:
        grade.append(get_sentence_grade(sentence))
    
    pos_num = len([v for v in grade if v>=5])
    neg_num = len([v for v in grade if v< 5])
    weight['积极'] = float(pos_num)/(pos_num+neg_num)*100
    weight['消极'] = float(neg_num)/(pos_num+neg_num)*100
    for v in grade:
        if v<3:
            value['1-2分']+=1
        elif v>=3 and v<5:
            value['3-4分']+=1
        elif v>=5 and v<7:
            value['5-6分']+=1
        elif v>=7 and v<9:
            value['7-8分']+=1
        elif v>=9:
            value['9-10分']+=1
        else:pass

    return grade, weight, value



# if __name__ == "__main__":
#     print(badfreqItems)
#
#     # grade, weight, value = get_douban_grade(["满分。毕竟我已经很久没有看个电影哭得像个小孩子了 似乎大家又要说起那句老话：电影是绝佳的造梦机器。那些回不去的家乡 没能守护的家人也只有在梦里相见。",\
#     #                  "皮克斯保持原创的又一巅峰，回忆与遗忘的情感核心，在家庭、音乐、梦想、冒险的故事线下饱满溢出银幕，最后只能以泪洗面。2017年度最佳电影！",\
#     #                 "很差啊。"])
#
#     grade, weight, value = get_douban_grade(["还不错,便宜实用,安装方便"])
#
#     print(grade,weight,value)

