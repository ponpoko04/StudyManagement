#!/usr/bin/python
# -*- coding: utf-8 -*-

'''
Created on 2013/06/26

@author: Takayoshi-Uchida
'''

class Years(object):
    '''
        年モデル
    '''
    def __init__(self, val, isSelected):
        '''
        Constructor
        '''
        self.value = val
        self.selected = isSelected

#
class Months(object):
    '''
        月モデル
    '''
    def __init__(self, val, isSelected):
        '''
        Constructor
        '''
        self.value = val
        self.selected = isSelected

class Days(object):
    '''
        日モデル
    '''
    def __init__(self, val, isSelected):
        '''
        Constructor
        '''
        self.value = val
        self.selected = isSelected


class StudyTime(object):
    '''
        勉強時間モデル
    '''
    def __init__(self, subjectName, sumHour, sumMinute):
        '''
        Constructor
        '''
        self.subjectName = subjectName
        self.sumHour = sumHour
        self.sumMinute = sumMinute

