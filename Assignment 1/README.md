# Assignment 1

Implementing a dynamic Python invoker REST service. The service will have the following features:

## Usage Guide

Install the dependencies
```
source venv/bin/activate
pip2 install -r requirement.txt
```

Start the server with:
```
python2 server.py
```

## 1. Python Script Uploader

```bash
POST http://localhost:8000/api/v1/scripts
```

### Request


__foo.py__

```python
# foo.py
print("Hello World")
```

```bash
curl -i -X POST -H "Content-Type: multipart/form-data" 
-F "data=@/tmp/foo.py" http://localhost:8000/api/v1/scripts
```

```bash
HTTP/1.0 201 CREATED
Content-Type: application/json
Content-Length: 147
Server: Werkzeug/0.12.2 Python/2.7.13
Date: Tue, 17 Oct 2017 06:17:02 GMT
```

```json
{
    "scriptId": "1ad4c7c7-b302-11e7-84a0-60f81dc1f3c0", 
    "scriptLink": "localhost:8000/api/v1/scripts/1ad4c7c7-b302-11e7-84a0-60f81dc1f3c0"
}
```

## 2. Python Script Invoker

```bash
GET http://localhost:8000/api/v1/scripts/{script-id}
```

### Request

```bash
curl -i
http://localhost:8000/api/v1/scripts/1ad4c7c7-b302-11e7-84a0-60f81dc1f3c0
```

```bash
HTTP/1.0 200 OK
Content-Type: application/json
Content-Length: 16
Server: Werkzeug/0.12.2 Python/2.7.13
Date: Tue, 17 Oct 2017 06:15:10 GMT
```

```json
"Hello World"
```