#create a VM

terraform init
terraform plan -var-file=../credentials/terraform.tfvars
terraform apply -var-file=../credentials/terraform.tfvars

#change config in openstack.tf
#update instance
terraform plan -var-file=../credentials/terraform.tfvars
terraform apply -var-file=../credentials/terraform.tfvars