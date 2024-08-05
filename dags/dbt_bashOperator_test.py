from airflow import DAG
from airflow.operators.bash import BashOperator
from airflow.utils.dates import days_ago

default_args = {
    'owner': 'airflow',
    'depends_on_past': False,
    'email_on_failure': False,
    'email_on_retry': False,
    'retries': 1,
}

dag = DAG(
    'dbt_bashOperator_test',
    default_args=default_args,
    description='A simple dbt DAG',
    schedule_interval='@daily',
    start_date=days_ago(1),
    catchup=False,
)

# Define dbt run command
dbt_run = BashOperator(
    task_id='dbt_run',
    bash_command='cd /root/project/dbt_supermarket && dbt run',
    dag=dag,
)

# Define dbt test command
dbt_test = BashOperator(
    task_id='dbt_test',
    bash_command='cd /root/project/dbt_supermarket && dbt test',
    dag=dag,
)

# Define task dependencies
dbt_run >> dbt_test
