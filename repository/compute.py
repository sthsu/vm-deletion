from azure.identity import DefaultAzureCredential
from azure.mgmt.compute.aio import ComputeManagementClient
from azure.core.exceptions import HttpResponseError
import logging

logger = logging.getLogger(__name__)

class AzureCompute:
    def __init__(self, subscription_id: str):
        try:
            self.credential = DefaultAzureCredential()
            self.compute_client = ComputeManagementClient(
                credential=self.credential,
                subscription_id=subscription_id
            )
            self.credential.get_token(".default")
        except Exception as e:
            raise HttpResponseError(message="Failed to initialize ComputeManagementClient", response=e)
    
    async def list_vms(self, resource_group: str):
        try:
            vms = []
            async for vm in self.compute_client.virtual_machines.list(resource_group_name=resource_group):
                vms.append(vm.as_dict())
            return vms
        except HttpResponseError as e:
            logger.error(f"Failed to list VMs in resource group {resource_group}: {e.response.status_code}")
            return []
    
    async def get_instance_view(self, resource_group: str, vm_name: str):
        try:
            instance_view = await self.compute_client.virtual_machines.instance_view(
                resource_group_name=resource_group,
                vm_name=vm_name
            )
            return instance_view.as_dict()
        except HttpResponseError as e:
            logger.error(f"Failed to get instance view of VM {vm_name} in resource group {resource_group}: {e.response.status_code}")
            return {}
    
    async def delete_vm(self, resource_group: str, vm_name: str):
        try:
            operation = await self.compute_client.virtual_machines.begin_delete(
                resource_group_name=resource_group,
                vm_name=vm_name
            )
            await operation.wait()
            logger.info(f"VM {vm_name} has been deleted successfully.")
            return True
        except HttpResponseError as e:
            logger.error(f"Failed to delete VM {vm_name} in resource group {resource_group}: {e.response.status_code}")
            return False
