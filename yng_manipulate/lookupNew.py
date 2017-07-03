#tab length = 4 spaces
import os
import sys
import time
import logging



#Change to look for B commands for the Bcommand_lookup function
#Return the following at the end        return (COMMAND, SUB1, VAR1, SUB2, VAR2, SUB3, VAR3)
#on an error return (-1,-1,-1,-1)


##parse looking for Z and the number that follows, kind of like the B command lookup....
##return just the Z number for the main part of the program to look at/print '''

def Z_lookup(line):
#################################
    foundZ = 0
    CC = 0
    foundEND = 0
    foundSUB = 0
    ACTIVEBEDS = 0
    LOOKUP = ['']*250
#################################
    for z in line:
        #print z
        if(foundEND == 0):
            if(z == ';'):
                foundEND = 1
                #print "we found a semi colon at the beginning, throwing it away\n"
                #print line
            else:
                if(foundZ == 1):
                    if((z == ' ') | (z == "\n") | (z == "\r")):
                        CC = 0
                        foundZ = 2
                    else:
                        LOOKUP[CC] = z
                        CC = CC + 1
                if((z == 'Z') & (foundZ == 0)):
                    foundZ = 1

                if((( z == 'Z') | (z == 'z'))):
                    foundZ = 1
    #print "WHAT THE...... " + str(line)
    if foundZ:
        LOOKUP = float(str(''.join(LOOKUP)))
    else:
        LOOKUP = -1.0
    return (LOOKUP)



#############   Bcommand_lookup  ######################################################################################
def Bcommand_lookup(line):
############ Var inits ################
    foundB = 0
    COMMAND = ['']*10
    foundVAR1 = 0
    foundVAR2 = 0
    foundVAR3 = 0
    foundVAR4 = 0
    foundVAR5 = 0
    foundVAR6 = 0
    #foundVAR7 = 0
    VAR1 = ['']*10
    VAR2 = ['']*10
    VAR3 = ['']*10
    VAR4 = ['']*10
    VAR5 = ['']*10
    VAR6 = ['']*10
    #VAR7 = ['']*10
    ACTIVEBEDS = ['']*10
    foundSUB = 0
    SUBARRAY = ['']*10
    foundEND = 0
    CC = 0
    SPCC = 1
    SUB1 = 0
    SUB2 = 0
    SUB3 = 0
    SUB4 = 0
    SUB5 = 0
    SUB6 = 0
    SUBPHRASEARRAY = [0]*10

    #print SUBPHRASEARRAY
    for x in line:
        if(x == ';'):
            foundEND = 1
            #print "we found a semi colon at the beginning, throwing it away\n"
            #print line
        else:
            if(foundB == 1):
                #print "found B"
                if((x == ' ') | (x =="\n") | (x == "\r")):
                    CC = 0
                    foundB = 2
                else:
                    COMMAND[CC] = x
                    CC = CC + 1

            if(foundVAR1 == 1):
                if((x == ' ') | (x =="\n") | (x == "\r")):
                    CC = 0
                    foundVAR1 = 2
                else:
                    VAR1[CC] = x
                    CC = CC + 1

            if(foundVAR2 == 1):
                if((x == ' ') | (x == "\n") | (x == "\r")):
                    CC = 0
                    foundVAR2 = 2
                else:
                    VAR2[CC] = x
                    CC = CC + 1

            if(foundVAR3 == 1):
                if((x == ' ') | (x == "\n") | (x == "\r")):
                    CC = 0
                    foundVAR3 = 2
                else:
                    VAR3[CC] = x
                    CC = CC + 1

            if(foundVAR4 == 1):
                if((x == ' ') | (x == "\n") | (x == "\r")):
                    CC = 0
                    foundVAR4 = 2
                else:
                    VAR4[CC] = x
                    CC = CC + 1

            if(foundVAR5 == 1):
                if((x == ' ') | (x == "\n") | (x == "\r")):
                    CC = 0
                    foundVAR5 = 2
                else:
                    VAR5[CC] = x
                    CC = CC + 1

            if(foundVAR6 == 1):
                if((x == ' ') | (x == "\n") | (x == "\r")):
                    CC = 0
                    foundVAR6 = 2
                else:
                    VAR6[CC] = x
                    CC = CC + 1

            #if(foundVAR7 == 1):
                #if((x == ' ') | (x == "\n") | (x == "\r")):
                    #CC = 0
                    #foundVAR7 = 2
                #else:
                    #VAR7[CC] = x
                    #CC = CC + 1

            if x in('P','S','E','T','A','H'):
                SUBARRAY[SPCC] = x
                SPCC = SPCC + 1
                if((SPCC == 2) & (foundVAR1 == 0)):
                    foundVAR1 = 1
                if((SPCC == 3) & (foundVAR2 == 0)):
                    foundVAR2 = 1
                if((SPCC == 4) & (foundVAR3 == 0)):
                    foundVAR3 = 1
                if((SPCC == 5) & (foundVAR4 == 0)):
                    foundVAR4 = 1
                if((SPCC == 6) & (foundVAR5 == 0)):
                    foundVAR5 = 1
                if((SPCC == 7) & (foundVAR6 == 0)):
                    foundVAR6 = 1
                #if((SPCC == 8) & (foundVAR7 == 0)):
                    #foundVAR7 = 1

            if((x == 'B') & (foundB == 0)):
                foundB = 1

            if((x == 'P') & (SUB1 == 0)):
                foundVAR1 = 1
                SUB1 = x
                #print SUB1
            if((x == 'S') & (SUB2 == 0)):
                foundVAR2 = 1
                SUB2 = x
                #print SUB2
            if((x == 'E') & (SUB3 == 0)):
                foundVAR3 = 1
                SUB3 = x
                #print SUB3
            #if((x == 'T') & (SUB4 == 0)):
                #foundVAR4 = 1
                #SUB4 = x
                #print SUB4
            #if((x == 'A') & (SUB5 == 0)):
                #foundVAR5 = 1
                #SUB5 = x
                #print SUB5
            #if((x == 'H') & (SUB6 == 0)):
                #foundVAR6 = 1
                #SUB6 = x
                #print SUB6
            #if((x == '') & (SUB7 == 0)):
                #foundVAR7 = 1
                #SUB7 = x
                #print SUB7



    #ACTIVEBEDS = int(str(''.join(ACTIVEBEDS))
    #VARS1 = str(''.join(VAR1))
    #VARS2 = str(''.join(VAR2))
    #VARS3 = str(''.join(VAR3))

    #BEDSUBARRAY[0] = SPCC - 1
    #BEDSUBARRAY = int(VAR1), int(VAR2), int(VAR3)
    #return(ACTIVEBEDS, BEDSUBARRAY, SUBPHRASEARRAY)

    #print line
    #print COMMAND
    COMMAND = int(str(''.join(COMMAND)))

    if(VAR1[0] == ''):
        #print "null var 1"
        VAR1[0] = '0'
    if(VAR2[0] == ''):
        #print "null var 2"
        VAR2[0] = '0'
    if(VAR3[0] == ''):
        #print "null var 3"
        VAR3[0] = '0'
    VAR1 = str(''.join(VAR1))
    VAR2 = str(''.join(VAR2))
    VAR3 = str(''.join(VAR3))
    #VAR4 = str(''.join(VAR4))
    #VAR5 = str(''.join(VAR5))
    #VAR6 = str(''.join(VAR6))
    #VAR7 = str(''.join(VAR7))
    #return(COMMAND, SUB1, VAR1, SUB2, VAR2, SUB3, VAR3)
    #print COMMAND
    #print VAR1
    #print VAR2
    #print VAR3
    #print "test"
    #print COMMAND
    SUBARRAY[0] = SPCC - 1

    SUBPHRASEARRAY = int(VAR1), int(VAR2), int(VAR3)#, int(VAR4), int(VAR5), int(VAR6)

    return(COMMAND, SUBARRAY, SUBPHRASEARRAY)
