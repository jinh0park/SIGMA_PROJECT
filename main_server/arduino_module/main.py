import serial


class ArduinoControl:

    def __init__(self, port, baudrate=9600):
        self.ser = serial.Serial(port=port, baudrate=baudrate, parity=serial.PARITY_NONE,
                    stopbits=serial.STOPBITS_ONE, bytesize=serial.EIGHTBITS, timeout=0)

    def __del__(self):
        self.ser.close()

    def runServo(self, angles):
        assert len(angles) == 4
        command = ":".join(list(map(str, angles)))
        self.ser.write(bytes(command, encoding='ascii'))
