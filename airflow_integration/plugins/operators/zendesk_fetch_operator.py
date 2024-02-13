from airflow.models import BaseOperator
from airflow.utils.decorators import apply_defaults
import requests

class ZendeskFetchOperator(BaseOperator):
    @apply_defaults
    def __init__(self, zendesk_subdomain, access_token, *args, **kwargs):
        super(ZendeskFetchOperator, self).__init__(*args, **kwargs)
        self.zendesk_subdomain = zendesk_subdomain
        self.access_token = access_token

    def execute(self, context):
        headers = {
            "Authorization": f"Bearer {self.access_token}"
        }
        response = requests.get(f"https://{self.zendesk_subdomain}/api/v2/tickets.json", headers=headers)
        
        if response.status_code == 200:
            tickets = response.json()['tickets']
            # Here you would process and store the tickets as needed
            self.log.info(f"Fetched {len(tickets)} tickets")
        else:
            raise Exception(f"Failed to fetch tickets: {response.text}")
