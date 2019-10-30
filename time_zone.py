#!/usr/bin/python3.6

string = input("please input the TW time, this program will cal. the IL and ALT time:")
print("TW time is:"+string)
if(int(string)<12):
    ALT_time=int(string)+12
else:
    ALT_time=int(string)-12
if (int(string)>=6):
    Israel_time=int(string)-6
else:
    Israel_time=int(string)-6+24
    
print("ALT time is:%d" %(ALT_time) )
print("Israel time is:%d" %(Israel_time) )

