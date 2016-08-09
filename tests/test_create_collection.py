#!/usr/bin/env python
# -*- coding: utf-8 -*-
import pymongo as m
import test_connection
from unittest import TestCase
SHOW_ERROR_MESSAGES = True

def create():

    try:
        test_connection.connect()
        db = conn['mongo_test']
        db['mongo_collection'].count()
        return(db)
    
    except Exception as e:
        print(e)
        return False

def get_count(xdb):
    try:
        count =xdb['mongo_collection'].count()
        return(count)
    
    except Exception as e:
        print(e)
        return False

class test_connection(TestCase):
    def test(self):
        mydb = create()
        if (mydb):
            self.assertTrue(get_count(my_db))
        else
            self.assertTrue(False)
