from azure.identity.aio import DefaultAzureCredential
from azure.mgmt.compute.aio import ComputeManagementClient
from azure.core.exceptions import HttpResponseError
class test:
    def __init__(self):
        self.credential = DefaultAzureCredential()
            