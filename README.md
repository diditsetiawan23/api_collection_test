# Postman Test Application

Welcome to the Postman Test Application! This application is designed to test a Postman collection along with an environment. It sends the test report to an email and a Telegram group.

## Step 1
- Change the recipient for the email report, go to the config directory and open configuration.py.

## Features

- Tests a Postman collection with an environment.
- Sends the test report to both email and a Telegram group.
- Dockerized for easy deployment.

## Getting Started

### Docker Installation

1. **Build the Docker image:**

    ```bash
    docker build . -t postman-test-app .
    ```

2. **Run the Docker container:**

    ```bash
    docker run -it postman-test-app
    ```

### Local Installation

To run the application locally, make sure you have the following installed:

- Node.js
- Newman
- Newman reporter HTML Extra
- Python (with required libraries, see below)

Install Python libraries:

```bash
pip install -r requirements.txt
```

### Configuration
If you need to customize the configuration:

- To change the recipient for the email report, go to the config directory and open configuration.py.
- To join the Telegram group and receive alerts, click https://t.me/+h9PxYVJguFlkYWRl.

### Contributors
- Didit Setiawan

