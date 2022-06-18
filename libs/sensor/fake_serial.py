import json
from random import randint
from ..config import DEFAULT_BOARD_MODE

class fake_serial():
    def __init__(self, board: str) -> None:
        self.input_buffer: str = ''
        self.output_buffer: str = ''
        self.mode = DEFAULT_BOARD_MODE
        self.board_name = board
        if board == 'B1':
            self.data_cnt = 16  
            self.sensor_no = "0,1,2,3,5,6,7,8,10,11,12,13,15,16,17,18".split(',') 
        elif board == 'B2':
            self.data_cnt = 25-16
            self.sensor_no = "4,9,14,19,20,21,22,23,24".split(',')
        
        self.mode_map = {
            1: self._mode1,
            2: self._mode2,
            3: self._mode3
        }
    def write(self, data: str):
        try:
            self.input_buffer = str(data)
            self.process()
            return len(data)
        except Exception as e:
            return f"{e}"

    def process(self):
        for s in self.input_buffer:
            response = self._iner_process(s)
            self.output_buffer += response
    def _iner_process(self, s: str) -> str:
        if s == 'w':
            return f"{self.board_name}\r\n"
        if s == 'm':
            return f"Board mode={self.mode}\r\n"
        if '1'<= s <= '3':
            self.mode = int(s)
            return f"Set board mode={s}\r\n"
        if s == 's':
            rand_data = {sensor: randint(0,1024) for sensor in self.sensor_no}
            return self.mode_map[int(self.mode)](rand_data)

    '''
    TODO
    return in byte
    '''
    def read(self):
        out = self.output_buffer[0] if self.output_buffer else ""
        self.output_buffer = "" if len(self.output_buffer) <= 1 else self.output_buffer[1:]
        return out
    
    def read_all(self):
        out = self.output_buffer
        self.output_buffer = ''
        return out.strip()
    
    def readline(self):
        new_buff, out, flag= '', '', False
        for s in self.output_buffer:
            if flag: new_buff += s
            else: out += s
            if s == '\n':
                flag = True
        self.output_buffer = new_buff
        return out.strip()
            
    def write_readall(self, input: str):
        self.write(input)
        return self.read_all()
    
    def write_readline(self, input: str):
        self.write(input)
        return self.readline()
    


    @staticmethod
    def _mode1(data: dict):
        return "\r\n".join([f"{d}" for d in data]) + "\r\n"

    @staticmethod
    def _mode2(data: dict):
        return json.dumps(data) + "\r\n"

    @staticmethod
    def _mode3(data: dict):
        return f"{[d for d in data.values()]}\r\n"