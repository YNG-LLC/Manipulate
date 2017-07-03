# indents are 4 SPACES
import os
import sys
import dupeBeds
import logging

def do_something():
    logging.info('Logging writeBeds.py: ')

def writeBeds(Zone_Max_X, Zone_Min_X, Zone_Max_Y, Zone_Min_Y, NumberXBeds, NumberYBeds, MAX_X, MAX_Y, x_16offset, x_GToffset, y_16offset, y_GToffset, BedType, DUPE_CHECK, writeHeatBedsActive=[0]*16, FORGOT_BEDS=[0]*16, *args):
    writeZoneValues = [int(Zone_Max_X),int(Zone_Min_X),int(Zone_Max_Y),int(Zone_Min_Y)]

    # print " put this here start of # 2"
    # print Zone_Max_X
    # print Zone_Min_X
    # print Zone_Max_Y
    # print Zone_Min_Y
    # print NumberXBeds
    # print NumberYBeds
    # print MAX_X
    # print MAX_Y
    # print x_16offset
    # print x_GToffset
    # print y_16offset
    # print y_GToffset
    # print BedType
    # print DUPE_CHECK
    # print writeHeatBedsActive
    # print FORGOT_BEDS
    # print "end of # 2"
    # print "\n"
    # print "ZoneValues from WriteBeds.py:"
    # print writeZoneValues
    # print "\n"
    Max_X = writeZoneValues[0]                                   # this is a local VAR for writeBedControl.py . not to be confused with the MAX_X & MAX_Y
    Min_X = writeZoneValues[1]
    Max_Y = writeZoneValues[2]
    Min_Y = writeZoneValues[3]
    # Dimensions set according to BedType

    if BedType == "GT":
        writeHeatBedsActive = ['0']*4
        wxCheck = ['0']*4
        wyCheck = ['0']*4

        if DUPE_CHECK > 0:
            WMX1 = 0
            WMX2 = (MAX_X)*1
            WMX3 = (MAX_X)*2
            WMX4 = (MAX_X)*3

        else:
            WMX1 = 0
            WMX2 = (MAX_X/NumberXBeds)*1
            WMX3 = (MAX_X/NumberXBeds)*2
            WMX4 = (MAX_X/NumberXBeds)*3


        WMY1 = 0
        WMY2 = (MAX_Y/NumberYBeds)*1
        WMY3 = (MAX_Y/NumberYBeds)*2
        WMY4 = (MAX_Y/NumberYBeds)*3

        writeBed1 = [WMX1, WMY1]
        writeBed2 = [WMX2, WMY1]
        writeBed3 = [WMX2, WMY2]
        writeBed4 = [WMX1, WMY2]



    if BedType == "FRANK3":
        writeHeatBedsActive = ['0']*16
        wxCheck = ['0']*16
        wyCheck = ['0']*16

        if DUPE_CHECK > 0:
            WMX1 = 0
            WMX2 = (MAX_X/2)*1
            WMX3 = (MAX_X/2)*2
            WMX4 = (MAX_X/2)*3
        else:
            WMX1 = 0
            WMX2 = (MAX_X/NumberXBeds)*1
            WMX3 = (MAX_X/NumberXBeds)*2
            WMX4 = (MAX_X/NumberXBeds)*3


        WMY1 = 0
        WMY2 = (MAX_Y/NumberYBeds)*1
        WMY3 = (MAX_Y/NumberYBeds)*2
        WMY4 = (MAX_Y/NumberYBeds)*3

        writeBed1 = [WMX1, WMY1]
        writeBed2 = [WMX2, WMY1]
        writeBed3 = [WMX3, WMY1]
        writeBed4 = [WMX4, WMY1]
        writeBed5 = [WMX4, WMY2]
        writeBed6 = [WMX3, WMY2]
        writeBed7 = [WMX2, WMY2]
        writeBed8 = [WMX1, WMY2]
        writeBed9 = [WMX1, WMY3]
        writeBed10 = [WMX2, WMY3]
        writeBed11 = [WMX3, WMY3]
        writeBed12 = [WMX4, WMY3]
        writeBed13 = [WMX4, WMY4]
        writeBed14 = [WMX3, WMY4]
        writeBed15 = [WMX2, WMY4]
        writeBed16 = [WMX1, WMY4]


    if BedType == "reveal3D":
        writeHeatBedsActive = ['0']*16
        wxCheck = ['0']*16
        wyCheck = ['0']*16

        print "Max X (BEFORE): " + str(Max_X)
        if DUPE_CHECK > 0:
            WMX1 = 0
            WMX2 = (MAX_X/2)*1
            WMX3 = (MAX_X/2)*2
            WMX4 = (MAX_X/2)*3
        else:
            WMX1 = 0
            WMX2 = (MAX_X/NumberXBeds)*1
            WMX3 = (MAX_X/NumberXBeds)*2
            WMX4 = (MAX_X/NumberXBeds)*3

        print "this is Max X: " + str(WMX2)
        WMY1 = 0
        WMY2 = (MAX_Y/NumberYBeds)*1
        WMY3 = (MAX_Y/NumberYBeds)*2
        WMY4 = (MAX_Y/NumberYBeds)*3

        writeBed1 = [WMX1, WMY1]
        writeBed2 = [WMX2, WMY1]
        writeBed3 = [WMX3, WMY1]
        writeBed4 = [WMX4, WMY1]
        writeBed5 = [WMX4, WMY2]
        writeBed6 = [WMX3, WMY2]
        writeBed7 = [WMX2, WMY2]
        writeBed8 = [WMX1, WMY2]
        writeBed9 = [WMX1, WMY3]
        writeBed10 = [WMX2, WMY3]
        writeBed11 = [WMX3, WMY3]
        writeBed12 = [WMX4, WMY3]
        writeBed13 = [WMX4, WMY4]
        writeBed14 = [WMX3, WMY4]
        writeBed15 = [WMX2, WMY4]
        writeBed16 = [WMX1, WMY4]

############################# Turns Beds ON  ###########################################
### List order: [Max_X, Min_X, Max_Y, Min_Y]

    if (BedType == "FRANK3") or (BedType == "reveal3D"):

        # Bed 1
        while (writeBed1[0]) <= (x_16offset):                                # Two while loops, one for x and one for Y.

            if writeHeatBedsActive[0] == 1:                      # sets the scope of values of the writeBed, Breaks loop if writeBed is active
                break

            if writeBed1[0] in range(Min_X,Max_X):               # Checks min/max  x-values in range of the writeBed dimension
                wxCheck[0] = 1                               # ^^ if true, marks the wxCheck as TRUE --> '1'.

            writeBed1[0] += 1
            # print "adding X: " + str(writeBed1[0])

        while (writeBed1[1]) <= (y_16offset):
            if writeHeatBedsActive[0] == 1:
                break

            if(writeBed1[1] in range(Min_Y,Max_Y)):
                wyCheck[0] = 1

            writeBed1[1] += 1

        if((wxCheck[0] == 1) & (wyCheck[0] == 1)):            # if wxCheck and wyCheck are TRUE, the writeBed will activate
            print "writeBed #1 is ON"
            writeHeatBedsActive[0] = 1                           # States the writeBed has been turned on
            FORGOT_BEDS[0] = 1
            print "FORGOT_BEDS[0]: " + str(FORGOT_BEDS[0])


        # Bed 2
        print writeBed2
        print x_16offset*2
        print x_16offset
        print Min_X
        print Max_X
        print Min_Y
        print Max_Y
        print y_16offset
        while ((writeBed2[0]) <= (x_16offset*2)):

            if writeHeatBedsActive[1] == 1:
                print "IT BROKE ON #2 (writebeds.py)"
                break

            if(writeBed2[0] in range(Min_X,Max_X)):
                # print "Its in range x!!!"
                wxCheck[1] = 1

            writeBed2[0] += 1
            # print writeBed2[0]

        while ((writeBed2[1]) <= (y_16offset)):
            if writeHeatBedsActive[1] == 1:
                break

            if(writeBed2[1] in range(Min_Y,Max_Y)):
                #print "Its in range y!!!"
                wyCheck[1] = 1

            writeBed2[1] += 1
            # print writeBed2[1]

        if((wxCheck[1] == 1) & (wyCheck[1] == 1)):
            print "writeBed #2 is ON"
            writeHeatBedsActive[1] = 1
            FORGOT_BEDS[1] = 1
            print "FORGOT_BEDS[1]: " + str(FORGOT_BEDS[1])




        # Bed 3
        while writeBed3[0] <= x_16offset*3:
            if writeHeatBedsActive[2] == 1:
                break

            if(writeBed3[0] in range(Min_X,Max_X)):
                wxCheck[2] = 1

            writeBed3[0] += 1

        while writeBed3[1] <= y_16offset:
            if writeHeatBedsActive[2] == 1:
                break

            if(writeBed3[1] in range(Min_Y,Max_Y)):
                wyCheck[2] = 1

            writeBed3[1] += 1

        if((wxCheck[2] == 1) & (wyCheck[2] == 1)):
            print "writeBed #3 is ON"
            writeHeatBedsActive[2] = 1
            FORGOT_BEDS[2] = 1
            print "FORGOT_BEDS[2]: " + str(FORGOT_BEDS[2])



        # Bed 4
        while writeBed4[0] <= x_16offset*4:
            if writeHeatBedsActive[3] == 1:
                break

            if(writeBed4[0] in range(Min_X,Max_X)):
                wxCheck[3] = 1

            writeBed4[0] += 1

        while writeBed4[1] <= y_16offset:
            if writeHeatBedsActive[3] == 1:
                break

            if(writeBed4[1] in range(Min_Y,Max_Y)):

                wyCheck[3] = 1

            writeBed4[1] += 1

        if((wxCheck[3] == 1) & (wyCheck[3] == 1)):
            print "writeBed #4 is ON"
            writeHeatBedsActive[3] = 1
            FORGOT_BEDS[3] = 1
            print "FORGOT_BEDS[3]: " + str(FORGOT_BEDS[3])


        # Bed 5
        while writeBed5[0] <= x_16offset*4:
            if writeHeatBedsActive[4] == 1:
                break

            if(writeBed5[0] in range(Min_X,Max_X)):
                wxCheck[4] = 1

            writeBed5[0] += 1

        while writeBed5[1] <= y_16offset*2:
            if writeHeatBedsActive[4] == 1:
                break

            if(writeBed5[1] in range(Min_Y,Max_Y)):
                wyCheck[4] = 1

            writeBed5[1] += 1

        if((wxCheck[4] == 1) & (wyCheck[4] == 1)):
            print "writeBed #5 is ON"
            writeHeatBedsActive[4] = 1
            FORGOT_BEDS[4] = 1
            print "FORGOT_BEDS[4]: " + str(FORGOT_BEDS[4])



        # Bed 6
        while writeBed6[0] <= x_16offset*3:
            if writeHeatBedsActive[5] == 1:
                break

            if(writeBed6[0] in range(Min_X,Max_X)):
                wxCheck[5] = 1

            writeBed6[0] += 1

        while writeBed6[1] <= y_16offset*2:
            if writeHeatBedsActive[5] == 1:
                break

            if(writeBed6[1] in range(Min_Y,Max_Y)):
                wyCheck[5] = 1

            writeBed6[1] += 1

        if((wxCheck[5] == 1) & (wyCheck[5] == 1)):
            print "writeBed #6 is ON"
            writeHeatBedsActive[5] = 1
            FORGOT_BEDS[5] = 1
            print "FORGOT_BEDS[5]: " + str(FORGOT_BEDS[5])



        # Bed 7
        while writeBed7[0] <= x_16offset*2:
            if writeHeatBedsActive[6] == 1:
                break

            if(writeBed7[0] in range(Min_X,Max_X)):
                wxCheck[6] = 1

            writeBed7[0] += 1

        while writeBed7[1] <= y_16offset*2:
            if writeHeatBedsActive[6] == 1:
                break

            if(writeBed7[1] in range(Min_Y,Max_Y)):
                wyCheck[6] = 1

            writeBed7[1] += 1

        if((wxCheck[6] == 1) & (wyCheck[6] == 1)):
            print "writeBed #7 is ON"
            writeHeatBedsActive[6] = 1
            FORGOT_BEDS[6] = 1
            print "FORGOT_BEDS[6]: " + str(FORGOT_BEDS[6])


        # Bed 8
        while writeBed8[0] <= x_16offset:
            if writeHeatBedsActive[7] == 1:
                break

            if(writeBed8[0] in range(Min_X,Max_X)):
                wxCheck[7] = 1

            writeBed8[0] += 1

        while writeBed8[1] <= y_16offset*2:
            if writeHeatBedsActive[7] == 1:
                break

            if(writeBed8[1] in range(Min_Y,Max_Y)):
                wyCheck[7] = 1

            writeBed8[1] += 1

        if((wxCheck[7] == 1) & (wyCheck[7] == 1)):
            print "writeBed #8 is ON"
            writeHeatBedsActive[7] = 1
            FORGOT_BEDS[7] = 1
            print "FORGOT_BEDS[7]: " + str(FORGOT_BEDS[7])


        # Bed 9
        while writeBed9[0] <= x_16offset:
            if writeHeatBedsActive[8] == 1:
                break

            if(writeBed9[0] in range(Min_X,Max_X)):
                wxCheck[8] = 1

            writeBed9[0] += 1

        while writeBed9[1] <= y_16offset*3:
            if writeHeatBedsActive[8] == 1:
                break

            if(writeBed9[1] in range(Min_Y,Max_Y)):
                wyCheck[8] = 1

            writeBed9[1] += 1

        if((wxCheck[8] == 1) & (wyCheck[8] == 1)):
            print "writeBed #9 is ON"
            writeHeatBedsActive[8] = 1
            FORGOT_BEDS[8] = 1
            print "FORGOT_BEDS[8]: " + str(FORGOT_BEDS[8])


        # Bed 10
        while writeBed10[0] <= x_16offset*2:
            if writeHeatBedsActive[9] == 1:
                break

            if(writeBed10[0] in range(Min_X,Max_X)):
                wxCheck[9] = 1

            writeBed10[0] += 1

        while writeBed10[1] <= y_16offset*3:

            if writeHeatBedsActive[9] == 1:
                break

            if(writeBed10[1] in range(Min_Y,Max_Y)):
                wyCheck[9] = 1

            writeBed10[1] += 1

        if((wxCheck[9] == 1) & (wyCheck[9] == 1)):
            print "writeBed #10 is ON"
            writeHeatBedsActive[9] = 1
            FORGOT_BEDS[9] = 1
            print "FORGOT_BEDS[9]: " + str(FORGOT_BEDS[9])



        # Bed 11
        while writeBed11[0] <= x_16offset*3:
            if writeHeatBedsActive[10] == 1:
                break

            if(writeBed11[0] in range(Min_X,Max_X)):
                wxCheck[10] = 1

            writeBed11[0] += 1

        while writeBed11[1] <= y_16offset*3:
            if writeHeatBedsActive[10] == 1:
                break

            if(writeBed11[1] in range(Min_Y,Max_Y)):
                wyCheck[10] = 1

            writeBed11[1] += 1

        if((wxCheck[10] == 1) & (wyCheck[10] == 1)):
            print "writeBed #11 is ON"
            writeHeatBedsActive[10] = 1
            FORGOT_BEDS[10] = 1
            print "FORGOT_BEDS[10]: " + str(FORGOT_BEDS[10])


        # Bed 12
        while writeBed12[0] <= x_16offset*4:
            if writeHeatBedsActive[11] == 1:
                break
            if(writeBed12[0] in range(Min_X,Max_X)):
                wxCheck[11] = 1

            writeBed12[0] += 1

        while writeBed12[1] <= y_16offset*3:
            if writeHeatBedsActive[11] == 1:
                break

            if(writeBed12[1] in range(Min_Y,Max_Y)):
                wyCheck[11] = 1

            writeBed12[1] += 1

        if((wxCheck[11] == 1) & (wyCheck[11] == 1)):
            print "writeBed #12 is ON"
            writeHeatBedsActive[11] = 1
            FORGOT_BEDS[11] = 1
            print "FORGOT_BEDS[11]: " + str(FORGOT_BEDS[11])


        # Bed 13
        while writeBed13[0] <= x_16offset*4:
            if writeHeatBedsActive[12] == 1:
                break

            if(writeBed13[0] in range(Min_X,Max_X)):
                wxCheck[12] = 1

            writeBed13[0] += 1

        while writeBed13[1] <= y_16offset*4:
            if writeHeatBedsActive[12] == 1:
                break

            if(writeBed13[1] in range(Min_Y,Max_Y)):
                wyCheck[12] = 1

            writeBed13[1] += 1

        if((wxCheck[12] == 1) & (wyCheck[12] == 1)):
            print "writeBed #13 is ON"
            writeHeatBedsActive[12] = 1
            FORGOT_BEDS[12] = 1
            print "FORGOT_BEDS[12]: " + str(FORGOT_BEDS[12])



        # Bed 14
        while writeBed14[0] <= x_16offset*3:
            if writeHeatBedsActive[13] == 1:
                break

            if(writeBed14[0] in range(Min_X,Max_X)):
                wxCheck[13] = 1

            writeBed14[0] += 1

        while writeBed14[1] <= y_16offset*4:

            if writeHeatBedsActive[13] == 1:
                break

            if(writeBed14[1] in range(Min_Y,Max_Y)):
                wyCheck[13] = 1

            writeBed14[1] += 1

        if((wxCheck[13] == 1) & (wyCheck[13] == 1)):
            print "writeBed #14 is ON"
            writeHeatBedsActive[13] = 1
            FORGOT_BEDS[13] = 1
            print "FORGOT_BEDS[13]: " + str(FORGOT_BEDS[13])


        # Bed 15
        while writeBed15[0] <= x_16offset*2:
            if writeHeatBedsActive[14] == 1:
                break

            if(writeBed15[0] in range(Min_X,Max_X)):
                wxCheck[14] = 1

            writeBed15[0] += 1

        while writeBed15[1] <= y_16offset*4:

            if writeHeatBedsActive[14] == 1:
                break

            if(writeBed15[1] in range(Min_Y,Max_Y)):
                wyCheck[14] = 1

            writeBed15[1] += 1

        if((wxCheck[14] == 1) & (wyCheck[14] == 1)):
            print "writeBed #15 is ON"
            writeHeatBedsActive[14] = 1
            FORGOT_BEDS[14] = 1
            print "FORGOT_BEDS[14]: " + str(FORGOT_BEDS[14])



        # Bed 16
        while writeBed16[0] <= x_16offset:
            if writeHeatBedsActive[15] == 1:
                break

            if(writeBed16[0] in range(Min_X,Max_X)):
                wxCheck[15] = 1

            writeBed16[0] += 1

        while writeBed16[1] <= y_16offset*4:
            if writeHeatBedsActive[15] == 1:
                break

            if(writeBed16[1] in range(Min_Y,Max_Y)):
                wyCheck[15] = 1

            writeBed16[1] += 1

        if((wxCheck[15] == 1) & (wyCheck[15] == 1)):
            print "writeBed #16 is ON"
            writeHeatBedsActive[15] = 1
            FORGOT_BEDS[15] = 1
            print "FORGOT_BEDS[15]: " + str(FORGOT_BEDS[15])



########################################  GT  ############################################################

    if BedType == "GT":
        print "Found GT"
        # Bed 1
        while writeBed1[0] <= x_GToffset:                                # Two while loops, one for x and one for Y.
            if writeHeatBedsActive[0] == 1:                      # sets the scope of values of the writeBed, Breaks loop if writeBed is active
                # print "GT Bed 1 == 1"
                break

            if writeBed1[0] in range(Min_X,Max_X):               # Checks min/max  x-values in range of the writeBed dimension
                wxCheck[0] = 1                               # ^^ if true, marks the wxCheck as TRUE --> '1'.
                # print "Bed 1 X-value is in range of Min,Max X"

            writeBed1[0] += 1

        while writeBed1[1] <= y_GToffset:
            if writeHeatBedsActive[0] == 1:
                #print "GT Bed 1 == 1"
                break

            if(writeBed1[1] in range(Min_Y,Max_Y)):
                #print "Bed1 Y-value is in rage of Min, Max X"
                wyCheck[0] = 1

            writeBed1[1] += 1

        if((wxCheck[0] == 1) & (wyCheck[0] == 1)):            # if wxCheck and wyCheck are TRUE, the writeBed will activate
            print "writeBed #1 is ON"
            writeHeatBedsActive[0] = 1                           # States the writeBed has been turned on
            FORGOT_BEDS[0] = 1
            print "GT FORGOT_BEDS[0]: " + str(FORGOT_BEDS[0])


        # Bed 2
        while writeBed2[0] <= x_GToffset*2:
            if writeHeatBedsActive[1] == 1:
                break

            if(writeBed2[0] in range(Min_X,Max_X)):
                wxCheck[1] = 1

            writeBed2[0] += 1

        while writeBed2[1] <= y_GToffset:
            if writeHeatBedsActive[1] == 1:
                break

            if(writeBed2[1] in range(Min_Y,Max_Y)):
                wyCheck[1] = 1

            writeBed2[1] += 1

        if((wxCheck[1] == 1) & (wyCheck[1] == 1)):
            print "writeBed #2 is ON"
            writeHeatBedsActive[1] = 1
            FORGOT_BEDS[1] = 1
            print "GT FORGOT_BEDS[1]: " + str(FORGOT_BEDS[1])


        # Bed 3
        while writeBed3[0] <= x_GToffset*2:
            if writeHeatBedsActive[2] == 1:
                break

            if(writeBed3[0] in range(Min_X,Max_X)):
                wxCheck[2] = 1

            writeBed3[0] += 1

        while writeBed3[1] <= y_GToffset*2:
            if writeHeatBedsActive[2] == 1:
                break

            if(writeBed3[1] in range(Min_Y,Max_Y)):
                wyCheck[2] = 1

            writeBed3[1] += 1

        if((wxCheck[2] == 1) & (wyCheck[2] == 1)):
            print "writeBed #3 is ON"
            writeHeatBedsActive[2] = 1
            FORGOT_BEDS[2] = 1
            print "GT FORGOT_BEDS[2]: " + str(FORGOT_BEDS[2])


        # Bed 4
        while writeBed4[0] <= x_GToffset:
            if writeHeatBedsActive[3] == 1:
                break

            if(writeBed4[0] in range(Min_X,Max_X)):
                wxCheck[3] = 1

            writeBed4[0] += 1

        while writeBed4[1] <= y_GToffset*2:
            if writeHeatBedsActive[3] == 1:
                break

            if(writeBed4[1] in range(Min_Y,Max_Y)):
                wyCheck[3] = 1

            writeBed4[1] += 1
        if((wxCheck[3] == 1) & (wyCheck[3] == 1)):
            print "writeBed #4 is ON"
            writeHeatBedsActive[3] = 1
            FORGOT_BEDS[3] = 1
            print "GT FORGOT_BEDS[3]: " + str(FORGOT_BEDS[3])


    if DUPE_CHECK > 0:
        dupeBeds.dupWrite(writeHeatBedsActive, BedType, FORGOT_BEDS)
        print"\nwriteBEDS.py recognizes DUPE MODE!"

    print "\nForgot_Beds: " + str(FORGOT_BEDS)
    print "\nwriteBeds.py's Active Beds: " + str(writeHeatBedsActive)
    print "\nBedType: " + str(BedType)
    print "\nBeds to be written with M104 Commands: " + str(FORGOT_BEDS)
    print "\n"
    # print writeHeatBedsActive
    print "\n"

#############################################################################################################################
##########################################################################################################################
