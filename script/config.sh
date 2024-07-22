# config.sh

# Azure subscription ID
subscription_id="2213e8b1-dbc7-4d54-8aff-b5e315df5e5b"

# Resource group and location
resource_group="1-0c1a6494-playground-sandbox"
location="eastus"

# Virtual network and subnet
vnet_name="managedBastionVNet"
subnet_name="managedBastionSubnet"
address_prefix="10.0.0.0/16"
subnet_prefix="10.0.1.0/24"

# VM specifications
image="Ubuntu2204"
size="Standard_D2s_v3"
admin_username="azureuser"
admin_password="1qaz@WSX3edc"

# Service principal credentials
client_id="c47e8837-c323-45b4-90dc-cff27b027c4b"
client_secret=""
tenant_id="84f1e4ea-8554-43e1-8709-f0b8589ea118"
