import urllib2
import json
import time
import datetime

import os
from AM2320 import AM2320
#!/usr/bin/python
import smbus
import math
# Power management registers
power_mgmt_1 = 0x6b
power_mgmt_2 = 0x6c

def read_byte(adr):
    return bus.read_byte_data(address, adr)

def read_word(adr):
    high = bus.read_byte_data(address, adr)
    low = bus.read_byte_data(address, adr+1)
    val = (high << 8) + low 
    return val 

def read_word_2c(adr): 
      val = read_word(adr) 
      if (val >= 0x8000):
        return -((65535 - val) + 1)
      else:
        return val

def dist(a,b):
    return math.sqrt((a*a)+(b*b))

def get_y_rotation(x,y,z):
    radians = math.atan2(x, dist(y,z))
    return -math.degrees(radians)

def get_x_rotation(x,y,z):
    radians = math.atan2(y, dist(x,z))
    return math.degrees(radians)

bus = smbus.SMBus(0) # or bus = smbus.SMBus(1) for Revision 2 boards
address = 0x68       # This is the address value read via the i2cdetect command

# Now wake the 6050 up as it starts in sleep mode
bus.write_byte_data(address, power_mgmt_1, 0)


APIKEY = "vUAoLurFOH=xkqr9s7w4dXuXBGY=" 

def get_temp():
        file = open("/sys/class/thermal/thermal_zone0/temp") 
        temp = float(file.read()) / 1000 
        file.close() 
        print "CPU temp: %.3f" %temp 
        return temp
               

# Return CPU temperature as a character string
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

def getRAMinfo():
    p = os.popen('free')
    i = 0
    while 1:
        i = i+1
        line = p.readline()
        if i == 2:
            return(line.split()[1:4])

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

    gyro_xout = read_word_2c(0x43)
    gyro_yout = read_word_2c(0x45)
    gyro_zout = read_word_2c(0x47)

    gyro_xout_scaled = gyro_xout/131
    gyro_yout_scaled = gyro_yout/131
    gyro_zout_scaled = gyro_zout/131

    accel_xout = read_word_2c(0x3b)
    accel_yout = read_word_2c(0x3d)
    accel_zout = read_word_2c(0x3f)

    accel_xout_scaled = accel_xout / 16384.0
    accel_yout_scaled = accel_yout / 16384.0
    accel_zout_scaled = accel_zout / 16384.0

    x_rotation = get_x_rotation(accel_xout_scaled, accel_yout_scaled, accel_zout_scaled)
    y_rotation = get_y_rotation(accel_xout_scaled, accel_yout_scaled, accel_zout_scaled)

    am2320 = AM2320(0)
    TemperatureC = am2320.getTempC()
    TemperatureF = am2320.getTempF()
    Humidity        = am2320.getHumidity()

    url='http://api.heclouds.com/devices/500237898/datapoints'
    values={'datastreams':[{"id":"temp","datapoints":[{"at":CurTime.isoformat(),"value":temperature}]},
                               {"id":"gyro_xout","datapoints":[{"value":gyro_xout}]},
                               {"id":"gyro_yout","datapoints":[{"value":gyro_yout}]},
                               {"id":"gyro_zout","datapoints":[{"value":gyro_zout}]},
                               {"id":"gyro_xout_scaled","datapoints":[{"value":gyro_xout_scaled}]},
                               {"id":"gyro_yout_scaled","datapoints":[{"value":gyro_yout_scaled}]},
                               {"id":"gyro_zout_scaled","datapoints":[{"value":gyro_zout_scaled}]},
                               {"id":"accel_xout","datapoints":[{"value":accel_xout}]},
                               {"id":"accel_yout","datapoints":[{"value":accel_yout}]},
                               {"id":"accel_zout","datapoints":[{"value":accel_zout}]},
                               {"id":"accel_xout_scaled","datapoints":[{"value":accel_xout_scaled}]},
                               {"id":"accel_yout_scaled","datapoints":[{"value":accel_yout_scaled}]},
                               {"id":"accel_zout_scaled","datapoints":[{"value":accel_zout_scaled}]},
                               {"id":"x_rotation","datapoints":[{"value":x_rotation}]},
                               {"id":"y_rotation","datapoints":[{"value":y_rotation}]},
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
                               {"id":"DISK_perc","datapoints":[{"value":DISK_perc}]},
                               {"id":"TemperatureC","datapoints":[{"value":TemperatureC}]},
                               {"id":"TemperatureF","datapoints":[{"value":TemperatureF}]},
                               {"id":"Humidity","datapoints":[{"value":Humidity}]}
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
      
