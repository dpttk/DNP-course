import zmq
import json
import sys
import threading
from datetime import datetime, timedelta

WEATHER_INPUT_PORT= 5555
FASHION_SOCKET_PORT = 5556

IP_ADD = '127.0.0.1'

latest_data = {}

def average_temperature_humidity():
    pass


def recommendation():
    result = ""
    average_temperature_humidity()
    if latest_data['average-temp'] <10:
        result = "Today weather is cold. Its better to wear warm clothes"
    elif latest_data['average-temp'] >10 and latest_data['average-temp'] <25:
        result = "Feel free to wear spring/autumn clothes"
    else:
        result = "Go for light clothes"
    print(result)    
    return result

def report():
    average_temperature_humidity()
    result = f"The last 30 sec average Temperature is {latest_data['average-temp']} and Humidity {latest_data['average-hum']}"
    print(result)
    return result


def main():
    pass

if __name__ == "__main__":
    main()
