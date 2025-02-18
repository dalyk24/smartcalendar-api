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

    suggestion.rule = 2


rules = [
    (overlapping_tasks, modify_overlapping),
    (no_task_after_10pm, modify_nta10pm),
]