import asyncio
import pymodbus.client, pymodbus.framer, pymodbus.exceptions, pymodbus.pdu



async def start_connection(
    port: str,
    framer=pymodbus.framer.ModbusRtuFramer,
) -> pymodbus.client:
    try:
        client = pymodbus.client.AsyncModbusSerialClient(
            port,
            framer=framer,
            timeout=1,
            retries=3,
            baudrate=9600, #Insert baudrate (Type hint: integer)
            bytesize=8, #Insert bytesize (Type hint: integer)
            parity="E", #Insert parity (Type hint: string)
            stopbits=1, #Insert stopbits (Type hint: integer)
        )

        print("Connecting to slave")
        await client.connect()

        if client.connected:
            print("Connected successfully")
            return client
        else:
            print("Failed to connect to the Modbus server")
            return None
    except Exception as e:
        print(f"Exception in start_connection: {e}")
        return None


def close_connection(client: pymodbus.client) -> None:
    try:
        if client is not None:
            print("Closing connection")
            client.close()
    except Exception as e:
        print(f"Exception in close_connection: {e}")

async def run_async_simple_client(
    port: str,
    function_code: int,
    address_register: int,
    amount_registers: int,
    slave: int,

) -> list:

    client = await start_connection(port=port)

    if client is None:
        return

    print("Getting data")

    try:
        if function_code == 3:
            rr = await client.read_holding_registers(
                address=address_register, count=amount_registers, slave=slave
            )
        else:
            rr = await client.read_input_registers(
                address=address_register, count=amount_registers, slave=slave
            )

        if rr.isError():
            print(f"Exception reading registers: {rr}")
            return None
        if isinstance(rr, pymodbus.pdu.ExceptionResponse):
            print(f"Exception in instance of Modbus library: {rr}")
            return None
        
        # Conversión a flotante

        irradiance = round(client.convert_from_registers(rr.registers[:2], data_type=client.DATATYPE.FLOAT32),3)
        temperature = round(client.convert_from_registers(rr.registers[2:4], data_type=client.DATATYPE.FLOAT32),3)
        
        return rr.registers,irradiance,temperature if rr else None
    except pymodbus.exceptions.ModbusException as e:
        print(f"Modbus library exception: {e}")
        return None
    finally:
        close_connection(client=client)

async def main()-> None:
    try: 
        serial_settings = "COM2" #Insert COM# port (Type hint: string)
        function = 4 #Insert function (Type hint: integer)
        address = 40035 #Insert initial address (Type hint: integer)
        quantity = 4 #Insert quantity of registes (Type hint: integer)
        slave_id =  2#Insert slave_id (Type hint: integer)

        read_registers = await run_async_simple_client(
            port=serial_settings,
            function_code=function,
            address_register=address,
            amount_registers=quantity,
            slave=slave_id,
        )

        if read_registers is not None:
            print(f"Registers: {read_registers[0]}")
            print(f"Irradiance: {read_registers[1]}")
            print(f"Temperature: {read_registers[2]}")
        else:
            print("Failed to read registers")
    except Exception as e:
        print(f"Exception in main: {e}")

if __name__ == "__main__":

    asyncio.run(
        main(),
        debug=False,
    )