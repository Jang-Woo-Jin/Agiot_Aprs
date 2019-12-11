sudo /etc/init.d/mosquitto start
mosquitto_sub -d -t soil | tee output_mqtt.txt &
python main_module.py
