import bme680 #Allows Sensor data to be read by the raspberry pi
import time
import datetime
from time import sleep, strftime, time
import influxdb
from influxdb import InfluxDBClient

sensor = bme680.BME680()
sensor.set_humidity_oversample(bme680.OS_2X)
sensor.set_pressure_oversample(bme680.OS_4X)
sensor.set_temperature_oversample(bme680.OS_8X)
sensor.set_filter(bme680.FILTER_SIZE_3)

sensor.set_gas_status(bme680.ENABLE_GAS_MEAS)
sensor.set_gas_heater_temperature(320)
sensor.set_gas_heater_duration(150)
sensor.select_gas_heater_profile(0)


# influx configuration - edit these
ifuser = "pi"
ifpass = "markis34"
ifdb   = "BME680"
ifhost = "127.0.0.1"
ifport = 8086
measurement_name = "system"


# connect to influx
#ifclient = InfluxDBClient(ifhost,ifport,ifuser,ifpass,ifdb)

# write the measurement
#ifclient.write_points(body)

loop=0
while True:
	with open("/home/pi/BME680/OutputData.csv", "a") as log:
		ifclient = InfluxDBClient(ifhost,ifport,ifuser,ifpass,ifdb)
		if sensor.get_sensor_data():
			output = sensor.data.temperature, sensor.data.pressure, sensor.data.humidity, sensor.data.gas_resistance
			timestamp = datetime.datetime.utcnow()
			log.write("{0},{1}\n".format(strftime("%Y-%m-%d %H:%M:%S"),output))
			print(output)
			body = [
				{
					"measurement": measurement_name,
					"time": timestamp,
					"fields": {
						"temperature": sensor.data.temperature,
						"pressure": sensor.data.pressure,
		  				"humidity": sensor.data.humidity,
                  				"gas Resistance": sensor.data.gas_resistance
				}
				}
			]

			ifclient.write_points(body)
			sleep(4)



















