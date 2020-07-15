import subprocess, requests, json

#Upload XML file to plivobin
# try:
# 	for i in range(1000,2000):
# 		file_name_customer = 'MPC_TEST_XML_LOAD_' + str(i) + '_CUSTOMER.xml'
# 		file_name_agent = 'MPC_TEST_XML_LOAD_' + str(i) + '_AGENT.xml'
# 		file_name_supervisor = 'MPC_TEST_XML_LOAD_' + str(i) + '_SUPERVISOR.xml'
# 		file_content_customer = '<Response>\n<MultiPartyCall role="Customer" maxDuration="300" waitMusicUrl="http://plivobin.non-prod.plivops.com/api/v1/MPC_TEST_Wait.xml" agentHoldMusicUrl="http://plivobin.non-prod.plivops.com/api/v1/MPC_TEST_AGENT_HOLD.xml" customerHoldMusicUrl="http://plivobin.non-prod.plivops.com/api/v1/MPC_TEST_CUSTOMER_HOLD.xml" record="True" recordingCallbackUrl="http://plivobin.non-prod.plivops.com/api/v1/MPC_TEST_RECORDING.xml" enterSound="http://plivobin.non-prod.plivops.com/api/v1/MPC_TEST_ENTER_CUSTOMER.xml" exitSound="http://plivobin.non-prod.plivops.com/api/v1/MPC_TEST_EXIT_CUSTOMER.xml" statusCallbackUrl="http://3.6.226.68:7001/mpc_status" stayAlone="True">MPC_TEST_XML_LOAD_' + str(i) + '</MultiPartyCall>\n</Response>'
# 		file_content_agent = '<Response>\n<MultiPartyCall role="Agent" enterSound="http://plivobin.non-prod.plivops.com/api/v1/MPC_TEST_ENTER_AGENT.xml" exitSound="http://plivobin.non-prod.plivops.com/api/v1/MPC_TEST_EXIT_SUPERVISOR.xml">MPC_TEST_XML_LOAD_' + str(i) + '</MultiPartyCall>\n</Response>'
# 		file_content_supervisor = '<Response>\n<MultiPartyCall role="Supervisor" enterSound="http://plivobin.non-prod.plivops.com/api/v1/MPC_TEST_ENTER_SUPERVISOR.xml" exitSound="http://plivobin.non-prod.plivops.com/api/v1/MPC_TEST_EXIT_SUPERVISOR.xml">MPC_TEST_XML_LOAD_' + str(i) + '</MultiPartyCall>\n</Response>'
# 		fh_customer = open(file_name_customer,'w')
# 		fh_agent = open(file_name_agent,'w')
# 		fh_supervisor = open(file_name_supervisor,'w')
# 		fh_customer.write(file_content_customer)
# 		fh_agent.write(file_content_agent)
# 		fh_supervisor.write(file_content_supervisor)
# 		fh_customer.close()
# 		fh_agent.close()
# 		fh_supervisor.close()
# 		out = subprocess.Popen(['curl', '-X', 'POST', 'https://plivobin.non-prod.plivops.com/api/v1/xml', '-F', 'file=@' + file_name_customer], stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
# 		out = subprocess.Popen(['curl', '-X', 'POST', 'https://plivobin.non-prod.plivops.com/api/v1/xml', '-F', 'file=@' + file_name_agent],stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
# 		out = subprocess.Popen(['curl', '-X', 'POST', 'https://plivobin.non-prod.plivops.com/api/v1/xml', '-F', 'file=@' + file_name_supervisor],stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
# except Exception as e:
# 	print("Excpetion while uploading files. " + str(e))

#Add application. get app ID and add endpoint
url_application = 'https://api-qa.voice.plivodev.com/v1/Account/MAM2RLM2IZNDK3MDHINZ/Application/'
url_endpoint = 'https://api-qa.voice.plivodev.com/v1/Account/MAM2RLM2IZNDK3MDHINZ/Endpoint/'
headers_data = {'Content-Type': 'application/json'}

for i in range(1000,2000):
	with open('Customer.txt','a+') as fh:
		payload_app = {'app_name': 'MPC_TEST_XML_LOAD_' + str(i) + '_CUSTOMER', 'answer_url':'https://plivobin.non-prod.plivops.com/api/v1/MPC_TEST_XML_LOAD_' + str(i) + '_CUSTOMER.xml'}
		response = requests.post(url_application, data=json.dumps(payload_app), headers=headers_data, auth=('MAM2RLM2IZNDK3MDHINZ','MDBmNjZkODY0YzA2NGEwYWQ2ZjQ1NmE1ZTRkY2Qy'))
		app_id_customer = json.loads(response.content)['app_id']
		payload_endpoint = {'username':'MPCXMLLOADCUSTOMER','password':'plivo','alias':'VINAY_MPC_LOAD_XML_CUSTOMER_'+ str(i),'app_id':app_id_customer}
		response = requests.post(url_endpoint, data=json.dumps(payload_endpoint), headers=headers_data, auth=('MAM2RLM2IZNDK3MDHINZ','MDBmNjZkODY0YzA2NGEwYWQ2ZjQ1NmE1ZTRkY2Qy'))
		endpoint_id_customer = json.loads(response.content)['endpoint_id']
		endpoint_username_customer = json.loads(response.content)['username']
		endpoint_alias_customer = json.loads(response.content)['alias']
		fh.write(endpoint_alias_customer + ", " + endpoint_username_customer + ", " + endpoint_id_customer + "\n")

	with open('Agent.txt', 'a+') as fh:
		payload_app = {'app_name': 'MPC_TEST_XML_LOAD_' + str(i) + '_AGENT', 'answer_url':'https://plivobin.non-prod.plivops.com/api/v1/MPC_TEST_XML_LOAD_' + str(i) + '_AGENT.xml'}
		response = requests.post(url_application, data=json.dumps(payload_app), headers=headers_data, auth=('MAM2RLM2IZNDK3MDHINZ','MDBmNjZkODY0YzA2NGEwYWQ2ZjQ1NmE1ZTRkY2Qy'))
		app_id_agent = json.loads(response.content)['app_id']
		payload_endpoint = {'username':'MPCXMLLOADAGENT','password':'plivo','alias':'VINAY_MPC_LOAD_XML_AGENT_'+ str(i),'app_id':app_id_agent}
		response = requests.post(url_endpoint, data=json.dumps(payload_endpoint), headers=headers_data, auth=('MAM2RLM2IZNDK3MDHINZ','MDBmNjZkODY0YzA2NGEwYWQ2ZjQ1NmE1ZTRkY2Qy'))
		endpoint_id_agent = json.loads(response.content)['endpoint_id']
		endpoint_username_agent = json.loads(response.content)['username']
		endpoint_alias_agent = json.loads(response.content)['alias']
		fh.write(endpoint_alias_agent + ", " + endpoint_username_agent + ", " + endpoint_id_agent + "\n")

	with open('Supervisor.txt', 'a+') as fh:
		payload_app = {'app_name': 'MPC_TEST_XML_LOAD_' + str(i) + '_SUPERVISOR', 'answer_url':'https://plivobin.non-prod.plivops.com/api/v1/MPC_TEST_XML_LOAD_' + str(i) + '_SUPERVISOR.xml'}
		response = requests.post(url_application, data=json.dumps(payload_app), headers=headers_data, auth=('MAM2RLM2IZNDK3MDHINZ','MDBmNjZkODY0YzA2NGEwYWQ2ZjQ1NmE1ZTRkY2Qy'))
		app_id_supervisor = json.loads(response.content)['app_id']
		payload_endpoint = {'username':'MPCXMLLOADSUPERVISOR','password':'plivo','alias':'VINAY_MPC_LOAD_XML_SUPERVISOR_'+ str(i),'app_id':app_id_supervisor}
		response = requests.post(url_endpoint, data=json.dumps(payload_endpoint), headers=headers_data, auth=('MAM2RLM2IZNDK3MDHINZ','MDBmNjZkODY0YzA2NGEwYWQ2ZjQ1NmE1ZTRkY2Qy'))
		endpoint_id_supervisor = json.loads(response.content)['endpoint_id']
		endpoint_username_supervisor = json.loads(response.content)['username']
		endpoint_alias_supervisor = json.loads(response.content)['alias']
		fh.write(endpoint_alias_supervisor + ", " + endpoint_username_supervisor + ", " + endpoint_id_supervisor + "\n")