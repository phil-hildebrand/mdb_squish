#!/usr/bin/env python
# -*- coding: utf-8 -*-
import pymongo as m
from unittest import TestCase

def connect():

    try:
        # conn = m.MongoClient('mongodb://localhost:27017/?connectTimeoutMS=2000&socketTimeoutMS=2000')
        conn = m.MongoClient('localhost',27017,connectTimeoutMS=2000,socketTimeoutMS=2000)
        info = conn.server_info()
        return True
    
    except Exception as e:
        return False

class test_connection(TestCase):
    def test(self):
        self.assertTrue(connect())
