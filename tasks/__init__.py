from invoke import task

from tasks.db_tasks import recreate_local_db

task.auto_dash_names = True

__all__ = [recreate_local_db]
