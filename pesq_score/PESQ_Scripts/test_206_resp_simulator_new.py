import mimetypes
import os
import sys

from flask import Flask, request, send_file, Response

app = Flask(__name__)

@app.route('/get_mp3_file', methods = ['POST','GET'])
def send_file_partial():
    
    size = os.path.getsize('/home/ubuntu/0194f1ac-e621-11ea-8c3f-06f493bbae7d.mp3')    
    
    data = None
    with open('/home/ubuntu/0194f1ac-e621-11ea-8c3f-06f493bbae7d.mp3', 'rb') as f:
        data = f.read()

    end = str(int(size)-1024)
    rv = Response(data[1024:int(size)-1024], 206, mimetype='audio/mpeg', direct_passthrough=True)
    rv.headers.add('Content-Range', 'bytes {0}-{1}/{2}'.format('1024',end, size))

    return rv

if __name__ == '__main__':
        port_1 = int(sys.argv[1])
        app.run(host="0.0.0.0", port=port_1)
