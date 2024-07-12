from repository.identity import AzureIdentity
from repository.compute import AzureCompute
from repository.compute.manager import VMManager
from config.config import Config

class CleanupVmsFunction:
    def __init__(self):
        # List of resource groups to check
        self.resource_groups = ["ResourceGroup1", "ResourceGroup2"]
        self.identity = AzureIdentity()
        self.credential = self.identity.get_credential()
        self.subscription_id = Config.get_subscription_id()
        self.compute = AzureCompute(self.credential, self.subscription_id)
        self.vm_manager = VMManager(self.compute)

    def run(self):
        self.vm_manager.delete_stopped_vms(self.resource_groups)
