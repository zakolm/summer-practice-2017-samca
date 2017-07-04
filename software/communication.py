import serial, sys, io
def connect(ser):
    ser.baudrate = 19200
    ser.port = 'COM4'

ser = serial.Serial()        
connect(ser)    
s=''
while (s!='9'):
    ser.open()
    s=input('>>')
    ser.write(s.encode('utf-8'))
    sio = io.TextIOWrapper(io.BufferedRWPair(ser, ser))
    ser.close()
