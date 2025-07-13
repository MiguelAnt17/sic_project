# Computer Systems and Infrastructures: Smart Datacenter Monitoring System

- This project implements a containerized solution for monitoring a modern datacenter's environmental and operational data. It utilizes a suite of powerful open-source tools to collect, process, store, and visualize data, ensuring the datacenter's efficiency and uptime.

**About the Project**

The core of this project is to develop a robust monitoring system using a microservices architecture. This system emulates the collection of data from various sensors within a datacenter, processes this data through a message broker, stores it in a time-series database, and provides a visualization dashboard with configurable alerts.

The technology stack includes:
- Docker and Docker Compose: For containerizing and orchestrating the different services.
- Python: To simulate the data generation from various sensors.
- Apache Kafka: A distributed event streaming platform used as a message broker.
- Zookeeper: A centralized service for maintaining configuration information, naming, providing distributed synchronization, and providing group services for distributed applications.
- TICK Stack: A collection of open-source technologies for collecting, storing, graphing, and alerting on time-series data.
- Telegraf: A plugin-driven server agent for collecting and reporting metrics.
- InfluxDB: A high-performance time-series database.
- Chronograf and Kapacitor: While not explicitly implemented as separate services, their functionalities for visualization and alerting are handled through the InfluxDB UI.

**System Architecture**

The system is designed with a clear data flow:

- Data Generation: Python scripts within dedicated Docker containers simulate sensor data for temperature, power usage, cooling efficiency, and humidity.
- Data Ingestion: The generated data, formatted using the InfluxDB Line Protocol, is published to specific topics on an Apache Kafka broker.
- Data Collection and Storage: Telegraf subscribes to the Kafka topics, collects the sensor data, and writes it to an InfluxDB time-series database.
- Data Visualization and Alerting: An InfluxDB dashboard provides real-time visualization of the collected metrics. Threshold-based alerts are configured to monitor critical conditions.

The services are isolated into two main networks:
- kafka-net: For communication between the Python producer containers and the Kafka broker.
- tick-net: For communication between Telegraf and InfluxDB.


**Getting Started**

To get the project up and running, you will need to have Docker and Docker Compose installed on your system.

- Prerequisites:
  - Docker
  - Docker Compose

- Installation:
  - Clone the repository: git clone https://github.com/MiguelAnt17/sic_project
  - cd <repository-directory>

- Directory Structure:
  sic_project/
  |--dashboard/
  |  |--dashboard.json
  |--flux/
  |  |--cooling-flux.txt
  |  |--humidity-flux.txt
  |  |--power-flux.txt
  |  |--temp-flux.txt
  |--producer1/ (and producer 2-4 for the other sensors)
  |  |--Dockerfile
  |  |--producer.py
  |--telegraf/
  |  |--telegraf.conf
  |--docker-compose.yml

- Configuration:
  - docker-compose.yml: This file orchestrates the deployment of all services. It defines the   containers, networks, volumes, and dependencies.
  - .env file (Optional): For better management of configuration parameters, you can use a      .env file to store environment variables for services like InfluxDB credentials.
  -telegraf/telegraf.conf: This file configures Telegraf to use the Kafka consumer input        plugin to read from the specified topics and the InfluxDB output plugin to write to the database.

**Usage**
1- Build and run the containers:
  From the root directory of the project, run the following command: docker-compose up --build -d

2- Access the InfluxDB UI: Open your web browser and navigate to http://localhost:8086

3- Setup InfluxDB:
  User: admin
  Password: password
  Organization: sic
  Bucket: tp2
  Token: 

4- Import the Dashboard: Navigate to the "Dashboards" section in the UnfluxDB UI and click on "Import Dashboard" and upload the dashboard.json file

5- View the Alerts: Go to the "Alerts" section to see the configured threshold checks for temperature, power usage, cooling effieciency and humidity.
