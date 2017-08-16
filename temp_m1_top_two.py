#!/usr/bin/python

import RPi.GPIO as GPIO
import time
import pymysql
import datetime
current_time = datetime.datetime.now()
print('%s' %current_time )

channel_m1_top_one = 27
data_m1_top_one = []
j_top_one = 0



GPIO.setmode(GPIO.BCM)

time.sleep(1)

GPIO.setup(channel_m1_top_one, GPIO.OUT)


GPIO.output(channel_m1_top_one, GPIO.LOW)

time.sleep(0.02)

GPIO.output(channel_m1_top_one, GPIO.HIGH)



GPIO.setup(channel_m1_top_one, GPIO.IN)


while GPIO.input(channel_m1_top_one) == GPIO.LOW:
     continue

while GPIO.input(channel_m1_top_one) == GPIO.HIGH:
     continue


while j_top_one < 40:
     k_top_one = 0
     while GPIO.input(channel_m1_top_one) == GPIO.LOW:
         continue
     while GPIO.input(channel_m1_top_one) == GPIO.HIGH:
         k_top_one += 1
         if k_top_one > 100:
             break


     if k_top_one < 8:
         data_m1_top_one.append(0)
     else:
         data_m1_top_one.append(1)

     j_top_one += 1
print "sensor_m1_top_one is working."
print data_m1_top_one
  
humidity_bit_m1_top_one = data_m1_top_one[0:8]
humidity_point_bit_m1_top_one = data_m1_top_one[8:16]
temperature_bit_m1_top_one = data_m1_top_one[16:24]
temperature_point_bit_m1_top_one = data_m1_top_one[24:32]
check_bit_m1_top_one = data_m1_top_one[32:40]



humidity_m1_top_one = 0
humidity_point_m1_top_one = 0
temperature_m1_top_one = 0
temperature_point_m1_top_one = 0
check_m1_top_one = 0



for i in range(8):
     humidity_m1_top_one += humidity_bit_m1_top_one[i] * 2 ** (7 - i)
     humidity_point_m1_top_one += humidity_point_bit_m1_top_one[i] * 2 ** (7 - i)
     temperature_m1_top_one += temperature_bit_m1_top_one[i] * 2 ** (7 - i)
     temperature_point_m1_top_one += temperature_point_bit_m1_top_one[i] * 2 ** (7 - i)
     check_m1_top_one += check_bit_m1_top_one[i] * 2 ** (7 - i)
    

tmp_m1_top_one = humidity_m1_top_one + humidity_point_m1_top_one + temperature_m1_top_one + temperature_point_m1_top_one


if check_m1_top_one == tmp_m1_top_one:
     print "temperature_m1_top_one : ", temperature_m1_top_one, ", humidity_m1_top_one : " , humidity_m1_top_one

else:
    print"wrong_m1_top_one"
    print"temperature_m1_top_one:",temperature_m1_top_one,",humidity_m1_top_one:",humidity_m1_top_one,"check_m1_top_one:",check_m1_top_one,"tmp_m1_top_one:",tmp_m1_top_one




db = pymysql.connect('11.11.11.15', 'root', 'work@good308', 'temp')
cursor = db.cursor()
sql_m1_top_one = "INSERT INTO TEMP_M1_TOP_TWO (TEMP_M1_TOP_TWO,HUM_M1_TOP_TWO,TIME) VALUES ('%d','%d','%s')" % \
                                       (temperature_m1_top_one,humidity_m1_top_one,current_time )


cursor.execute(sql_m1_top_one)
db.commit()

db.close()
GPIO.cleanup()


