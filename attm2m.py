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
cpu_usage       = 'cpu_usage'
primary_api_key = 'primary_key from att m2x '
device_id       = 'device id'

cpu_load_threshold = 10 #10%
cpu_temp_threshold = 2 #2 celsius

#Create API access points
client = M2XClient(primary_api_key)

#stream identifier for each channel. Here CPU temperature and CPU load 
#time series value uploaded to cloud.
temp_stream = client.device(device_id).stream(cpu_temp)
cpu_usage_stream = client.device(device_id).stream(cpu_usage)

#result = stream.add_value(int(time.time()))
count          = 0
prv_temp       = 0
prev_cpu_usage = 0
start_time     = time.time()
report_interval = 300.0 #5 minutes

#Infinite loop. Check every 10 seconds and if there is changes above specified threshold
#update value to at&t m2x server
while (count < 10) :

    elapsed_time = time.time() - start_time


    CPU_temp = int(int(getCPUtemperature())/1000.0)

    curr_cpu_usage = float(getCPU_usage ())

    #Send CPU temperature value only if there is a change from previous to current
    #Threashold value > cpu_temp_threshold celsius
    if (abs(prv_temp - CPU_temp) > cpu_temp_threshold) or elapsed_time >= report_interval :
        temp_stream.add_value(CPU_temp)
        prv_temp = CPU_temp

    #Update CPU load only if considerable difference between previous and current
    #
    if (abs(prev_cpu_usage - curr_cpu_usage) > cpu_load_threshold) or elapsed_time >= report_interval :
        #send values to m2m service
        cpu_usage_stream.add_value(curr_cpu_usage)

        prev_cpu_usage = curr_cpu_usage

    if elapsed_time >= report_interval :
        start_time = time.time()

    print("elapsed time ", str(elapsed_time), "curr temp ", CPU_temp, "pretemp ", prv_temp, "cpu ", curr_cpu_usage, " prev ", prev_cpu_usage)
    time.sleep(10)
