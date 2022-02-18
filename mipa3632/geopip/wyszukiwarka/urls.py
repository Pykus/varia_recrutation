# -*- coding: utf-8 -*-

from django.conf.urls import url
from . import views

app_name='wyszukiwarka'
urlpatterns = [
    #url(r'^$', views.wyszukaj, name='hello_form'),
    url('link/(?P<miejscowosc>[\w -]*)/(?P<ulica>[\w ]*)/(?P<numer>[-\w\d/ ]*)$', views.wyszukaj, name='hello_form_post'),
    url('navi/(?P<nazwapracodawcy>[\w -]*)$', views.wyszukajWNavi, name='wyszukajWNavi'),
]
'''
urlpatterns =[
    #url(r'^$', views.IndexView.as_view(), name='index'),
    #url(r'^(?P<pk>[0-9]+)/$', views.DetailView.as_view(), name='detail'),
    #url(r'^(?P<pk>[0-9]+)/results/$', views.ResultsView.as_view(), name='results'),
    #url(r'^(?P<question_id>[0-9]+)/vote/$', views.vote, name='vote'),
    url(r'^$', views.index, name='index'),
    url(r'(?P<question_id>[0-9]+)/$', views.detail, name='detail'),
    url(r'(?P<question_id>[0-9]+)/results/$', views.results, name='results'),
    url(r'(?P<question_id>[0-9]+)/vote$', views.vote, name='vote'),
]
'''