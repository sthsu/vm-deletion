import os
import logging
from azure.identity import ClientSecretCredential, DefaultAzureCredential, ManagedIdentityCredential
from typing import Optional, Type, Union

# Configure logging
logger = logging.getLogger(__name__)

class CredentialProvider:
    def get_credential(self) -> Optional[any]:
        pass

class DefaultCredentialProvider(CredentialProvider):
    def get_credential(self) -> Optional[DefaultAzureCredential]:
        try:
            credential = DefaultAzureCredential()
            return credential
        except Exception as e:
            logger.error("Error occurred while getting default Azure credentials: %s", str(e))
            return None

class ServicePrincipalCredentialProvider(CredentialProvider):
    def __init__(self, tenant_id: Optional[str] = None, client_id: Optional[str] = None, client_secret: Optional[str] = None) -> None:
        self.tenant_id = tenant_id or os.environ.get("AZURE_TENANT_ID")
        self.client_id = client_id or os.environ.get("AZURE_CLIENT_ID")
        self.client_secret = client_secret or os.environ.get("AZURE_CLIENT_SECRET")

    def get_credential(self) -> Optional[ClientSecretCredential]:
        try:
            credential = ClientSecretCredential(self.tenant_id, self.client_id, self.client_secret)
            return credential
        except Exception as e:
            logger.error("Error occurred while getting Azure credentials with service principal: %s", str(e))
            return None

class ManagedIdentityCredentialProvider(CredentialProvider):
    def get_credential(self) -> Optional[ManagedIdentityCredential]:
        try:
            credential = ManagedIdentityCredential()
            return credential
        except Exception as e:
            logger.error("Error occurred while getting Azure credentials with managed identity: %s", str(e))
            return None
