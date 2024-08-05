from airflow import DAG
from airflow.providers.postgres.operators.postgres import PostgresOperator
from airflow.operators.bash import BashOperator
from airflow.utils.dates import days_ago
from airflow.operators.dummy import DummyOperator # type: ignore
import os

# Danh sách các bảng cần copy và offload
TABLES_TO_COPY = [
    'fct_user_orders',
    'dim_products',
    'dim_departments',
    'dim_aisles'
    # Thêm các bảng khác ở đây
]

# Đường dẫn thư mục lưu file CSV (trên WSL)
CSV_DIR = 'F:/AllCode/Data Engineer/'
CSV_DIR_WSL = '/mnt/f/AllCode/Data Engineer/'

# Đường dẫn bucket S3
S3_BUCKET = 's3://quannm-07252024-demo/supermarket-data/'

default_args = {
    'owner': 'airflow',
    'start_date': days_ago(1),
}

dag = DAG(
    'list_postgres_s3',
    default_args=default_args,
    description='A simple Postgres test DAG',
    schedule_interval=None,
)

start = DummyOperator(
    task_id='start',
    dag=dag,
)

end = DummyOperator(
    task_id='end',
    dag=dag,
)

# Tạo các task copy và offload các bảng lên S3
for table in TABLES_TO_COPY:
    csv_file_path = os.path.join(CSV_DIR, f'{table}.csv')
    csv_file_path_wsl = os.path.join(CSV_DIR_WSL, f'{table}.csv')
    s3_key = f'/{table}.csv'
    
    copy_task = PostgresOperator(
        task_id=f'copy_table_{table}',
        postgres_conn_id='postgres_supermarket',
        sql=f"""
        SET search_path TO supermarket;
        COPY {table} TO '{csv_file_path}' CSV HEADER;
        """,
        dag=dag,
    )

    offload_task = BashOperator(
        task_id=f'offload_to_s3_{table}',
        bash_command=f'aws s3 cp "{csv_file_path_wsl}" {S3_BUCKET}{s3_key}',
        dag=dag,
    )

    start >> copy_task >> offload_task >> end