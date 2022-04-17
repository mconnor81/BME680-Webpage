import bme680
import time
from time import sleep, strftime, time

sensor = bme680.BME680()
sensor.set_humidity_oversample(bme680.OS_2X)
sensor.set_pressure_oversample(bme680.OS_4X)
sensor.set_temperature_oversample(bme680.OS_8X)
sensor.set_filter(bme680.FILTER_SIZE_3)

sensor.set_gas_status(bme680.ENABLE_GAS_MEAS)
sensor.set_gas_heater_temperature(320)
sensor.set_gas_heater_duration(150)
sensor.select_gas_heater_profile(0)


loop=0
with open("/home/pi/BME680/OutputData.csv", "a") as log:
	while True:
		output = sensor.data.temperature, sensor.data.pressure, sensor.data.humidity, sensor.data.gas_resistance
		log.write("{0},{1}\n".format(strftime("%Y-%m-%d %H:%M:%S"),output))
		sleep(1)
		loop = loop+1
		print(output)
