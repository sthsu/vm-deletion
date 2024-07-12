import os

class Config:
    @staticmethod
    def get_subscription_id():
        return os.getenv('AZURE_SUBSCRIPTION_ID')
        