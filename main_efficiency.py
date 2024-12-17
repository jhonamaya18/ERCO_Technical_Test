from read_device import ReadDevice
import asyncio
import pymodbus.client, pymodbus.framer, pymodbus.exceptions, pymodbus.pdu
import time

weather_station = ReadDevice("COM2",4,40035,4,2)        # port: 2, function: 4, directión: 40035, quantity: 4, id: 2
pac3200 = ReadDevice("COM4",4,1,8,1)                    # port: 4, function: 4, direction: 00000 = 1, quantity: 8, id: 1
huawei_inverter = ReadDevice("COM6",4,30000,4,3)        # port: 6, function: 4, direction: 30000, quantity: 4, id: 3

while True:
    asyncio.run(weather_station.main(1,"Irradiancia","kWh/m2"))      # Irradiancia is variable 1
    asyncio.run(pac3200.main(2,"Active_Power","kWh"))                # Active_Energy (or power) is variable 2
    asyncio.run(huawei_inverter.main(1,"Generation_Accum","kWh"))    # Generation_Accum is variable 1
    for i in range(5):
        time.sleep(1)
        if i!=4: print(".") 