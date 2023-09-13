# GovA11l Cert Stream

Gov Cert Stream is a tool designed to monitor and log certificate streams, focusing on `.gov` and `.mil` domains. It integrates with various services including Sentry for error tracking and Pyroscope for performance monitoring, leveraging environmental variables for easy configuration.

## 🎯 Overview

The core of the application resides in the `app` directory which contains Python scripts to initiate monitoring, handle callbacks from the certificate updates, and log the status periodically.

- `app/__init__.py` - The entry point where all initial setups including Pyroscope and Sentry configurations are defined.
- `app/main.py` - Contains the main script to start monitoring the certificate stream.

## 💡 Features

- **Sentry Integration:** For error tracking and application monitoring.
- **Pyroscope Integration:** Facilitates performance monitoring with various configurable parameters.
- **GCloud Integration:** Utilizes Google Cloud services for operations like BigQuery table setup.
- **Rich Console Logging:** Utilizes rich console for improved logging experiences.

## 🛠️ Installation

To set up and run the Gov Cert Stream locally, you will need to install the necessary Python packages and set up your environment variables.

### Prerequisites
- Python
- Sentry account with a valid DSN
- Pyroscope server setup
- Google Cloud credentials with necessary permissions

### Environment Variables

Set up your environment variables in a `.env` file at the root of your project. Below are the essential variables that need to be configured:

```sh
PYROSCOPE_APPLICATION_NAME=your_pyroscope_application_name
PYROSCOPE_SERVER=your_pyroscope_server_address
PYROSCOPE_AUTH_TOKEN=your_pyroscope_auth_token
SENTRY_DSN=your_sentry_dsn
GCLOUD_DATASET_NAME=your_gcloud_dataset_name
GCLOUD_BIGQUERY_TABLE=your_gcloud_bigquery_table_name
```

### Installing Dependencies
Install the required Python packages using the following command:
```python
pip install -r requirements.txt
```


📚 Usage

To start the monitoring script, use the following command:

```
python -m app
```

This will initiate the monitoring process, logging status messages every hour and updating the Google BigQuery table with certificate data.

### 📁 Repo Overview

`app/utils/`: Directory containing utility scripts for various functionalities like Google Cloud authentication and logging.
`app/utils/gcloud.py`: Script to setup and manage Google Cloud services.
`app/utils/logger.py`: Utility script for logging functionalities.

### 👩‍💻👨‍💻 Contributing

We welcome contributions from the community. If you have suggestions or find any bugs, please create an issue or submit a pull request.

### 🎉 Final Thoughts

We thank you for checking out Gov Cert Stream and hope that it aids in your monitoring tasks, making the web a more secure place.

Happy coding! 🎉👩‍💻👨‍💻

### 📄 License

Gov Cert Stream is released under the GPL-3.0 License.
