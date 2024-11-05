# from django.conf.urls import url
from django.urls import path
from . import view

urlpatterns = [
    path('', view.index, name="test_index"),
]
