import threading
from datetime import datetime
import time
import sqlite3

end = False

def func(second = 1.0):
    global end
    if end:
        return

    flag = True
    while flag:
        try:
	    f = open("/home/woojin/Agiot_Aprs/web/output_agiot_mqtt.txt",'r')
            flag = False
        except:
            print("no file, retry after 5 second")
            time.sleep(5)
        
    s = f.read()
    f.close()
    f = open("/home/woojin/Agiot_Aprs/web/output_agiot_mqtt.txt", 'w')
    f.close()

    lines = s.splitlines()
    for line in lines:
	try:
            infos = line.split("##")[1]
	    datas = infos.split("#")
            print(datas)
            conn = sqlite3.connect('./db.sqlite3')
	    cur = conn.cursor()
	    now = datetime.now()
	    cur.execute('INSERT INTO dashboard_sensor (farm_id, soil_humidity, temperature, humidity, actuator, created_date) values (:farm_id, :s, :t, :h, :a, :d)', {'farm_id': int(datas[0]), 's': int(datas[1]), 't': float(datas[2]), 'h': float(datas[3]), 'a': False, 'd': now})        
	    conn.commit()
            conn.close()
		
	except:
	    print("Exception : No delimiter ##")

    threading.Timer(second, func, [second]).start()

def main():
    func(2.0)

if __name__ == '__main__':
    main()

