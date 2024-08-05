from airflow import DAG
from airflow.operators.bash import BashOperator
from airflow.providers.airbyte.operators.airbyte import AirbyteTriggerSyncOperator
from airflow.providers.airbyte.sensors.airbyte import AirbyteJobSensor
from airflow.utils.dates import days_ago

AIRBYTE_CONNECTION_ID = 'c1d20b3b-1e15-4a2a-9a71-ba1490abd00a'

default_args = {
    'owner' : 'airflow',
    'start_date' : days_ago(1),
}

dag = DAG(
    'airbyte_test',
    default_args=default_args,
    description='...',
    schedule_interval=None,
)

trigger_airbyte_sync = AirbyteTriggerSyncOperator(
       task_id='airbyte_trigger_sync',
       airbyte_conn_id='airflow-call-to-airbyte-example',
       connection_id=AIRBYTE_CONNECTION_ID,
       asynchronous=True,
       dag=dag,
)

wait_for_sync_completion = AirbyteJobSensor(
       task_id='airbyte_check_sync',
       airbyte_conn_id='airflow-call-to-airbyte-example',
       airbyte_job_id=trigger_airbyte_sync.output,
       dag=dag,
)

trigger_airbyte_sync >> wait_for_sync_completion