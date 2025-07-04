# add hosts to known hosts
while read -r server; do ssh-keyscan "$server"; done < servers.txt >> ~/.ssh/known_hosts

#apply ansible playbook
ansible-playbook /software/install_flask_app.yml -i /credentials/openstack-inventory.txt, -u ubuntu --private-key /credentials/tf-openstack-keypair.pem