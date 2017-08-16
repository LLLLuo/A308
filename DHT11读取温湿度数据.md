# DHT11读取温湿度数据

python程序中采用BCM编号方式，信号口使用的是27号即pin13,vcc接3.3V,GND接0V，NC悬空。

1.导入所需要的包后，先获取了当前程序运行的时间，然后通过设置PI的GPIO电平和编号方式使数据线设置为输出模式，读入二进制数据和检验位数据后将其存入数组中，在通过进制间的转换，将读得的温湿度值和检验位以十进制的方式存储起来，如果检验正常，测显示正确温湿度值，状态位显示NORMAL，若校验异常则显示异常温湿度值的同时状态位显示ERROR，最后通过mysql将采得数据传至建好的表格中，并且释放脚本中所使用的引脚。

2.使用树莓派中的定时器功能，每隔1分钟执行一次上述python程序，即每隔一分钟对温湿度值进行一次采集。

3.python代码

```
![IMG_0624 - 副本](C:\Users\lzh-pc\Desktop\IMG_0624 - 副本.JPG)

#!/usr/bin/python

import RPi.GPIO as GPIO
import time
import pymysql
import datetime

#获取当前时间
current_time = datetime.datetime.now()
print('%s' %current_time )

#设置所用管教 BCM27
channel_m1_top_one = 27
data_m1_top_one = []
j_top_one = 0


#编码方式设置为BCM编码
GPIO.setmode(GPIO.BCM)

time.sleep(1)

#通过一定时间的高低电平将数据线设置为输出模式
GPIO.setup(channel_m1_top_one, GPIO.OUT)


GPIO.output(channel_m1_top_one, GPIO.LOW)

time.sleep(0.02)

GPIO.output(channel_m1_top_one, GPIO.HIGH)



#设置数据线为输入
GPIO.setup(channel_m1_top_one, GPIO.IN)


while GPIO.input(channel_m1_top_one) == GPIO.LOW:
     continue

while GPIO.input(channel_m1_top_one) == GPIO.HIGH:
     continue

#二进制数据的获取
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


#将二进制数据转化为十进制数据
for i in range(8):
     humidity_m1_top_one += humidity_bit_m1_top_one[i] * 2 ** (7 - i)
     humidity_point_m1_top_one += humidity_point_bit_m1_top_one[i] * 2 ** (7 - i)
     temperature_m1_top_one += temperature_bit_m1_top_one[i] * 2 ** (7 - i)
     temperature_point_m1_top_one += temperature_point_bit_m1_top_one[i] * 2 ** (7 - i)
     check_m1_top_one += check_bit_m1_top_one[i] * 2 ** (7 - i)
    

tmp_m1_top_one = humidity_m1_top_one + humidity_point_m1_top_one + temperature_m1_top_one + temperature_point_m1_top_one

#进行数据校验
if check_m1_top_one == tmp_m1_top_one:
     print "temperature_m1_top_one : ", temperature_m1_top_one, ", humidity_m1_top_one : " , humidity_m1_top_one
     state_m1_top_one = "NORMAL"
else:
    print"wrong_m1_top_one"
    state_m1_top_one = "ERROR"
    print"temperature_m1_top_one:",temperature_m1_top_one,",humidity_m1_top_one:",humidity_m1_top_one,"check_m1_top_one:",check_m1_top_one,"tmp_m1_top_one:",tmp_m1_top_one


# 通过mysql将采集到的温湿度数据和实时时间传至表中
db = pymysql.connect('11.11.11.15', 'root', 'work@good308', 'temp')
cursor = db.cursor()
sql_m1_top_one = "INSERT INTO TEMP_M1_TOP_TWO (TEMP_M1_TOP_TWO,HUM_M1_TOP_TWO,TIME) VALUES ('%d','%d','%s')" % \
                                       (temperature_m1_top_one,humidity_m1_top_one,current_time )


cursor.execute(sql_m1_top_one)
db.commit()
db.close()
#释放脚本中所使用的引脚
GPIO.cleanup()



```
4.**测试结果**

（1）树莓派采值结果正常

![IMG_0621](C:\Users\lzh-pc\Desktop\IMG_0621.JPG)



（2）每隔一分钟通过日志记录的数据正常



![IMG_0622](C:\Users\lzh-pc\Desktop\IMG_0622.JPG)



（3）mysql表格中实时记录的数据正常

![DE464983FBAE6CC4A29D8F00A0D84586](C:\Users\lzh-pc\Desktop\DE464983FBAE6CC4A29D8F00A0D84586.png)





**五.存在问题**

