import json
from django.shortcuts import redirect, render
from django.urls import reverse
from django.views import View
from django.http import JsonResponse
from django.contrib.auth.models import User
from validate_email import validate_email
from django.contrib import messages
from django.core.mail import EmailMessage

from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
from django.utils.encoding import force_bytes,  force_str, DjangoUnicodeDecodeError
from django.contrib.sites.shortcuts import get_current_site
from .utils import token_generator 
from django.contrib import auth
# Create your views here.



class registration_view(View):
    def get(self, request):
        return render(request,'auth/register.html')
    
    def post(self,request):
        username = request.POST["username"]
        email = request.POST['email']
        password = request.POST['password']
        context = { 
            'fieldValues':request.POST
        }

        if not User.objects.filter(username=username).exists():
            if not User.objects.filter(email=email).exists():
                if len(password) < 6:
                    messages.error(request,'password too short')
                    return render(request,'auth/register.html',context)
                user = User.objects.create_user(username=username, email=email)
                user.set_password(password)
                user.is_active = False
                user.save()
                
                uidb64 = urlsafe_base64_encode(force_bytes(user.pk))
                token = token_generator.make_token(user)

                domain = get_current_site(request).domain
                link = reverse('activate',kwargs={"uidb64":uidb64,"token":token})
                active_url = "http://" + domain + link

                email_subject = 'Account Activation'
                email_body = "Hello " + username + "\n use this link to verify ur account. \n" + active_url
                
                email = EmailMessage(
                    email_subject,
                    email_body,
                    'noreply@semycolon.com',
                    [email],
                )
                
                email.send(fail_silently=False)
                messages.success(request,'successfully registered. \n Check your email for an activation link and login to your account.\n See you soon!')            
        return render(request,'auth/register.html')
    
class login_view(View):
    def get(self,request):
        return render(request,'auth/login.html')
    
    def post(self,request):

        username = request.POST['username']
        password = request.POST['password']

        if username and password:
            user = auth.authenticate(username=username,password=password)

            if user:
                if user.is_active:
                    auth.login(request,user)
                    messages.success(request,'welcome' + username + "!")
                    return redirect('expenses')
            else:
                messages.error(request,"Verify it is you.")
            return render(request,'auth/login.html')
        else:
            messages.error(request,'Invalid credentials')
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
    
class verification_view(View):
    def get(self,request, uidb64, token):
        id = force_str(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=id)

        if not token_generator.check_token(user,token):
            return redirect('login' + '?message=' + 'User already activated')
        if user.is_active:
            return redirect('login')
        
        user.is_active = True
        user.save()
        messages.success(request,'activaed successful')
        return redirect('login')
    

class logout_view(View):
    def post(self,request):
        auth.logout(request)
        messages.success(request,'logged out succesfully')
        return redirect('login')


    
