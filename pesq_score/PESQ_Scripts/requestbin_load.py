from flask import Flask, request, Response
import json
import sys
import time
app = Flask(__name__)

BIG_LIST = []
counter = 0
@app.route('/mpc_status', methods = ['POST','GET'])
def capture_data():
    global counter
    headers_dict = {}
    for key in request.headers:
        headers_dict[key[0]]=request.headers[key[0]]
    form_data = request.form.to_dict(flat=False)
    for key in form_data:
        form_data[key]=form_data[key][0]
    query_string = request.args.to_dict(flat=False)
    for key in query_string:
        query_string[key]=query_string[key][0]
    if form_data:
        data = form_data
    else:
        data = query_string
    counter += 1
    print(data['MPCName'] + "  " + data['MPCUUID'] + "   " + data['EventName'] + "   " + str(counter))
    request_data = {'form_data':form_data, 'headers':headers_dict, 'query_string':query_string}
    resp = Response(status=200)
    return resp

@app.route('/mpc_status/requests', methods = ['GET'])
def get_all_data():
    js = json.dumps(BIG_LIST)
    resp = Response(js, status=200, mimetype='application/json')
    return resp

if __name__ == '__main__':
    port_1 = int(sys.argv[1])
    app.run(host="0.0.0.0", port=port_1)
