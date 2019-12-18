import sqlite3
from datetime import datetime

conn = sqlite3.connect('./db.sqlite3')
cur = conn.cursor()
now = datetime.now()
cur.execute('INSERT INTO dashboard_sensor (farm_id, soil_humidity, temperature, humidity, actuator, created_date) values (:farm_id, :s, :t, :h, :a, :d)', {'farm_id': 1, 's': 58, 't': 25.00, 'h': 16.00, 'a': False, 'd': now})
conn.commit()
conn.close()

