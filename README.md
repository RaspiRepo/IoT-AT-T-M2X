# IoT-AT&T-M2X RESTful APIs
Monitoring Raspberry PI CPU Temperature, CPU load using AT&amp;T M2X RESTful APIs
#Summary
  Its fun project to explore with AT&T iot Machine to Machin communication.  This sample code will get Raspberry PI CPU temperature, CPU usage (load) then connect ATT M2X cloud server upload time series values.  This code can be modified to run any Linux server to monitor its load.  
  
Public access to my device

RPI3  
https://m2x.att.com/catalog/a409729ce217060d60cee0525312d31c#streams

JetsonNano
https://m2x.att.com/catalog/7f66dd15291ec2a903e036b390cc0763


To use this script, first need to create account (Free) from https://m2x.att.com/ and add device (Max 10 device), get the API access key and device ID and replace into script.

Execute this script in background or auto start up (whenever device boots) so any time monitor device, write a trigger events and develop anything as per need.

API Resource

https://m2x.att.com/developer/documentation/v2/overview
