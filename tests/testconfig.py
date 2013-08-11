#!/usr/bin/env python
#encoding: utf-8

'''
Created on 2013/06/29

@author: Takayoshi-Uchida
'''

import os
import sys

#Windows環境
#GAE_HOME = 'D:\Private\Google\google_appengine'
#PROJECT_HOME = 'D:\Private\Python\StudyManagement\StudyManagement'

#Mac環境
GAE_HOME = '/Applications/GoogleAppEngineLauncher.app/Contents/Resources/GoogleAppEngine-default.bundle/Contents/Resources/google_appengine'
PROJECT_HOME = '/Users/Takayoshi_Uchida/Develop/workspace/StudyManagement'

#テストで使用するGAEのモジュールパス
EXTRA_PATHS = [
    GAE_HOME,
    PROJECT_HOME,
    os.path.join(GAE_HOME, 'google', 'appengine', 'api'),
    os.path.join(GAE_HOME, 'google', 'appengine', 'ext'),
    os.path.join(GAE_HOME, 'lib', 'yaml', 'lib'),
    os.path.join(GAE_HOME, 'lib', 'webob')
]

#パスを追加する
sys.path = EXTRA_PATHS + sys.path

