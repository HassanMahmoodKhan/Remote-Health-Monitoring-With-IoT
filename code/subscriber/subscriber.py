import paho.mqtt.client as mqtt
import time
import csv
import json

data = []
def on_connect(client, userdata, flags, rc): # connect callback function
    if rc==0:
        print("Connected ok.")
    else:
        print("Bad connection. Error code: ", str(rc))

def on_disconnect(client, userdata, flags, rc=0): # disconnect callback function
    print("Disconnected with code: ", str(rc))

def on_message(client, userdata, message): # message received callback function
    global data
    print("message received" ,str(message.payload.decode("utf-8")))
    print("message topic =",message.topic)
    print("message qos =",message.qos)
    print("message retain flag =",message.retain)

    topic = message.topic.split('/')[1]
    print(f"Printing topic: {topic}")
    if topic == 'movement':
        msg = json.loads(message.payload.decode())
        data = [x for x in msg['data']]
    else:
        data.append(str(json.loads(message.payload.decode())['data']))
    
    if len(data) == 6:
        with open('received_msgs.csv', mode='a') as file:
            writer = csv.writer(file)
            writer.writerow(data)
        
        data = []

broker_address = "127.0.0.1" # Ipv4 address (local)
client = mqtt.Client("P2")
client.on_connect = on_connect # Attaching client to callback function
client.on_message = on_message 
client.on_disconnect = on_disconnect

client.connect(broker_address, 1883) # Connect to broker
client.subscribe("HMS/+", 1) # Subscribing to all topics
time.sleep(3) # Wait for script to process the callbacks

client.loop_start()
# Keep the script running to receive messages

try:
    while True:
        pass

except KeyboardInterrupt:
    print("Script terminated by user")

finally:
    # Disconnect from the MQTT broker when the script is terminated
    client.disconnect()