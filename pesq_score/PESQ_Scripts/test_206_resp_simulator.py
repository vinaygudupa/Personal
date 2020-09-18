import mimetypes
import os
import re

from flask import request, send_file, Response

app = Flask(__name__)

@app.route('/get_mp3_file', methods = ['POST','GET'])
def send_file_partial():
    
    range_header = request.headers.get('Range', None)
    if not range_header: 
        return send_file(path)
    
    size = os.path.getsize('/home/ubuntu/0194f1ac-e621-11ea-8c3f-06f493bbae7d.mp3')    
    byte1, byte2 = 0, None
    
    m = re.search('(\d+)-(\d*)', range_header)
    g = m.groups()
    
    if g[0]: byte1 = int(g[0])
    if g[1]: byte2 = int(g[1])

    length = size - byte1
    if byte2 is not None:
        length = byte2 - byte1
    
    data = None
    with open(path, 'rb') as f:
        f.seek(byte1)
        data = f.read(length)

    rv = Response(data, 206, mimetype='audio/mpeg', direct_passthrough=True)
    rv.headers.add('Content-Range', 'bytes {0}-{1}/{2}'.format(byte1, byte1 + length - 1, size))

    return rv

if __name__ == '__main__':
        port_1 = int(sys.argv[1])
        app.run(host="0.0.0.0", port=port_1)
