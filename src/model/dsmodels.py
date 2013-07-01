#!/usr/bin/python
# -*- coding: utf-8 -*-

'''
Created on 2013/06/26

@author: Takayoshi-Uchida
'''

from google.appengine.ext import db

class Subject(db.Model):
    '''
        科目マスタモデル
    '''
    registrant = db.UserProperty(required=True)     #登録者
    subjectName = db.StringProperty()               #科目名

class StudyUnit(db.Model):
    '''
        勉強単位モデル
    '''
    registrant = db.UserProperty(required=True)         #登録者
    subject = db.ReferenceProperty(Subject)             #科目
    content = db.StringProperty(multiline=True)         #内容
    timeStamp = db.StringProperty()                     #勉強日付
    studyTimeHour = db.IntegerProperty()                #勉強時間(時)
    studyTimeMinute = db.IntegerProperty()              #勉強時間(分)
    updateDate = db.DateTimeProperty(auto_now=True)     #更新日時

