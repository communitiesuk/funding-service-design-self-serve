from tasks.db_tasks import recreate_local_db
from invoke import task

task.auto_dash_names=True

__all__ = [
    recreate_local_db
]