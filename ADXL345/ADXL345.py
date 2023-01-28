from pyftdi import i2c
REGISTERS = {
    'DEVID' : 0x00,
    'THRESH_TAP' : 0x1d,
    'OFSX' :0x1e,
    'OFSY':0X1F,
    'OFSZ':0X20,
    'DUR':0X21,
    'LATENT':0X22,
    'WINDOW':0X23,
    'TRESH_ACT':0X24,
    'THRESH_INACT':0X25,
    'TIME_INACT':0X26,
    'ACT_INACT_CTL':0X27,
    'THRESH_FF':0X28,
    'TIME_FF':0X29,
    'TAP_AXES':0X2A,
    'ACT_TAP_STATUS':0X2B,
    'BW_RATE':0X2C,
    'POWER_CTL':0X2D,
    'INT_ENABLE':0X2E,
    'INT_MAP':0X2F,
    'INT_SOURCE':0X30,
    'DATA_FORMAT':0X31,
    'DATAX0':0X32,
    'DATAX1':0X33,
    'DATAY0':0X34,
    'DATAY1':0X35,
    'DATAZ0':0X36,
    'DATAZ1':0X37,
    'FIFO_CTL':0X38,
    'FIFO_STATUS':0X39
}
DEVICE_ID=0x35
class ADXL345:

    def __init__(self,address=0x53, url='ftdi:///1') -> None:

        self.powerCtl = 1 << 2
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
    def read_from(self, regAddr, len=1):
        self._open()
        data = self.i2c.read_from(regAddr,len)
        self._close()

        return data
       
    def write_to(self, regAddr, data, datalen):
        self._open()

        self.i2c.write_to(regAddr,data)

        self._close()

    def getDeviceId(self):
        """
        Gets Device ID of adxl345
        The device id is fixed and should be 0x35
        """
        
        self._open()
        devIdBytes = self.read_from(REGISTERS['DEVID'], 1)
        self._close()
        

        if devIdBytes:
            return int.from_bytes(devIdBytes, 'big')
        else:
            return None

    def writePowerCtl(self, value):

        self.write_to(REGISTERS['POWER_CTL'], [value], 1)

    def readPowerCtl(self):
        pctl_bytes = self.read_from(REGISTERS['POWER_CTL'])

        return int.from_bytes(pctl_bytes, 'big')
    def powerCtlSetBit(self, bitNum):
        assert(bitNum < 8)

        pctrl = self.readPowerCtl()
        pctrl |= (1 << bitNum)
        self.writePowerCtl(pctrl)

    def powerCtlClearBit(self, bitNum):
        assert(bitNum < 8)
        pctrl = self.readPowerCtl()
        pctrl &= ~(1 << bitNum)
        self.writePowerCtl(pctrl)
        

    def enableSleep(self, enable):
        SLEEP_BIT=2
        if enable:
            self.powerCtlSetBit(SLEEP_BIT)
        else:
            self.powerCtlClearBit(SLEEP_BIT)

    def wakeup(self, frequency=3):
        assert(frequency >= 0 and frequency <= 3)
        self.writePowerCtrl(frequency)
    def enableMeasurement(self, enable):
        #TODO: DONT CLEAR BITS
        MEAS_BIT=3
        if enable:
            self.powerCtlSetBit(MEAS_BIT)
        else:
            self.powerCtlClearBit(MEAS_BIT)
    
    def getXRaw(self):
        

        return int.from_bytes(self.read_from(REGISTERS['DATAX0'], 2),'big')
    
    def getYRaw(self):
        return int.from_bytes(self.read_from(REGISTERS['DATAY0'], 2),'big')
        
        
    

    def getZRaw(self):
        return int.from_bytes(self.read_from(REGISTERS['DATAZ0'], 2),'big')
        
        

    def getXYZRaw(self):
        data = self.read_from(REGISTERS['DATAX0'], 6)

        return {
            'x' : int.from_bytes(data[:2], 'big'),
            'y' : int.from_bytes(data[2:4], 'big'),
            'z' : int.from_bytes(data[4:6], 'big'),
        }
        

        

        


    def isActive(self):
        return self.getDeviceId() == DEVICE_ID
