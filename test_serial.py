from libs.sensor.serial_port import init_boards
import numpy as np
import time

if __name__ == '__main__':
    sensors = init_boards()
    while(1):
        data = sensors.get_sensor_value()
        re_data = np.reshape(data,(5,5))
        print(f'\r{re_data}', end='')
        time.sleep(0.5)
        pass