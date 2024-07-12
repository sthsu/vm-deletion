class VMManager:
    def __init__(self, compute_client):
        self.compute_client = compute_client

    def delete_stopped_vms(self, resource_groups):
        for rg in resource_groups:
            vms = self.compute_client.list_vms(rg)
            for vm in vms:
                instance_view = self.compute_client.get_instance_view(rg, vm.name)
                statuses = {s.code.split('/')[1] for s in instance_view.statuses}
                if 'stopped' in statuses or 'deallocated' in statuses:
                    print(f"Deleting VM: {vm.name} in resource group: {rg}")
                    self.compute_client.delete_vm(rg, vm.name)
