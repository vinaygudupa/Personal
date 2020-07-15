# usage 
# Use python2. Also do "pip install redis-py-cluster==1.3.6"
# python clear_mpc_keys_from_proxy_redis.py <AUTH_ID>
import sys
import rediscluster
from rediscluster import connection
HOST = 'qa-voice-pr-cluster.vadfqq.clustercfg.usw1.cache.amazonaws.com'
PORT = 6379
cluster_pool = connection.ClusterConnectionPool(host=HOST, port=PORT, max_connections=5, skip_full_coverage_check=True)
REDIS_CLIENT = rediscluster.StrictRedisCluster(connection_pool=cluster_pool)
def list_acc_key(auth_id):
    return 'list:mpc_conferences:{}'.format(auth_id)
def conf_key(mpc_key):
    return 'conference:{}'.format(mpc_key)
def conf_member_key(mpc_key):
    return 'conference:{}:members'.format(mpc_key)
def participant_key(mpc_key, member_id, call_uuid):
    return 'participant:{}:{}:{}'.format(mpc_key, member_id, call_uuid)
def clean_mpc_data(main_auth_id):
    mpc_list_key = list_acc_key(main_auth_id)
    print('listing live mpc found under {}'.format(mpc_list_key))
    mpc_count = REDIS_CLIENT.zcard(mpc_list_key)
    print('account has {} live mpc'.format(mpc_count))
    print('fetching live key data...')
    mpc_data = REDIS_CLIENT.zrange(mpc_list_key, 0, mpc_count)
    mpc_data = [str(x) for x in mpc_data]
    sub_account = []
    for MPC in mpc_data:
        if MPC.split('_')[1].startswith("SA"):
            sub_account.append(MPC.split('_')[1])
        print('cleaning data for {}'.format(MPC))
        conf = conf_key(MPC)
        members = conf_member_key(MPC)
        print('fetching member data for {}'.format(MPC))
        members_data = REDIS_CLIENT.hgetall(members)
        for member_id, call_uuid in members_data.items():
            print('clearing participant == MPC: {}, MemberID: {}, CallUUID: {}'.format(MPC, member_id, call_uuid))
            REDIS_CLIENT.delete(participant_key(MPC, member_id, call_uuid))
            print('participant cleared')
        print('all participants cleared, cleaning member and conf data')
        REDIS_CLIENT.delete(conf)
        REDIS_CLIENT.delete(members)
        print('member and conf data cleared')
    if len(sub_account) > 0:
        print('cleaning sub account data')
        for s in sub_account:
            print('cleaning sub account {}'.format(s))
            REDIS_CLIENT.delete(list_acc_key(s))
    print('deleting list data under key {}'.format(mpc_list_key))
    REDIS_CLIENT.delete(mpc_list_key)
if __name__ == '__main__':
    accounts = sys.argv[1:]
    for acc in accounts:
        print('starting cleanup')
        clean_mpc_data(acc.strip())
        print('cleanup complete for acc {}'.format(acc))
