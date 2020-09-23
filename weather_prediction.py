import threading
import time
from datetime import datetime
import pyodbc

minTemp = 1000
maxTemp = 0
temp9am = 0
temp3pm = 0
humidity9am = 0
humidity3pm = 0
pressure9am = 0
pressure3pm = 0

now = datetime.now().time()

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

while (True):
    t1 = threading.Thread(target=variableAssignment(98, 38, 40))

    t1.start()
    t1.join()



    time.sleep(15)

server = 'enrollmentsdbserver1.database.windows.net,1433'
database = 'EnrollmentsDB'
username = 'EnrollmentsSA'
password = 'Chance123'
driver= '{ODBC Driver 17 for SQL Server}'

odbc = 'DRIVER={ODBC Driver 17 for SQL Server};SERVER='+server+';DATABASE='+database+';UID='+username+';PWD='+password+''
with pyodbc.connect(odbc) as conn:
    with conn.cursor() as cursor:
        cursor.execute("SELECT * FROM Student")
        row = cursor.fetchone()
        while row:
            print (str(row[0]) + " " + str(row[1]))
            row = cursor.fetchone()
