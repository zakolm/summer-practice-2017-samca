import serial, sys, io
import threading
def connect(ser,name):
    ser.baudrate = 19200
    ser.port = name
    ser.timeout=1
def transmitt(name):
    ser = serial.Serial()        
    connect(ser,name)
    s=''
    while (s!='9'):
        
        ser.open()
        s=input('>>')
        ser.write(s.encode('utf-8'))
        st=ser.read().decode('utf-8')
        print(st)
        ser.close()


t = threading.Thread(target=transmitt, args=('COM4',))
t.daemon = True
t.start()

    
