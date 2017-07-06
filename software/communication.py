import serial, sys
import threading
reading=True

def connect():
    res=False
    ser = serial.Serial()
    ser.baudrate = 19200
    ser.timeout = 0.01
    ports = ['COM%s' % (i + 1) for i in range(256)]
    for port in ports:
        try:
            ser.port=port
            ser.open()
            ser.write(b't')
            s=ser.read().decode('utf-8')
            ser.close()
            if s=='t':
                res=True
                break
        except (OSError, serial.SerialException):
            pass
    if res:
        return ser
    else:
        return None

def transmitt(name,path):
    s=''
    ser = connect()
    if ser!=None:
        ser.open()
        ser.write(path.encode('utf-8'))
        ser.close()
        while reading:
            ser.open()
            s=ser.read().decode('utf-8')
            if (s=='1'):
                print(1)
                #пройти вперед
            if (s=='2'):
                print(2)
            if (s=='3'):
                print(3)
            ser.close()
    else:
        print("Not connected")
path='12312313230'
t = threading.Thread(target=transmitt, args=('COM4',path,))
t.daemon = True
t.start()

