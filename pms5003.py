from machine import UART


class PMS5003:
    """
    Simple Micropython driver for PMS5003 particle sensor.
    """
    
    START_BYTE_1 = 0x42
    START_BYTE_2 = 0x4d

    CMD_GET_PASSIVE_READING = 0xe2
    CMD_CHANGE_MODE = 0xe1
    CMD_SLEEP_ACTION = 0xe4

    MODE_PASSIVE = 0x00
    MODE_ACTIVE = 0x01
    CMD_SLEEP = 0x00
    WAKEUP = 0x01

    FRAME_LENGTH = 28


    def __init__(self, uart: UART, mode: str):
        self._mode = mode
        self._uart = uart

        if self._mode == "active":
            self._uart.write(bytearray([self.CMD_CHANGE_MODE, self.MODE_ACTIVE]))
        elif self._mode == "passive":
            self._uart.write(bytearray([self.CMD_CHANGE_MODE, self.MODE_PASSIVE]))
        else:
            raise ValueError("Invalid sensor mode, pick 'active' or 'passive'")

        # Init data
        self.pm1_concentration_indoor = 0
        self.pm2_concentration_indoor = 0
        self.pm10_concentration_indoor = 0

        self.pm1_concentration_outdoor = 0
        self.pm2_concentration_outdoor = 0
        self.pm10_concentration_outdoor = 0

        self.pm_per_1l_0_3 = 0
        self.pm_per_1l_0_5 = 0
        self.pm_per_1l_1_0 = 0
        self.pm_per_1l_2_5 = 0
        self.pm_per_1l_5_0 = 0
        self.pm_per_1l_10_0 = 0

    def read(self):
        if self._mode == "active":
            self._read_active()
        elif self._mode == "passive":
            self._read_passive()
        else:
            raise ValueError("Invalid sensor mode, pick 'active' or 'passive'")

    def _read_active(self):
        recv = False
        while not recv:
            data = self._uart.read()
            if data is not None:
                self._parse_data(data)
                recv = True

    def _read_passive(self):
        recv = False
        self._uart.write(bytearray([self.CMD_GET_PASSIVE_READING]))
        while not recv:
            data = self._uart.read()
            if data is not None:
                self._parse_data(data)
                recv = True

    def _parse_data(self, data: bytes):
        frame_length = data[2] << 8 | data[3]
        assert frame_length == self.FRAME_LENGTH

        checksum_sum = sum(data[:30])
        checksum_data = data[30] << 8 | data[31]
        assert checksum_sum == checksum_data

        self.pm1_concentration_indoor = data[4] << 8 | data[5]
        self.pm2_concentration_indoor = data[6] << 8 | data[7]
        self.pm10_concentration_indoor = data[8] << 8 | data[9]

        self.pm1_concentration_outdoor = data[10] << 8 | data[11]
        self.pm2_concentration_outdoor = data[12] << 8 | data[13]
        self.pm10_concentration_outdoor = data[14] << 8 | data[15]

        self.pm_per_1l_0_3 = data[16] << 8 | data[17]
        self.pm_per_1l_0_5 = data[18] << 8 | data[19]
        self.pm_per_1l_1_0 = data[20] << 8 | data[21]
        self.pm_per_1l_2_5 = data[22] << 8 | data[23]
        self.pm_per_1l_5_0 = data[24] << 8 | data[25]
        self.pm_per_1l_10_0 = data[26] << 8 | data[27]
