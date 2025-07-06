#!/bin/bash
trap 'read -p "run: $BASH_COMMAND"' DEBUG

#pulumi lokal installieren brew install pulumi
export OS_CLIENT_CONFIG_FILE='../credentials/clouds.yaml'
export OS_CLOUD='openstack'

cd pulumi

source ../.venv/bin/activate

pulumi login --local
pulumi stack init dev
pulumi up

cd ..

ansible-playbook -i credentials/inventory.ini ansible/k3s_cluster/install_k3s_cluster.yml

pulumi destroy
pulumi stack rm dev

export KUBECONFIG=credentials/k3s.yaml