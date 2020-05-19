from django.urls import path

from .views import CartAddView

urlpatterns = [
    path('cart', CartAddView.as_view()),
]
