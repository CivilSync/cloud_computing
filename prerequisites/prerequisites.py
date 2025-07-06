from openstack import connection
import utils_open_stack as utils
import os

os.environ['OS_CLIENT_CONFIG_FILE'] = '../credentials/clouds.yaml'

KEY_NAME = "d-pulumi-k8s-cluster-keypair"
MY_PUBLIC_IP = '134.155.177.55/32'
SEC_GROUP_NAME = "d-pulumi-k8s-cluster-sec-group"

conn = connection.from_config(cloud='openstack')

key_pair, key_pair_path = utils.create_keypair(conn, key_name=KEY_NAME)

security_group = utils.create_security_group(conn, group_name=SEC_GROUP_NAME, my_public_ip=MY_PUBLIC_IP, desc="", ssh=True, http=True, flask=True)
