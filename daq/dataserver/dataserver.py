#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Jan 31 15:12:13 2018

@author: derek
"""

import abc


class AbstractDataserver(metaclass=abc.ABCMeta):
    def __init__(self):
        pass
    
    @abc.abstractmethod
    def get_id_by_name(self,name):
        pass
    
    
class HTTPDataserver(AbstractDataserver):
    def __init__(self):
        pass
    
    def get_id_by_name(self,name):
        pass
    
class Datagate(HTTPDataserver):
    def __init__(self):
        pass
    
    def get_id_by_name(self,name):
        pass
    