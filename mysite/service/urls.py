from django.urls import path
from . import views

urlpatterns = [
    path("advise/", views.advise, name="advise")
]
