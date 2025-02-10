from datetime import datetime
from .lib import fetch_overlap, find_free_slots

no_task_after_10pm = lambda task : task.end_time.hour > 22 or (task.end_time.hour == 22 and task.end_time.minute > 0)

def modify_nta10pm(suggestion):
    suggestion.new_end = suggestion.new_end.replace(hour=22, minute=0)
    suggestion.rule = 1

def overlapping_tasks(task):
    tasks = fetch_overlap(task.owner, task.start_time, task.end_time)
    return len(tasks) > 0

def modify_overlapping(suggestion):
    free = find_free_slots(suggestion.task.owner, suggestion.new_start.date().isoformat())
    long_enough = []
    length = suggestion.new_end - suggestion.new_start
    now = datetime.now()
    for slot in free:       
        #Convert into datetime objects with arbitrary date because "-" not supported for datetime.time objects
        slot_start = datetime.combine(now.date(), slot[0])
        slot_end = datetime.combine(now.date(), slot[1])
        if length > (slot_end - slot_start):
            continue
        long_enough.append(slot)

    if len(long_enough) == 0:
        return
    
    start_time = suggestion.new_start.time()
    end_time = suggestion.new_end.time()
    
    for slot in long_enough:
        if slot[1] > start_time and end_time > slot[1]:
            suggestion.new_end = datetime.combine(suggestion.new_end.date(), slot[1])
            suggestion.new_start = suggestion.new_end - length
            break
        if (end_time > slot[0] and slot[0] > start_time) or slot[0] > end_time:
            suggestion.new_start = datetime.combine(suggestion.new_start.date(), slot[0])
            suggestion.new_end = suggestion.new_start + length
            break
    
    if suggestion.new_start.time() == start_time:
        suggestion.new_end = datetime.combine(suggestion.new_end.date(), long_enough[-1][1])
        suggestion.new_start = suggestion.new_end - length

    suggestion.rule = 2


rules = [
    (overlapping_tasks, modify_overlapping),
    (no_task_after_10pm, modify_nta10pm),
]