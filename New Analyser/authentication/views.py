# -*- encoding: utf-8 -*-
"""
Copyright (c) 2019 - present AppSeed.us
"""

from os import name
from django.shortcuts import render
import psutil
import platform

# Create your views here.
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User
from django.forms.utils import ErrorList
from django.http import HttpResponse
from .forms import LoginForm, SignUpForm
from .models import Analyser,Cpu, Disks, Net_info,Memory,Gpu,usage,battery
from datetime import datetime as datetime
import GPUtil
import platform
import psutil
import socket
import os.path
import os
import time
import getpass


def get_size(bytes ,suffix ="B"):
    factor = 1024
    for unit in ["","K","M","G","T","P"]:
        if bytes < factor:
            return f"{bytes:.2f}  {unit}{suffix}"
        bytes/=factor     

def get_size1(bytes ,suffix ="B"):
    factor = 1024
    for unit in ["","K","M","G","T","P"]:
        if bytes < factor:
            return f"{bytes:.2f} "
        bytes/=factor     

         

def convertTime(seconds):
    minutes,seconds = divmod(seconds ,60)
    hours , minutes = divmod(minutes,60)
    return "%dHr:%02dmin:%02dsec" %(hours ,minutes,seconds)  

def get_per():
    
    while True:
        cpu =psutil.cpu_percent(interval =1)
        return(cpu)

def login_view(request):
    form = LoginForm(request.POST or None)

    msg = None

    if request.method == "POST":

        if form.is_valid():
            username = form.cleaned_data.get("username")
            password = form.cleaned_data.get("password")
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect("/")
            else:    
                msg = 'Invalid credentials'    
        else:
            msg = 'Error validating the form'    

    return render(request, "accounts/login.html", {"form": form, "msg" : msg})

def register_user(request):

    msg     = None
    success = False

    if request.method == "POST":
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get("username")
            raw_password = form.cleaned_data.get("password1")
            user = authenticate(username=username, password=raw_password)

            msg     = 'User created - please <a href="/login">login</a>.'
            success = True
            
            #return redirect("/login/")

        else:
            msg = 'Form is not valid'    
    else:
        form = SignUpForm()

    return render(request, "accounts/register.html", {"form": form, "msg" : msg, "success" : success })



#system Information
def info(request):
    #System Info
    des1=Analyser()
    des1.os= platform.system
    des1.node=platform.node
    des1.release=platform.release
    des1.version=platform.version
    des1.machine=platform.machine
    des1.processor=platform.processor
    #User info
    des1.host_name=socket.getfqdn()
    des1.homedir=os.path.expanduser("~")
    des1.user_name=getpass.getuser()
    return render(request , 'system_info.html',{"des1":des1})



#Cpu Information
def cpu_info(request):
    #cpu Core
    cp1 =Cpu()
    cp1.physicalcore=psutil.cpu_count(logical=False)
    cp1.Totalcores=psutil.cpu_count(logical=True)
    #cpu Frequency
    cpufreq=psutil.cpu_freq()         
    cp1.Maxfrequency= cpufreq.max
    cp1.Minfrequency=cpufreq.min
    cp1.Currentfrequency=cpufreq.current
    #Boot_Time
    boot_time_timestamp = psutil.boot_time()
    cp1.Boot_time = datetime.fromtimestamp(boot_time_timestamp)
   
    cp1.cpu_count  = os.cpu_count()
   

    return render(request ,'basic.html',{'cp1':cp1})

def Cpu_Usage(request):
    obj= usage()
    obj.cpu_usage = get_per()
    obj.cpu_usage1 = 100 -get_per()

    return render(request ,'cpu_usage.html',{'obj':obj})

def Battery(request):
    obj1 = battery()
    newbattery = psutil.sensors_battery()
    obj1.battery_per =newbattery.percent
    obj1.battery_left =convertTime(newbattery.secsleft)
    obj1.battery_stat= newbattery.power_plugged
    return render(request,'battery.html',{'obj1':obj1})




def memory_info (request):
    mem =Memory()
    svmem = psutil.virtual_memory()
    mem.vir_total = get_size(svmem.total)
    mem.vir_used = get_size(svmem.used)
    mem.vir_free =get_size(svmem.available)
    mem.vir_percentage = svmem.percent
    swap = psutil.swap_memory()
    mem.swap_total= get_size(swap.total)
    mem.swap_used =get_size(swap.used)
    mem.swap_free =get_size(swap.free)
    mem.swap_percentage=swap.percent
    return render(request ,'memory.html',{"mem":mem})




def disk(request):
    disk2 = Disks()
    partitions = psutil.disk_partitions()
    for partition in partitions:
        disk2.disk_divice =partition.device
        disk2.disk_mountpoint =partition.mountpoint
        disk2.disk_filesystem =partition.fstype
        partition_usage = psutil.disk_usage(partition.mountpoint)    
        disk2.disk_size = get_size(partition_usage.total)
        disk2.disk_used = get_size1(partition_usage.used)
        disk2.disk_avail =get_size1(partition_usage.free)
        # in GB
        disk2.used = get_size(partition_usage.used)
        disk2.free =get_size(partition_usage.free)
        disk2.disk_per = partition_usage.percent
        for par in partitions:
            disk2.disk_divice1 = par.device 
            partition_usage1 = psutil.disk_usage(par.mountpoint)    
            disk2.disk_size1 = get_size(partition_usage1.total)
            disk2.disk_used1 = get_size1(partition_usage1.used)
            disk2.disk_avail1 =get_size1(partition_usage1.free)
            # In GB
            disk2.used1 = get_size(partition_usage1.used)
            disk2.free1 =get_size(partition_usage1.free)
            disk2.disk_per1 = partition_usage1.percent  
            disk2.disk_filesystem1 =partition.fstype
            disk_io =psutil.disk_io_counters()  
            disk2.disk_read1 = get_size(disk_io.read_bytes)           
        disk_io =psutil.disk_io_counters()
        disk2.disk_read =get_size(disk_io.read_bytes)
        disk2.disk_Write =get_size(disk_io.write_bytes)
        return render (request ,"disk.html" ,{"disk2":disk2})
    
 

def net(request):
    net1 = Net_info()
    if_addrs = psutil.net_if_addrs()
    for interface_name ,interface_addresses in if_addrs.items():
        for address in interface_addresses:
            net1.interface = interface_name
            if str(address.family) =='AddressFamily.AF_INET':
                net1.ipaddress = address.address
                net1.broadcastip = address.broadcast
                net1.netmask =address.netmask

            elif str(address.family) =='AddressFamily.AF_PACKET':
                net1.macaddress =address.address
                net1.netmaskmac = address.netmask
                net1.broadcastmac =address.broadcast
            net_io =psutil.net_io_counters()
            net1.send =get_size(net_io.bytes_sent)
            net1.recived=get_size(net_io.bytes_recv)            
        return render (request ,"network.html",{"net1":net1})

def gpu(request):
    gpu1 = Gpu()
    gpus = GPUtil.getGPUs()
    for gpu2 in gpus:

        gpu1.id = gpu2.id
        gpu1.name =gpu2.name
        gpu1.load = gpu2.load
        gpu1.freememory = (gpu2.memoryFree)
        gpu1.totalmemory = gpu2.memoryTotal
        gpu1.usedmemory = gpu2.memoryUsed
        gpu1.temp = gpu2.temperature
        gpu1.uuid = gpu2.uuid

        return render( request , "gpu.html",{"gpu1":gpu1})



def get_processes_info(request):
        processes =[]
        p1 = psutil.process_iter()
        for p2 in p1:

            with p2.oneshot():

                pid = p2.pid
                if pid  == 0:
                    continue
                name = p2.name  
                try:
                    create_time = datetime.fromtimestamp(p2.create_time()) 
                except OSError:
                    create_time = datetime.fromtimestamp(psutil.boot_time())  
                try:
                    cores = len(p2.cpu_affinity())
                except psutil.AccessDenied:
                    cores = 0  
                cpu_usage = p2.cpu_percent()
                status = p2.status
                try:
                    nice = int(p2.nice())
                except psutil.AccessDenied:
                    nice = 0 
                try:
                    memory_usage =p2.memory_full_info()
                except psutil.AccessDenied:
                    memory_usage = 0    
                io_counters = p2.io_counters()
                read_bytes = io_counters.read_bytes
                write_bytes = io_counters.write_bytes
                n_threads = p2.num_threads()
                try:
                    username = p2.username()
                except psutil.AccessDenied:
                    username ='N/A'


            processes.append({'pid':pid , 'name':name , 'create_time': create_time , 'cores':cores ,'cpu_usage':cpu_usage,
              'nice':nice,'status':status ,'memory_usage':memory_usage,'read_bytes':read_bytes,"write_bytes":write_bytes,'n_threads':n_threads,'username':username})
        return render(request ,'processes.html',{'processes':processes})




