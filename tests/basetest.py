#!/usr/bin/env python
#encoding: utf-8

'''
Created on 2013/06/29

@author: Takayoshi-Uchida
'''

import os
import testconfig
import unittest
import datetime

#スタブをインポート
from google.appengine.api import apiproxy_stub_map
from google.appengine.api import datastore_file_stub
from google.appengine.api import user_service_stub
from google.appengine.api import users
from google.appengine.tools import dev_appserver_login

#テスト対象のクラスをインポート
#from models import *
from mainControler import mainControler
import dsmodels


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

    def test_hoge(self):
        controler = mainControler()
        self.assertEqual((controler.d + datetime.timedelta(hours=15)).hour, datetime.datetime.now().hour, "not gae timezone")

    def test_getYearsList(self):
        #年の配列を取得するテスト
        #リストの３番目に現在年が格納されていることを確認
        controler = mainControler()
        years = controler.getYearsList()
        self.assertEqual(controler.d.year, years[02].value, 'not now year')

    def test_getMonthsList(self):
        #月の配列を取得するテスト
        #リストの選択フラグ=Trueを持つオブジェクトに現在月が格納されていることを確認
        controler = mainControler()
        months = controler.getMonthsList()
        cftarget = str(controler.d.month).zfill(2)
        for month in months:
            if month.selected:
                self.assertEqual(cftarget, month.value, 'not now month')

    def test_getDaysList(self):
        #日の配列を取得するテスト
        #リストの選択フラグ=Tureを持つオブジェクトに現在月が格納されていることを確認
        controler = mainControler()
        days = controler.getDaysList()
        cftarget = str(controler.d.day).zfill(2)
        for day in days:
            if day.selected:
                self.assertEqual(cftarget, day.value, 'not now day')

    def test_sumUpStudyHours_registercount(self):
        #科目別勉強時間集計処理のテスト
        #勉強単位モデルの登録数を確認

        #テストデータ作成
        sub = dsmodels.Subject(registrant=users.get_current_user(),
                               subjectName='test_subject')
        sub.put()
        su = dsmodels.StudyUnit(registrant=users.get_current_user(),
                                subject=sub,
                                content='test_content',
                                timeStamp='20130711',
                                studyTimeHour=3,
                                studyTimeMinute=30)
        su.put()

        studyUnits = dsmodels.StudyUnit.all().filter('registrant = ', users.get_current_user())
        controler = mainControler()
        studyTimes = controler.sumUpStudyHours(studyUnits)
        self.assertEqual(studyUnits.count(), len(studyTimes), 'length not equals')

        #テストデータ削除
        sub.delete()
        su.delete()

if __name__ == '__main__':
    unittest.main()

