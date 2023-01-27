from pyftdi import i2c

class ADXL345:


    def __init__(self,address=0x53, url='ftdi:///1') -> None:
        self.address = address
        self.url = url
        self.controller = i2c.I2cController()
        self._open()
        self.i2c = self.controller.get_port(self.address)
        
        
    
    def __del__(self):

        self.controller.terminate()

    def setFtdiURL(self, url):
        self.url = url

    def setAddress(self,address):
        self.address = address
        self.i2c = self.controller.get_port(address)


    def _open(self):
        self.controller.configure(self.url)
    def _close(self):
        self.controller.terminate()

    def getDeviceId(self):
        """
        Gets Device ID of adxl345
        The device id is fixed and should be 0x35
        """
        DEVID_REG=0x00
        self._open()
        devIdBytes = self.i2c.read_from(DEVID_REG, 1)
        self._close()
        

        if devIdBytes:
            return int.from_bytes(devIdBytes, 'big')
        else:
            return None

    def isActive(self):
        return self.getDeviceId() == 0x35
