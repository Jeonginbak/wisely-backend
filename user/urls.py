from django.urls import path
from .views      import EmailCheckView, SignUpView, LogInView

urlpatterns = [
    path('check', EmailCheckView.as_view()),
    path('signup', SignUpView.as_view()),
    path('login', LogInView.as_view())
]
