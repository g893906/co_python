#!/usr/bin/python3.6
# =======================================
# establish communication using python
# =======================================

import time
import serial
import os
import datetime
import _thread
import binascii
import array
import codecs
import subprocess
import sys
# initialization and open the port
# possible timeout values:
#    1. None: wait forever, block call
#    2. 0: non-blocking mode, return immediately
#    3. x, x is bigger than 0, float allowed, timeout block call

ser = serial.Serial()

ser.port = "/dev/ttyS13" #set the com port number

ser.baudrate = 115200     #set the baudrate
ser.bytesize = serial.EIGHTBITS #number of bits per bytes
ser.parity = serial.PARITY_NONE #set parity check: no parity
ser.stopbits = serial.STOPBITS_ONE #number of stop bits
#ser.timeout = None          #block read
ser.timeout = 0             #non-block read
#ser.timeout = 2              #timeout block read

ser.xonxoff = False     #disable software flow control
ser.rtscts = False     #disable hardware (RTS/CTS) flow control
ser.dsrdtr = False       #disable hardware (DSR/DTR) flow control
ser.writeTimeout = 2     #timeout for write

today =  datetime.datetime.now()


cur_path = os.getcwd()
log_folder_path = cur_path + "\log-" + str(today.year) + str(today.month) + str(today.day) + "_" + "APU_board_testing" "\\"
chk_path = os.path.exists(log_folder_path)
if(chk_path != True):
    os.mkdir(log_folder_path)
print (log_folder_path)

logtime = time.time()
st_time = datetime.datetime.fromtimestamp(logtime).strftime('%Y-%m-%d %H:%M:%S')
wlog = open(log_folder_path+"/"+st_time+".txt","a")

try:
    ser.open()
except getopt.GetoptError as e:
        print ("error openning serial port",str(e))
        exit()
flag=0
if ser.isOpen():
        try:
                ser.flushInput() #flush input buffer, discarding all its contents
                ser.flushOutput()#flush output buffer, aborting current output
                #and discard all that is in buffer
                #write data
                ser.write (b'bootm\r')
                print ("ac_spi_slash 3 sent")
                time.sleep(0.5)  #give the serial port sometime to receive the data
                numOfLines = 0

                while True:
                        response = ser.readline().decode('utf-8')
                        #msg = 'read data %s.' %response
                        #if ( 'bytes' in response):
                        #    logtime = time.time()
                        #    st_time = datetime.datetime.fromtimestamp(logtime).strftime('%Y-%m-%d %H:%M:%S')
                        #    wlog.write(st_time+' '+response)
                        #    if ( (numOfLines%2) >0 ):
                        #        ser.setRTS(False)
                        #        ser.setDTR(False)
                        #    else:
                        #        ser.setRTS(True)
                        #        ser.setDTR(True) 
                        #    print(response)
                        #    numOfLines = numOfLines + 1
                        #    #if (numOfLines >= 5):
                        #    #    break
                        if ( 'ZynqMP>' in response):
                            print(response)
                            ser.write("mii write 5 d 1f\n".encode() )
                            ser.write("mii write 5 e 86\n".encode() )
                            ser.write("mii write 5 d 401f\n".encode() )
                            ser.write("mii write 5 e 0x08\n".encode() )
                            ser.write("mii read 5 e\n".encode() )
                            wlog.write(response)
                            #wlog.close()
                            ser.write("bootm\n".encode())
                        elif ( 'login:' in response):
                            print(response)
                            time.sleep(2)
                            ser.write("root\r\n".encode())
                            time.sleep(2)
                            ser.write("root\r\n".encode())
                        elif ( 'Password:' in response):
                            print(response)
                            time.sleep(2)
                            ser.write("root\r\n".encode())
                        elif ( 'Login incorrect' in response):
                            print(response)
                        elif ( 'root@se_gsi_apu_18_wnc:~#' in response ):
                            print(response)
                            logtime = time.time()
                            data='ifconfig eth0 192.168.33.10\n'
                            data=data.encode()
                            ser.write(data)
                            data='ping -c 100 192.168.33.60\n'.encode()
                            ser.write(data)
                        elif ( 'packets trans' in response ):
                            print(response)
                            logtime = time.time()
                            st_time = datetime.datetime.fromtimestamp(logtime).strftime('%Y-%m-%d %H:%M:%S')
                            #wlog
                            wlog.write(st_time+' '+response)
                            #wlog.close()
                        elif ( 'round-trip' in response ):
                            print(response)
                            logtime = time.time()
                            st_time = datetime.datetime.fromtimestamp(logtime).strftime('%Y-%m-%d %H:%M:%S')
                            #wlog
                            wlog.write(st_time+' '+response)
                            #wlog.close()
                        #elif ( 'root@se_gsi_apu_18_wnc:~#' in response ):
                        #    print(response)
                        #    logtime = time.time()
                        #    st_time = datetime.datetime.fromtimestamp(logtime).strftime('%Y-%m-%d %H:%M:%S')
                        #    if flag==0:
                        #        data='ifconfig eth0 192.168.33.10\n'
                        #        #data=data.encode("utf-8").decode("cp950","ignore")
                        #        data=data.encode()
                        #        ser.write(data)
                        #        flag=flag+1;
                        #        wlog.write(st_time+' '+"ifconfig")
                        #    elif flag==1:
                        #        data="tftp -g -r BOOT.bin 192.168.33.60\n"
                        #        data=data.encode()
                        #        ser.write(data)
                        #        wlog.write(st_time+' '+"tftp")
                        #        flag=flag+1;
                        #    elif flag==2:
                        #        data="mv BOOT.bin BOOT1.bin\n"
                        #        data=data.encode()
                        #        ser.write(data)
                        #        wlog.write(st_time+' '+"mv")
                        #        flag=flag+1;
                        #    elif flag==3:
                        #        data="tftp -p -l BOOT1.bin 192.168.33.60\n"
                        #        data=data.encode()
                        #        ser.write(data)
                        #        wlog.write(st_time+' '+"tftp -p")
                        #else:
                        #    print(response)
                ser.close()
                #wlog.close()

        except getopt.GetoptError as e1:
                print ("error communicating...: ",str(e1));
else:
        print ("cannot open serial port ")
