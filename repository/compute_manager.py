import logging
import asyncio
from typing import List
from repository.compute import AzureCompute

logger = logging.getLogger(__name__)

class VMManager:
    def __init__(self, subscription_id: str):
        self.compute_client = AzureCompute(subscription_id)

    async def get_deallocated_vms(self, resource_group: str) -> List:
        deallocated_vms = []
        try:
            vms = await self.compute_client.list_vms(resource_group)
            for vm in vms:
                instance_view = await self.compute_client.get_instance_view(resource_group, vm['name'])
                statuses = {status['code'] for status in instance_view['statuses']}
                if 'PowerState/deallocated' in statuses:
                    deallocated_vms.append(vm)
        except Exception as e:
            logger.error(f"Error occurred while getting deallocated VMs: {str(e)}")
        return deallocated_vms

    async def delete_stopped_vms(self, resource_groups: List[str]):
        tasks = []
        try:
            for rg in resource_groups:
                deallocated_vms = await self.get_deallocated_vms(rg)
                for vm in deallocated_vms:
                    task = asyncio.create_task(self.compute_client.delete_vm(rg, vm['name']))
                    tasks.append(task)

            # Wait for all delete operations to complete
            await asyncio.gather(*tasks)
        except Exception as e:
            logger.error(f"Error occurred while deleting VMs: {str(e)}")
