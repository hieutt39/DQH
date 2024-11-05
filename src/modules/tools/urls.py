# from django.conf.urls import url
from django.urls import path
from . import web

urlpatterns = [
    path('', web.index, name="web_index"),
    path('kham-pha-the-gioi-ma-tuy', web.khamphathegioimatuy, name="web_khamphathegioimatuy"),
    path('test', web.test, name="web_test"),
    # path("<str:task_name>/", tools.task, name="tools_task"),
]
