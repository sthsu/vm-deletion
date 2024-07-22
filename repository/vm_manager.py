from typing import List
from azure.identity import DefaultAzureCredential
from azure.mgmt.compute import ComputeManagementClient
from azure.core.exceptions import HttpResponseError
from model.vm_info import VMInfo
from concurrent.futures import ThreadPoolExecutor, as_completed
import logging

logger = logging.getLogger(__name__)

class VMManager:
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
    
    def list_vms(self, resource_group_list: List[str])->List[VMInfo]:
        try:
            vms = []
            for rg in resource_group_list:
                vms_iter = self.compute_client.virtual_machines.list(resource_group_name=rg)
                for vm in vms_iter:
                    vms.append(VMInfo(rg, vm.name))
            return vms
        except HttpResponseError as e:
            logger.error(f"Failed to list all VMs {e.response.status_code}: {e}")
            return []   
        
    def get_instance_view(self, resource_group_name: str, vm_name: str):
        try:
            instance_view = self.compute_client.virtual_machines.instance_view(
                resource_group_name=resource_group_name,
                vm_name=vm_name
            )
            return instance_view.as_dict()
        except HttpResponseError as e:
            logger.error(f"Failed to get instance view of VM {vm_name} in resource group {resource_group_name}: {e.response.status_code}")
            return {}
        
    def get_deallocated_vms(self, resource_group_list: List[str]) -> List[VMInfo]:
        deallocated_vms = []
        try:
            vms = self.list_vms(resource_group_list)
            for vm in vms:
                instance_view = self.get_instance_view(vm.resource_group_name, vm.name)
                statuses = {status['code'] for status in instance_view['statuses']}
                if 'PowerState/deallocated' in statuses:
                    deallocated_vms.append(vm)
            return deallocated_vms
        except Exception as e:
            logger.error(f"Error occurred while getting deallocated VMs: {str(e)}")
            return []
    
    def delete_deallocated_vms(self, resource_group_list: List[str]):
        try:
            deletion_futures={}
            deallocated_vms = self.get_deallocated_vms(resource_group_list)
            with ThreadPoolExecutor() as executor:
                for vm in deallocated_vms:
                    logging.warning(f'Deleting VM: {vm.name}')
                    future = executor.submit(self.compute_client.virtual_machines.begin_delete(vm.resource_group_name,vm.name))
                    deletion_futures[future] = vm.name
            for future in as_completed(deletion_futures.keys()):
                vm_name = deletion_futures[future]
                try:
                    future.result()
                    logger.info(f"VM {vm_name} has been deleted successfully.")
                except Exception as e:
                    logging.error(f'An error occurred during delete of VM "{vm_name}": {e}')
            return True
        except Exception as e:
            logger.error(f"Failed to delete deallocated vms: {e}")
            return False

