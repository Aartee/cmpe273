'''
################################## server.py #############################
# 
################################## server.py #############################
'''
import time
import grpc
import datastore_pb2
import datastore_pb2_grpc
import rocksdb
from functools import wraps


from concurrent import futures

_ONE_DAY_IN_SECONDS = 60 * 60 * 24

arrDataDict = []

class MyDatastoreServicer(datastore_pb2_grpc.DatastoreServicer):
    '''
    '''

    def __init__(self):
        '''
        '''
        self.db = rocksdb.DB("db/master.db", rocksdb.Options(create_if_missing=True))
        self.totalConnections = 0
        print("init")

    def startReplication(self, request, context):
        '''
        Connect client follower and start replication
        '''

        myNumber = self.totalConnections
        arrDataDict.append([])
        self.totalConnections += 1
        print("Start Replication: " + str(myNumber))
        
        while True:
            if len(arrDataDict[myNumber]) != 0:
                data = arrDataDict[myNumber].pop(0)
                yield datastore_pb2.ResponseStream(key=data["key"], value=data["value"])

    def replicator(f):
        '''
        Replicator function which adds inserted values to the in memory queue for each follower client
        '''
        @wraps(f)
        def decorator_function(*args, **kwargs):
            for i in range(args[0].totalConnections):
                arrDataDict[i].append({"key": args[1].key, "value":args[1].value})
            return f(*args, **kwargs)

        return decorator_function
        

    @replicator
    def putData(self, request, context):
        '''
        Insert/Update data in RocksDB
        '''
        print(request)
        return datastore_pb2.GetPutResponse(key=request.key, value=request.value)

    def getData(self, request, context):
        '''
        Get Data from RocksDB
        '''
        return datastore_pb2.GetPutResponse(key="key", value="value")


def run(host, port):
    '''
    Run the GRPC server
    '''
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    datastore_pb2_grpc.add_DatastoreServicer_to_server(MyDatastoreServicer(), server)
    server.add_insecure_port('%s:%d' % (host, port))
    server.start()

    try:
        while True:
            print("Server started at...%d" % port)
            time.sleep(_ONE_DAY_IN_SECONDS)
    except KeyboardInterrupt:
        server.stop(0)


if __name__ == '__main__':
    run('0.0.0.0', 3000)