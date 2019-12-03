import threading
import subprocess
from datetime import datetime

class AsyncTask:
    def __init__(self):
        pass

    def Task(self):
        now = datetime.today().strftime("%Y-%m-%d")
        file_name = now+".log"
        f = open("/home/pi/Document/" + file_name, "r")
        s = f.read()
        f.close()
        f = open("/home/pi/Document/" + file_name, "w")
        f.close()
        lines = s.splitlines()

        for line in lines:
            try:
                info = line.split("##")[1]
                subprocess.call('mosquitto_pub -h 192.168.2.74 -t test -m "'+info+'"', shell=True)
                print(info)
            except:
                print("test?")
        
        threading.Timer(2,self.Task).start()
        
def main():
    at = AsyncTask()                                                        
    at.Task()

if __name__ == '__main__':
    main()
