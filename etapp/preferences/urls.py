from . import views
from django.urls import path
from django.views.decorators.csrf import csrf_exempt

urlpatterns = [
    path('',csrf_exempt(views.preference_view.as_view()),name='preferences'),
]