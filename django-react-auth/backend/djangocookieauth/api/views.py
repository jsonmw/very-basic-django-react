from django.shortcuts import render
import json
from django.contrib.auth import authenticate, login, logout
from django.http import JsonResponse
from django.views.decorators.csrf import ensure_csrf_cookie
from django.views.decorators.http import require_POST

# Parses JSON info from request body and extracts username/password
@require_POST
def login_view(request):
    data = json.loads(request.body)
    username = data.get("username")
    password = data.get("password")

    if username is None or password is None:
        return JsonResponse({"detail":"Please provide username and password."})
    
    # Check if user is valid
    user = authenticate(username=username, password=password)
    if user is None:
        return JsonResponse({"detail": "Invalid credentials."}, 
                            status=400)
    login(request, user)
    return JsonResponse({"detail": "Successfully logged in."})

def logout_view(request):
    if not request.user.is_authenticated:
        return JsonResponse({"detail": "You are not logged in."}, status=400)
    logout(request)
    return JsonResponse({"detail": "Sucessfully logged out."})

@ensure_csrf_cookie
def session_view(request):
    if not request.user.is_authenticated:
        return JsonResponse({"isauthenticated": False})
    return JsonResponse({"isauthenticated": True})

def whoami_view(request):
    if not request.user.is_authenticated:
        return JsonResponse({"isauthenticated": False})
    return JsonResponse({"username": request.user.username})

