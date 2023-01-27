from pyftdi import i2c
from pyftdi.ftdi import Ftdi


def main():
    print('I2C Scanner')


    controller = i2c.I2cController()
    url = 'ftdi:///1'
    urlFt232h = 'ftdi://ftdi:232h:/1'
    controller.configure(url)

    adxl345 = controller.get_port(0x53)

    devId = adxl345.read_from(0x00, 1)

    controller.terminate()

    print(devId)








    pass

if __name__ == "__main__":
    main()