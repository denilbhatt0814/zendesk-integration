from airflow import DAG
from datetime import datetime, timedelta
from plugins.operators.zendesk_fetch_operator import ZendeskFetchOperator

default_args = {
    'owner': 'airflow',
    'start_date': datetime.date(),
    'catchup': False,
}
dag = DAG('dynamic_zendesk_ticket_fetch', default_args=default_args, schedule_interval=timedelta(minutes=1))


def create_fetch_task(session, zendesk_subdomain, access_token):
    return ZendeskFetchOperator(
        task_id=f'fetch_tickets_{zendesk_subdomain}',
        zendesk_domain=zendesk_subdomain,
        access_token=access_token,
        dag=dag,
    )