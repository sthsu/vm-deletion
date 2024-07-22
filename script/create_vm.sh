#!/bin/bash

# Load configuration
source config.sh

# Log in using the service principal
az login --service-principal --username $client_id --password $client_secret --tenant $tenant_id

# Loop to create 10 VMs
for i in $(seq -w 1 1); do
  vm_name="managedbastion00$i"
  nic_name="${vm_name}NIC"

  # Create a network interface
  az network nic create \
    --resource-group $resource_group \
    --location $location \
    --name $nic_name \
    --vnet-name $vnet_name \
    --subnet $subnet_name

  # Create the VM
  az vm create \
    --resource-group $resource_group \
    --name $vm_name \
    --nics $nic_name \
    --image $image \
    --size $size \
    --admin-username $admin_username \
    --admin-password $admin_password \
    --location $location \
    --os-disk-delete-option "Delete" \
    --data-disk-delete-option "Delete" \
    --nic-delete-option "Delete" \
    --no-wait

  echo "Complete creation of VM: $vm_name"

done

echo "VM creation and deallocation process started for managedbastion0001 to managedbastion0010."
