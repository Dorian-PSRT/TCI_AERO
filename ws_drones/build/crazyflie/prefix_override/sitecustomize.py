import sys
if sys.prefix == '/usr':
    sys.real_prefix = sys.prefix
    sys.prefix = sys.exec_prefix = '/home/alexmin9/Desktop/TCI_AERO/ws_drones/install/crazyflie'
