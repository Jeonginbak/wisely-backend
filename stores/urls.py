from django.urls import path

from .views import RazorCartView

urlpatterns = [
    path('razor-set/cart', RazorCartView.as_view()),
]
