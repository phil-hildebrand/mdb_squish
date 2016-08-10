#!/usr/bin/env python
# -*- coding: utf-8 -*-
import pymongo as m
import unittest as t

class test_connection(t.TestCase):
 
    def setUp(self):
        '''We should be able to create a connection'''

        self.conn = m.MongoClient('localhost',27017,connectTimeoutMS=2000,socketTimeoutMS=2000)
        self.db = self.conn['mongo_test']

    def test_get_count(self):
        '''We should be able to create a collection'''

        counter = self.db['mongo_collection'].count()

