from . import views
from django.urls import path
from django.views.decorators.csrf import csrf_exempt

urlpatterns = [
    path('',views.registration_view.as_view(), name='register'),
    path('register',views.registration_view.as_view(), name='register'),
    path('login',views.login_view.as_view(), name='login'),
    path('validateUsername',csrf_exempt(views.user_name_validation_view.as_view()), name='validateUsername'),
    path('validateEmail',csrf_exempt(views.email_validation.as_view()),name = 'validateEmail'),
    path('activate/<uidb64>/<token>',views.verification_view.as_view(),name = 'activate'),
    path('logout',views.logout_view.as_view(),name='logout'),
]