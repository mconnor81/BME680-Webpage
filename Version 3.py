import bme680 #Allows Sensor data to be read by the raspberry pi
import time
from time import sleep, strftime, time
import mysql.connector


sensor = bme680.BME680()
sensor.set_humidity_oversample(bme680.OS_2X)
sensor.set_pressure_oversample(bme680.OS_4X)
sensor.set_temperature_oversample(bme680.OS_8X)
sensor.set_filter(bme680.FILTER_SIZE_3)

sensor.set_gas_status(bme680.ENABLE_GAS_MEAS)
sensor.set_gas_heater_temperature(320)
sensor.set_gas_heater_duration(150)
sensor.select_gas_heater_profile(0)

# Settings for database connection
hostname = 'localhost'
username = 'pi'
password = 'markis34'
database = 'BME680'


# Routine to insert temperature records into the pidata.temps table:
def insert_record( device, datetime, temp, hum ):
	query = "INSERT INTO temps3 (device,datetime,temp,hum) " \
                "VALUES (%s,%s,%s,%s)"
    	args = (device,datetime,temp,hum)

    	try:
        	conn = MySQLdb.connect( host=hostname, user=username, passwd=password, db=database )
		cursor = conn.cursor()
        	cursor.execute(query, args)
		conn.commit()

    	except Exception as error:
        	print(error)

    	finally:
        	cursor.close()
        	conn.close()



loop=0
while True:
    with open("/home/pi/BME680/OutputData.csv", "a") as log:
        if sensor.get_sensor_data():
            output = sensor.data.temperature, sensor.data.pressure, sensor.data.humidity, sensor.data.gas_resistance
            insert_record(device,str(date),output)
	    log.write("{0},{1}\n".format(strftime("%Y-%m-%d %H:%M:%S"),output))
            loop = loop+1
            print(output)
            sleep(60)
