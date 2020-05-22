from django.urls import path

from .views      import SurveyView, ResultView

urlpatterns = [
    path('subscription-survey/<int:question_id>', SurveyView.as_view()),
    path('subscription-result', ResultView.as_view()),
]
