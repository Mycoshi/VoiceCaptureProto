import sys
import os

parent_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
sys.path.insert(0, parent_dir)

from google.oauth2 import service_account
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from JunoCore import add_TasksWithVoice

SCOPES = ['https://www.googleapis.com/auth/tasks']


#Global Variables
taskText = ''

def argument_inputs():
    global taskText
    task = 'Butts'
    taskText = task 

def authenticate():
    flow = InstalledAppFlow.from_client_secrets_file(
        'Tasks/client_secret_file.json', SCOPES)
    creds = flow.run_local_server(port=0)
    service = build('tasks', 'v1', credentials=creds)
    return service

def get_task_lists(service):
    results = service.tasklists().list().execute()
    items = results.get('items', [])
    return items

def create_task_list(service, title):
    task_list = {
        'title': title
    }
    result = service.tasklists().insert(body=task_list).execute()
    return result

def add_task(service, task_list_id, title):
    task = {
        'title': title
    }
    result = service.tasks().insert(tasklist=task_list_id, body=task).execute()
    return result

#RUN
service = authenticate()
argument_inputs()

# Retrieve and print existing task lists
task_lists = get_task_lists(service)
print("Existing task lists:")
for task_list in task_lists:
    print(f"{task_list['id']}: {task_list['title']}")

# Assume you want to add a task to the first task list in the list
if task_lists:
    selected_task_list_id = task_lists[0]['id']
    selected_task_list_title = task_lists[0]['title']
    print(f"Adding task to the task list: {selected_task_list_title}")

    # Add a new task to the selected task list
    new_task = add_task(service, selected_task_list_id, taskText)
    print(f"Task added: {new_task['title']}")
else:
    print("No task lists found.")