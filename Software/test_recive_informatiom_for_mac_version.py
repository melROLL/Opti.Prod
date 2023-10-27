from pymodbus.client.sync import ModbusTcpClient

# Arduino的IP地址和端口号
arduino_ip = "10.3.7.8"
arduino_port = 502

# 创建Modbus TCP客户端连接
client = ModbusTcpClient(arduino_ip, port=arduino_port)

try:
    # 连接到Arduino
    if client.connect():
        # 读取保持寄存器的值（假设地址为0x00）
        result = client.read_holding_registers(0x00, 20, unit=1)

        if result.isError():
            print(f"Modbus error: {result}")
        else:
            # 打印读取到的值
            print(f"Value from Arduino: {result.registers[0],result.registers[1],result.registers[2],result.registers[3]}")

finally:
    # 关闭连接
    client.close()