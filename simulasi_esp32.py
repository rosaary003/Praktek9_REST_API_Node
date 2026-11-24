import paho.mqtt.client as mqtt
import json
import time
import random
from datetime import datetime

BROKER = "localhost"
PORT = 1883

TOPIC_SENSOR = "iot/sensor"
TOPIC_KONTROL = "iot/kontrol"

client = mqtt.Client(
    mqtt.CallbackAPIVersion.VERSION2,
    client_id="ESP32-Simulator"
)

def on_connect(client, userdata, flags, reason_code, properties):
    print("Terhubung ke MQTT Broker!")
    client.subscribe(TOPIC_KONTROL)

def on_message(client, userdata, msg):
    print("Perintah diterima:", msg.payload.decode())

client.on_connect = on_connect
client.on_message = on_message

client.connect(BROKER, PORT, 60)
client.loop_start()

print("ESP32 Simulator berjalan... Ctrl+C untuk berhenti")

try:
    while True:
        data = {
            "suhu": round(random.uniform(25, 32), 1),
            "kelembaban": round(random.uniform(55, 80), 1),
            "timestamp": datetime.now().isoformat()
        }

        client.publish(TOPIC_SENSOR, json.dumps(data))

        print("Publish:", data)

        time.sleep(3)

except KeyboardInterrupt:
    print("Simulator dihentikan")

finally:
    client.loop_stop()
    client.disconnect()