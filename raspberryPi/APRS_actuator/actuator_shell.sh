rtl_fm -f 144.390M - | direwolf -l ~/Documents -c sdr.conf -r 24000 -D 1 -> ~/Documents/direwolf_log.txt &
python parsing_actuator.py
