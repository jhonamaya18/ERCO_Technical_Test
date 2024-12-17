# ERCO_Technical_Test

## Description
Technical test for TO analyst position in ERCO Energy. A brief description of the scripts is

## main_efficiency.py

Script that defines the connections to the weather station devices, pac3200 network analyzer and Huawei inverter through the modbus RS485 protocol. Afterwards, it shows every 5 seconds the values ​​of the variables: irradiance of the weather station, active power of the pac3200 and accumulated energy of the Huawei inverter.

 **A brief description of the other scripts is:**

### test_rtu_values.py 

Script that allows reading data from a modbus RS485 protocol, inserting the protocol variables in the main function.

### read_device.py 

module with the ReadDevice class that allows defining objects with the attributes of the protocol connection for each specific device. In addition, a specific variable is read using the main method.

### main.py 

Example of use of read_device.py (weather station)

### main_devices.py 

Example of use of read_device.py with 3 devices (weather station, pac3200, huawei_inverter)





