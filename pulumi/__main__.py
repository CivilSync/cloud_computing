import pulumi
import pulumi_openstack as openstack
from pulumi import ResourceOptions

# Konfiguration
config = pulumi.Config()
worker_count = config.get_int("worker_count")
image_name = config.get("image_name")
flavor_name = config.get("flavor_name")
network_name = config.get("network_name")
security_group = config.get("security_group")
keypair_name = config.get("keypair_name")

print(worker_count)

# Netzwerk
network = openstack.networking.get_network(name="provider_912")

# SSH-Key
keypair = openstack.compute.get_keypair(name=keypair_name)

# Security Group
secgroup = openstack.networking.get_sec_group(name=security_group)

# Master-Node
master = openstack.compute.Instance(
    "d-k8s-master",
    image_name=image_name,
    flavor_name=flavor_name,
    key_pair=keypair.name,
    security_groups=[secgroup.name],
    networks=[{"uuid": network.id}],
)

# Worker-Nodes
workers = []
for i in range(worker_count):
    worker = openstack.compute.Instance(
        f"d-k8s-worker-{i}",
        image_name=image_name,
        flavor_name=flavor_name,
        key_pair=keypair.name,
        security_groups=[secgroup.name],
        networks=[{"uuid": network.id}],
        opts=ResourceOptions(depends_on=[master]),
    )
    workers.append(worker)

# Schreibe inventory.ini nach Ressourcenbereitstellung
def write_inventory(args):
    master_ip, worker_ips = args
    with open("../credentials/inventory.ini", "w") as f:
        f.write("[master]\n")
        f.write(f"{master_ip} ansible_user=ubuntu ansible_ssh_private_key_file=credentials/{keypair_name}.pem\n\n")

        f.write("[worker]\n")
        for ip in worker_ips:
            f.write(f"{ip} ansible_user=ubuntu ansible_ssh_private_key_file=credentials/{keypair_name}.pem\n")
    return {}

pulumi.Output.all(master.access_ip_v4, [w.access_ip_v4 for w in workers]).apply(write_inventory)

# Outputs (optional)
pulumi.export("master_ip", master.access_ip_v4)
pulumi.export("worker_ips", [w.access_ip_v4 for w in workers])
