import urllib2
import json
import time
import datetime

import os
 
APIKEY = "vUAoLurFOH=xkqr9s7w4dXuXBGY=" 

# Return CPU temperature as a character string
def get_temp():
        file = open("/sys/class/thermal/thermal_zone0/temp") 
        temp = float(file.read()) / 1000 
        file.close() 
        print "CPU temp: %.3f" %temp 
        return temp

def getCPUtemperature():
    res = os.popen('vcgencmd measure_temp').readline()
    return(res.replace("temp=","").replace("'C\n",""))
 
def getCPUtemperature_2():
    return os.popen('vcgencmd measure_temp').read()[5:9]
 
def getCPUtemperature_3():
    with open("/sys/class/thermal/thermal_zone0/temp") as tempFile:
        res = tempFile.read()
        res=str(float(res)/1000)
    return res
 
# Return RAM infomation(unit=kb) in a list
# Index 0: total RAM
# Index 1: used RAM
# Index 2: free RAM
def getRAMinfo():
    p = os.popen('free')
    i = 0
    while 1:
        i = i+1
        line = p.readline()
        if i == 2:
            return(line.split()[1:4])
 
# Return information about disk space as a list (unit include)
# Index 0: total disk space
# Index 1: used disk space
# Index 2: remaining disk space
# Index 3: percentaage of disk used
def getDiskSpace():
    p = os.popen("df -h /")
    i = 0
    while 1:
         i = i + 1
         line = p.readline()
         if i == 2:
             return(line.split()[1:5])

def http_put():

    CPU_temp = getCPUtemperature()
    CPU_temp_2 = getCPUtemperature_2()
    CPU_temp_3 = getCPUtemperature_3()

    RAM_stats = getRAMinfo()
    RAM_total = round(int(RAM_stats[0]) / 1000, 1)
    RAM_used = round(int(RAM_stats[1]) / 1000, 1)
    RAM_free = round(int(RAM_stats[2]) /1000, 1)

    DISK_stats = getDiskSpace()
    DISK_total = DISK_stats[0]
    DISK_used = DISK_stats[1]
    DISK_perc = DISK_stats[3]

    temperature = get_temp() 
    CurTime = datetime.datetime.now()


    url='http://api.heclouds.com/devices/500237898/datapoints'
    values={'datastreams':[{"id":"temp","datapoints":[{"at":CurTime.isoformat(),"value":temperature}]},
                               {"id":"CPU_temp","datapoints":[{"value":CPU_temp}]},
                               {"id":"CPU_temp_2","datapoints":[{"value":CPU_temp_2}]},
                               {"id":"CPU_temp_3","datapoints":[{"value":CPU_temp_3}]},
                               {"id":"RAM_stats","datapoints":[{"value":RAM_stats}]},
                               {"id":"RAM_total","datapoints":[{"value":RAM_total}]},
                               {"id":"RAM_used","datapoints":[{"value":RAM_used}]},
                               {"id":"RAM_free","datapoints":[{"value":RAM_free}]},
                               {"id":"DISK_stats","datapoints":[{"value":DISK_stats}]},
                               {"id":"DISK_total","datapoints":[{"value":DISK_total}]},
                               {"id":"DISK_used","datapoints":[{"value":DISK_used}]},
                               {"id":"DISK_perc","datapoints":[{"value":DISK_perc}]}
                               ]}             


    jdata = json.dumps(values)          
    print jdata
    request = urllib2.Request(url, jdata)
    request.add_header('api-key', APIKEY)
    request.get_method = lambda:'POST'      
    request = urllib2.urlopen(request)
    return request.read()

if __name__ == '__main__':
        resp = http_put()
        print "OneNET output: \n %s \n" %resp