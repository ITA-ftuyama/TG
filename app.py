import serial
import time
import win32api
ser = serial.Serial('COM3', 9600, timeout=0)
# while 1:
#     print 'reading'
#     print ser.readline()
#     time.sleep(1)
for i in range(100):
    x, y = win32api.GetCursorPos()
    if x > 100:
        print "up"
        ser.write('H')
        time.sleep(0.1)
    else:
        print "down"
        ser.write('L')
        time.sleep(0.1)
