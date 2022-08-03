import json
import sys
import glob
import serial
import time
from typing import List
from libs.config import DEFAULT_BOARD_MODE, SERIAL_RT_COUNT, DATA_ORDER
from libs.sensor.fake_serial import fake_serial
from multiprocessing import Pool

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

    def decode(func):
        def wrap(self, d: bool=True, *args):
            output = getattr(super(), func.__name__)(*args)
            if d: 
                return output if isinstance(output, str) else output.decode().strip()
            return output
        return wrap

    def write(self, data: str):
        self.reset_output_buffer()
        data = str(data)
        data = data.encode() if isinstance(data, str) else data
        return super().write(data)
    
    def write_readall(self, data: str, wait: float=0.01 ) -> str:
        self.write(data)
        n = time.perf_counter()
        while(1):
            if time.perf_counter() - n > wait:
                return self.read_all()

    def write_readline(self, data: str) -> str:
        self.write(data)
        return self.readline()

    @decode
    def read_all(self, d: bool=True) -> str:
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


class Sensor_Board(object):
    def __init__(self, board_1: Serial, board_2: Serial) -> None:
        self.board_1 = board_1
        self.board_2 = board_2
        self.boards = (self.board_1, self.board_2)
        self.mode = DEFAULT_BOARD_MODE

    def set_board_mode(self, mode: int = DEFAULT_BOARD_MODE):
        for i, board in enumerate(self.boards, 1):
            print(f'B{i}', board.write_readline(f'{mode}'))
        self.mode = mode

    def get_board_mode(self):
        res1 = self.board_1.write_readline('m')
        for b in self.boards:
            res = b.write_readline('m')
            if res1 != res:
                raise ValueError(f"Board mode misatch! {b.name} mode={res}, {self.board_1.name} mode={res1} !")
        self.mode = int(res[res.find('=')+1])
        return self.mode

    def get_sensor_value(self) -> List[int]:
        """only support mode 3"""
        value1 = json.loads(self.board_1.write_readline('s'))
        value2 = json.loads(self.board_2.write_readline('s'))
        data = [(value1+value2)[i] for i in DATA_ORDER]
        return data

def init_boards() -> Sensor_Board:
    """Init two arduino boards
    """
    board1, board2 = fake_serial("B1"), fake_serial("B2")
    ports = list_serial_ports()
    if ports == []:
        print("No COM ports found!")
    for port in ports:
        try:
            s = Serial(port, timeout=10, write_timeout=1)
            time.sleep(1.2)
            t_count = 0
            while(s.in_waiting != 4):
                s.reset_input_buffer()
                s.write('w')
                t_count += 1
                time.sleep(0.2)
                if t_count > SERIAL_RT_COUNT:
                    raise TimeoutError(f'board not response untill maximun retry count. ({SERIAL_RT_COUNT})')
            ans = s.readline()
            print(f"port:{port} board:{ans}")
            if ans == 'B1':
                board1 = s
            elif ans == 'B2':
                board2 = s
            
            s.reset_input_buffer()
            s.reset_output_buffer()
            t_count = 0
            while(t_count < SERIAL_RT_COUNT):
                mod = s.write_readline(DEFAULT_BOARD_MODE) #設定板子預設模式
                if f"Set board mode={DEFAULT_BOARD_MODE}" in mod :
                    print(ans, mod)
                    s.reset_output_buffer()
                    s.reset_input_buffer()
                    break
                t_count += 1

        except (serial.SerialException, TimeoutError) as e:
            print(f"port:{port}, error:{e}")
            s.close()

    return Sensor_Board(board_1=board1, board_2=board2)




def main():
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
    

    