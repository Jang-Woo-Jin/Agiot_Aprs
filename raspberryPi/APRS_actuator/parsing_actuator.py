import threading
from datetime import datetime
import RPi.GPIO as GPIO
import time

pin = 5
GPIO.setmode(GPIO.BCM)
GPIO.setup(pin, GPIO.OUT)

class AsyncTask:
    def __init__(self):
        pass

    def Task(self):
        now = datetime.today().strftime("%Y-%m-%d")
        file_name = now+".log"
        
        flag = True
        while flag:
            try:
                f = open("/home/pi/Documents/" + file_name, "r")
                flag = False
            except:
                print(file_name)
                print("no file, retry after 5 second")
                time.sleep(5)
        s = f.read()
        f.close()
        f = open("/home/pi/Documents/" + file_name, "w")
        f.close()
        lines = s.splitlines()

        for line in lines:
            try:
                info = line.split("##")[1]
                print(info)
                if int(info) == 1:
                    print("HIGH") 
                    GPIO.output(pin, GPIO.HIGH)    
                elif int(info) == 0:
                    print("LOW")
                    GPIO.output(pin, GPIO.LOW)
                else:
                    pass
            except:
                print("test?")
        
        threading.Timer(2,self.Task).start()
        
def main():
    at = AsyncTask()                                                        
    at.Task()

if __name__ == '__main__':
    main()
