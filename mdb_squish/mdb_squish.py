#!/usr/bin/python
# -*- coding: utf-8 -*-
import argparse
import glob
import json
import logging as log
import os
import pymongo as m
import re
import sys
import time
from multiprocessing.pool import ThreadPool

###############################################################################

databases = []
collections = dict([])

###############################################################################
#    Routine to verify file/directory exists
###############################################################################


def verify_file(f):
    if not os.path.exists(f):
        print ("Fatal: %s does not exist, exiting program." % f)
        log.error('  %s does not exist, exiting program.' % f)
        sys.exit(2)


###############################################################################
#    Compact collections
###############################################################################


def compact(collection_args):
    my_collection_db, my_collection, my_concurrency, my_stats_dir = collection_args
    db = conn[my_collection_db]
    stats = db.command("collstats", my_collection)
    before = stats['storageSize']
    log.debug(' - compacting collection %s.%s (%d Bytes)' % (my_collection_db, my_collection, before))
    start_time = time.time()
    s = db.command("compact", my_collection)
    duration = time.time() - start_time
    stats = db.command("collstats", my_collection)
    after = stats['storageSize']
    log.debug(' - compacted collection %s.%s (%d Bytes)' % (my_collection_db, my_collection, after))
    diff = before - after
    return (my_collection_db, my_collection, s, diff, duration)

###############################################################################
#    Parse Comandline Options
###############################################################################

parser = argparse.ArgumentParser()
parser.add_argument('-v', '--verbose', action='store_true',
                    help='increase output verbosity')
parser.add_argument('-s', '--server', default='localhost',
                    help='MongoDB Host Server Name (short name only)')
parser.add_argument('-p', '--port', type=int, default=27017,
                    help='MongoDB Port (default=27017)')
parser.add_argument('-d', '--database', nargs='+', default='all',
                    help='limit stats to database X (default=all)')
parser.add_argument('--collections', nargs='+',
                    help='limit compaction to these collections')
parser.add_argument('-c', '--concurrency', default=3, type=int,
                    help='# of compaction threads (default=3)')
parser.add_argument('-r', '--stats-rate', default=2, type=int,
                    help='update stats file after x compcations (default=2)')
parser.add_argument('--log-dir', default='/var/log',
                    help='MongoDB Get compaction log file location (default=/var/log)')
parser.add_argument('--stats-dir', default='/tmp',
                    help='MongoDB compaction stats dump file location (default=/tmp/<server>.mdb_squish_stats')
args = parser.parse_args()

###############################################################################
#    Setup Logging Options
###############################################################################

baselevel = log.INFO

if args.verbose:
    baselevel = log.DEBUG
    log.basicConfig(filename='%s/mdb_squish.log' % args.log_dir,
                    format='%(asctime)s %(levelname)s: %(message)s',
                    level=baselevel)
else:
    log.basicConfig(filename='%s/mdb_squish.log' % args.log_dir,
                    format='%(asctime)s %(levelname)s: %(message)s',
                    level=baselevel)

# Log to console as well

formatter = log.Formatter('%(levelname)s: %(message)s')

console = log.StreamHandler()
console.setLevel(baselevel)
console.setFormatter(formatter)

log.getLogger('').addHandler(console)

log.info('******** Gathering Stats/Configs *********')

if args.server:
    mongo_host = args.server
    stats_dir = '%s/%s' % (args.stats_dir, mongo_host)
    log.debug('DB Host: %s' % mongo_host)

if not os.path.exists(stats_dir):
    os.makedirs(stats_dir)

if args.port:
    mongo_port = args.port
    log.debug('DB Port: %s' % mongo_port)

log.debug('Verbose output.')


verify_file(args.log_dir)
verify_file(stats_dir)

###############################################################################
#    Connection details
###############################################################################

log.debug('Attempting to connecting to %s:%s' % (mongo_host, mongo_port))

try:
    conn = m.MongoClient('mongodb://%s:%s/' % (mongo_host, mongo_port))
    info = conn.server_info()
    log.debug(' Connected : %s' % info)

except Exception as e:
    print ("Fatal: could not establish database connection to %s:%s, exiting program." % (mongo_host, mongo_port))
    log.error('No database connection could be established.')
    log.error(e)
    sys.exit(2)

###############################################################################
#    Parse database and collection list and run compactions in parallel
###############################################################################

compact_collections = []
collection_stats = {}
total_compacted = 0
total_duration = 0.0
total_collections = 1.0
pool = ThreadPool(args.concurrency)
skip_dbs = ['local', 'admin']
skip_collections = ['system.namespaces', 'system.indexes',
                    'system.profile', 'system.js']

if args.database[0] != 'all':
    compact_db = args.database[0]
    db = conn[compact_db]
    if compact_db not in skip_dbs:
        log.debug('Compacting all collections in database %s' % compact_db)
        for collection in db.collection_names():
            if collection not in skip_collections:
                log.debug('Scheduling Compaction for collection %s' % collection)
                collection_stats[collection] = {'name': collection, 'compacted': 0,
                                                'initial_size': 'unknown',
                                                'compacted_size': 'unknown',
                                                'saved': 0, 'duration': 0.0}
                compact_collections.append([compact_db, collection, args.concurrency, args.stats_dir])
else:

    ###############################################################################
    #    If collection objects not filtered, Get full database and table list
    #     and run compactions in parallel
    ###############################################################################

    log.debug('Compacting all collections in all databases')
    for compact_db in conn.database_names():
        if compact_db not in skip_dbs:
            db = conn[compact_db]
            for collection in db.collection_names():
                if collection not in skip_collections:
                    collection_stats[collection] = {'name': collection, 'compacted': 0,
                                                    'initial_size': 'unknown',
                                                    'compacted_size': 'unknown',
                                                    'saved': 0, 'duration': 0.0}
                    log.debug('Scheduling compaction for %s' % collection)
                    compact_collections.append([compact_db, collection, args.concurrency, args.stats_dir])

#######################################################################################
#    Compact collections in parallel, and log timings per collection
#######################################################################################

for (compact_db, collection, stats, diff, duration) in pool.imap(compact, compact_collections):
    # Don't allow '/' to occur in collection name output
    collection = re.sub(r'\/', '_', collection)
    total_compacted = total_compacted + diff
    total_duration = total_duration + duration
    avg_duration = total_duration / total_collections
    total_collections += 1.0
    collection_stats[collection]['saved'] = diff
    collection_stats[collection]['duration'] = duration
    collection_stats[collection]['compacted'] = 1
    log.debug('%s.%s stats: \n%s (%d, %0.4f)\n' % (compact_db, collection, stats, diff, duration))
    log.debug('\n  %s \n' % (json.dumps(collection_stats)))
    if (total_collection % stats_rate) == 0:
        with open('%s/mdb_squish_%s_stats.json' % (stats_dir, compact_db, collection), 'w') as outfile:
            json.dump(collection_stats, outfile)

log.info(' Total space saved via compaction: %d Bytes' % total_compacted)
log.info(' Total Time for compacting all collections: %0.4f Seconds' % total_duration)
log.info(' Avg Time to compact a collection: %0.4f Seconds' % avg_duration)
log.info('=======Mongo CompactionComplete.========')
