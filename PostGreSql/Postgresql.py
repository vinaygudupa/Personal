import psycopg2
import sshtunnel

sshtunnel.SSH_TIMEOUT = 10.0
sshtunnel.TUNNEL_TIMEOUT = 10.0


class Postgresql(object):
    def __init__(self):
        self.server = None
        self.conn = None
        self.cur = None
        self.jumpBox_ip = '52.53.41.213'
        self.jumpBox_User = 'qa-automation'
        self.jumpBox_pkeyFile = '/Users/vinay/Python_Dir/Personal/PostGreSql/sipp-qa-automation.pem'
        self.jumpBox_loopbackIP = '127.0.0.1'
        self.databases = [
            'plivo_cloud_logs', 'dblog-master-qa.voice.plivodev.com', 'plivolog', 'hello', '5432']

    def _create_ssh_tunnel_to_DbLog(self):
        try:
            print("Inside tunnel creation")
            self.server = sshtunnel.SSHTunnelForwarder((self.jumpBox_ip, 22), ssh_username=self.jumpBox_User,
                                                       ssh_pkey=self.jumpBox_pkeyFile,
                                                       remote_bind_address=(self.databases[1],
                                                                            int(self.databases[4])), logger=sshtunnel.create_logger(loglevel=1))
            self.server.start()
            print("Tunnel creation success at port " +
                  str(self.server.local_bind_port))
        except Exception as e:
            print("Vinay : Tunnel creation failed with reason : " + str(e))

    def _connect_to_dbLog(self):
        try:
            if not self.server:
                self._create_ssh_tunnel_to_DbLog()
            self.conn = psycopg2.connect(database=self.databases[0],
                                         user=self.databases[2],
                                         password=self.databases[3],
                                         host=self.jumpBox_loopbackIP,
                                         port=self.server.local_bind_port)
        except Exception as e:
            print("Vinay : Connection creation failed with reason : " + str(e))

    def execute_select_command(self, command):
        try:
            if not self.conn:
                self._connect_to_dbLog()
            self.cur = self.conn.cursor()
            self.cur.execute(command)
            rows = self.cur.fetchall()
            return rows
        except Exception as e:
            print("Vinay : Command execution failed with reason : " + str(e))

    def close_db_conection(self):
        self.conn.close()
        self.server.stop()
        self.server.close()


if __name__ == '__main__':
    DB = Postgresql()
    m = DB.execute_select_command(
        "SELECT extra_data FROM plivo_logs_calldetailrecord_m7 WHERE call_uuid='13f2d7aa-af73-11e9-8ecd-f97804229c4f'")
    print(m)
