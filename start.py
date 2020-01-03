#import 我們所需要的套件，包含GPIO，DHT，OS，flask
from flask import Flask, render_template, request
import RPi.GPIO as GPIO
import Adafruit_DHT
import os

DHT_SENSOR = Adafruit_DHT.DHT22
DHT_PIN = 23

#創建名為app的Flask物件
app = Flask(__name__)

#設定GPIO的pin numbering為BCM，並取消警告
GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)

times=0

#輸入網址時為回傳start.html
@app.route('/')
def index():
    return render_template('start.html')

#跳轉至monitor.html後顯示濕度與溫度
@app.route('/monitor.html')
def monitor():
    #給定兩個變數humidity與temperature來存放溫溼度的參數
    humidity, temperature = Adafruit_DHT.read_retry(DHT_SENSOR, DHT_PIN)
    humidity = round(humidity,2)
    temperature = round(temperature,2)
    return render_template('monitor.html',humidity=humidity,temperature=temperature)
    
#按下start按鈕後啟動風扇的判斷程式
@app.route('/monitor.html',methods = ['POST'])
def start():
    global times
    if(times == 0):
        times+=1
        os.system('sudo python /home/pi/Desktop/flask/app.py')

#對ip address近來綁定
if __name__ == "__main__":
   app.run(host='192.168.31.43', port=80, debug=True)
