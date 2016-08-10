#!/usr/bin/env python
# -*- coding: utf-8 -*-
import pymongo as m
import unittest as t

class test_connection(t.TestCase):

    def setUp(self):
        '''We should be able to create a connection'''

        try:
            # self.conn = m.MongoClient('localhost',27017,connectTimeoutMS=2000,socketTimeoutMS=2000)
            self.conn = "test"
            pass

        except Exception:
            fail

    def test_create(self):
        '''We should be able to create a database'''

        db = self.conn['mongo_test']
   
    def test_get_count(db):
        '''We should be able to create a collection'''

        self.assertgreater(db['mongo_collection'].count(),-1)

if __name__ == '__main__':
    t.main()
