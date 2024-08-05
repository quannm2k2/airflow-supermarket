from airflow import DAG
from airflow.providers.postgres.operators.postgres import PostgresOperator
from airflow.utils.dates import days_ago
from airflow.operators.dummy import DummyOperator # type: ignore

default_args = {
    'owner': 'airflow',
    'start_date': days_ago(1),
}

dag = DAG(
    'postgres_test',
    default_args=default_args,
    description='A simple Postgres test DAG',
    schedule_interval=None,
)

start = DummyOperator(
    task_id='start',
    dag=dag,
)

create_table = PostgresOperator(
    task_id='create_table',
    postgres_conn_id='postgres_supermarket',
    sql="""
    CREATE TABLE IF NOT EXISTS example_table (
        id SERIAL PRIMARY KEY,
        name VARCHAR(50) NOT NULL,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    );
    """,
    dag=dag,
)

insert_data = PostgresOperator(
    task_id='insert_data',
    postgres_conn_id='postgres_supermarket',
    sql="""
    INSERT INTO example_table (name) VALUES ('Airflow User'), ('Airflow Example');
    """,
    dag=dag,
)

select_data = PostgresOperator(
    task_id='select_data',
    postgres_conn_id='postgres_supermarket',
    sql="""
    SELECT * FROM example_table;
    """,
    dag=dag,
)

end = DummyOperator(
    task_id='end',
    dag=dag,
)

start >> create_table >> insert_data >> select_data >> end
