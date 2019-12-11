import serial
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
      
ser.write('1')
