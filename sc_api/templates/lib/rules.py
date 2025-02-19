from datetime import datetime
from .lib import fetch_overlap, find_free_slots, categorize_time, change_to_time_of_day, model
from copy import deepcopy
from random import randint
import numpy as np

no_task_after_10pm = lambda task : task.end_time.hour > 22 or (task.end_time.hour == 22 and task.end_time.minute > 0)

def modify_nta10pm(suggestion, _):
    suggestion.new_end = suggestion.new_end.replace(hour=22, minute=0)
    return 1

def overlapping_tasks(task):
    tasks = fetch_overlap(task.owner, task.start_time, task.end_time)
    return len(tasks) > 0

def modify_overlapping(suggestion, _):
    free = find_free_slots(suggestion.task.owner, suggestion.new_start.date().isoformat())
    long_enough = []
    length = suggestion.new_end - suggestion.new_start
    date = datetime.now().date()
    for slot in free:       
        #Convert into datetime objects with arbitrary date because "-" not supported for datetime.time objects
        slot_start = datetime.combine(date, slot[0])
        slot_end = datetime.combine(date, slot[1])
        if length > (slot_end - slot_start):
            continue
        long_enough.append(slot)

    if len(long_enough) == 0:
        return
    
    start_time = suggestion.new_start.time()
    end_time = suggestion.new_end.time()
    
    distances = []
    for slot in long_enough:
        distances.append([slot, min(abs(datetime.combine(date, slot[1]) - datetime.combine(date, end_time)),
                                    abs(datetime.combine(date, slot[0]) - datetime.combine(date, start_time)))])

    best_slot = min(distances, key=lambda x: x[1])

    if best_slot[1] == abs(datetime.combine(date, best_slot[0][1]) - datetime.combine(date, end_time)):
        suggestion.new_end = datetime.combine(suggestion.new_end.date(), best_slot[0][1])
        suggestion.new_start = suggestion.new_end - length
    else:
        suggestion.new_start = datetime.combine(suggestion.new_start.date(), best_slot[0][0])
        suggestion.new_end = suggestion.new_start + length

    return 2

def ml_model(task):
    return task.type == "Exercise" or task.type == "Leisure"

def modify_ml(suggestion, task):
    rule_id = 0
    modified = False

    duration = (task.end_time - task.start_time).total_seconds() // 60
    arr = [duration] + [0] * 6
    if task.type == "Exercise":
        arr[-2] = 1
    else:
        arr[-1] = 1
    all_times = [deepcopy(arr) for _ in range(4)]
    for i in range(4):
        all_times[i][1 + i] = 1

    all_times = np.array(all_times)

    predictions = model.predict(all_times)

    max_index = max(range(len(predictions)), key=predictions.__getitem__)

    if predictions[categorize_time(task)] != max(predictions) and randint(0, 1) == 0:
        rule_id = 3
        change_to_time_of_day(suggestion, max_index)
        modified = True
    
    predictions[max_index] = 0

    if not modified and predictions[categorize_time(task)] < max(predictions):
        rule_id = 3
        max_index = max(range(len(predictions)), key=predictions.__getitem__)
        change_to_time_of_day(suggestion, max_index)
    
    if len(fetch_overlap(task.owner, suggestion.new_start, suggestion.new_end)) > 0:
        if rule_id == 0:
            rule_id = 2
        modify_overlapping(suggestion, task)

    return rule_id

rules = [
    (ml_model, modify_ml),
    (overlapping_tasks, modify_overlapping),
    (no_task_after_10pm, modify_nta10pm),
]