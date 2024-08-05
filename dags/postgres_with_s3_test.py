from airflow import DAG
from airflow.providers.postgres.operators.postgres import PostgresOperator
from airflow.operators.bash import BashOperator
from airflow.utils.dates import days_ago
from airflow.operators.dummy import DummyOperator # type: ignore

default_args = {
    'owner': 'airflow',
    'start_date': days_ago(1),
}

dag = DAG(
    'postgres_with_s3_test',
    default_args=default_args,
    description='A simple Postgres test DAG',
    schedule_interval=None,
)

start = DummyOperator(
    task_id='start',
    dag=dag,
)

connect_supermarket_schema_task = PostgresOperator(
    task_id='connect_supermarket_schema',
    postgres_conn_id='postgres_supermarket',
    sql="""
    SET search_path TO supermarket;
    """,
)

copy_table = PostgresOperator(
    task_id='copy_table',
    postgres_conn_id='postgres_supermarket',
    sql="""
    COPY fct_user_orders TO 'F:/AllCode/Data Engineer/fct_user_orders.csv' CSV HEADER;
    """,
    dag=dag,
)

offload_to_s3 = BashOperator(
    task_id='offload_to_s3',
    bash_command='aws s3 cp "/mnt/f/AllCode/Data Engineer/fct_user_orders.csv" s3://quannm-07252024-demo/supermarket-data/fct_user_orders.csv',
    dag=dag,
)

end = DummyOperator(
    task_id='end',
    dag=dag,
)

start >> connect_supermarket_schema_task >> copy_table >> offload_to_s3 >> end
