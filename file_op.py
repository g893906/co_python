#!/usr/bin/python3.6
import serial
import time
import binascii
import array
import os
import datetime
import codecs
import subprocess
import sys
first_log_path = ''


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
        print("in f_close")
        self.f_handle.close()

class files_operation:
    def __init__(self,text):
        self.exit=0
        self.log_path=text
        print("in files oper.")
        print(text)
    def write(self,data):
        global  first_log_path
        if( first_log_path != 1 ):
            files_op.log_path = log_folder_path+str(today.hour)+"-"+str(today.minute)+".log"
        first_log_path = 1
        fp_log = FileIO(self.log_path,"a")
        fp_log.f_write(data)
        fp_log.f_close()


def FILE_OP():
    print("FILE_OP")
    global  files_op
    global  fp_log
    count = 1
    files_op = files_operation(log_folder_path)
    print("call file op write")
    files_op.write("test write is ok?")
    while 1:
        time_value = datetime.datetime.now()
        files_op.write( str(time_value.second) )
        time.sleep(1)
    print("over")

### START HERE  ###
today = datetime.datetime.now()
cur_path = os.getcwd()
log_folder_path = cur_path + "/log-" + str(today.year) + str(today.month) + str(today.day) + "_" + "file_op" "/"
chk_path = os.path.exists(log_folder_path)
if(chk_path != True):
    os.mkdir(log_folder_path)

try:
    FILE_OP()
except:
    print("Error: unable to operate file")

