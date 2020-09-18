from flask import Flask, request, Response
import json
import sys
app = Flask(__name__)

BIG_DICT = {}

@app.route('/status/', methods = ['POST','GET'])
def capture_data():
	if request.method == 'POST':
		data = request.form.to_dict(flat=False)
	else:
		data = request.args.to_dict(flat=False)
	MPCUUID = data['MPCUUID']
	if type(MPCUUID)==list:
		MPCUUID = MPCUUID[0]
	ParticipantCallUUID = data['ParticipantCallUUID']
	if type(ParticipantCallUUID)==list:
		ParticipantCallUUID = ParticipantCallUUID[0]
	EventName = data['EventName']
	if type(EventName)==list:
		EventName=EventName[0]

	if not BIG_DICT.get(MPCUUID,None):
		BIG_DICT[MPCUUID]={}
	
	if not BIG_DICT[MPCUUID].get(ParticipantCallUUID,None):
		BIG_DICT[MPCUUID][ParticipantCallUUID] = {}
	
	BIG_DICT[MPCUUID][ParticipantCallUUID][EventName] = {}
	
	for key in data:
		if type(data[key])==list:
			value=data[key][0]
		else:
			value=data[key]
		BIG_DICT[MPCUUID][ParticipantCallUUID][EventName][key] = value
	resp = Response(status=200)
	return resp

@app.route('/get_all_data', methods = ['GET'])
def get_all_data():	
	js = json.dumps(BIG_DICT)
	resp = Response(js, status=200, mimetype='application/json')
	return resp

@app.route('/get_mpc/<mpc_uuid>', methods = ['GET'])
def get_mpc(mpc_uuid):
        js = json.dumps(BIG_DICT[mpc_uuid])
        resp = Response(js, status=200, mimetype='application/json')
        return resp

@app.route('/get_participant/<mpc_uuid>/<participant_uuid>', methods = ['GET'])
def get_participant(mpc_uuid,participant_uuid):
        js = json.dumps(BIG_DICT[mpc_uuid][participant_uuid])
        resp = Response(js, status=200, mimetype='application/json')
        return resp

@app.route('/get_all_events/<mpc_uuid>', methods = ['GET'])
def get_all_events(mpc_uuid):
	mpc_data = BIG_DICT[mpc_uuid]
	event_dict = {}
	for participant_uuid in mpc_data.keys():
		for event_type in BIG_DICT[mpc_uuid][participant_uuid]:
			if not event_dict.get(event_type,None):
				event_dict[event_type]=[]
			event_dict[event_type].append(BIG_DICT[mpc_uuid][participant_uuid][event_type])
	js = json.dumps(event_dict)
	resp = Response(js, status=200, mimetype='application/json')
	return resp

@app.route('/del_mpc/<mpc_uuid>', methods = ['DELETE'])
def del_mpc_data(mpc_uuid):
	if BIG_DICT.get(mpc_uuid, None):
		del BIG_DICT[mpc_uuid]
	resp = Response(status=202)
	return resp

if __name__ == '__main__':
	port_1 = int(sys.argv[1])
	app.run(host="0.0.0.0", port=port_1)

