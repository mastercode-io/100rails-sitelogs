import anvil.server
import anvil.users
from AnvilFusion.server.utils import get_logged_user, save_logged_user
from anvil.tables import app_tables
import traceback
import datetime
import importlib


def register_background_task(task_id, context=None, logged_user=None):
    bg_task_row = app_tables.app_background_tasks.get(task_id=task_id)
    if bg_task_row is None:
        app_tables.app_background_tasks.add_row(
            task_id=task_id,
            context=context,
            logged_user=logged_user,
            status='running',
            start_time=datetime.datetime.now(),
        )


def update_background_task(task_id, status=None, result=None):
    bg_task_row = app_tables.app_background_tasks.get(task_id=task_id)
    if not bg_task_row:
        return
    if status:
        bg_task_row['status'] = status
        bg_task_row['result'] = result
        bg_task_row['updated_time'] = datetime.datetime.now()
    else:
        bg_task = anvil.server.get_background_task(task_id)
        if bg_task and bg_task_row['status'] == 'running':
            bg_task_row['status'] = 'running' if bg_task.is_running() else bg_task.get_termination_status()
            bg_task_row['result'] = bg_task.get_return_value()
            bg_task_row['updated_time'] = datetime.datetime.now()


@anvil.server.callable
def get_background_task_status(task_id):
    update_background_task(task_id)
    bg_task_row = app_tables.app_background_tasks.get(task_id=task_id)
    if not bg_task_row:
        return
    else:
        return {
            'task_id': bg_task_row['task_id'],
            'status': bg_task_row['status'],
            'result': bg_task_row['result'],
            'start_time': bg_task_row['start_time'].isoformat() if bg_task_row['start_time'] else None,
            'updated_time': bg_task_row['updated_time'].isoformat() if bg_task_row['updated_time'] else None,
        }


@anvil.server.background_task
def background_task_manager(logged_user, context, module_name, func_name, *args, **kwargs):
    if logged_user:
        save_logged_user(current_user=logged_user)
    else:
        logged_user = {}
    register_background_task(
        anvil.server.context.background_task_id,
        context=context,
        logged_user=logged_user,
    )
    try:
        module = importlib.import_module(module_name)
        func = getattr(module, func_name)
        result = func(*args, **kwargs)
        status = 'completed'
    except Exception as e:  # noqa
        result = traceback.format_exc()
        status = 'failed'
    update_background_task(
        anvil.server.context.background_task_id,
        status=status,
        result=result,
    )
    return result
