#引入需要的套件
import time
import RPi.GPIO as GPIO
import Adafruit_DHT
 
#設定DHT sensor的格式
DHT_SENSOR = Adafruit_DHT.DHT22
DHT_PIN = 23

MONITOR_PIN = 22
#設定pin numbering為BCM
GPIO.setmode(GPIO.BCM)

#設定GPIO的腳位
GPIO.setup(MONITOR_PIN, GPIO.IN)
GPIO.setup(LED_PIN, GPIO.OUT)
GPIO.setup(17,GPIO.OUT)
GPIO.setup(27,GPIO.OUT)

#定義旋轉的設定
def rotate():
    GPIO.output(17,True)
    GPIO.output(27,False)
    time.sleep(5)
    
print('press Ctrl-C to stop the process') 
try:
    while True:
        #給定兩個變數humidity與temperature來存放溫溼度的參數
        humidity, temperature = Adafruit_DHT.read_retry(DHT_SENSOR, DHT_PIN)
        print("Temp={0:0.1f}*C  Humidity={1:0.1f}%".format(temperature, humidity))
        #當濕度大於70時開始偵測
        if(humidity > 70):
            #偵測到人體移動時開始旋轉
            if GPIO.input(MONITOR_PIN):
                print('1')
                rotate()
            else:
                print('2')
                GPIO.output(17,False)
                GPIO.output(27,False)
        else:
            print('3')
            GPIO.output(17,False)
            GPIO.output(27,False)
            
        time.sleep(0.1)
    
#ctrl+c可停止執行
except KeyboardInterrupt:
    print('close')
finally:
    GPIO.cleanup()    

    


    



