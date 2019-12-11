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
                ser = serial.Serial('/dev/ttyUSB0', 9600)
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
