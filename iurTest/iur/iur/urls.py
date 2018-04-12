"""iur URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.8/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import include, url
from django.contrib import admin
from django.conf.urls import *
from django.conf import settings
from main.views import index, login_page, uindex
from main.views import check_in_units
from main.views import units_list
from main.views import units_borrow
from main.views import myView
from main.views import search_results
from main.views import send_email
from main.views import b_d_request
from main.views import b_d_request_list
from main.views import report_down_load
from main.views import login_view, createuser, logout
from main.views import b_d_request_success

urlpatterns = [
    url(r'^admin/', include(admin.site.urls)),
    url(r'^index/$', index),
    url(r'^uindex/$', uindex),
    url(r'^units/checkin/', check_in_units),
    url(r'^test/$', myView.as_view()),
    url(r'^units/list/', units_list),
    url(r'^units/borrow/', units_borrow),
    url(r'^search/result/', search_results),
    url(r'^search/result/', search_results),
    url(r'^send_email/', send_email),
    url(r'^b_d_request/send_request', b_d_request),
    url(r'^b_d_request/list/', b_d_request_list),
    url(r'^report_down_load/$', report_down_load),
    url(r'^login_action/$', login_view),
    url(r'^login/$',login_page),
    url(r'^logout/$',logout),
    url(r'^signup_action/$',createuser),
    url(r'^b_d_request/success', b_d_request_success),
]
