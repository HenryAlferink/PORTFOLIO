### INTRODUCTION ###

'''
on CLI you can use "airflow run <dag_id> <task_id> <start_date>"

simply run "airflow" in CLI to list possible commands
'''

from airflow.models import DAG
from datetime import datetime

default_arguments = {
    'owner': 'jdoe',
    'email':'jdoe@datacamp.com',
    'start_date': datetime(2020, 1, 20)  # earliest time dag could be run
}

# the var etl_dag is just to be used to interact with the object in Python;
# when interacting in CLI you'd use the dag_id: etl_workflow
etl_dag = DAG('etl_workflow', default_args=default_arguments)

''' airflow in CLI

"airflow -h"
"airflow list_dags"

Should you use the CLI of Python?
- CLI for starting Airflow processes, manaully running DAGs, getting log info
- Python for creating the DAG, editing DAGs

It is also possible to use a web UI instead of CLI. But CLI may be easier to use if
you're accessing through SSH for example.
'''


### OPERATORS ###
# represent a single task in a workflow
# usually run independently from one another

# Bash operator. This runs in a temporary directory. Can specify environ variables to try replicate
# running a task on a local system (environment variables are runtime settings interpretted by the shell).
from ariflow.operators.bash_operator import BashOperator
example_bash_operator = BashOperator(
    task_id='bash_example',
    bash_command='cat addresses.txt | awk "NF==10" > cleaned.txt',
    dag=dag
)

# gotchas: if one operator runs in a certain directory, it's not certain whether another operator
# will have access to that same information. If this is required it must be explicitly set up. 
# May require extensive environment variables. E.g. in Bash the tilde represents the home directory,
# but this isn't set by default in airflow.
# It can be difficult to run tasks with elevated privileges.

# example_bash_operator is an example of an Airflow task. A task is an *instance* of an operator.
# They are usually assigned to Python variables.

''' Task dependencies
Most tasks have dependencies associated with them. 
There are upstream and downstream tasks. Upstream tasks must be completed before any tasks downstream
from it are completed. Use the *bitshift* operators (<< (downstream), >> (upstream)) to define dependencies between operators.
'''

example_dag = DAG('example_dag', default_args=default_arguments)

task1 = BashOperator(
    task_id='first_task',
    bash_command='echo 1',
    dag=example_dag
)

task2 = BashOperator(
    task_id='second_task',
    bash_command='echo 2',
    dag=example_dag
)

# set first_task to run before second_task
task1 >> task2  # "task1 is 'upstream' of task2"
# or:
# task 2 << task1