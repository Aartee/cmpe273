'''
################################## client.py #############################
# 
################################## client.py #############################
'''
import grpc
import datastore_pb2
import datastore_pb2_grpc
import sys

Key = ""
Value = ""

class DatastoreClient():
    '''
    '''

    def __init__(self, host='0.0.0.0', port=3000):
        '''
        '''
        self.channel = grpc.insecure_channel('%s:%d' % (host, port))
        self.stub = datastore_pb2_grpc.DatastoreStub(self.channel)
        print("Client is running...")

    def put(self, key, value):
        '''
        '''
        print("Pushing Data to Master Database...")
        response = self.stub.putData(datastore_pb2.PutRequest(key=key, value=value))
        return response

    def get(self, key):
        '''
        '''
        response = self.stub.getData(datastore_pb2.GetRequest(key=key))
        return response

if len(sys.argv) == 3:
    Key = sys.argv[1]
    Value = sys.argv[2]
else:
    print("Invalid Arguments. Usage: pushData.py <key> <value>")
    exit()

client = DatastoreClient()

response = client.put(Key, Value)
print(response.key, response.value)