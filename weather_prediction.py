import threading
import time
from datetime import datetime
import pyodbc
import board
import busio
import adafruit_bme280

#weather variables
minTemp = 1000
maxTemp = 0
temp9am = 0
temp3pm = 0
humidity9am = 0
humidity3pm = 0
pressure9am = 0
pressure3pm = 0
mlp = 0.0
tl  = 0

now = datetime.now().time()
i2c = busio.I2C(board.SCL, board.SDA)
bme280 = adafruit_bme280.Adafruit_BME280_I2C(i2c)

def variableAssignment(temperature, humidiy, pressure):
    global minTemp, maxTemp, temp9am, temp3pm, humidity9am, humidity3pm, pressure9am, pressure3pm
    if temperature < minTemp:
        minTemp = temperature
    elif temperature > maxTemp:
        maxTemp = temperature

    if now.strftime('%H:%M') == '9:00':
        temp9am = temperature
        humidity9am = humidiy
        pressure9am = pressure
    elif now.strftime('%H:%M') == '15:00':
        temp3pm = temperature
        humidity3pm = humidiy
        pressure3pm = pressure

def glmPrediction(min_Temp, max_Temp, temp_9am, temp_3pm, humidity_9am, humidity_3pm, pressure_9am, pressure_3pm):
    global mlp
    mlp =-0.2033 + 3.22194*min_Temp + 2.12412*max_Temp + 0.34488*humidity_9am + 5.53933*humidity_3pm + 5.05836*pressure_9am - 11.7592*pressure_3pm - 1.98098*temp_9am - 5.30753*temp_3pm

def tradPrediction(pressure_9am, pressure_3pm):
    global tl
    lowPressure = 1009.144
    if (pressure_3pm <= lowPressure & pressure_3pm <= pressure_9am):
        tl = 1
    else:
        tl = 0

def updateDatabase(pressure,temperature, humidity, ml, trad):
    #ODBC database information
    server = 'weatherdb.database.windows.net'
    port='1433'
    database = 'WeatherDB'
    username = 'weatheradmin'
    password = 'Weatherapp!'
    driver= 'FreeTDS'
    #params = {'Name', 'Test'}
    pyodbcon = ('DRIVER='+driver+';SERVER='+server+';PORT='+port+';DATABASE='+database+';UID='+username+';PWD='+password+';TDS_Version=8.0')
    with pyodbc.connect(pyodbcon) as conn:
        with conn.cursor() as cursor:
            #cursor.execute("DELETE * FROM Weather")
            cursor.execute('INSERT INTO Weather (Pressure,Temperature, Humidity, MLPrediction,TradPrediction ) VALUES ({:.2f},{:.2f},{:.2f},{:.2f},{})'.format(pressure,temperature, humidity, ml, trad))

i = 1
while (True):
    print("loop " ,i)
    i = i + 1
    t1 = threading.Thread(target=variableAssignment(bme280.temperature, bme280.humidity, bme280.pressure))
    t1.start()
    t1.join()
    if now.strftime('%H:%M') == '15:01':
        glmPrediction(minTemp, maxTemp, temp9am, temp3pm, humidity9am, humidity3pm, pressure9am, pressure3pm)
        tradPrediction(pressure9am, pressure3pm)
        t2 = threading.Thread(target=updateDatabase(bme280.pressure, bme280.temperature, bme280.humidity,mlp,tl))
        t2.start()
        t2.join()
    else:
        #until 3:01 pm, predictions are set to previous days predictions.
        t2 = threading.Thread(target=updateDatabase(bme280.pressure, bme280.temperature, bme280.humidity,mlp,tl))
        t2.start()
        t2.join()
    time.sleep(60)
