#!/usr/bin/env python
# -*- coding: utf-8 -*-

import pymongo as m
import random
import string
import sys
import time
import unittest as t


class test_connection(t.TestCase):
 
    def setUp(self):
        '''We should be able to create a connection for load tests'''

        self.conn = m.MongoClient('localhost',27017,connectTimeoutMS=2000,socketTimeoutMS=2000)
        self.db = self.conn['mongo_test']

    def big_string(self, chars):
        return ''.join(random.choice(string.ascii_letters) for _ in range(chars))


    def test_load_collection(self):
        insertions = 100
        total_insert = 0
        avg_insert = 0
    
        start_time = time.time()
        for ins in range(insertions):
            insert_time = time.time()
            my_text = self.big_string(100)
            try:
                x = self.db['mongo_collection'].insert_one({"type": "Load Test",
                                                            "randString": my_text,
                                                            "created": insert_time,
                                                            "concurrency": 1})
    
            except Exception as e:
                print ('Load Insert Failed: (%s)' % e)
    
            inserted_time = time.time()
            avg_insert = (inserted_time - start_time) / (ins + 1)
        total_insert = inserted_time
    
        total_insert_duration = total_insert - start_time
        print(' - inserted %d in %9.2f seconds' % (100, total_insert_duration))
        print('  - Avg insert time: %9.4f seconds' % avg_insert)
        return (total_insert_duration + total_select_duration)

