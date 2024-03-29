# zendesk-integration

This project is designed to connect to Zendesk APIs using OAuth authentication. Once the client's access tokens are obtained, the project keeps track of their new tickets. This is achieved by utilizing Apache Airflow DAGs (Directed Acyclic Graphs) to schedule and execute tasks.

## Features

- OAuth Connect: The project allows users to initiate an OAuth connection to Zendesk APIs. This is done by redirecting users to the Zendesk OAuth authorization page, where they can grant access to their Zendesk account. Once authorized, the project retrieves the access token and stores it for future use.

- New Ticket Tracking: The project utilizes Apache Airflow DAGs to periodically fetch new tickets for each client. The DAGs are scheduled to run at regular intervals, such as every minute or every day. The project keeps track of the last fetch timestamp for each client, ensuring that only new tickets are fetched during subsequent runs.

- Ticket Summarization: At the end of each day, the project summarizes the number of new tickets for each client. This information is stored in a separate table or database, allowing users to easily view and analyze the ticket count trends over time.

## Installation

1. Clone the project repository to your local machine.
2. Install the required dependencies by running `pip install -r requirements.txt`.
3. Set up the necessary configurations, such as Zendesk subdomain, client ID, client secret, and redirect URI, in the project's settings file.
4. Set up the Apache Airflow environment and configure the DAGs to run at the desired intervals.
5. Run the project using the appropriate command or script, depending on your setup.

## Usage

1. Start the project by running the main script or command.
2. Access the project's web interface to initiate the OAuth connection with Zendesk APIs.
3. Once the access tokens are obtained, the project will automatically start tracking new tickets for each client.
4. Use the Apache Airflow interface to monitor the DAGs and their execution status.
5. At the end of each day, the project will summarize the number of new tickets for each client and store the information for future reference.
