from airflow import DAG
from airflow.operators.python import PythonOperator
from airflow.utils.dates import days_ago
import subprocess

default_args = {
    'owner': 'airflow',
    'depends_on_past': False,
    'email_on_failure': False,
    'email_on_retry': False,
    'retries': 1,
}

dag = DAG(
    'dbt_subprocess_test',
    default_args=default_args,
    description='A simple dbt DAG',
    schedule_interval='@daily',
    start_date=days_ago(1),
    catchup=False,
)

# Function to run dbt commands using subprocess
def run_dbt_command(command):
    try:
        subprocess.run(
            command, 
            shell=True, 
            check=True, 
            cwd='/mnt/c/Users/Admin/dbt_supermarket',
            text=True
        )
    except subprocess.CalledProcessError as e:
        print(f"Command '{e.cmd}' returned non-zero exit status {e.returncode}.")
        raise

# Define dbt run task
dbt_run = PythonOperator(
    task_id='dbt_run',
    python_callable=run_dbt_command,
    op_args=['dbt run'],
    dag=dag,
)

# Define dbt test task
dbt_test = PythonOperator(
    task_id='dbt_test',
    python_callable=run_dbt_command,
    op_args=['dbt test'],
    dag=dag,
)

# Define task dependencies
dbt_run >> dbt_test
