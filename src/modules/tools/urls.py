# from django.conf.urls import url
from django.urls import path, re_path
from . import web

urlpatterns = [
    path('', web.index, name="home"),
    path('quiz', web.quiz_index, name="quiz_index"),
    re_path(r'kptgmt/pdf/(?P<id>\w+)/$', web.kptgmt_pdf, name="web_kptgmt_pdf"),
    re_path(r'ndccmt/video/$', web.ndccmt_video, name="web_ndccmt_video"),
    re_path(r'thcmt/video/$', web.thcmt_video, name="web_thcmt_video"),
    re_path(r'thcmt/pdf/(?P<id>\w+)/$', web.thcmt_pdf, name="web_thcmt_pdf"),
    re_path(r'knpcmt/pdf/(?P<id>\w+)/$', web.knpcmt_pdf, name="web_knpcmt_pdf"),
    re_path(r'library/digital/pdf/(?P<id>\w+)/$', web.library_library, name="library_library"),
]
