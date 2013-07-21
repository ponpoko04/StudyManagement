#!/usr/bin/python
# -*- coding: utf-8 -*-

'''
Created on 2013/06/26

@author: Takayoshi-Uchida
'''

import os
import webapp2
import json

import dsmodels

from google.appengine.api import users
from google.appengine.ext.webapp import template

class SubjectMainte(webapp2.RequestHandler):
    '''
    科目メンテ画面
    '''
    def get(self):
        '''
        科目メンテ 初期表示
        '''
        subjects = dsmodels.Subject.all().filter('registrant = ', users.get_current_user())

        template_values = {
            'subjects': subjects
            }
        path = os.path.join(os.path.dirname(__file__), '../views/subjectMainte.html')
        self.response.out.write(template.render(path, template_values))

    def post(self):
        '''
        科目メンテ 登録
        '''
        #入力された科目を登録します
        newSubject = dsmodels.Subject(registrant=users.get_current_user(),
                             subjectName=self.request.get('subjectName'))
        newSubject.put()

        #登録科目数を取得します
        counter = dsmodels.Subject.all().filter('registrant = ', users.get_current_user()).count()
        counter = 0 if (counter is None) else counter
        responseHtml = ''
        updateName = u'更新'.encode('utf_8')
        deleteName = u'削除'.encode('utf_8')

        #登録済一覧に新規登録分を追加するため、HTMLを生成します
        #（なぜか新規登録分を登録直後では取ってこれないため、HTMLをJSで追加する処理としている）
        responseHtml += '<tr><td><input type="text" value="' + newSubject.subjectName.encode('utf_8') + '" name="' + str(newSubject.key()).encode('utf_8') + '" id="TxtSubjectName"></td>'
        responseHtml += '<td><input type="submit" id="update' + str(counter) + '" value="' + updateName + '" '
        responseHtml += ' name="' + str(newSubject.key()).encode('utf_8') + '" class="Js-UpdateSubject" onclick="return subjectMainte.updateSubject(event, $(this));"></td>'
        responseHtml += '<td><input type="submit" id="delete' + str(counter) + '" value="'+ deleteName + '"'
        responseHtml += ' name="' + str(newSubject.key()).encode('utf_8') + '" class="Js-DeleteSubject" onclick="return subjectMainte.deleteSubject(event, $(this));"></td>'
        responseHtml += '</tr>'

        self.response.headers['Content-Type'] = 'text/html'
        self.response.out.write(responseHtml)

class UpdateSubject(webapp2.RequestHandler):
    '''
    科目メンテ 更新処理
    '''
    def post(self):
        #変更された科目を更新します
        updateSubject = dsmodels.Subject(key=self.request.get('updateKey'),
                                         registrant=users.get_current_user())
        updateSubject.subjectName = self.request.get('updateSubjectName')
        updateSubject.put()

        json_to_send = {'subjectName': updateSubject.subjectName}
        self.response.headers['Content-Type'] = 'application/json'
        self.response.out.write(json.dumps(json_to_send))

class DeleteSubject(webapp2.RequestHandler):
    '''
    科目メンテ 削除処理
    '''
    def post(self):
        #科目、科目を使用している勉強単位を削除します
        deleteSubject = dsmodels.Subject(key=self.request.get('deleteKey'),
                                registrant=users.get_current_user())
        deleteStudyUnit = dsmodels.StudyUnit.all().filter('registrant = ', users.get_current_user()).filter('subject = ', deleteSubject)
        for deleteUnit in deleteStudyUnit:
            deleteUnit.delete()
        deleteSubject.delete()

        json_to_send = {'deleteKey': deleteSubject.subjectName}
        self.response.headers['Content-Type'] = 'application/json'
        self.response.out.write(json.dumps(json_to_send))
