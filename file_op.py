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



class FileIO:
    def __init__(self,f_path,f_flag):
        self.f_path = f_path
        self.f_flag = f_flag
        self.f_handle = open(self.f_path,self.f_flag)
    def f_write(self,data):
        print("in f_write")
        data = data.encode("utf-8").decode("cp950","ignore")
        self.f_handle.write(data)
        self.f_handle.write("\n")
    def f_close(self):
        self.f_handle.close()

class files_operation:
    def __init__(self):
        self.exit=0
        self.log_path="123"
    def write(self,text):
        print("in files operation write")
        global today
        global first_log_path
        global ori_log_path
        first_log_path = 1
        files_op.log_path = log_folder_path + str(today.hour) + "-" + ".log"
        fp_log = FileIO(self.log_path,"a")
        fp_log.f_write(text)
        fp_log.f_close()


def FILE_OP():
    print("FILE_OP")
    global  files_op
    fp_log = FileIO(log_folder_path+".log","a")
    fp_log.f_write(text)
    files_op = files_operation()
    files_op.write(test)
    while 1:
        print("in while")
        files_op.write(test)
    print("over")

### START HERE  ###
today = datetime.datetime.now()
cur_path = os.getcwd()
log_folder_path = cur_path + "\log-" + str(today.year) + str(today.month) + str(today.day) + "_" + "file_op" "\\"
chk_path = os.path.exists(log_folder_path)
if(chk_path != True):
    os.mkdir(log_folder_path)

try:
    FILE_OP()
except:
    print("Error: unable to operate file")

