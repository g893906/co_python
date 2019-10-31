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


today = datetime.datetime.now()
first_log_path=''

class FileIO:
    def __init__(self,f_path,f_flag):
        self.f_path = f_path
        self.f_flag = f_flag
        self.f_handle = open(self.f_path,self.f_flag)
    def f_write(self,data):
        data = data.encode("utf-8").decode("cp950","ignore")
        self.f_handle.write(data)
        self.f_handle.write("\n")
    def f_close(self):
        self.f_handle.close()


class serial_port:
    def __init__(self):	  
        self.exit=0
        self.log_path="123"
        self.time_start= 0
        self.time_end  = 0	  
        self.enTimeOut = 0		  
        self.inEndLoop = 0
    def open(self,comport,baudrate,to):
        print ("com port initial")
        print(comport)
        print(baudrate)
        self.ser = serial.Serial(comport, 9600, timeout=float(to))
        self.time_start = time.time()
    def write(self,cmd):
        cmd = cmd.encode("utf-8")
        self.ser.write(cmd)
        time.sleep(0.5)
    def on_off(self,cmd):
        if( cmd == 'on'):
            self.ser.setDTR(False)
        elif( cmd == 'off'):
            self.ser.setDTR(True)
    def reset_on_off(self,cmd):
        if( cmd == 'on'):
            self.ser.setRTS(True)	#RTS output low signal to reset EVB
        elif( cmd == 'off'):
            self.ser.setRTS(False)	#RTS output high signal to deassert reset EVB
    def read(self,comport):
        print("com port read")
        global today
        global boot_proc_check
        global wusb_cycle_check
        global rusb_cycle_check
        global wsdc_cycle_check
        global rsdc_cycle_check
        global emac_cycle_check
        global video_cycle_check
        global first_log_path
        global ori_log_path
        global slt_test_res
        global sensor_run
        global err_flag
        global test_cnt
        global stop_run
        if (self.inEndLoop != 1 and first_log_path != 1):
            ser_port.log_path = log_folder_path+str(today.hour)+"-"+str(today.minute)+".log"
        first_log_path = 1
        
        print("com port read1")
        try:
            print("com port read2")
            input = self.ser.readline().decode("utf-8")
            print("com port read3")
            print(input)
        except:
            print("com port read4")
            input = self.ser.readline().decode("latin-1").rstrip()  		
        if (self.inEndLoop != 1):
            print("com port read5")
            fp_log = FileIO(self.log_path,"a")
        if ( 'I2C' in input):
            self.inEndLoop = 0
            boot_proc_check = 0
            wusb_cycle_check = 0
            rusb_cycle_check = 0
            wsdc_cycle_check = 0
            rsdc_cycle_check = 0
            emac_cycle_check = 0
            video_cycle_check = 0
            first_log_path = 0
            slt_test_res = 0
            sensor_run = 1
            err_flag = 0
            stop_run = 0
            self.time_start = time.time()
            today = datetime.datetime.now()
            fp_log = FileIO(self.log_path,"a")
            fp_log.f_write('PASS: Boot process, Power on')
            fp_log.f_close()
            self.write("mii write 5 d 1f\n" )
            self.write("mii write 5 e 86\n" )
            self.write("mii write 5 d 401f\n" )
            self.write("mii write 5 e 0x08\n" )
            self.write("mii read 5 e\n" )
            self.write("bootm\n")
        elif ( 'login:' in input):
            print(input)
            time.sleep(2)
            self.write("root\r\n".encode())
            time.sleep(2)
            self.write("root\r\n".encode())
        elif ( 'Password:' in input):
            print(input)
            time.sleep(2)
            self.write("root\r\n".encode())
        elif ( 'Login incorrect' in input):
            print(response)
        elif ( 'root@se_gsi_apu_18_wnc:~#' in input ):
            print(input)
            logtime = time.time()
            data='ifconfig eth0 192.168.33.10\n'
            data=data.encode()
            self.write(data)
            data='ping -c 100 192.168.33.60\n'
            self.write(data)
        elif ( 'Scan' in input ):
            print(input)
            logtime = time.time()
            st_time = datetime.datetime.fromtimestamp(logtime).strftime('%Y-%m-%d %H:%M:%S')
            fp_log.f_write(st_time+' '+input)
            fp_log.f_close()
        elif ( 'round-trip' in input ):
            print(input)
            logtime = time.time()
            st_time = datetime.datetime.fromtimestamp(logtime).strftime('%Y-%m-%d %H:%M:%S')
            fp_log.f_write(st_time+' '+input)
            fp_log.f_close()
        else:
            print("read 6, no key word get")
def UART0( COM_N,BAUDRATE ):
    print ("com port node is:"+COM_N)
    print ("com port baudrate is:"+BAUDRATE)
    global ser_port
    ser_port = serial_port()
    ser_port.open(COM_N,BAUDRATE,3.0)
    ser_port.on_off("off")       #EVB power on
    time.sleep(3)
    ser_port.on_off("on")        #EVB power on
    ser_port.reset_on_off("on")  #EVB reset assert
    time.sleep(3)
    ser_port.reset_on_off("off") #EVB reset deassert

    while 1:
        ser_port.read(COM_N)
    
    print('Over')

def manual_conn_com():
    print("Hint: you could use command to check the com port number:")
    print(">ls /dev/ttyS, then press tap")
    string = input("please input COM port number:")
    port = '/dev/ttyS' + str(string)
    return port

def manual_baudrate():
    print("Select the baudrate of you DUT: such as 9600, 115200, 38400...:")
    string1 = input("please input the baudrate:")
    speed = str(string1)
    return speed
### START HERE ###

cur_path = os.getcwd()
log_folder_path = cur_path + "/log-" + str(today.year) + str(today.month) + str(today.day) + "_" + "file_op" "/"
chk_path = os.path.exists(log_folder_path)
if(chk_path != True):
    os.mkdir(log_folder_path)

port = manual_conn_com()
speed = manual_baudrate()
try:
    #_thread.start_new_thread ( UART0,(port,speed,) )
    UART0(port,speed)

except:
    print ("Error: unable to start thread")

while 1:
    x = input('pySerial timeout (3.0 sec), key [bye] to exit\n')
    if(x == 'bye'):
        break
