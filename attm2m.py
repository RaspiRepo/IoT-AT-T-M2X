import os
import time
from m2x.client import M2XClient

# Return CPU temperature as a character string
def getCPUtemperature():
    #res = os.popen('vcgencmd measure_temp').readline()
    temp = os.popen('cat /sys/class/thermal/thermal_zone0/temp').readline()
    return(temp)

def getCPU_usage ():
    temp = os.popen('ps -eo pcpu | sort -r | head -n 2')
    temp.readline()
    return(temp.readline().strip())

#information (unit=kb) in a list
# Index 0: total RAM
# Index 1: used RAM
# Index 2: free RAM
def getRAMinfo():
    p = os.popen('free')
    i = 0
    while 1:
        i = i + 1
        line = p.readline()
        if i==2:
            return(line.split()[1:4])

#PI3 M2x
cpu_temp        = 'cpu_temperature'
primary_api_key = '91da0dbfec6930a7c1ee1659acdd3064'
device_id       = 'a409729ce217060d60cee0525312d31c'

client = M2XClient(primary_api_key)
temp_stream = client.device(device_id).stream(cpu_temp)
cpu_usage_stream = client.device(device_id).stream('cpu_usage')

#result = stream.add_value(int(time.time()))
count = 0
prv_temp       = 0
prev_cpu_usage = 0

while (count < 10) :
    CPU_temp = int(int(getCPUtemperature())/1000.0)

    curr_cpu_usage = float(getCPU_usage ())

    if (abs(prv_temp - CPU_temp) > 2) :
        temp_stream.add_value(CPU_temp)
        prv_temp = CPU_temp

    if (abs(prev_cpu_usage - curr_cpu_usage) > 10) :
        #send values to m2m service
        cpu_usage_stream.add_value(curr_cpu_usage)

        prev_cpu_usage = curr_cpu_usage

    print("curr temp ", CPU_temp, "pretemp ", prv_temp, "cpu ", curr_cpu_usage, " prev ", prev_cpu_usage)
    time.sleep(10)
    count += 0