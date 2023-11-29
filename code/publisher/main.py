import csv
import time
import json
import serial
from mpu6050 import mpu6050
from sensor_reading import ypr, is_fall_detected

import paho.mqtt.client as mqtt

mpu = mpu6050(0x68)
ser = serial.Serial('/dev/ttyACM0', 9600)

def on_connect(client, userdata, flags, rc):
	if rc == 0:
		print("Connected ok.")
	else:
		print("Bad Connection. Error Code: ", str(rc))

def on_disconnect(client, userdata, flags, rc=0):
	print("Disconnected with code: ", str(rc))


port = 1883
broker_address = "0.0.0.0" # Specify broker address; run ipconfig on a terminal, use the ipv4 address of your device
message_interval = 1

client = mqtt.Client('P1')
client.on_connect = on_connect
client.on_disconnect = on_disconnect


while True:
	try:
		client.connect(broker_address, port, 60)
		client.loop_start()
		
		while True:
			accel_data = mpu.get_accel_data()
			gyro_data = mpu.get_gyro_data()
			temp = mpu.get_temp()
			
			heartbeat = float(ser.readline().decode().strip())
			_, roll, pitch, a_mag = ypr(accel_data, gyro_data) 
			isfall = "Yes" if is_fall_detected(a_mag, pitch, roll) else "No"
			
			client.publish("HMS/movement", json.dumps({"data":[roll, pitch, a_mag]}), 1)
			client.publish("HMS/heart_rate", json.dumps({"data": str(heartbeat)}), 1)
			client.publish("HMS/temperature", json.dumps({"data": temp}), 1)
			client.publish("HMS/fall_detected", json.dumps({"data": isfall}), 1)
			
			time.sleep(0.01)
			
			print(f"Roll: {roll:.2f}, Pitch: {pitch:.2f}, Acc_magnitude: {a_mag:.2f}, HeartBeat: {heartbeat:.2f}, Tempreture: {temp:.2f}, Fall Detected: {isfall}.")
	except KeyboardInterrupt:
		break
	
	except Exception as e:
		print(f"Error: {e}")
		print("Attempting to reconnect...")
		time.sleep(2)
		client.disconnect()

client.disconnect()
