import json
import sys
import glob
import serial
import time
from typing import Tuple

class Serial(serial.Serial):
    """Inheritance from pyserial serial.Serial class

       Method Overriding

        :write(data)
            encode data if data is string and write to serial port

        :read()/read_all()
            decode the byte read from serial port

    """
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def write(self, data: str):
        data = data.encode() if isinstance(data, str) else data
        super().write(data)

    def decode(func):
        def wrap(self, d: bool=True, *args):
            output = getattr(super(), func.__name__)(*args)
            if d: return output if isinstance(output, str) else output.decode().strip()
            return output
        return wrap

    @decode
    def read_all(self, d: bool=True):
        pass

    @decode
    def readline(self, d: bool=True, __size: int = None) -> str:\
        pass

def list_serial_ports():
    """ Lists serial port names

        :raises EnvironmentError:
            On unsupported or unknown platforms
        :returns:
            A list of the serial ports available on the system
    """
    if sys.platform.startswith('win'):
        ports = ['COM%s' % (i + 1) for i in range(256)]
    elif sys.platform.startswith('linux') or sys.platform.startswith('cygwin'):
        # this excludes your current terminal "/dev/tty"
        ports = glob.glob('/dev/tty[A-Za-z]*')
    elif sys.platform.startswith('darwin'):
        ports = glob.glob('/dev/tty.*')
    else:
        raise EnvironmentError('Unsupported platform')

    result = []
    for port in ports:
        try:
            s = serial.Serial(port)
            s.close()
            result.append(port)
        except (OSError, serial.SerialException):
            pass
    return result

def init_boards() -> Tuple[Serial, Serial]:
    """Init two arduino boards

    TODO
     - Dummy serial instance
    """
    board1, board2 = None, None 
    ports = list_serial_ports()
    if ports == []:
        print("No COM ports found!")
    for port in ports:
        try:
            s = Serial(port)
            time.sleep(1.5)
            s.write('w')
            ans = s.readline()
            print(f"port:{port} board:{ans}")
            if ans == 'B1':
                board1 = s
            elif ans == 'B2':
                board2 = s
            else:
                s.close()
        except (serial.SerialException) as e:
            print(f"port:{port}, error:{e}")
            s.close()
            continue
        
    return board1, board2

if __name__ == '__main__':
    s1, s2 = init_boards()
    s1.write('3')
    while(1):
        try:
            s1.write('s')
            res = s1.readline() 
            print(f"\r{json.loads(res)}"+" "*(96-len(res)), end='')
        except json.JSONDecodeError:
            s1.write('s')
            pass
        except KeyboardInterrupt:
            print("\n Interrupt")
            break
    
    s1.close()
    