from django.urls import path , include
from . import views

urlpatterns = [
    path('expenses', views.index, name="expenses"),
    path('add_expenses',views.add_expenses, name='add_expenses'),
    
]