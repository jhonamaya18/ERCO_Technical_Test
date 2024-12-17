import asyncio
import pymodbus.client, pymodbus.framer, pymodbus.exceptions, pymodbus.pdu


class ReadDevice:
    def __init__(self,port:str,function:int,address:int,quantity:int,slave_id:int):
        self.port = port
        self.function_code = function
        self.address = address
        self.quantity = quantity
        self.slave = slave_id
        self.client = None

    async def start_connection(
        self,
        framer=pymodbus.framer.ModbusRtuFramer,
    ) -> pymodbus.client:
        try:
            self.client = pymodbus.client.AsyncModbusSerialClient(
                self.port,
                framer=framer,
                timeout=1,
                retries=3,
                baudrate=9600, #Insert baudrate (Type hint: integer)
                bytesize=8, #Insert bytesize (Type hint: integer)
                parity="E", #Insert parity (Type hint: string)
                stopbits=1, #Insert stopbits (Type hint: integer)
            )

            # print("Connecting to slave")
            await self.client.connect()

            if self.client.connected:
                # print("Connected successfully")
                return self.client
            else:
                print("Failed to connect to the Modbus server")
                return None
        except Exception as e:
            print(f"Exception in start_connection: {e}")
            return None


    def close_connection(self,client: pymodbus.client) -> None:
        try:
            if self.client is not None:
                # print("Closing connection")
                client.close()
        except Exception as e:
            print(f"Exception in close_connection: {e}")

    async def run_async_simple_client(self,position) -> list:

        self.client = await self.start_connection()

        if self.client is None:
            return

        # print("Getting data")

        try:
            if self.function_code == 3:
                rr = await self.client.read_holding_registers(
                    address = self.address, count=self.quantity, slave=self.slave
                )
            else:
                rr = await self.client.read_input_registers(
                    address = self.address, count=self.quantity, slave=self.slave
                )

            if rr.isError():
                print(f"Exception reading registers: {rr}")
                return None
            if isinstance(rr, pymodbus.pdu.ExceptionResponse):
                print(f"Exception in instance of Modbus library: {rr}")
                return None
            n = (position-1)*2
            register = round(self.client.convert_from_registers(rr.registers[n:n+2], data_type=self.client.DATATYPE.FLOAT32),3) # conversión a flotante
            return register if rr else None
        except pymodbus.exceptions.ModbusException as e:
            print(f"Modbus library exception: {e}")
            return None
        finally:
            self.close_connection(client=self.client)

    async def main(self,position:int,name:str,units:str)-> None:
        try: 

            read_registers = await self.run_async_simple_client(position)

            if read_registers is not None:
                print(name+f": {read_registers} "+units)
            else:
                print("Failed to read register of "+name)
        except Exception as e:
            print(f"Exception in main: {e}")

