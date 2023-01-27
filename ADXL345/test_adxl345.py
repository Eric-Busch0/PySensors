import ADXL345

"""
Test bench for ADXL345

Prints Device ID of Part

Expected Part # is 0xE5

"""
adxl345 = ADXL345.ADXL345()

devId = adxl345.getDeviceId() 

print('Device ID', hex(devId))