terraform {
  required_providers {
    openstack = {
      source  = "terraform-provider-openstack/openstack"
      version = "~> 1.52.1" # oder eine andere gültige Version
    }
  }
}

provider "openstack" {
  auth_url    = var.auth_url
  domain_name = var.domain_name
  tenant_name = var.tenant_name
  user_name   = var.user_name
  password    = var.password
  region      = var.region
}

resource "openstack_compute_instance_v2" "mydemoinstance" {
  # Set to some custom value
  name = "tf-test-1"
  # Look up in the Dashboard
  image_name  = "Ubuntu 24.04 2025-01"
  flavor_name = "mb1.small"

  tags = ["tf_test_vm"]

  # Set security group to default
  security_groups = ["default"]

  # Set to your key pair name
  key_pair = "tf-openstack-keypair"

  # Set to the name of an existing network
  network {
    name = "provider_912"
  }
}

resource "local_file" "floating_ip" {
  content  = openstack_compute_instance_v2.mydemoinstance.network.0.fixed_ip_v4
  filename = "${path.module}/../credentials/openstack-inventory.txt"
}
