# https://airflow.apache.org/docs/apache-airflow/stable/start/local.html

# Airflow needs a home. `~/airflow` is the default, but you can put it
# somewhere else if you prefer (optional)
export AIRFLOW_HOME=${PWD}

# Install Airflow using the constraints file
AIRFLOW_VERSION=2.2.4
PYTHON_VERSION="$(python --version | cut -d " " -f 2 | cut -d "." -f 1-2)"
CONSTRAINT_URL="https://raw.githubusercontent.com/apache/airflow/constraints-${AIRFLOW_VERSION}/constraints-${PYTHON_VERSION}.txt"
pip install "apache-airflow==${AIRFLOW_VERSION}" --constraint "${CONSTRAINT_URL}"

airflow db init
airflow users create -u admin -p welcome -f Dongkyun -l You -r Admin -e admin@airflow.com

# The Standalone command will initialise the database, make a user,
# and start all components for you.
# airflow standalone

# Visit localhost:8080 in the browser and use the admin account details
# shown on the terminal to login.
# Enable the example_bash_operator dag in the home page
