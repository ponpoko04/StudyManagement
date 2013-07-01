#!/usr/bin/env python
#encoding: utf-8

'''
Created on 2013/06/29

@author: Takayoshi-Uchida
'''

from google.appengine.api import users

from tests.basetest import GAETestBase

import mainControler

#mainControlerクラステスト
class test_mainControler(GAETestBase):

    def test_createLoginInfo(self):
        controler = mainControler()
        controler.createLoginInfo(users.get_current_user())
        self.assertEqual(False, controler.isAuth, 'ログイン処理成功')
