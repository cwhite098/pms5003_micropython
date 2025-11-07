from pms5003 import PMS5003
from machine import UART, Pin


def main():
    pms5003 = PMS5003(
        uart=UART(1, tx=Pin(4), rx=Pin(5), baudrate=9600),
        mode="passive"
    )

    pms5003.read()

    print(pms5003.pm1_concentration_indoor)
    print(pms5003.pm2_concentration_indoor)
    print(pms5003.pm10_concentration_indoor)

    print(pms5003.pm1_concentration_outdoor)
    print(pms5003.pm2_concentration_outdoor)
    print(pms5003.pm10_concentration_outdoor)

    print(pms5003.pm_per_1l_0_3)
    print(pms5003.pm_per_1l_0_5)
    print(pms5003.pm_per_1l_1_0)
    print(pms5003.pm_per_1l_2_5)
    print(pms5003.pm_per_1l_5_0)
    print(pms5003.pm_per_1l_10_0)


if __name__ == "__main__":
    main()
