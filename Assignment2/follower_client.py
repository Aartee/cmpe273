'''
################################## client.py #############################
# 
################################## client.py #############################
'''
import grpc
import datastore_pb2
import datastore_pb2_grpc

class DatastoreClient():
    '''
    '''

    def __init__(self, host='0.0.0.0', port=3000):
        '''
        '''
        self.channel = grpc.insecure_channel('%s:%d' % (host, port))
        self.stub = datastore_pb2_grpc.DatastoreStub(self.channel)

    def connect(self):
        '''
        '''
        resp = self.stub.startReplication(datastore_pb2.Request())
        for data in resp:
            print(data.key, data.value)


print("Client is running...")
client = DatastoreClient()

client.connect()
