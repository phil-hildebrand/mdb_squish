#!/usr/bin/env python
# -*- coding: utf-8 -*-

import pymongo as m
import json
import random
import sys
import time
import unittest as t


class test_compcation(t.TestCase):
 
    def setUp(self):
        '''We should be able to create a connection for compaction tests'''

        self.conn = m.MongoClient('localhost',27017,connectTimeoutMS=2000,socketTimeoutMS=2000)
        self.db = self.conn['mongo_test']

    def test_compact(self):
        '''We should be able to compact a collection'''

        s = self.db.command("collstats", 'mongo_collection')
        print (json.dumps(s, sort_keys=True, indent=4, separators=(',', ': ')))
    
        start_time = time.time()
        try:
            result = self.db.command("compact", 'mongo_collection')
    
        except Exception as e:
            print ('Copmcation Failed: (%s)' % e)
            t.testcase.fail ('Compcation Failed')
    
        s = self.db.command("collstats", 'mongo_collection')
        print (json.dumps(s, sort_keys=True, indent=4, separators=(',', ': ')))

