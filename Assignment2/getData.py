'''
################################## client.py #############################
# 
################################## client.py #############################
'''

import rocksdb
import sys

Key = ""
DatabaseName = ""

if len(sys.argv) == 3:
    FollowerId = sys.argv[1]
    Key = sys.argv[2]
else:
    print("Invalid Arguments. Usage: getData.py <follower_client_id> <key>")
    exit()

DatabaseName = "db/follower_" + FollowerId + ".db"

db = rocksdb.DB(DatabaseName,rocksdb.Options(create_if_missing=False))
Value = db.get(Key)

print(Key, Value)
