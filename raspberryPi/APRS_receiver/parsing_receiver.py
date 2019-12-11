import threading
import subprocess
import time
from datetime import datetime

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

        topics = ["temp", "hum", "soil"]
        for line in lines:
            try:
                infos = line.split("##")[1]
                datas = infos.split("!")
                for i,data in enumerate(datas):
                    subprocess.call('mosquitto_pub -h 192.168.2.74 -t ' + topics[i] + ' -m "' + "!" + data + '"', shell=True)
                print(info) 
            except:
                print("No informations") 
         
        threading.Timer(2,self.Task).start() 
         
def main(): 
    at = AsyncTask()                                                         
    at.Task() 
 
if __name__ == '__main__': 
    main()
