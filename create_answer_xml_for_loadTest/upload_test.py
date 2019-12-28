import subprocess
for i in range(490003330101, 490003330301):
	file_name = str(i) + ".xml"
	file_content = '<Response>\n<Conference startConferenceOnEnter="true" endConferenceOnExit="false" exitSound="beep:1" enterSound="beep:1" digitsMatch="006,007,008,009,010,011,013,014,*" callbackUrl="https://plivobin.non-prod.plivops.com/api/v1/' + str(i) + '.xml" maxMembers="10" record="true" recordFileFormat="mp3">' + str(i) + '_Conf </Conference>\n</Response>'
	fh = open(file_name,'w')
	fh.write(file_content)
	fh.close()
	out = subprocess.Popen(['curl', '-X', 'POST', 'https://plivobin.non-prod.plivops.com/api/v1/xml', '-F', 'file=@'+str(i)+'.xml'], stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
