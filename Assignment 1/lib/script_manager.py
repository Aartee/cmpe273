from db_manager import DBManager
import uuid
import os
import json
import subprocess
from werkzeug.utils import secure_filename

UPLOAD_DIRECTORY = os.path.dirname(os.path.realpath(__file__)) + '/../uploads/'
ALLOWED_FILE_EXTENSIONS = set(['py'])
HOST_ADDRESS = "localhost"
HOST_PORT = 8000

class ScriptManager():
    """
    Script upload and runn manager class
    """

    def __init__(self):
        self.db_manager = DBManager()
            
    def upload_script(self, request):
        """
        Upload python script on server and add that entry in database
            :param self: 
            :param request: http request parameter
        """   
        response = Response()
        file = self.get_file_object(request)
        if file is None:
            response.Error = "Please upload valid python file with .py extension."
            return response.toJSON(), 400

        unique_id = str(uuid.uuid1())

        upload_file_directory = os.path.join(UPLOAD_DIRECTORY, unique_id)
        if not os.path.exists(upload_file_directory):
            os.makedirs(upload_file_directory)

        filename = secure_filename(file.filename)
        file.save(os.path.join(upload_file_directory,filename))
        self.db_manager.add_file(unique_id, filename)
        response.scriptId = unique_id        
        response.scriptLink = HOST_ADDRESS + ":" + str(HOST_PORT) + "/api/v1/scripts/" + unique_id
        return response.toJSON(), 201

    def run_script(self, uuid):
        """
        Run uploaded python script on server with uuid and get the result of the file in return statement
            :param self: 
            :param uuid: 
        """   
        response = Response()
        filename = self.db_manager.get_file(uuid)
        if filename is None:
            response.Error = "Invalid Script. Script Not Found."
            return response.toJSON(), 400

        strFilePath = UPLOAD_DIRECTORY + uuid + '/' + filename
        cmd = "python " + strFilePath
        #cmd = "docker run -it --rm -v " + UPLOAD_DIRECTORY + uuid + ":/usr/src/myapp -w /usr/src/myapp ubuntu-python3.6-rocksdb-grpc:1.0 python3 " + filename
        cmd = cmd.split()

        sp = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, universal_newlines=True)
        out, err = sp.communicate()
        if err:
            return err.strip('\n')

        return out.strip('\n')

    def get_file_object(self,request):
        """
        Get file object from request object
        return None if something is wrong with the request else file object
            :param self: 
            :param request: 
        """   
        if 'data' not in request.files:
            return None
        file = request.files['data']
        if file.filename == '' or self.allowed_files(file.filename):
            return None
        return file

    def allowed_files(self,filename):
        return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() not in ALLOWED_FILE_EXTENSIONS

class Response():
    """
    Response format class
    """

    def toJSON(self):
        return json.dumps(self.__dict__)