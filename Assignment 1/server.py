from flask import Flask, request
from flask_restful import Resource, Api
import rocksdb
from lib.script_manager import ScriptManager

app = Flask(__name__)

api = Api(app)

script_manager = ScriptManager()

class ScriptUploader(Resource):
    def post(self):
        return script_manager.upload_script(request)

class ScriptGetter(Resource):
    def get(self, uuid):
        return script_manager.run_script(uuid)

api.add_resource(ScriptUploader, '/api/v1/scripts')
api.add_resource(ScriptGetter, '/api/v1/scripts/<uuid>')

if __name__ == "__main__":    
    app.run(host='localhost', port=8000)