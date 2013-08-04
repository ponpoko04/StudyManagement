#!/usr/bin/python
# -*- coding: utf-8 -*-

'''
Created on 2013/07/15

@author: Takayoshi_Uchida
'''

import os
import webapp2
import datetime
import json

import dsmodels

from google.appengine.api import users
from google.appengine.ext.webapp import template

class ListPerDate(webapp2.RequestHandler):
    '''
    日付別一覧
    '''

    def get(self):
        '''
        日付別一覧 初期表示
        '''

        today = datetime.datetime.now()
        today = str(today.year) + str(today.month).zfill(2) + str(today.day).zfill(2)
        studyUnits = dsmodels.StudyUnit.all().filter('registrant = ', users.get_current_user()).filter('timeStamp = ', today)
        existDataLists = (ListPerDate()).getExistData(today)

        template_values = {
            'studyUnits': studyUnits,
            'existDataLists': existDataLists
        }
        path = os.path.join(os.path.dirname(__file__), '../views/listPerDate.html')
        self.response.out.write(template.render(path, template_values))

    def post(self):
        '''
        日付別一覧 検索
        '''
        
        searchDay =self.request.get('searchDay')
        studyUnits = dsmodels.StudyUnit.all().filter('registrant = ', users.get_current_user()).filter('timeStamp = ', searchDay)

        template_values = {
            'studyUnits': studyUnits
        }
        path = os.path.join(os.path.dirname(__file__), '../views/listPerDateForSearch.html')
        self.response.headers['Content-Type'] = 'text/html'
        self.response.out.write(template.render(path, template_values))
        
    def getExistData(self, targetDay):
        '''
        対象年月の勉強単位データ存在日付を取得します
        '''
        
        thisMonthDataLists = dsmodels.StudyUnit.all().filter('registrant = ', users.get_current_user()).filter('timeStamp > ', targetDay[:6] + '00').filter('timeStamp <= ', targetDay[:6] + '31')
        existDataLists = [existDataList.timeStamp[-2:] for existDataList in thisMonthDataLists]
        # 日付の重複排除後リストを返却します
        return sorted(set(existDataLists), key=existDataLists.index)

class UpdateExistDate(webapp2.RequestHandler):
    '''
    勉強単位データの存在する日付更新処理
    '''
    
    def post(self):
        '''
        Hidden部を再作成します
        '''
        
        targetDay = self.request.get('movedMonth')
        existDataLists = (ListPerDate()).getExistData(targetDay)

        template_values = {
            'existDataLists': existDataLists
        }
        path = os.path.join(os.path.dirname(__file__), '../views/listPerDateForExistDataList.html')
        self.response.headers['Content-Type'] = 'text/html'
        self.response.out.write(template.render(path, template_values))
        
class DeleteStudyUnit(webapp2.RequestHandler):
    '''
    勉強単位を削除します
    '''

    def post(self):
        '''
        キーを元に勉強単位を削除します
        '''
        
        deleteStudyUnit = dsmodels.StudyUnit(key=self.request.get('deleteKey'),
                                             registrant=users.get_current_user())
        deleteStudyUnit.delete()

        json_to_send = {'deleteMsg': '削除しました。'}
        self.response.headers['Content-Type'] = 'application/json'
        self.response.out.write(json.dumps(json_to_send))

        