#!/usr/bin/env python
# -*- coding: utf-8 -*-

import pymongo as m
import json
import random
import string
import sys
import time
import unittest as t


class test_compaction(t.TestCase):
    def big_string(self, chars):
        return ''.join(random.choice(string.ascii_letters)
                       for _ in range(chars))

    def load_collection_docs(self,databases):
        '''We should be able to insert data into a collection for load tests'''
        insertions = 200
        total_insert = 0
        avg_insert = 0
        test_collections = ['mongo_collection', 'mongo_collection_one', 'mongo_collection_two']

        for collections in test_collections:
            start_time = time.time()
            for ins in range(insertions):
                insert_time = time.time()
                my_text = self.big_string(100)
                try:
                    x = self.db[collections].insert_one({"type": "Load Test",
                                                         "randString": my_text,
                                                         "created": insert_time,
                                                         "concurrency": 1})

                except Exception as e:
                    print ('Load Insert Failed: (%s)' % e)

                inserted_time = time.time()
                avg_insert = (inserted_time - start_time) / (ins + 1)
            total_insert = inserted_time

            total_insert_duration = total_insert - start_time
            print('%s.%s - inserted %d in %9.2f seconds' % (databases,
                                                            collections,
                                                            ins,
                                                            total_insert_duration))
            print('  - Avg insert time: %9.4f seconds' % avg_insert)
        return (total_insert_duration)

    def delete_collection_docs(self,databases):
        '''We should be able to delete a subset of documents from a collection'''

        deletes = 120
        total_delete = 0
        avg_delete = 0
        test_collections = ['mongo_collection', 'mongo_collection_one', 'mongo_collection_two']

        for collections in test_collections:
            start_time = time.time()
            for delete in range(deletes):
                delete_time = time.time()
                try:
                    result = self.db['mongo_collection'].delete_one({"randString": {"$exists": "true"}})
                    deleted += result.deleted_count

                except Exception as e:
                    print ('Delete Failed: (%s)' % e)
                    t.testcase.fail('Delete Failed')

                deleted_time = time.time()
                avg_delete = (deleted_time - start_time) / (delete + 1)
            total_delete = deleted_time

            total_delete_duration = total_delete - start_time
            print('%s.%s - Deleted %d in %9.2f seconds' % (databases,
                                                           collections,
                                                           deleted,
                                                           total_delete_duration))
            print(' - Avg delete time: %9.4f seconds' % avg_delete)
        return (total_delete_duration)

    def setUp(self):
        '''We should be able to create a connection, load and delete data for compaction tests'''
        test_dbs = ['mongo_test', 'mongo_test_one', 'mongo_test_two']

        self.conn = m.MongoClient('localhost', 27017,
                                  connectTimeoutMS=2000, socketTimeoutMS=2000)
        for databases in test_dbs:
            self.db = self.conn[databases]
            load_duration = self.load_collection_docs(databases)
            delete_duration = self.delete_collection_docs(databases)

    def test_compaction(self):
        '''We should be able to compact a collection'''

        s = self.db.command("collstats", 'mongo_collection')
        print (json.dumps(s, sort_keys=True, indent=4, separators=(',', ': ')))

        start_time = time.time()
        try:
            result = self.db.command("compact", 'mongo_collection')

        except Exception as e:
            print ('Copmcation Failed: (%s)' % e)
            t.testcase.fail('Compcation Failed')

        s = self.db.command("collstats", 'mongo_collection')
        print(json.dumps(s, sort_keys=True, indent=4, separators=(',', ': ')))
