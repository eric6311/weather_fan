# IOT_Project:氣象偵測風扇

![image](https://github.com/eric6311/weather_fan/blob/master/P_20200107_150546.jpg)
Demo影片連結:https://www.youtube.com/watch?v=QfSV7oaN_Ew
由溫溼度感應器偵測溫度與濕度，並顯示於網頁上。當溫溼度超過一定範圍時，紅外線感應器開始運作，偵測到人即開始運轉。

Input: PIR sensor, 溫溼度感應器

Output:網頁與馬達



所需材料:

樹梅派*1

人體紅外線感應器*1

L298N馬達控制板*1

直流馬達*1

2MM孔徑塑膠扇葉*1

1.5V33號電池*4

電池盒*1

DHT22溫溼度感應器*1

杜邦線約20條



## 步驟一:安裝Flask

參考網站:https://flask.palletsprojects.com/en/1.1.x/installation/

```
$ pip install Flask
```



## 步驟二:安裝DHT22 library

參考網站:https://kingfff.blogspot.com/2018/05/raspberry-pi-3-model-bdht22.html

下載git上的python DHT22 library

`$ git clone https://github.com/adafruit/Adafruit_Python_DHT.git`

安裝該library

`cd Adafruit_Python_DHT sudo`

`apt-get install build-essential python-dev python-openssl` 

`sudo python setup.py install`



## 步驟三:接上線路

GPIO參考網址:https://pinout.xyz/

連接馬達控制板與馬達:https://shop.cpu.com.tw/product/46920/info/

連接PIR sensor:http://coopermaa2nd.blogspot.com/2011/03/arduino-pir-motion-sensor-led.html

連接溫溼度感應器:https://kingfff.blogspot.com/2018/05/raspberry-pi-3-model-bdht22.html



## 步驟四:撰寫溫溼度與人體監測程式app.py

```
#引入需要的套件

import time

import RPi.GPIO as GPIO

import Adafruit_DHT

 

\#設定DHT sensor的格式

DHT_SENSOR = Adafruit_DHT.DHT22

DHT_PIN = 23



MONITOR_PIN = 22

\#設定pin numbering為BCM

GPIO.setmode(GPIO.BCM)



\#設定GPIO的腳位

GPIO.setup(MONITOR_PIN, GPIO.IN)

GPIO.setup(LED_PIN, GPIO.OUT)

GPIO.setup(17,GPIO.OUT)

GPIO.setup(27,GPIO.OUT)



\#定義旋轉的設定

def rotate():

  GPIO.output(17,True)

  GPIO.output(27,False)

  time.sleep(5)

  

print('press Ctrl-C to stop the process') 

try:

  while True:

​    \#給定兩個變數humidity與temperature來存放溫溼度的參數

​    humidity, temperature = Adafruit_DHT.read_retry(DHT_SENSOR, DHT_PIN)

​    print("Temp={0:0.1f}*C Humidity={1:0.1f}%".format(temperature, humidity))

​    \#當濕度大於70時開始偵測

​    if(humidity > 70):

​      \#偵測到人體移動時開始旋轉

​      if GPIO.input(MONITOR_PIN):

​        print('1')

​        rotate()

​      else:

​        print('2')

​        GPIO.output(17,False)

​        GPIO.output(27,False)

​    else:

​      print('3')

​      GPIO.output(17,False)

​      GPIO.output(27,False)

​      

​    time.sleep(0.1)

  

\#ctrl+c可停止執行

except KeyboardInterrupt:

  print('close')

finally:

  GPIO.cleanup()  
```



##   步驟五:撰寫server程式start.py

```
![圖片 214](C:\Users\kartd\OneDrive\圖片\螢幕擷取畫面\圖片 214.png)#import 我們所需要的套件，包含GPIO，DHT，OS，flask

from flask import Flask, render_template, request

import RPi.GPIO as GPIO

import Adafruit_DHT

import os



DHT_SENSOR = Adafruit_DHT.DHT22

DHT_PIN = 23



\#創建名為app的Flask物件

app = Flask(__name__)



\#設定GPIO的pin numbering為BCM，並取消警告

GPIO.setmode(GPIO.BCM)

GPIO.setwarnings(False)



times=0



\#輸入網址時為回傳start.html

@app.route('/')

def index():

  return render_template('start.html')



\#跳轉至monitor.html後顯示濕度與溫度

@app.route('/monitor.html')

def monitor():

  \#給定兩個變數humidity與temperature來存放溫溼度的參數

  humidity, temperature = Adafruit_DHT.read_retry(DHT_SENSOR, DHT_PIN)

  humidity = round(humidity,2)

  temperature = round(temperature,2)

  return render_template('monitor.html',humidity=humidity,temperature=temperature)

  

\#按下start按鈕後啟動風扇的判斷程式

@app.route('/monitor.html',methods = ['POST'])

def start():

  global times

  if(times == 0):

​    times+=1

​    os.system('sudo python /home/pi/Desktop/flask/app.py')



\#對ip address進行綁定

if __name__ == "__main__":

  app.run(host='192.168.31.43', port=80, debug=True)
```



## 步驟六:開始使用

開啟start.py  

進入設定的網址，按下啟動按鈕後開始監測溫溼度

再按下start按鈕啟動風扇監測
