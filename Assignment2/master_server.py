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

from concurrent import futures

_ONE_DAY_IN_SECONDS = 60 * 60 * 24

class MyDatastoreServicer(datastore_pb2_grpc.DatastoreServicer):
    '''
    '''

    def __init__(self):
        '''
        '''
        self.db = rocksdb.DB("master.db", rocksdb.Options(create_if_missing=True))
        print("init")

    def startReplication(self, request, context):
        '''
        '''
        print("Start Replication: ")
        for i in range(0,10):
            time.sleep( 5 )
            yield datastore_pb2.ResponseStream(key=str(i), value=str(i))
        

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