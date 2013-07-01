#!/usr/bin/python
# -*- coding: utf-8 -*-

'''
Created on 2013/06/26

@author: Takayoshi-Uchida
'''

import os
import webapp2

from mainControler import mainControler
import dsmodels

from google.appengine.api import users
from google.appengine.ext.webapp import template

class MainPage(webapp2.RequestHandler):
    '''
        勉強管理画面
    '''
    #勉強管理 表示
    def get(self):
        '''
                勉強管理 初期表示
        '''
        controler = mainControler()
        controler.createLoginInfo(self.request.uri)

        years = controler.getYearsList()
        months = controler.getMonthsList()
        days = controler.getDaysList()

        hours = ["00","01","02","03","04","05","06","07","08","09",
                 "10","11","12","13","14","15","16","17","18","19",
                 "20","21","22","23"]
        minutes = ["00","10","20","30","40","50"]

        subjects = dsmodels.Subject.all().filter('registrant = ', users.get_current_user())
        studyUnits = dsmodels.StudyUnit.all().filter('registrant = ', users.get_current_user())
        studyTimes = controler.sumUpStudyHours(studyUnits)

        template_values = {
            'url': controler.url,
            'url_linktext': controler.url_linktext,
            'isAuth': controler.isAuth,
            'years': years,
            'months': months,
            'days': days,
            'hours': hours,
            'minutes': minutes,
            'subjects': subjects,
            'studyTimes': studyTimes
            }
        path = os.path.join(os.path.dirname(__file__), '../views/index.html')
        self.response.out.write(template.render(path, template_values))

    def post(self):
        '''
                勉強管理 登録
        '''
        #入力された勉強記録を登録します
        subject = dsmodels.Subject(key=self.request.get('item'),
                          registrant=users.get_current_user())
        studyUnit = dsmodels.StudyUnit(registrant=users.get_current_user(),
                              subject=subject,
                              content=self.request.get('content'),
                              timeStamp=self.request.get('studyTimeYear') + self.request.get('studyTimeMonth') + self.request.get('studyTimeDay'),
                              studyTimeHour=int(self.request.get('studyTimeHour'), 10),
                              studyTimeMinute=int(self.request.get('studyTimeMinute'), 10))

        studyUnit.put()

        responseHtml = '<tr><td>Success!!!</td></tr>'
        self.response.headers['Content-Type'] = 'text/html'
        self.response.out.write(responseHtml)


