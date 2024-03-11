from airflow import DAG
from datetime import datetime, timedelta
from airflow.operators.empty import EmptyOperator
from airflow.operators.python import PythonOperator
from airflow.utils.dates import days_ago
# from dags.integration.task import fetch_subdomains, fetch_tickets
import sqlite3
import requests
import json
import math

# SERVICE:
class ZendeskService:
    def __init__(self, subdomain):
        self.subdomain = subdomain

    def fetch_tickets(self):
        access_token = self.__get_access_token()
        last_fetch = self._get_last_fetch_timestamp()

        if last_fetch:
            tickets = self.__incremental_ticket_fetch(access_token, last_fetch)
            
        else:
            tickets = self.__full_ticket_fetch(access_token)
        
        self.__update_last_fetch_timestamp()
        return tickets
    
    def __incremental_ticket_fetch(self, access_token, last_fetch):
        timestamp = math.floor((last_fetch - timedelta(seconds=65)).timestamp())
        params = {
            "start_time": timestamp
        }
        url = f"https://{self.subdomain}.zendesk.com/api/v2/incremental/tickets/cursor.json"
        headers = {
            "Authorization": f"Bearer {access_token}"
        }
        response = requests.get(url, headers=headers, params=params)
        print(response.json())
        tickets = []

        if response.status_code == 200:
            data = response.json()
            tickets.extend(data['tickets'])
            try:
                while not data["end_of_stream"]:
                    url = data["after_url"]
                    headers = {
                        "Authorization": f"Bearer {access_token}"
                    }
                    response = requests.get(url, headers=headers)
                    data = response.json()
                    tickets.extend(data["tickets"])
            except Exception as e:
                print(f"Next incremental fetches failed! - {self.subdomain}", e)

            print(f"INCR: Fetched {len(tickets)} tickets")
            return tickets
        else:
            raise Exception("Error fetching full tickets", response.status_code)



    def __full_ticket_fetch(self, access_token):
        headers = {
            "Authorization": f"Bearer {access_token}"
        }
        response = requests.get(f"https://{self.subdomain}.zendesk.com/api/v2/tickets.json", headers=headers)

        if response.status_code == 200:
            tickets = response.json()['tickets']
            # Here you would process and store the tickets as needed
            print(f"Fetched {len(tickets)} tickets")
            return tickets
        else:
            raise Exception("Error fetching full tickets", response.status_code)

    def __update_last_fetch_timestamp(self):
        conn = None

        try:
            conn = sqlite3.connect("db.sqlite3")
            cursor = conn.cursor()

            # Update the last_fetch timestamp to the current timestamp
            current_timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            query_update = "UPDATE zendesk_accesstoken SET last_fetch=? WHERE subdomain=?"
            cursor.execute(query_update, (current_timestamp, self.subdomain,))
            
            # Commit the changes to the database
            conn.commit()
            
        except sqlite3.Error as error:
            raise Exception(f"Database error: {error}")
        finally:
            if conn:
                conn.close()

        # Return the current timestamp for reference if needed
        return current_timestamp


    def _get_last_fetch_timestamp(self):
        conn = None
        timestamp = None

        try:
            conn = sqlite3.connect("db.sqlite3")
            cursor = conn.cursor()

            query = "SELECT last_fetch FROM zendesk_accesstoken WHERE subdomain=?"
            cursor.execute(query, (self.subdomain,))
            
            row = cursor.fetchone()
            print(row)
            if row and row[0]:
                datetime_str = row[0]
                timestamp = datetime.strptime(datetime_str, '%Y-%m-%d %H:%M:%S')
            
        except sqlite3.Error as error:
            raise Exception(f"Database error: {error}")
        finally:
            if conn:
                conn.close()   
        return timestamp


    def __get_access_token(self):

        conn = None
        token = None

        try:
            conn = sqlite3.connect("db.sqlite3")
            cursor = conn.cursor()

            # if not conn:
            #     raise

            query = "SELECT token FROM zendesk_accesstoken WHERE subdomain=?"
            cursor.execute(query, (self.subdomain,))
            
            row = cursor.fetchone()
            print(row)
            if row:
                token = row[0]
            else:
                raise Exception("Token not found for the specified subdomain.")
        except sqlite3.Error as error:
            raise Exception(f"Database error: {error}")
        finally:
            if conn:
                conn.close()   
        return token

    def store_ticket(self, ticket):
        url = 'http://localhost:8000/zendesk/api/tickets/'

        for key, value in ticket.items():
            if isinstance(value, list):
                ticket[key] = json.dumps(value)
        data = ticket
        data["ticket_id"] = ticket["id"]
        del data["id"]
        data["subdomain"] = self.subdomain

        headers = {
            'Content-Type': 'application/json',
        }

        print(data)
        response = requests.post(url, data=json.dumps(data), headers=headers)
        print("POST: ", response.status_code)
        print(response.text)

    def update_ticket_instore(self, ticket):
        id = ticket["id"]
        url = f'http://localhost:8000/zendesk/api/tickets/{id}/'

        for key, value in ticket.items():
            if isinstance(value, list):
                ticket[key] = json.dumps(value)
        data = ticket

        headers = {
            'Content-Type': 'application/json',
        }

        print(data)
        response = requests.patch(url, data=json.dumps(data), headers=headers)
        print("PATCH: ", response.status_code)
        print(response.text)
    
    def check_for_ticket_instore(self, ticket_id):
        url = "http://127.0.0.1:8000/zendesk/api/tickets/get_by_ticket_id_and_subdomain/"
        # ?ticket_id=2&subdomain=self4077
        params = {
            "ticket_id": ticket_id,
            "subdomain": self.subdomain
        }

        response = requests.get(url=url, params=params)
        print("CHECK: ", response.status_code)
        return response

    def count_new_tickets_in_last_24hrs(self):
        conn = None
        count = 0

        try:
            conn = sqlite3.connect("db.sqlite3")
            cur = conn.cursor()

            # Calculate current time and 24 hours before
            current_time = datetime.now()
            time_24_hours_before = current_time - timedelta(days=1)

            # Format times as strings in the format SQLite understands (YYYY-MM-DD HH:MM:SS)
            current_time_str = current_time.strftime('%Y-%m-%d %H:%M:%S')
            time_24_hours_before_str = time_24_hours_before.strftime('%Y-%m-%d %H:%M:%S')

            # SQL query with placeholders for parameters
            sql_query = """
            SELECT COUNT(*) 
            FROM zendesk_ticket 
            WHERE created_at >= ? 
            AND created_at < ?;
            """

            cur.execute(sql_query, (time_24_hours_before_str, current_time_str))

            row = cur.fetchone()
            print(f"Number of records from 24 hours ago to now: {count}")
            if row:
                count = row[0]
            else:
                raise Exception("Tickets not found for the specified subdomain.")
        except sqlite3.Error as error:
            raise Exception(f"Database error: {error}")
        finally:
            if conn:
                conn.close()   
        return count

    def store_ticket_count_last24hrs(self, count):
        url = f'http://localhost:8000/zendesk/api/daily-ticket-count/'

        headers = {
            'Content-Type': 'application/json',
        }

        data = {
            "date": datetime.now().date(),
            "ticket_count": count,
            "subdomain": self.subdomain
        }

        try:
            response = requests.post(url, data=json.dumps(data), headers=headers)
            print("POST: ", response.status_code)
            print(response.text)
            return
        except Exception as e:
            print("POST COUNT ERROR!!")
            return

# TASKS:
def fetch_subdomains():
    conn = sqlite3.connect('db.sqlite3')
    cursor = conn.cursor()
    cursor.execute("SELECT subdomain FROM zendesk_accesstoken")
    subdomains = list(map(lambda x: x[0], cursor.fetchall()))
    conn.close()
    return subdomains

def fetch_tickets(**kwargs):
    subdomains = kwargs['ti'].xcom_pull(task_ids='fetch_subdomains')
    
    print(subdomains, type(subdomains))
    for subdomain in subdomains:
        zendesk_svc = ZendeskService(subdomain=subdomain)
        tickets = zendesk_svc.fetch_tickets()
        print(type(tickets), tickets)
        for ticket in tickets:
            response = zendesk_svc.check_for_ticket_instore(ticket_id=ticket["id"])
            if response.status_code == 200:
                ticket = response.json()
                zendesk_svc.update_ticket_instore(ticket)
            else: # create new entry
                zendesk_svc.store_ticket(ticket)
        
def sum_tickets_inlast24hr(**kwargs):
    subdomains = kwargs['ti'].xcom_pull(task_ids='fetch_subdomains')
    
    print(subdomains, type(subdomains))
    for subdomain in subdomains:
        zendesk_svc = ZendeskService(subdomain=subdomain)

        count = zendesk_svc.count_new_tickets_in_last_24hrs()


# MAIN
default_args = {
    'owner': 'airflow',
    'start_date': datetime(2024, 2, 14),
    'catchup': False,
}

# CONTINUOUS TICKET FETCHING DAG
dag = DAG('dynamic_zendesk_ticket_fetch', default_args=default_args, schedule=timedelta(minutes=1), catchup=False)

t0 = EmptyOperator(task_id="start_task", dag=dag)
fetch_subdomains_task = PythonOperator(task_id="fetch_subdomains",
                    python_callable=fetch_subdomains,
    dag=dag)
fetch_tickets_task = PythonOperator(task_id="fetch_tickets",
                    python_callable=fetch_tickets,
    op_kwargs={'subdomains': "{{ ti.xcom_pull(task_ids='fetch_subdomains') }}"},
    dag=dag)

t0 >> fetch_subdomains_task >> fetch_tickets_task

# MAIN
d_args = {
    'owner': 'airflow',
    'retries': 1,
    'retry_delay': timedelta(minutes=5),
    'start_date': days_ago(1),
    'catchup': False,
}
# SUMARIZE LAST 24 HRs new Tickets
sum_last_24hr_tickets_dag = DAG('zendesk_new_tickets_last24hr', default_args=d_args, schedule_interval='0 0 * * *', catchup=False)

t1 = EmptyOperator(task_id="start_task", dag=sum_last_24hr_tickets_dag)
fetch_subdomains_task_t = PythonOperator(task_id="fetch_subdomains",
                    python_callable=fetch_subdomains,
    dag=sum_last_24hr_tickets_dag)

sum_tickets_inlast24hr_task = PythonOperator(task_id="sum_tickets_inLast24Hrs",
                    python_callable=sum_tickets_inlast24hr,
    op_kwargs={'subdomains': "{{ ti.xcom_pull(task_ids='fetch_subdomains') }}"},
    dag=sum_last_24hr_tickets_dag)

t1 >> fetch_subdomains_task_t >> sum_tickets_inlast24hr_task