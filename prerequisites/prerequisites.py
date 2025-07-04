from openstack import connection
import utils_open_stack as utils
import os
import yaml

os.environ['OS_CLIENT_CONFIG_FILE'] = '../credentials/clouds.yaml'

KEY_NAME = "tf-openstack-keypair"
MY_PUBLIC_IP = '141.72.158.236/32'
IMAGE_NAME = "Ubuntu 22.04"
FLAVOUR_NAME = "mb1.small"
TAG = "tf_test_vm"

conn = connection.from_config(cloud='openstack')

key_pair, key_pair_path = utils.create_keypair(conn, key_name=KEY_NAME)

security_group = utils.create_security_group(conn, group_name="tf_main_security_group", my_public_ip=MY_PUBLIC_IP, desc="", ssh=True, http=True, flask=True)

clouds_yaml_path = "../credentials/clouds.yaml"          
output_tfvars_path = "../credentials/terraform.tfvars"
output_variables_tf_path = "../infrastructure/variables.tf"
cloud_name = "openstack"

with open(clouds_yaml_path, "r") as f:
    clouds_data = yaml.safe_load(f)

cloud = clouds_data.get("clouds", {}).get(cloud_name, {})
auth = cloud.get("auth", {})

tfvars_data = {
    "auth_url": auth.get("auth_url", ""),
    "user_name": auth.get("username", ""),
    "password": auth.get("password", ""),
    "tenant_name": auth.get("project_name", ""),
    "domain_name": auth.get("user_domain_name", ""),
    "region": cloud.get("region_name", ""),
}

with open(output_tfvars_path, "w") as f:
    for key, value in tfvars_data.items():
        f.write(f'{key} = "{value}"\n')
