#!/usr/bin/python3.6

Time_zone = input("Input the Time Location, TW or IL or ALT:") 

Time = input("Input the "+Time_zone+" time"", this program will cal. other location time:")

if ('TW' in Time_zone):
    print( Time_zone + " time is:"+Time )
    Time = int(Time)
    if( Time < 12):
        ALT_time = Time + 12
    else:
        ALT_time = Time - 12
    if ( Time >= 6 ):
        Israel_time = Time - 6
    else:
        Israel_time = Time - 6 + 24 
    if ( Time >15 ):
        CA_time = Time - 15
    else:
        CA_time = Time -15 + 24 
    print("ALT time is:%d" %(ALT_time) )
    print("Israel time is:%d" %(Israel_time) )
    print("California time is:%d" %(CA_time) )

elif ('IL' in Time_zone):
    print( Time_zone + " time is:"+Time )
    Time = int(Time)
    if ( Time >= 18 ):
        TW_time = Time - 18
    else:
        TW_time = Time  + 6
    if( TW_time < 13 ):
        ALT_time = TW_time + 11
    else:
        ALT_time = TW_time - 13
    print("ALT time is:%d" %(ALT_time) )
    print("TW time is:%d" %(TW_time) )

elif ('ALT' in Time_zone):
    print( Time_zone + " time is:"+Time )
    Time = int(Time)
    if ( Time > 11 ):
        TW_time = Time - 11
    else:
        TW_time = Time  + 13
    if( TW_time >= 6 ):
        IL_time = TW_time - 6
    else:
        IL_time = TW_time - 6 + 24
    print("IL time is:%d" %(IL_time) )
    print("TW time is:%d" %(TW_time) )
else:
    print("Please input the correct format location and time, bye!!!")
