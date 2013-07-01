#!/usr/bin/python
# -*- coding: utf-8 -*-

'''
Created on 2013/06/01

@author: Takayoshi-Uchida
'''
import webapp2
import appengine_config

routes = [
  ('/',              'studyManagement.MainPage'),
  ('/register',      'studyManagement.MainPage'),
  ('/subject',       'subjectMainte.SubjectMainte'),
  ('/updateSubject', 'subjectMainte.UpdateSubject'),
  ('/deleteSubject', 'subjectMainte.DeleteSubject')
]

app = webapp2.WSGIApplication(routes,debug=True)

