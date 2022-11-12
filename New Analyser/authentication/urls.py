# -*- encoding: utf-8 -*-
"""
Copyright (c) 2019 - present AppSeed.us
"""

from django.urls import path
from .views import login_view, register_user
from django.contrib.auth.views import LogoutView
from .import views

urlpatterns = [
    path('login/', login_view, name="login"),
    path('register/', register_user, name="register"),
    path("logout/", LogoutView.as_view(), name="logout"),
     path("system_info",views.info,name="system_info"),
    path("cpu_info",views.cpu_info,name="cpu_info"),
    path("battery_info",views.Battery,name='battery_info'),
    path("usage_info",views.Cpu_Usage,name='usage_info'),
    path("disk_info",views.disk,name='disk_info'),
    path("memory_info",views.memory_info,name='memory_info'),
    path("network_info",views.net,name='network_info'),
    path("gpu_info",views.gpu,name='gpu_info'),
    path("processes_info",views.get_processes_info,name='processes_info'),






]
