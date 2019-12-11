import threading
from datetime import datetime
import serial

end = False

def func(second = 1.0):
    global end
    if end:
        return
    f = open("/home/pi/output_mqtt.txt",'r')
    print(datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
    s = f.read()
    print(s)
    f.close()
    f = open("/home/pi/output_mqtt.txt", 'w')
    f.close()

    lines = s.splitlines()
    try:
        datas = lines[-1].split("!")[1]
        print(datas)
        
        port_num = 0
        usb_port = '/dev/ttyUSB'
        port_flag = True
        while(port_flag):
            try:
                ser = serial.Serial(usb_port + str(port_num), 9600)
                port_flag = False
            except:
                print("port number error : " + str(port_num))
                port_num = port_num + 1
                port_num = port_num % 5

        if int(datas) < 200:
            ser.write('1')
            print("1")
        else:
            ser.write('0')
            print("0")
    except:
        print("exceptions")

    threading.Timer(second, func, [second]).start()

def main():
    func(2.0)

if __name__ == '__main__':
    main()
