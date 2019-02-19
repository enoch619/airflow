# The Dag object; We'll need this to instantiate a DAG
from airflow import DAG

# Operators: We need this to operate
from airflow.operators.bash_operator import BashOperator
from airflow.operators.latest_only_operator import LatestOnlyOperator

from datetime import datetime, timedelta

default_args = {
    'owner': 'airflow',
    'depends_on_past': False,
    'start_date': datetime(2018, 12, 01),
#    'email': ['ttd_api_b4wv00q@amnetgroup.com'],
    'email_on_failure': True,
    'email_on_retry': True,
    'retries': 3,
    'retry_delay': timedelta(minutes=5),
    # 'queue': 'bash_queue',
    # 'pool': 'backfill',
    # 'priority_weight': 10,
    # 'end_date': datetime(2016, 1, 1),
    }

dag = DAG('ttd_reporting', catchup=False, default_args=default_args, schedule_interval=timedelta(hours=6))

latest_only = LatestOnlyOperator(task_id='latest_only', dag=dag)

t1 = BashOperator(
    task_id='artech_daily',
    depends_on_past=False,
    bash_command="python ~/amnet_application/ttd/artech_daily.py",
    dag=dag
)

t2 = BashOperator(
    task_id='uaf_daily',
    depends_on_past=False,
    bash_command="python ~/amnet_application/ttd/uaf_daily.py",
    dag=dag
)

t3 = BashOperator(
    task_id='uaf_dcm_merge',
    depends_on_past=False,
    bash_command="python ~/amnet_application/ttd/ttd_dcm_uaf.py",
    dag=dag
)

t1.set_upstream(latest_only)
t2.set_upstream(t1)
t3.set_upstream(t2)                                                                                                       