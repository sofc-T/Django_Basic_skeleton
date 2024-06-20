from django.shortcuts import redirect, render
import os
import json
from django.conf import settings
from django.shortcuts import render
from django.views import View
from .models import UserPreferences
from django.contrib import messages 

# Create your views here.

class preference_view(View):
    file_path = os.path.join(settings.BASE_DIR,'preferences/currency_data.json')
    with open(file_path) as currency_data:                  
        currency_data = json.load(currency_data)
    def get(self,request):

        try :
            user_preferences = UserPreferences.objects.get(user=request.user)
            
        except:
            UserPreferences.objects.create(user=request.user,currency=None)
            user_preferences = UserPreferences.objects.get(user=request.user)
        return render(request,'preferences/index.html',{'currency_data':self.currency_data,'user_preferences':user_preferences})

    def post(self,request):
        
        currency = request.POST['currency']
        
        try :
            user_preferences = UserPreferences.objects.get(user=request.user)
            user_preferences.currency = currency
        except:
            UserPreferences.objects.create(user=request.user,currency=currency)
            user_preferences = UserPreferences.objects.get(user=request.user)


        user_preferences.save()
        messages.success(request,'changes saved')
        return render(request,'preferences/index.html',{'currency_data':self.currency_data,'user_preferences':user_preferences})


