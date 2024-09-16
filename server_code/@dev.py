import anvil.server
import anvil.users
from AnvilFusion.server.utils import get_logged_user, save_logged_user
from .app import models
from anvil.tables import app_tables


def add_background_task(task_id, context=None, logged_user=None):
    bg_task_row = app_tables.app_background_tasks.get(task_id=task_id)
    if bg_task_row is None:
        app_tables.app_background_tasks.add_row(task_id=task_id, context=context, logged_user=logged_user)
    else:
        bg_task_row['context'] = context
        bg_task_row['logged_user'] = logged_user


def update_background_task(task_id, status, result=None):
    bg_task_row = app_tables.app_background_tasks.get(task_id=task_id)
    if bg_task_row:
        bg_task_row['status'] = status
        bg_task_row['result'] = result


@anvil.server.background_task
def background_task(logged_user=None):
    # print('Background task started')
    print('background task context', anvil.server.context)
    print('logged_user', get_logged_user())
    anvil.server.task_state = 'my bg task'
    print('task_state', anvil.server.task_state)
    if logged_user:
        save_logged_user(current_user=logged_user)
    # print('AnvilFusion function', get_logged_user())
    add_background_task(
        anvil.server.context.background_task_id,
        logged_user=get_logged_user()
    )
    result = bar()
    update_background_task(
        anvil.server.context.background_task_id,
        status='finished',
        result=result
    )
    return 'Background task done'


@anvil.server.callable
def foo():
    print('Lunching BG task')
    print('server context', anvil.server.context)
    bg_task = anvil.server.launch_background_task('background_task', get_logged_user())
    print(bg_task, bg_task.get_id())


def bar():
    print('bar task state', anvil.server.task_state)
    locations = models.Location.search()
    for location in locations:
        print(location['name'])


@anvil.server.callable
def foo_bar():
    rows = app_tables.app_background_tasks.search()
    for row in rows:
        print(row['task_id'], row['status'], row['result'])
