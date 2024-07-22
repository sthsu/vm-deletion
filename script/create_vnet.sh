#!/bin/bash
set -e

# Load configuration
source config.sh

# Log in using the service principal
az login --service-principal --username $client_id --password $client_secret --tenant $tenant_id

# Create virtual network
az network vnet create \
  --resource-group $resource_group \
  --name $vnet_name \
  --address-prefix $address_prefix \
  --location $location \
  --subnet-name $subnet_name \
  --subnet-prefix $subnet_prefix

echo "Virtual network $vnet_name with subnet $subnet_name created successfully."
