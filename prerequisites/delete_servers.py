from openstack import connection

TAG = "tf_test_vm"

conn = connection.from_config(cloud='openstack')

servers = conn.compute.servers(details=True)
for server in servers:
    if TAG in (server.tags or []):
        conn.compute.delete_server(server)