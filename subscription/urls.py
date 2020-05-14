from django.urls import path

from .views      import SurveyView

urlpatterns = [
    path('subscription-survey/<int:question_id>', SurveyView.as_view()),
]
