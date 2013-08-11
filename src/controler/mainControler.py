#!/usr/bin/python
# -*- coding: utf-8 -*-

'''
Created on 2013/06/26

@author: Takayoshi-Uchida
'''

import datetime
from google.appengine.api import users
import datamodels
import Tzinfo
from operator import attrgetter

class mainControler(object):
    '''
    index.html コントローラ
    '''

    def __init__(self):
        '''
        Constructor
        '''
        self.url = ''
        self.url_linktext = ''
        self.isAuth = True
        self.d = Tzinfo.jst_date(datetime.datetime.now())

    def createLoginInfo(self, reqUri):
        '''
        ログイン情報を構築します
        '''
        if users.get_current_user() is None:
            self.url = users.create_login_url(reqUri)
            self.url_linktext = 'Login'
            self.isAuth = False

    def getYearsList(self):
        '''
        年の配列を取得します
        '''
        years = []
        for i in range(self.d.year - 2, self.d.year + 10):
            if i == self.d.year:
                years.append(datamodels.Years(i, True))
            else:
                years.append(datamodels.Years(i, False))

        return years

    def getMonthsList(self):
        '''
        月の配列を取得します
        '''
        months = []
        for i in range(1, 13):
            if i == self.d.month:
                months.append(datamodels.Months(str(i).zfill(2), True))
            else:
                months.append(datamodels.Months(str(i).zfill(2), False))

        return months

    def getDaysList(self):
        '''
        日の配列を取得します
        '''
        days = []
        for i in range(1, 32):
            if i == self.d.day:
                days.append(datamodels.Days(str(i).zfill(2), True))
            else:
                days.append(datamodels.Days(str(i).zfill(2), False))

        return days

    def sumUpStudyHours(self, studyUnits):
        '''
        科目ごとの勉強時間集計を行います
        '''
        tmpStudyHours = {}
        tmpStudyMinutes = {}
        studyTimes = []
        if studyUnits.count() > 0:
            #科目ごと集計処理
            for studyUnit in studyUnits:
                tmpStudyHours = self.sumUpHours(studyUnit.subject.subjectName, studyUnit.studyTimeHour, tmpStudyHours)
                tmpStudyMinutes = self.sumUpMinutes(studyUnit.subject.subjectName, studyUnit.studyTimeMinute,
                                                    tmpStudyHours, tmpStudyMinutes)

            #画面項目リスト作成処理
            studyTimes = [datamodels.StudyTime(key, tmpStudyHours[key], tmpStudyMinutes[key]) for key in tmpStudyHours.keys()]

        return sorted(studyTimes,key=attrgetter('subjectName'))

    def sumUpHours(self, subjectName, hour, tmpStudyHours):
        '''
        時間を集計します
        '''
        if subjectName in tmpStudyHours:
            tmpStudyHours[subjectName] += hour
        else:
            tmpStudyHours[subjectName] = hour

        return tmpStudyHours

    def sumUpMinutes(self, subjectName, minute, tmpStudyHours, tmpStudyMinutes):
        '''
        分を集計します
        '''
        if subjectName in tmpStudyMinutes:
            tmpStudyMinutes[subjectName] += minute
            #時間への繰り上げ処理
            if tmpStudyMinutes[subjectName] >= 60:
                tmpMinutes = tmpStudyMinutes[subjectName]
                tmpStudyHours[subjectName] += tmpMinutes // 60    #繰り上げ
                tmpStudyMinutes[subjectName] = tmpMinutes % 60    #残りを戻す
        else:
            tmpStudyMinutes[subjectName] = minute

        return tmpStudyMinutes

