from django.contrib.auth import login as auth_login, logout as auth_logout, authenticate
from django.contrib.auth.models import User
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json

# Versi BARU yang sudah benar
@csrf_exempt
def login(request):
    if request.method == 'POST':
        # 1. Ganti json.loads jadi request.POST
        username = request.POST.get('username') # <-- BENAR
        password = request.POST.get('password') # <-- BENAR
        
        user = authenticate(request, username=username, password=password) # 2. Tambahkan 'request'
        
        if user is not None:
            if user.is_active:
                auth_login(request, user)
                return JsonResponse({
                    "username": user.username,
                    "status": True,
                    "message": "Login successful!"
                }, status=200)
            else:
                return JsonResponse({"status": False, "message": "Login failed, account is disabled."}, status=401)
        else:
            return JsonResponse({"status": False, "message": "Login failed, please check your username or password."}, status=401)
    return JsonResponse({"status": False, "message": "Invalid request method."}, status=400)

@csrf_exempt
def register(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        username = data.get('username')
        password = data.get('password1')
        password2 = data.get('password2')

        if password != password2:
            return JsonResponse({"status": False, "message": "Passwords do not match."}, status=400)
        
        if User.objects.filter(username=username).exists():
            return JsonResponse({"status": False, "message": "Username already exists."}, status=400)
        
        user = User.objects.create_user(username=username, password=password)
        user.save()
        
        return JsonResponse({
            "username": user.username,
            "status": 'success',
            "message": "User created successfully!"
        }, status=200)
    return JsonResponse({"status": False, "message": "Invalid request method."}, status=400)

@csrf_exempt
def logout(request):
    if request.method == 'POST':
        auth_logout(request)
        return JsonResponse({"status": True, "message": "Logout successful!"}, status=200)
    return JsonResponse({"status": False, "message": "Invalid request method."}, status=400)