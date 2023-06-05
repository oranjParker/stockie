# views.py
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import authenticate, login, get_user_model
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from django.views import View
from django.http import JsonResponse
from .models import User
import json

from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import get_user_model

class LoginView(View):
    def post(self, request):
        data = json.loads(request.body)
        username = data.get('username')
        password = data.get('password')

        User = get_user_model()
        try:
            user = User.objects.get(username=username)
        except User.DoesNotExist:
            return JsonResponse({"error": "Invalid credentials"}, status=401)

        if not user.check_password(password):
            return JsonResponse({"error": "Invalid password"}, status=401)

        user = authenticate(request, username=username, password=password)
        if user is None:
            return JsonResponse({"error": "Invalid login"}, status=400)

        login(request, user)

        refresh = RefreshToken.for_user(user)

        return JsonResponse({
            "message": "Logged in successfully", 
            "access": str(refresh.access_token),
            "refresh": str(refresh),
        }, status=200)

@method_decorator(csrf_exempt, name='dispatch')
class RegisterView(View):
    def post(self, request):
        # Print the body of the request to the console
        print(request.body)
        data = json.loads(request.body)
        username = data.get('username')
        password = data.get('password')
        email = data.get('email')
        is_creator = data.get('is_creator') == 'true'

        if User.objects.filter(username=username).exists():
            return JsonResponse({"error": "Username already exists"}, status=400)

        if User.objects.filter(email=email).exists():
            return JsonResponse({"error": "Email already exists"}, status=400)

        if len(password) < 8:
            return JsonResponse({"error": "Password too short"}, status=400)

        try:
            user = User.objects.create_user(username, email, password)
            user.is_creator = is_creator
            user.save()
        except Exception as e:
            return JsonResponse({"error": str(e)}, status=500)

        return JsonResponse({"message": "User created successfully"}, status=201)
