def create_key_pair(ec2_client, key_name):
    path = f"{key_name}.pem"
    key_pair = ec2_client.create_key_pair(KeyName=key_name)
    with open(path, "w") as file:
        file.write(key_pair["KeyMaterial"])
    print(f"Key-Pair {key_name} wurde erstellt und gespeichert.")
    return path
    
def create_security_group(ec2_client, group_name, my_public_ip, desc = "", ssh=False, http=False, flask=False):
    permissions = []
    ssh_perm = {
                'IpProtocol': 'tcp',
                'FromPort': 22,
                'ToPort': 22,
                'IpRanges': [{'CidrIp': my_public_ip}]
        }
    http_perm = [{
            'IpProtocol': 'tcp',
            'FromPort': 80,
            'ToPort': 80,
            'IpRanges': [{'CidrIp': '0.0.0.0/0'}]
        },
        {
            'IpProtocol': 'tcp',
            'FromPort': 8080,
            'ToPort': 8080,
            'IpRanges': [{'CidrIp': '0.0.0.0/0'}]
        }
        ]
    flask_perm = {
            'IpProtocol': 'tcp',
            'FromPort': 5000,
            'ToPort': 5000,
            'IpRanges': [{'CidrIp': '0.0.0.0/0'}]
        }
    if ssh:
        permissions.append(ssh_perm)
    if http:
        permissions.extend(http_perm)
    if flask:
        permissions.append(flask_perm)
        
    response = ec2_client.create_security_group(
        GroupName=group_name,
        Description=desc
    )
    security_group_id = response['GroupId']
    print(f'Created security group {security_group_id}')

    ec2_client.authorize_security_group_ingress(
        GroupId=security_group_id,
        IpPermissions=permissions
    )
    print('Security Group ingres authorized.')
    return security_group_id

def create_instance(ec2_resource, instance_name, image_id, instance_type, key_name, security_group_id):

    instances = ec2_resource.create_instances(
        ImageId=image_id,
        InstanceType=instance_type,
        KeyName=key_name,
        MinCount=1,
        MaxCount=1,
        TagSpecifications=[
            {
                "ResourceType": "instance",
                "Tags": [{"Key": "Name", "Value": instance_name}],
            }
        ],
        SecurityGroupIds=[security_group_id]
    )

    instance = instances[0]
    print(f"Instanz-ID: {instance.id} wird gestartet...")
    instance.wait_until_running()
    instance.reload()
    print(f"Instanz läuft. Öffentliche IP: {instance.public_ip_address}")
    return instance