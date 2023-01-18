#!/usr/bin/python
import paho.mqtt.client as mqtt 
import RPi.GPIO as GPIO
import time


mqttBroker ="localhost" 
client = mqtt.Client("Water_level")
client.connect(mqttBroker) 

while True:
    try:
        GPIO.setmode(GPIO.BOARD)

        PIN_TRIGGER = 7
        PIN_ECHO = 11

        GPIO.setup(PIN_TRIGGER, GPIO.OUT)
        GPIO.setup(PIN_ECHO, GPIO.IN)

        GPIO.output(PIN_TRIGGER, GPIO.LOW)

        time.sleep(2)

        GPIO.output(PIN_TRIGGER, GPIO.HIGH)

        time.sleep(0.00001)

        GPIO.output(PIN_TRIGGER, GPIO.LOW)

        while GPIO.input(PIN_ECHO)==0:
            pulse_start_time = time.time()
        while GPIO.input(PIN_ECHO)==1:
            pulse_end_time = time.time()

        pulse_duration = pulse_end_time - pulse_start_time
        distance = round(pulse_duration * 17150, 2)
        print ("Distance:",distance,"cm")
        client.publish("DISTANCE", distance)
        print("Published " + str(distance) + " to topic DISTANCE")

    finally:
        GPIO.cleanup()
