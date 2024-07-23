import time
import threading
import board
import adafruit_dht
import Adafruit_GPIO.SPI as SPI
import Adafruit_MCP3008
import requests
from pulsesensor import Pulsesensor  

dhtDevice = adafruit_dht.DHT11(board.D17)


SPI_PORT = 0
SPI_DEVICE = 0
mcp = Adafruit_MCP3008.MCP3008(spi=SPI.SpiDev(SPI_PORT, SPI_DEVICE))

def send_data_to_server(data):
    url = "http://ai.eprime.app/sensor/public/api/sensor"
    headers = {'Content-Type': 'application/json'}
    response = requests.post(url, json=data, headers=headers)
    return response.status_code


pulse_sensor = Pulsesensor(channel=4, bus=0, device=0)
pulse_sensor.startAsyncBPM()

while True:
    try:
        
        temperature_c = dhtDevice.temperature
        humidity = dhtDevice.humidity
        force_data = mcp.read_adc(7)
        bend_data = mcp.read_adc(6)
        pressure_data = mcp.read_adc(5)
        pulse_rate = pulse_sensor.BPM

        sensor_data = {
            "temperature_c": temperature_c,
            "humidity": humidity,
            "force": force_data,
            "bend": bend_data,
            "pressure": pressure_data,
            "pulse_rate": pulse_rate
        }
        status = send_data_to_server(sensor_data)
        print(f"Data: {sensor_data}")
        
    except RuntimeError as error:
        # print(error.args[0])
        pass
    except Exception as error:
        # print(f"Error: {error}")
        pass

    time.sleep(1)
pulse_sensor.stopAsyncBPM()
