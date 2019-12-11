rtl_fm -f 144.350M - | direwolf -l ~/Document -c sdr.conf -r 24000 -D 1 - > direwolf_log.txt &
python parser.py
