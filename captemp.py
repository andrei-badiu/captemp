import paho.mqtt.client as mqtt
import lcddriver
import time

lcd = lcddriver.lcd()
 
MQTT_SERVER = "localhost"
MQTT_PATH = "test_channel"
 
# The callback for when the client receives a CONNACK response from the server.
def on_connect(client, userdata, flags, rc):
    print("Connected with result code "+str(rc))
 
    # Subscribing in on_connect() means that if we lose the connection and
    # reconnect then subscriptions will be renewed.
    client.subscribe(MQTT_PATH)
 
# The callback for when a PUBLISH message is received from the server.
def on_message(client, userdata, msg):
    print(msg.topic+" "+str(msg.payload))
    #display_text(str(msg.payload))
    long_string(str(msg.payload))
    # more callbacks, etc

def display_text(msg):
    try:
        lcd.lcd_clear()
        print("Writing to display")
        lcd.lcd_display_string(msg, 1)
    except KeyboardInterrupt:
        print("Cleaning up!")
        lcd.lcd_clear()

def long_string(text = '', num_line = 1, num_cols = 16):
    print(text)
    if(len(text) > num_cols):
        print(text)
        lcd.lcd_display_string(text[:num_cols],num_line)
        time.sleep(1)
        for i in range(len(text) - num_cols + 1):
            text_to_print = text[i:i+num_cols]
            lcd.lcd_display_string(text_to_print,num_line)
            time.sleep(0.2)
        time.sleep(1)       
    else:
            lcd.lcd_display_string(text,num_line)
            
        
	

    
client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message
 
client.connect(MQTT_SERVER, 1883, 60)
 
# Blocking call that processes network traffic, dispatches callbacks and
# handles reconnecting.
# Other loop*() functions are available that give a threaded interface and a
# manual interface.
client.loop_forever()
