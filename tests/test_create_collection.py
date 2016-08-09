#!/usr/bin/env python
# -*- coding: utf-8 -*-
import pymongo as m
import test_connection
from unittest import TestCase

def create():

    try:
        test_connection.connect()
        db = conn['mongo_test']
        db.mongo_collection.count()
        return True
    
    except Exception as e:
        return False

class test_connection(TestCase):
    def test(self):
        self.assertTrue(create())
