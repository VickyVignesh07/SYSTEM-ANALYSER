

from typing import AsyncGenerator
from django.db import models



# Create your models here.

#Converts the memory in to Bytes  

#Systen Information
class Analyser():
    os=str 
    node=str
    release=float
    version=float
    machine=float
    processor=float
    boot_time=float
    user_name=str
    host_name=str
    homedir =str
   

#cpu Information
class Cpu():
    physicalcore=int
    Totalcores=int
    Maxfrequency=float
    Minfrequency=float
    Currentfrequency = float
    #Boot_Time
    Boot_time = float
    #cpu usage
    
    
    cpu_count=float
    cpu_cou = float
   

class usage():
    cpu_usage=float 
    cpu_usage1=float

class battery():
     battery_per =float
     battery_stat=float
     battery_left = float


class Memory():
    vir_total = float
    vir_free =float
    vir_used = float
    vir_percentage = float
    swap_total =float
    swap_free =float
    swap_used =float
    swap_percentage =float
    
class Disks():
    disk_size = float
    disk_used = float
    disk_avail = float
    disk_per = float
    disk_divice =float
    disk_mountpoint =float
    disk_filesystem = float
    disk_read =float
    disk_Write =float
    disk_size1 = float
    disk_used1 = float
    disk_avail1 = float
    disk_per1 = float
    disk_divice1 =float
    disk_filesystem1= float
    disk_read1 =float
    used =float
    free =float
    used1=float
    free1=float
   
class Net_info():
    interface =str
    address_family = str
    ipaddress = float
    netmask = float
    broadcastip = float
    macaddress= float
    broadcastmac =float
    netmaskmac =float
    send = float
    recived = float

class Gpu():
    id = int
    name = str
    load = float
    freememory = float
    usedmemory = float
    totalmemory = float
    temp = float
    uuid =float
    cpu_time = float
    cpu_percent = float
    create_time = float
    ppid=float
    status =float
    p1=str
    process = float

class home():
    main =float    