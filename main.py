import ADXL345


adxl345 = ADXL345.ADXL345()

devId = adxl345.getDeviceId() 

print(hex(devId))