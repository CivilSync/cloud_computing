import os

def create_keypair(conn, key_name):
    keypair = conn.compute.find_keypair(key_name)
    path = f"{key_name}.pem"

    if not keypair:
        print("Create keypair:")

        keypair = conn.compute.create_keypair(name=key_name)

        with open(f"{key_name}.pem", 'w') as f:
            f.write(str(keypair.private_key))

        os.chmod(f"{key_name}.pem", 0o400)

        print(f"Created keypair {key_name}")

    return keypair, path

def create_server(conn, image_name, flavor_name, network_name, server_name, key_name):
    server = conn.compute.find_server(server_name)
    if not server:
        print("Create Server:")

        image = conn.image.find_image(image_name)
        flavor = conn.compute.find_flavor(flavor_name)
        network = conn.network.find_network(network_name)
        keypair = conn.compute.find_keypair(key_name)

        server = conn.compute.create_server(
            name=server_name,
            image_id=image.id,
            flavor_id=flavor.id,
            networks=[{"uuid": network.id}],
            key_name=keypair.name,
        )

        server = conn.compute.wait_for_server(server)

        print(f"Created server {server_name} on public ip {server.access_ipv4}")
    
    return server
    
def create_security_group(conn, group_name, my_public_ip, desc="", ssh=False, http=False, flask=False):
    sec_group = conn.network.find_security_group(group_name)
    if not sec_group:
        sec_group = conn.network.create_security_group(name=group_name, description=desc)
        print(f'Created security group {sec_group.id}')
        
        rules = []
        if ssh:
            rules.append({
                'direction': 'ingress',
                'protocol': 'tcp',
                'port_range_min': 22,
                'port_range_max': 22,
                'remote_ip_prefix': my_public_ip
            })
        if http:
            rules.append({
                'direction': 'ingress',
                'protocol': 'tcp',
                'port_range_min': 80,
                'port_range_max': 80,
                'remote_ip_prefix': '0.0.0.0/0'
            })
            rules.append({
                'direction': 'ingress',
                'protocol': 'tcp',
                'port_range_min': 8080,
                'port_range_max': 8080,
                'remote_ip_prefix': '0.0.0.0/0'
            })
        if flask:
            rules.append({
                'direction': 'ingress',
                'protocol': 'tcp',
                'port_range_min': 5000,
                'port_range_max': 5000,
                'remote_ip_prefix': '0.0.0.0/0'
            })

        for rule in rules:
            conn.network.create_security_group_rule(
                security_group_id=sec_group.id,
                direction=rule['direction'],
                protocol=rule['protocol'],
                port_range_min=rule['port_range_min'],
                port_range_max=rule['port_range_max'],
                remote_ip_prefix=rule['remote_ip_prefix']
            )
        print('Security Group ingress rules authorized.')
    return sec_group