import logging
from azure.mgmt.compute import ComputeManagementClient
from azure.core.exceptions import HttpResponseError
from typing import List

# Configure logger
logger = logging.getLogger(__name__)

class AzureCompute:
    def __init__(self, credential, subscription_id):
        self.compute_client = ComputeManagementClient(
            credential=credential,
            subscription_id=subscription_id
        )

    def list_vms(self, resource_group: str) -> List[dict]:
        try:
            vms = self.compute_client.virtual_machines.list(resource_group)
            return list(vms)
        except HttpResponseError as e:
            logger.error(f"Failed to list VMs in resource group {resource_group}: {e.response.status_code}")
            return []

    def get_instance_view(self, resource_group: str, vm_name: str) -> dict:
        try:
            instance_view = self.compute_client.virtual_machines.instance_view(resource_group, vm_name)
            return instance_view.as_dict()
        except HttpResponseError as e:
            logger.error(f"Failed to get instance view of VM {vm_name} in resource group {resource_group}: {e.response.status_code}")
            return {}

    def delete_vm(self, resource_group: str, vm_name: str) -> bool:
        try:
            operation = self.compute_client.virtual_machines.begin_delete(resource_group, vm_name)
            operation.wait()
            logger.info(f"VM {vm_name} has been deleted successfully.")
            return True
        except HttpResponseError as e:
            logger.error(f"Failed to delete VM {vm_name} in resource group {resource_group}: {e.response.status_code}")
            return False
