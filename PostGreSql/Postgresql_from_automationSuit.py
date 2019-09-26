from robot.api import logger
import psycopg2
import sshtunnel
import datetime
import json

sshtunnel.SSH_TIMEOUT = 10.0
sshtunnel.TUNNEL_TIMEOUT = 10.0

EXPECTED_DIMENSIONS_DATA_IN_CDR = {
    "INBOUND":{
        "SOURCE": {
            "SIP_INTERNAL": {
                "source_number_type": "SIP_INTERNAL",
                "source_client_type": "OTHER",
                "source_client_sdk_version_major": "UNKNOWN",
                "source_client_sdk_version_minor": "UNKNOWN",
                "source_client_sdk_version_patch": "UNKNOWN"
            },
            "ANDROID": {
                "source_number_type": "SIP_INTERNAL",
                "source_client_type": "ANDROID_SDK",
                "source_client_sdk_version_major": "2",
                "source_client_sdk_version_minor": "0",
                "source_client_sdk_version_patch": "5"
            },
            "IOS": {
                "source_number_type": "SIP_INTERNAL",
                "source_client_type": "IOS_SDK",
                "source_client_sdk_version_major": "2",
                "source_client_sdk_version_minor": "1",
                "source_client_sdk_version_patch": "4"
            },
            "PSTN": {
                "source_number_type": "PSTN",
                "source_client_type": "UNKNOWN",
                "source_client_sdk_version_major": "UNKNOWN",
                "source_client_sdk_version_minor": "UNKNOWN",
                "source_client_sdk_version_patch": "UNKNOWN"
            },
            "SIP_EXTERNAL": {
                "source_number_type": "SIP_EXTERNAL",
                "source_client_type": "OTHER",
                "source_client_sdk_version_major": "UNKNOWN",
                "source_client_sdk_version_minor": "UNKNOWN",
                "source_client_sdk_version_patch": "UNKNOWN"
            },
            "IOS_DEFAULT": {
                "source_number_type": "SIP_INTERNAL",
                "source_client_type": "IOS_SDK",
                "source_client_sdk_version_major": "2",
                "source_client_sdk_version_minor": "0",
                "source_client_sdk_version_patch": "0"
            },
            "ANDROID_DEFAULT": {
                "source_number_type": "SIP_INTERNAL",
                "source_client_type": "ANDROID_SDK",
                "source_client_sdk_version_major": "2",
                "source_client_sdk_version_minor": "0",
                "source_client_sdk_version_patch": "0"
            }
        },
        "DESTINATION": {
            "SIP_INTERNAL": {
                "destination_number_type": "SIP_INTERNAL",
                "destination_client_type": "UNKNOWN",
                "destination_client_sdk_version_major": "UNKNOWN",
                "destination_client_sdk_version_minor": "UNKNOWN",
                "destination_client_sdk_version_patch": "UNKNOWN"
            },
            "PSTN": {
                "destination_number_type": "PSTN",
                "destination_client_type": "UNKNOWN",
                "destination_client_sdk_version_major": "UNKNOWN",
                "destination_client_sdk_version_minor": "UNKNOWN",
                "destination_client_sdk_version_patch": "UNKNOWN"
            },
            "FIXED": {
                "destination_number_type": "FIXED",
                "destination_client_type": "UNKNOWN",
                "destination_client_sdk_version_major": "UNKNOWN",
                "destination_client_sdk_version_minor": "UNKNOWN",
                "destination_client_sdk_version_patch": "UNKNOWN"
            },
            "MOBILE": {
                "destination_number_type": "MOBILE",
                "destination_client_type": "UNKNOWN",
                "destination_client_sdk_version_major": "UNKNOWN",
                "destination_client_sdk_version_minor": "UNKNOWN",
                "destination_client_sdk_version_patch": "UNKNOWN"
            },
            "TOLLFREE": {
                "destination_number_type": "TOLLFREE",
                "destination_client_type": "UNKNOWN",
                "destination_client_sdk_version_major": "UNKNOWN",
                "destination_client_sdk_version_minor": "UNKNOWN",
                "destination_client_sdk_version_patch": "UNKNOWN"
            }
        }
    },
    "OUTBOUND":{
        "SOURCE": {
            "PSTN": {
                "source_number_type": "PSTN",
                "source_client_type": "UNKNOWN",
                "source_client_sdk_version_major": "UNKNOWN",
                "source_client_sdk_version_minor": "UNKNOWN",
                "source_client_sdk_version_patch": "UNKNOWN"
            }
        },
        "DESTINATION": {
            "SIP_INTERNAL": {
                "destination_number_type": "SIP_INTERNAL",
                "destination_client_type": "OTHER",
                "destination_client_sdk_version_major": "UNKNOWN",
                "destination_client_sdk_version_minor": "UNKNOWN",
                "destination_client_sdk_version_patch": "UNKNOWN"
            },
            "ANDROID": {
                "destination_number_type": "SIP_INTERNAL",
                "destination_client_type": "ANDROID_SDK",
                "destination_client_sdk_version_major": "2",
                "destination_client_sdk_version_minor": "0",
                "destination_client_sdk_version_patch": "5"
            },
            "IOS": {
                "destination_number_type": "SIP_INTERNAL",
                "destination_client_type": "IOS_SDK",
                "destination_client_sdk_version_major": "2",
                "destination_client_sdk_version_minor": "1",
                "destination_client_sdk_version_patch": "4"
            },
            "PSTN": {
                "destination_number_type": "PSTN",
                "destination_client_type": "UNKNOWN",
                "destination_client_sdk_version_major": "UNKNOWN",
                "destination_client_sdk_version_minor": "UNKNOWN",
                "destination_client_sdk_version_patch": "UNKNOWN"
            },
            "SIP_EXTERNAL": {
                "destination_number_type": "SIP_EXTERNAL",
                "destination_client_type": "OTHER",
                "destination_client_sdk_version_major": "UNKNOWN",
                "destination_client_sdk_version_minor": "UNKNOWN",
                "destination_client_sdk_version_patch": "UNKNOWN"
            },
            "IOS_DEFAULT": {
                "destination_number_type": "SIP_INTERNAL",
                "destination_client_type": "IOS_SDK",
                "destination_client_sdk_version_major": "2",
                "destination_client_sdk_version_minor": "0",
                "destination_client_sdk_version_patch": "0"
            },
            "ANDROID_DEFAULT": {
                "destination_number_type": "SIP_INTERNAL",
                "destination_client_type": "ANDROID_SDK",
                "destination_client_sdk_version_major": "2",
                "destination_client_sdk_version_minor": "0",
                "destination_client_sdk_version_patch": "0"
            },
            "SIP_NON_EXISTANT": {
                "destination_number_type": "SIP_INTERNAL",
                "destination_client_type": "UNKNOWN",
                "destination_client_sdk_version_major": "UNKNOWN",
                "destination_client_sdk_version_minor": "UNKNOWN",
                "destination_client_sdk_version_patch": "UNKNOWN"
            },
            "SIP_UNREG": {
                "destination_number_type": "SIP_INTERNAL",
                "destination_client_type": "UNKNOWN",
                "destination_client_sdk_version_major": "UNKNOWN",
                "destination_client_sdk_version_minor": "UNKNOWN",
                "destination_client_sdk_version_patch": "UNKNOWN"
            }
        }
    }
}

class Postgresql(object):

    ROBOT_LIBRARY_SCOPE = 'TEST SUITE'

    def __init__(self, data, user, jumpbox):
        logger.info(
            "Creating SSH Tunnel and PostgreSQL DB connection......", also_console='true')
        self.server = None
        self.conn = None
        self.cur = None
        self.jumpBox_ip = jumpbox.host
        self.jumpBox_User = jumpbox.user
        self.jumpBox_pkey = jumpbox.key
        self.jumpBox_loopbackIP = jumpbox.loopback_IP
        self.databases = data['databases']

    def _create_ssh_tunnel_to_DbLog(self):
        try:
            self.server = sshtunnel.SSHTunnelForwarder((self.jumpBox_ip, 22), ssh_username = self.jumpBox_User, ssh_pkey = self.jumpBox_pkey, remote_bind_address=(self.databases['dblog']['host'], int(self.databases['dblog']['port'])))
            self.server.start()
        except Exception as e:
            logger.info('Jump server tunnel failed : ' +
                        str(e), also_console='true')

    def _connect_to_dbLog(self):
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
            logger.info("PostgreSql select Command execution failed with reason : " +
                        str(e), also_console='true')

    def get_dimensions_from_cdr(self, call_uuid):
        try:
            month = str(datetime.datetime.now()).split(' ')[0].split('-')[1]
            if month[0] == '0':
                month = month[1:]
            command = "SELECT extra_data FROM plivo_logs_calldetailrecord_m" + month + " WHERE call_uuid='" + call_uuid + "'"
            extra_data = self.execute_select_command(command)
            dimensions = extra_data[0][0]['dimensions']
            return dimensions
        except Exception as e:
            logger.info("PostgreSql get dimensions failed with reason : " + str(e), also_console='true')

    def merge_dict(self, dict_a, dict_b):
        z = dict_a.copy()
        z.update(dict_b)
        return z

    def verify_dimensions_from_cdr(self, call_uuid, direction, source_type, destination_type, media_server_ip, application_type='XML', application_id='NOT_APPLICABLE',carrier_mediaserver_ip='NOT_APPLICABLE',carrier_priority=0):
        try:
            if isinstance(call_uuid,list):
                call_uuid = call_uuid[0]
            dimensions = self.get_dimensions_from_cdr(call_uuid)
            if direction == 'inbound':
                DIRECTION = 'INBOUND'
                application_dict = {
                    "application_type":application_type,
                    "application_id":application_id
                }
                if source_type == "PSTN":
                    carrier_dict = {
                        "carrier_mediaserver_ip":carrier_mediaserver_ip,
                        "outgoing_carrier_priority":0
                    }
                else:
                    carrier_dict = {
                        "carrier_mediaserver_ip":"NOT_APPLICABLE",
                        "outgoing_carrier_priority":0
                    }
            else:
                DIRECTION = 'OUTBOUND'
                application_dict = {
                    "application_type": "NOT_APPLICABLE",
                    "application_id": "NOT_APPLICABLE"
                }
                if destination_type == "PSTN":
                    carrier_dict = {
                        "carrier_mediaserver_ip": media_server_ip,
                        "outgoing_carrier_priority": carrier_priority
                    }
                else:
                    carrier_dict = {
                        "carrier_mediaserver_ip": "NOT_APPLICABLE",
                        "outgoing_carrier_priority": 0
                    }

            source_dict = EXPECTED_DIMENSIONS_DATA_IN_CDR[DIRECTION]["SOURCE"][source_type]
            dest_dict = EXPECTED_DIMENSIONS_DATA_IN_CDR[DIRECTION]["DESTINATION"][destination_type]
            media_server_dict = {
                "count_of_plivo_mediaservers":1,
                "first_plivo_mediaserver_ip":media_server_ip,
                "last_plivo_mediaserver_ip":media_server_ip
            }

            temp_1 = self.merge_dict(source_dict,dest_dict)
            temp_2 = self.merge_dict(temp_1,media_server_dict)
            temp_3 = self.merge_dict(temp_2,application_dict)
            expected_dict = self.merge_dict(temp_3,carrier_dict)

            for key in expected_dict.keys():
                if expected_dict[key] != dimensions[key]:
                    logger.info(DIRECTION + " -> " + key + " did not match ", also_console='true')
                    logger.info("Expected is " + str(expected_dict[key]) + " . Instead, we got " + str(dimensions[key]), also_console='true')
                    return "False"
            return "True"
        except Exception as e:
            logger.info("Exception in verify_dimensions_from_cdr. Error is : " + str(e), also_console='true')


    def close_db_connection(self):
        logger.info("Closing SSH Tunnel and PostgreSQL DB connection",
                    also_console='true')
        self.conn.close()
        self.server.stop()
        self.server.close()

