import sys
from paypalcheckoutsdk.core import PayPalHttpClient, SandboxEnvironment

class PayPalClient:
    def __init__(self):

        self.client_id="AfXDNTBc-g6d_4ZI0q8N3vShp2RQXtX6slCx0pONRY5nVVusytlTq4vqhA0yuYyzEYhvbjPDvinStSU4"
        self.client_secret="ECHQoOr7uaN2aa-gyLc3ZMUn2Roo37Ew-wgnMB5EiCIJOnpMTGslln545-9isVW1Lg14o5Xjk5cVJ91r"
        self.environment=SandboxEnvironment(client_id=self.client_id, client_secret=self.client_secret)
        self.client =PayPalHttpClient(self.environment)
        