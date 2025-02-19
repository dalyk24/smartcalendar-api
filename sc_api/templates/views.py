from django.http import JsonResponse, HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.core import serializers
from .models import *
from .lib.lib import *
import json

def test_view(request):
    return JsonResponse({"message": "Hello from the Django API!"})

def new_user(request):
    user = User.objects.create()
    return JsonResponse({"userID": user.id})

@csrf_exempt
def new_task(request):
    if request.method != 'POST':
        return HttpResponse("Only POST allowed", status=400)
    try:
        data = json.loads(request.body)
        required_fields = ['start_time', 'end_time', 'name', 'userID', 'type']
        for field in required_fields:
            if field not in data:
                return JsonResponse({"error": f"Missing field: {field}"}, status=400)
        task = create_task(data)

        return JsonResponse({"task": serializers.serialize("json", [task])}, status=200)
    except json.JSONDecodeError:
        return JsonResponse({"error": "Invalid JSON format"}, status=400)

@csrf_exempt
def update_task(request):
    if request.method != 'POST':
        return HttpResponse("Only POST allowed", status=400)
    try:
        data = json.loads(request.body)
        required_fields = ['start_time', 'end_time', 'name', 'userID', 'taskID', 'type']
        original = data["old"]
        for field in required_fields:
            if field not in original:
                return JsonResponse({"error": f"Missing field: {field}"}, status=400)
        task = Task.objects.get(start_time=original["start_time"], id=original["taskID"], type=original["type"],
                                end_time=original["end_time"], name=original["name"], owner=original["userID"])
        modify_task(task, data["new"])
        return HttpResponse("OK", status=200)
    except json.JSONDecodeError:
        return JsonResponse({"error": "Invalid JSON format"}, status=400)

@csrf_exempt
def delete_task(request):
    if request.method != 'POST':
        return HttpResponse("Only POST allowed", status=400)
    try:
        data = json.loads(request.body)
        required_fields = ['start_time', 'end_time', 'name', 'userID', 'taskID', 'type']
        for field in required_fields:
            if field not in data:
                return JsonResponse({"error": f"Missing field: {field}"}, status=400)
        task = Task.objects.get(start_time=data["start_time"], id=data["taskID"], type=data["type"],
                                end_time=data["end_time"], name=data["name"], owner=data["userID"])
        task.delete()
        return HttpResponse("OK", status=200)
    except json.JSONDecodeError:
        return JsonResponse({"error": "Invalid JSON format"}, status=400)

@csrf_exempt
def get_tasks(request):
    if request.method != 'POST':
        return HttpResponse("Only POST allowed", status=400)
    try:
        data = json.loads(request.body)
        required_fields = ['start_time', 'end_time', 'userID']
        for field in required_fields:
            if field not in data:
                return JsonResponse({"error": f"Missing field: {field}"}, status=400)
        
        tasks = fetch_tasks(data["userID"], data["start_time"], data["end_time"])
        
        task_list = list(tasks.values(
            "id", "start_time", "end_time", "name", "type", "satisfaction"
        ))
        return JsonResponse({"tasks": task_list}, status=200)
    except json.JSONDecodeError:
        return JsonResponse({"error": "Invalid JSON format"}, status=400)

@csrf_exempt
def evaluate_task(request):
    if request.method != 'POST':
        return HttpResponse("Only POST allowed", status=400)
    
    try:
        data = json.loads(request.body)
        
        if not data.get("taskID"):
            required_fields = ['start_time', 'end_time', 'userID', 'type']
            for field in required_fields:
                if field not in data:
                    return JsonResponse({"error": f"Missing field: {field}"}, status=400)

        suggestion = evaluate(data)
        
        if suggestion:
            suggestion_data = {
                "id": suggestion.id,
                "task": suggestion.task.id,
                "new_start": suggestion.new_start.isoformat(),
                "new_end": suggestion.new_end.isoformat(),
                "rule": suggestion.rule
            }
            return JsonResponse({"suggestion": [suggestion_data]}, status=200)
        
        return JsonResponse({"suggestion": "None"}, status=200)
    
    except json.JSONDecodeError:
        return JsonResponse({"error": "Invalid JSON format"}, status=400)
    
@csrf_exempt
def batch_ratings(request):
    if request.method != 'POST':
        return HttpResponse("Only POST allowed", status=400)
    try:
        data = json.loads(request.body)
        if "ratings" not in data:
            return JsonResponse({"error": f"Missing field: ratings"}, status=400)
        for rating_pair in data["ratings"]:
            task = Task.objects.get(id=rating_pair["id"])
            task_data = {"satisfaction": rating_pair["satisfaction"]}
            modify_task(task, task_data)
        return HttpResponse("OK", status=200)
    
    except json.JSONDecodeError:
        return JsonResponse({"error": "Invalid JSON format"}, status=400)
