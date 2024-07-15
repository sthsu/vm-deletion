import logging
from repository.compute_manager import VMManager

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class CleanupVmsFunction:
    def __init__(self, subscription_id: str, resource_group_list: list[str]):
        self.resource_groups = resource_group_list
        self.subscription_id = subscription_id
        self.vm_manager = VMManager(subscription_id)

    async def run(self):
        try:
            logger.info("Starting cleanup of stopped/deallocated VMs in resource groups: %s", self.resource_groups)
            await self.vm_manager.delete_stopped_vms(self.resource_groups)
            logger.info("Cleanup of stopped/deallocated VMs completed successfully")
        except Exception as e:
            logger.error("An error occurred during VM cleanup: %s", str(e))
            raise