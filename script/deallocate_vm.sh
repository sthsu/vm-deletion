#!/bin/bash

# Load configuration
source config.sh

# Log in using the service principal
az login --service-principal --username $client_id --password $client_secret --tenant $tenant_id

# Loop to create 10 VMs
for i in $(seq -w 1 1); do
  vm_name="managedbastion00$i"
  # Deallocate the VM to stop it
  az vm deallocate \
    --resource-group $resource_group \
    --name $vm_name

  echo "Deallocated VM: $vm_name"
done