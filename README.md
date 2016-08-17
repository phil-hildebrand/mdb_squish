
# MDB_Squish
 
 *_MongoDB Parallel Compaction Tool_*

![Build Status](https://travis-ci.org/phil-hildebrand/mdb_squish.svg?branch=master)

## Overview

 MDB Squish is a tool that can be pointed at a MongoDB database to run collection
compaction in parallel for any or all collections.  It will also keep statistics on
how much space compaction is saving and crude estimates of completion / run time.

## Requirements

- Python 2.7 or 3.5 _it may work with other versions, but this is what's tested_
- Mongo >= 3.2 _it may work with other versions, but this is waht's testsed_

## Installation

- `pip install git+https://github.com/phil-hildebrand/mdb_squish.git@{release}` (_IE: v0.1.1_)

  *_or_*
  

- `pip install git+https://github.com/phil-hildebrand/mdb_squish.git`  (_for latest release_)


## Usage

```
usage: mdb_squish [-h] [-v] [-s SERVER] [-p PORT] [-d DATABASE [DATABASE ...]]
                  [--collections COLLECTIONS [COLLECTIONS ...]]
                  [-c CONCURRENCY] [--log-dir LOG_DIR] [--stats-dir STATS_DIR]

optional arguments:
  -h, --help            show this help message and exit
  -v, --verbose         increase output verbosity
  -s SERVER, --server SERVER
                        MongoDB Host Server Name (short name only)
  -p PORT, --port PORT  MongoDB Port (default=27017)
  -d DATABASE [DATABASE ...], --database DATABASE [DATABASE ...]
                        limit stats to database X (default=all)
  --collections COLLECTIONS [COLLECTIONS ...]
                        limit compaction to these collections
  -c CONCURRENCY, --concurrency CONCURRENCY
                        # of compaction threads (default=3)
  -r RATE, --rate RATE  update stats file after x compcations (default=2)
  --log-dir LOG_DIR     MongoDB Get compaction log file location
                        (default=/var/log)
  --stats-dir STATS_DIR
                        MongoDB compaction stats dump file location
                        (default=/tmp/)
```

### Statistics

 MDB Squish will dump a stats file per database in the stats-dir.
By default, the stats-dir is /tmp.  Each stat file is json output and
named `mdb_stats_<dbname>.json`.

 Example Data:
```
{
    "mongo_collection": {
        "compacted": 1,
        "compacted_size": 125,
        "duration": 0.0009090900421142578,
        "initial_size": 75,
        "name": "mongo_collection",
        "saved": -4096
    },
    "mongo_collection_one": {
        "compacted": 1,
        "compacted_size": 125,
        "duration": 0.005066871643066406,
        "initial_size": 75,
        "name": "mongo_collection_one",
        "saved": 0
    },
    "mongo_collection_two": {
        "compacted": 1,
        "compacted_size": 125,
        "duration": 0.0020208358764648438,
        "initial_size": 75,
        "name": "mongo_collection_two",
        "saved": 86016
    }
}
```

## Known Issues

- Currently it does not support auth based access for Mongo
- Current version does not have a feature to ignore/skip collections that were
   recently compacted

