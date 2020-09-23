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
    pass

def tradPrediction(temperature, humidity, pressure):
    pass

def updateDatabase(temperature, humidity, pressure):
    #ODBC database information
    server = 'enrollmentsdbserver1.database.windows.net,1433'
    database = 'EnrollmentsDB'
    username = 'EnrollmentsSA'
    password = 'Chance123'
    driver= '{ODBC Driver 17 for SQL Server}'
    params = {'Name', 'Test'}
    odbc = 'DRIVER={ODBC Driver 17 for SQL Server};SERVER='+server+';DATABASE='+database+';UID='+username+';PWD='+password+''

    with pyodbc.connect(odbc) as conn:
        with conn.cursor() as cursor:
            cursor.execute("DELETE * FROM Student")
            cursor.execute("INSERT INTO Weather (currentTemp, currentHumidity, currentPressure, ) VALUES (temperature, humidity, pressure)")

while (True):
    t1 = threading.Thread(target=variableAssignment(bme280.temperature, bme280.humidity, bme280.pressure))
    t2 = threading.Thread(target=glmPrediction(minTemp, maxTemp, temp9am, temp3pm, humidity9am, humidity3pm, pressure9am, pressur_3pm))
    t3 = threading.Thread(target=updateDatabase(bme280.temperature, bme280.humidity, bme280.pressure))
    t1.start()
    t2.start()
    t3.start()
    t1.join()
    t2.join()
    t3.join()
    time.sleep(15)
