# indents are 4 SPACES
import os
import sys
import logging


# G29 P3 L50 R220 F50 B360 T V4

###### AUTO LEVELING ######
# multiply together to get square area, gives square area for this print. take values for 1, 2 or 3 bed and extrapulate it out.
# max probe points would be 8x8, so 8 probe points, if all 16 beds.
# would give four positions on every bed being probe.
# if square area is greater than 3x3 beds is, probe 8. always probes a square.


def gInject(Zone_Max_X, Zone_Min_X, Zone_Max_Y, Zone_Min_Y, cloneFile, DUPE_CHECK,BedType, MAX_X, MAX_Y):

    l = Zone_Min_X
    r = Zone_Max_X
    f = Zone_Min_Y
    b = Zone_Max_Y
    p = 0
    i = 0

    print "value of L is: " + str(l)

    zone_l = 240
    zone_f = 240

    lsub = 100
    fsub = 100
    radd = 100
    badd = 100


#l = 50
#r = 220
#f = 50
#b = 360
#p = 0
#i = 0

# Find Square Area for Print
    i = ((r-l)*(b-f))
    print "\n"
    print "Value of i: " + str(i)
    print "\n"

# Determine Probe Points Needed

    if((i >= ((240**2)*9))):
        # 9 Zones
        # probe 64
        if l < 20:
            l = 20
            print "PASSED l < 20"

        if f < 20:
            f = 20
            print "PASSED f < 20"
        cloneFile.write("G29 P8 " + "L" + str(l) + " R" + str(r) + " F" + str(f) + " B" +str(b) + " T V4\r\n")
        print "probed 8 or greater than 8"
        print "AUTO LVL VALUE: " + str(i)

    elif((i >= ((240**2)*5))) & ((i < ((240**2)*9))):
        # 5 Zones
        # probe 49
        if l < 20:
            l = 20
            print "PASSED l < 20"

        if f < 20:
            f = 20
            print "PASSED f < 20"
        cloneFile.write("G29 P7 " + "L" + str(l) + " R" + str(r) + " F" + str(f) + " B" +str(b) + " T V4\r\n")
        print "probed 7"
        print "AUTO LVL VALUE: " + str(i)

    elif((i >= ((240**2)*4))) & ((i < ((240**2)*5))):
        # 4 Zones
        # probe 36
        if l < 20:
            l = 20
            print "PASSED l < 20"

        if f < 20:
            f = 20
            print "PASSED f < 20"
        cloneFile.write("G29 P6 " + "L" + str(l) + " R" + str(r) + " F" + str(f) + " B" +str(b) + " T V4\r\n")
        print "probed 6"
        print "AUTO LVL VALUE: " + str(i)

    elif((i >= ((240**2)*3))) & ((i < ((240**2)*4))):
        # 3 Zones
        # probe 25
        if l < 20:
            l = 20
            print "PASSED l < 20"

        if f < 20:
            f = 20
            print "PASSED f < 20"
        cloneFile.write("G29 P5 " + "L" + str(l) + " R" + str(r) + " F" + str(f) + " B" +str(b) + " T V4\r\n")
        print "probed 5"
        print "AUTO LVL VALUE: " + str(i)

    elif((i >= ((240**2)*2))) & ((i < ((240**2)*3))):
        # 2 Zones
        # probe 16
        if l < 20:
            l = 20
            print "PASSED l < 20"

        if f < 20:
            f = 20
            print "PASSED f < 20"
        cloneFile.write("G29 P4 " + "L" + str(l) + " R" + str(r) + " F" + str(f) + " B" +str(b) + " T V4\r\n")
        print "probed 4"
        print "AUTO LVL VALUE: " + str(i)

############### 'i' is falling between above if and (<240**2), so... ##############
    elif((i >= ((240**2)))) & ((i < ((240**2)*2))):
        # 2 Zones
        # probe 16
        if l < 20:
            l = 20
            print "PASSED l < 20"

        if f < 20:
            f = 20
            print "PASSED f < 20"

        cloneFile.write("G29 P4 " + "L" + str(l) + " R" + str(r) + " F" + str(f) + " B" +str(b) + " T V4\r\n")
        print "probed 4"
        print "AUTO LVL VALUE: " + str(i)

###################################################################################

    elif(i < (240**2)):
        print "passed through elif"

        if i < 150**2: 
            print "passed 'i' if"
            print "L (BEFORE): "+str(l)
            # if(l > (zone_l*3)):
            #     l = l-(zone_l*3)
            #     val_l = 3
            # elif(l > (zone_l*2)):
            #     l = l-(zone_l*2)
            #     val_l = 2
            # elif(l >= (zone_l*1)):
            #     l = l-(zone_l*1)
            #     val_l = 1
            # elif(l < zone_l):
            #     val_l = 0

            if (l >= 120):
                lsub = 100
                radd = 100

            elif (l >= 110) & (l < 120):
                lsub = 90
                radd = 110

            elif (l >= 100) & (l < 110):
                lsub = 80
                radd = 120

            elif (l >= 90) & (l < 100):
                lsub = 70
                radd = 130

            elif (l >= 80) & (l < 90):
                lsub = 60
                radd = 140

            elif (l >= 70) & (l < 80):
                lsub = 50
                radd = 150

            elif (l >= 60) & (l < 70):
                lsub = 40
                radd = 160

            elif (l >= 50) & (l < 60):
                lsub = 30
                radd = 170

            elif (l >= 40) & (l < 50):
                lsub = 20
                radd = 180

            elif (l >= 30) & (l< 40):
                lsub = 10
                radd = 190

            elif (l < 30):
                lsub = 0
                radd = 200

            else:
                print "I went to else #1"

############### (fsub, badd) ##################
            print "F (BEFORE): "+str(f)

            # if(f > (zone_f*3)):
            #     f = f-(zone_f*3)
            #     val_f = 3
            # elif(f > (zone_f*2)):
            #     f = f-(zone_f*2)
            #     val_f = 2
            # elif(f >= (zone_f*1)):
            #     f = f-(zone_f*1)
            #     val_f = 1
            # elif(f < zone_f):
            #     val_f = 0

            if (f >= 120):
                fsub = 100
                badd = 100

            elif (f >= 110) &  (f < 120):
                fsub = 90
                badd = 110

            elif (f >= 100) & (f < 110):
                fsub = 80
                badd = 120

            elif (f >= 90) & (f < 100):
                fsub = 70
                badd = 130

            elif (f >= 80) & (f < 90):
                fsub = 60
                badd = 140

            elif (f >= 70) & (f < 80):
                fsub = 50
                badd = 150

            elif (f >= 60) & (f < 70):
                fsub = 40
                badd = 160

            elif (f >= 50) & (f < 60):
                fsub = 30
                badd = 170

            elif (f >= 40) & (f < 50):
                fsub = 20
                badd = 180

            elif (f >= 30) & (f < 40):
                fsub = 10
                badd = 190

            elif (f < 30):
                fsub = 0
                badd = 200

            else:
                print "I went to Else #2"


            print "\n"
            print "L (AFTER SUB & ADD CHECK): "+str(l)
            print "F (AFTER SUB & ADD CHECK): "+str(f)
            print "lsub: "+str(lsub)
            print "radd: "+str(radd)
            print "fsub: "+str(fsub)
            print "badd: "+str(badd)
            # print "val_l: "+str(val_l)
            # print "val_f: "+str(val_f)
            print "Duplication: "+str(DUPE_CHECK)
            print "Printer: "+str(BedType)
            print "\n"


            # l = (l - lsub) +(250*val_l)

            # r = r + radd

            # f = (f - fsub) + (250*val_f)

            # b = b + badd


        if l < 20:
            l = 20
            print "PASSED l < 20"

        if f < 20:
            f = 20
            print "PASSED f < 20"

        if r >= (MAX_X - 15):
            r = (MAX_X - 20)
            print "r bounds Passed"
        if b >= (MAX_Y - 15):
            b = (MAX_Y - 20)
            print "b bounds Passed"
        
        # if DUPE_CHECK > 0:
        #     if BedType == "GT":
        #         if b > (Zone_Min_Y/2): 
        #             b = 247.5
        #         if r > (Zone_Min_X/2):
        #             r = 225
        #     if BedType == "FRANK3":
        #         if b > (Zone_Min_Y/2): 
        #             b = 425
        #         if r > 440:
        #             r = 425
        #     if BedType == "reveal3D":
        #         if b > (Zone_Min_Y/2): 
        #             b = 510
        #         if r > 525:
        #             r = 510
            

        # elif DUPE_CHECK <= 0:
        #     if BedType == "GT":
        #         if b > Zone_Min_Y: 
        #             b = 510
        #         if r > 480:
        #             r = 465
        #     if BedType == "FRANK3":
        #         if b > Zone_Min_Y: 
        #             b = 475
        #         if r > 480:
        #             r = 475
        #     if BedType == "reveal3D":
        #         if b > Zone_Min_Y:
        #             b = 975
        #         if r > Zone_Min_X:
        #             r = 975
            

        # A Single Zone
        # probe 9 --> One Zone
        cloneFile.write("G29 P3 " + "L" + str(l) + " R" + str(r) + " F" + str(f) + " B" +str(b) + " T V4" + "\r\n")
        print ("G29 P3 " + "L" + str(l) + " R" + str(r) + " F" + str(f) + " B" +str(b) + " T V4" + "\r\n")
        print "probed 1"

    else:
        print "Probes not Deployed"

    print "\n"
