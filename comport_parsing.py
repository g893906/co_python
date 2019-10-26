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

ser.port = "/dev/ttyS5" #set the com port number

ser.baudrate = 9600     #set the baudrate
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

wlog = open(log_folder_path+"/log.txt","w")

try:
    ser.open()
except getopt.GetoptError as e:
        print ("error openning serial port",str(e))
        exit()

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
                        #response = ser.readline()
                        response = ser.readline().decode('utf-8')
                        #msg = 'read data %s.' %response
                        if ( 'I2C' in response):
                            logtime = time.time()
                            st_time = datetime.datetime.fromtimestamp(logtime).strftime('%Y-%m-%d %H:%M:%S')
                            wlog.write(st_time+' '+response)
                            print(response)
                            numOfLines = numOfLines + 1
                            if (numOfLines >= 5):
                                break
                ser.close()
                wlog.close()

        except getopt.GetoptError as e1:
                print ("error communicating...: ",str(e1));
else:
        print ("cannot open serial port ")
