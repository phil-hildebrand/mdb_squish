#!/usr/bin/env python
# -*- coding: utf-8 -*-
import pymongo as m

def test_connection():

    #############################################################################
    #    Connection details
    #############################################################################
    
    try:
        conn = m.MongoClient('mongodb://localhost:27017/')
        info = conn.server_info()
        print(' Connected : %s' % info)
    
    except Exception as e:
        print('Fatal: Could not connect to mongo database')
        sys.exit(2)

