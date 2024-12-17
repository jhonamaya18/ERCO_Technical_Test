from read_device import ReadDevice
import asyncio
import pymodbus.client, pymodbus.framer, pymodbus.exceptions, pymodbus.pdu
import time

weather_station = ReadDevice("COM2",4,40035,4,2)            # port: 2, function: 4, address: 40035, id: 2
asyncio.run(weather_station.main(1,"Irradiancia","kWh/m2")) # Irradiancia is variable 1


