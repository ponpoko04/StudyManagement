#!/usr/bin/env python
#encoding: utf-8

'''
Created on 2013/06/29

@author: Takayoshi-Uchida
'''

import os
import testconfig
import unittest

#スタブをインポート
from google.appengine.api import apiproxy_stub_map
from google.appengine.api import datastore_file_stub
from google.appengine.api import user_service_stub
from google.appengine.api import users

#テスト対象のクラスをインポート
#from models import *
from mainControler import mainControler

APP_ID = u'test_id'
AUTH_DOMAIN = 'gmail.com'
LOGGED_IN_USER = 'test@example.com'

#単体テストのベースクラス
class GAETestBase(unittest.TestCase):

    #ベースクラスのsetUp内でスタブを登録しておく
    def setUp(self):
        #API Proxyを登録
        apiproxy_stub_map.apiproxy = apiproxy_stub_map.APIProxyStubMap()

        #Datastoreのスタブを登録
        stub = datastore_file_stub.DatastoreFileStub(APP_ID, '/dev/null', '/dev/null')
        apiproxy_stub_map.apiproxy.RegisterStub('datastore_v3', stub)

        #APPLICATION_IDの設定
        #コレを忘れるとDatastoreがエラーを出す
        os.environ['APPLICATION_ID'] = APP_ID

        #UserServiceのスタブを登録
        apiproxy_stub_map.apiproxy.RegisterStub('user',user_service_stub.UserServiceStub())
        os.environ['AUTH_DOMAIN'] = AUTH_DOMAIN
        os.environ['USER_EMAIL'] = LOGGED_IN_USER

#mainControlerクラステスト
class test_mainControler(GAETestBase):

    def test_createLoginInfo(self):
        controler = mainControler()
        controler.createLoginInfo(users.get_current_user())
        self.assertTrue(controler.isAuth, 'test')

if __name__ == '__main__':
    unittest.main()

