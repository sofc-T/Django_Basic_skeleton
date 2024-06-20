import json
from django.shortcuts import render
from django.views import View
from django.http import JsonResponse
from django.contrib.auth.models import User
from validate_email import validate_email
from django.contrib import messages
# Create your views here.



class registration_view(View):
    def get(self, request):
        return render(request,'auth/register.html')
    
    def POST(self,request):
        messages.success(request,'Successfully Done')
        return render(request,'auth/registration.html')
    
class login_view(View):
    def get(self,request):
        return render(request,'auth/login.html')
    
class user_name_validation_view(View):
    def post(self,request):
        data = json.loads(request.body)
        username = data["userName"]
        if not str(username).isalnum():
            return JsonResponse({'usernameError':' Username should contain only Alphanumeric characters.'},status=400)
        if User.objects.filter(username = username).exists():
            return JsonResponse({'usernameError':"Username taken. Please Choose another."}, status=409)
        return JsonResponse({'valid':True})

class email_validation(View):
    def post(sef,request):
        data = json.loads(request.body)
        email = data['email']
        if not validate_email(email):
            return JsonResponse({'emailError':'Not a valid email'}, status = 400)
        if User.objects.filter(email=email).exists():
            return JsonResponse({'emailError':'Account already exists with this email. Please choose another one'},status = 400)
        
        return JsonResponse({'valid':True})
    
