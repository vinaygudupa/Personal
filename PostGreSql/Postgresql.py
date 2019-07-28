from robot.api import logger
import psycopg2
from sshtunnel import SSHTunnelForwarder


class Postgresql(object):
    def __init__(self, data, user, jumpbox):
        self.server = None
        self.conn = None
        self.cur = None
        self.jumpBox_ip = jumpbox.host
        self.jumpBox_User = jumpbox.user
        self.jumpBox_pkeyFile = jumpbox.key
        self.jumpBox_loopbackIP = jumpbox.loopback_IP
        self.databases = data['databases']

    def _create_ssh_tunnel_to_DbLog(self):
        try:
            self.server = SSHTunnelForwarder((self.jumpBox_ip, 22), ssh_username=self.jumpBox_User,
                                             ssh_pkey='/Users/viddnay/.ssh/id_rsa',
                                             remote_bind_address=(self.databases['dblog']['host'],
                                                                  int(self.databases['dblog']['port'])))
            self.server.start()
        except Exception as e:
            logger.info('Vinay : Jump server tunnel failed : ' +
                        str(e), also_console='true')

    def _connect_to_dbLog(self,):
        try:
            if not self.server:
                self._create_ssh_tunnel_to_DbLog()
            self.conn = psycopg2.connect(database=self.databases['dblog']['name'],
                                         user=self.databases['dblog']['user'],
                                         password=self.databases['dblog']['password'],
                                         host=self.jumpBox_loopbackIP,
                                         port=self.server.local_bind_port)
        except Exception as e:
            logger.info("DB connection failed with reason : ", str(e))

    def execute_select_command(self, command):
        try:
            if not self.conn:
                self._connect_to_dbLog()
            self.cur = self.conn.cursor()
            self.cur.execute(command)
            rows = self.cur.fetchall()
            return rows
        except Exception as e:
            logger.info("Command execution failed with reason : " +
                        str(e), also_console='true')

    def get_nested_value_from_resp(self, input_data='', key_list=''):
        try:
            if input_data != '':
                command_response = input_data
                if key_list != '':
                    for key in key_list:
                        key = str(key)
                        if key.isdigit():
                            key = int(key)
                        command_response = command_response[key]
                    return command_response
                else:
                    logger.info('Key list is empty', also_console='true')
            else:
                logger.info('Select command did not return response',
                            also_console='true')
        except Exception as e:
            logger.info("Command failed with reason : " +
                        str(e), also_console='true')

    def close_db_conection(self):
        self.conn.close()
        self.server.stop()
        self.server.close()
