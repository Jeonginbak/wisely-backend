from django.urls import path

from .views      import SurveyView, ResultView

urlpatterns = [
    path('survey/<int:question_id>', SurveyView.as_view()),
    path('result', ResultView.as_view()),
]
