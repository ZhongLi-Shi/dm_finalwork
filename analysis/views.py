#-*- coding: UTF-8 -*-
from django.shortcuts import render, render_to_response
from django.http import HttpResponse, HttpResponseRedirect
from . import spider,elongSpider
from .LIP import evaluation
import sys,os

def analysis_sentence(request):
    sentence = request.GET.get('sentence')
    grade = evaluation.get_single_sentence_grade(sentence)
    split = evaluation.get_sentence_split(sentence)
    # group = evaluation.get_sentence_group(sentence)
    if  grade==0:star=0
    if grade>0and grade<=2:star=1
    if grade>2 and grade<=4:star=2
    if grade>4 and grade<=6:star=3
    if grade>6 and grade<=8:star=4
    if grade>8 and grade<=10:star=5
    return render(request, 'analysis_sentence.html', {'sentence': sentence, 'grade': grade,'star':star,'splits': split, })


def analysis_douban(request):
    url = request.GET.get('url')
    comment_list = spider.spider_excute(url)
    if None is comment_list:
        return render(request, 'index_douban.html', {'error': '网址输入错误或没有评论'})

    grade_list, weight, value = evaluation.get_douban_grade(comment_list)
    grade = []
    for (comment, g) in zip(comment_list, grade_list):
        grade.append([comment,g])
    # value1_2 = 10
    # value3_4 = 10
    # value5_6 = 10
    # value7_8 = 30
    # value9_10 = 40
    # # value = {'value1_2': value1_2, 'value3_4': value3_4, 'value5_6': value5_6, 'value7_8': value7_8,
    # #          'value9_10': value9_10}
    # value = {'1-2分': value1_2, '3-4分': value3_4, '5-6分': value5_6, '7-8分': value7_8,
    #          '9-10分': value9_10}
    return render(request, 'analysis_douban.html',
                  {'grades': grade, 'values': value, 'weights': weight})

def analysis_jiudian_all(request):
    url = request.GET.get('url')
    comment_list = elongSpider.elongSpiderExcute(url)
    if None is comment_list:
        return render(request, 'index_hotel.html', {'error': '网址输入错误或没有评论'})
    grade_list, weight, value = hotel_eval.get_jiudian_grade(comment_list)
    grade = []
    for (comment, g) in zip(comment_list, grade_list):
        grade.append([comment, g])
    return render(request, 'analysis_hotel.html',
                  {'grades': grade, 'values': value, 'weights': weight})

def analysis_jiudian(request):
    sentence = request.GET.get('sentence')
    grade = hotel_eval.get_sentence_grade(sentence)
    split = hotel_eval.get_sentence_split(sentence)
    # group = evaluation.get_sentence_group(sentence)
    if grade == 0: star = 0
    if grade > 0 and grade <= 2: star = 1
    if grade > 2 and grade <= 4: star = 2
    if grade > 4 and grade <= 6: star = 3
    if grade > 6 and grade <= 8: star = 4
    if grade > 8 and grade <= 10: star = 5
    return render(request, 'analysis_sentence.html',
                  {'sentence': sentence, 'grade': grade, 'star': star, 'splits': split, })

def index(request):
    return render_to_response('index.html')


def index_douban(request):
    return render_to_response('index_douban.html')

def index_hotel(request):
    return render_to_response('index_hotel.html')

# Create your views here.
