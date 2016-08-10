#!/usr/bin/env python
# -*- coding: utf-8 -*-

import pymongo as m
import random
import sys
import time
import unittest as t


class test_deletes(t.TestCase):
 
    def setUp(self):
        '''We should be able to create a connection for delete tests'''

        self.conn = m.MongoClient('localhost',27017,connectTimeoutMS=2000,socketTimeoutMS=2000)
        self.db = self.conn['mongo_test']

    def test_collection_deletes(self):
        '''We should be able to delete a subset of documents from collections'''

        deletes = 40
        total_delete= 0
        avg_delete= 0
    
        start_time = time.time()
        for doc in range(deletes):
            delete_time = time.time()
            try:
                # deleted = self.db['mongo_collection'].findOneAndDelete({"randString": {"$exists": "true"}})
                # id = self.db['mongo_collection'].find({"randString": {"$exists": "true"}}).limit(1)
                result = self.db['mongo_collection'].delete_one({"randString": {"$exists": "true"}})
                print result.deleted_count
    
            except Exception as e:
                print ('Delete Failed: (%s)' % e)
                t.testcase.fail ('Delete Failed')
    
            deleted_time = time.time()
            avg_delete = (deleted_time - start_time) / (doc + 1)
        total_delete = deleted_time
    
        total_delete_duration = total_delete - start_time
        print(' - deleted %d in %9.2f seconds' % (100, total_delete_duration))
        print('  - Avg delete time: %9.4f seconds' % avg_delete)
        return (total_delete_duration)
