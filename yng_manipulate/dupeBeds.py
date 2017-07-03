# indents are 4 SPACES
import os
import sys
import logging




def dupBed(heatBedsActive, BedType, FORGOT_BEDS=[0]*16, *args):

        print heatBedsActive
        print BedType
        print FORGOT_BEDS
        print "dup write"
        if((BedType == "FRANK3") or (BedType =="reveal3D")):
            if(heatBedsActive[0] == 1):
                FORGOT_BEDS[2] = 2
                print FORGOT_BEDS[2]
                print "Zone 1 Duplicating in Zone 3"

            if(heatBedsActive[1] == 1):
                FORGOT_BEDS[3] = 2
                print "Zone 2 Duplicating in Zone 4"

            if(heatBedsActive[7] == 1):
                FORGOT_BEDS[5] = 2
                print "Zone 8 Duplicating in Zone 6"

            if(heatBedsActive[6] == 1):
                FORGOT_BEDS[4] = 2
                print "Zone 7 Duplicating in Zone 5"

            if(heatBedsActive[8] == 1):
                FORGOT_BEDS[10] = 2
                print "Zone 9 Duplicating in Zone 11"

            if(heatBedsActive[9] == 1):
                FORGOT_BEDS[11] = 2
                print "Zone 10 Duplicating in Zone 12"

            if(heatBedsActive[15] == 1):
                FORGOT_BEDS[13] = 2
                print "Zone 16 Duplicating in Zone 14"

            if(heatBedsActive[14] == 1):
                FORGOT_BEDS[12] = 2
                print "Zone 15 Duplicating in Zone 13"






        if(BedType == "GT"):
            if(writeHeatBedsActive[0] == 1):
                FORGOT_BEDS[1] = 2
                print "GT Zone 1 Duplicating in Zone 2"

            if(writeHeatBedsActive[3] == 1):
                FORGOT_BEDS[2] = 2
                print "GT Zone 4 Duplicating in Zone 3"



        print "\nSTART (dupeBeds.py)"
        print heatBedsActive
        print BedType
        print FORGOT_BEDS
        print "END of dup write"

def dupWrite(writeHeatBedsActive, BedType, FORGOT_BEDS=[0]*16, *args):

        print writeHeatBedsActive
        print BedType
        print FORGOT_BEDS
        print "dup write"
        if((BedType == "FRANK3") or (BedType =="reveal3D")):
            if(writeHeatBedsActive[0] == 1):
                FORGOT_BEDS[2] = 2
                print FORGOT_BEDS[2]
                print "Zone 1 Duplicating in Zone 3"

            if(writeHeatBedsActive[1] == 1):
                FORGOT_BEDS[3] = 2
                print "Zone 2 Duplicating in Zone 4"

            if(writeHeatBedsActive[7] == 1):
                FORGOT_BEDS[5] = 2
                print "Zone 8 Duplicating in Zone 6"

            if(writeHeatBedsActive[6] == 1):
                FORGOT_BEDS[4] = 2
                print "Zone 7 Duplicating in Zone 5"

            if(writeHeatBedsActive[8] == 1):
                FORGOT_BEDS[10] = 2
                print "Zone 9 Duplicating in Zone 11"

            if(writeHeatBedsActive[9] == 1):
                FORGOT_BEDS[11] = 2
                print "Zone 10 Duplicating in Zone 12"

            if(writeHeatBedsActive[15] == 1):
                FORGOT_BEDS[13] = 2
                print "Zone 16 Duplicating in Zone 14"

            if(writeHeatBedsActive[14] == 1):
                FORGOT_BEDS[12] = 2
                print "Zone 15 Duplicating in Zone 13"






        if(BedType == "GT"):
            if(writeHeatBedsActive[0] == 1):
                FORGOT_BEDS[1] = 2
                print "GT Zone 1 Duplicating in Zone 2"

            if(writeHeatBedsActive[3] == 1):
                FORGOT_BEDS[2] = 2
                print "GT Zone 4 Duplicating in Zone 3"



        print "\nSTART (dupeBeds.py)"
        print writeHeatBedsActive
        print BedType
        print FORGOT_BEDS
        print "END of dup write"
