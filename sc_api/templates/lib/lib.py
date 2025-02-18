from ..models import *
from datetime import datetime, time
from django.db.models import Q

def create_task(data, tentative=False):
    if tentative:
        task = Tentative_Task()
    else:
        task = Task()
    task.owner = User.objects.get(id=data["userID"])
    task.start_time = datetime.fromisoformat(data["start_time"])
    task.end_time = datetime.fromisoformat(data["end_time"])
    task.name = data["name"]
    task.type = data["type"]
    task.save()
    return task

def modify_task(task, data):
    if data.get("start_time"):
        task.start_time = data["start_time"]
    if data.get("end_time"):
        task.end_time = data["end_time"]
    if data.get("name"):
        task.name = data["name"]
    if data.get("satisfaction"):
        task.satisfaction = data["satisfaction"]
    if data.get("type"):
        task.type = data["type"]
    task.save()

def fetch_tasks(userID, start, end):
    return Task.objects.filter(owner=userID, start_time__gte=start, start_time__lte=end).order_by("start_time")

def fetch_overlap(userID, start, end):
    return Task.objects.filter(Q(owner=userID), Q(start_time__gte=start, start_time__lte=end) | Q(end_time__gte=start, end_time__lte=end) | Q(start_time__lte=start, end_time__gte=end))

def create_suggestion(task, modifier):
    suggestion = Suggestion()
    suggestion.task = task
    suggestion.new_start = task.start_time
    suggestion.new_end = task.end_time
    modifier(suggestion)
    suggestion.save()
    return suggestion

def find_free_slots(user, date_str):
    start = datetime.fromisoformat(date_str + " 00:00")
    end = datetime.fromisoformat(date_str + " 23:59")
    
    tasks = fetch_tasks(user, start, end)

    if len(tasks) == 0:
        return [[time(), time(23, 59)]]
    
    occupied = []

    for task in tasks:
        start_time = task.start_time.time()
        end_time = task.end_time.time()
        if task.end_time.date() != task.start_time.date():
            end_time = time(23, 59)
        occupied.append([start_time, end_time])
    
    merged = merge_times(occupied)

    return invert_times(merged)

def merge_times(times):
    times.sort()
    merged = []
    merged.append(times[0])

    for i in range(1, len(times)):
        last = merged[-1]
        curr = times[i]
        if curr[0] <= last[1]:
            last[1] = max(last[1], curr[1])
        else:
            merged.append(curr)
    return merged

def invert_times(times):
    if len(times) == 0:
        return [[time(), time(23, 59)]]
    
    if times[0][0] != time():
        inverted = [[time(), times[0][0]]]
    else:
        inverted = []
    
    for i in range(1, len(times)):
        inverted.append([times[i - 1][1], times[i][0]])

    if times[-1][1] != time(23, 59):
        inverted.append([times[-1][1], time(23, 59)])
    
    return inverted

from .rules import rules

def evaluate(data):
    if data.get("taskID"):
        task = Tentative_Task.objects.get(id=data["taskID"])
    else:
        task = create_task(data, True)
    for (rule, modifier) in rules:
        if rule(task):
            return create_suggestion(task, modifier)
    return None