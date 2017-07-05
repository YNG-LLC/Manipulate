# indents are 4 SPACES
import os
import sys
import finalFunction
import dupeBeds
import gInject
import logging


#### Checks Which beds to turn ON/OFF and writes them to the manipulated gcode
def activateBeds(Zone_Max_X, Zone_Min_X, Zone_Max_Y, Zone_Min_Y, newFile, newFileLocation,FinalFileLocation, BedTemp, BedType, NumberXBeds, NumberYBeds, MAX_X, MAX_Y, x_16offset, x_GToffset, y_16offset, y_GToffset, TOOL_BED1, TOOL_BED2, TOOL_BED3, TOOL_BED4, DUPE_CHECK,  TOOL_LAYER1, TOOL_LAYER2, TOOL_LAYER3, TOOL_LAYER4, TOOL_SECLAYER1, TOOL_SECLAYER2, TOOL_SECLAYER3, TOOL_SECLAYER4, M104_TOOL=[0]*4, M109_TOOL=[0]*4, FORGOT_BEDS=[0]*16, *args):


	zoneValues = [int(Zone_Max_X),int(Zone_Min_X),int(Zone_Max_Y),int(Zone_Min_Y)]

	cloneFile = open(FinalFileLocation, 'w')  


	Max_X = zoneValues[0]                                    # this is a local VAR for bedControl.py . not to be confused with the MAX_X & MAX_Y
	Min_X = zoneValues[1]
	Max_Y = zoneValues[2]
	Min_Y = zoneValues[3]

	zoneActivatedREVEAL3D = [0]*16
	zoneActivatedGT = [0]*4
	waitTime = " W10\n"

	# print "M109 @ Variables init. : " + str(M109_TOOL)
	# print "M104 @ Variables init. : " + str(M104_TOOL)
	# print "Memory Address of M104 in bedControl:" + str(id(M104_TOOL))
	# print "Memory Address of M109 in bedControl:" + str(id(M109_TOOL))
	print "This is DUPE Check: " + str(DUPE_CHECK)

	if ((BedType == "reveal3D") or (BedType == "FRANK3") and  (DUPE_CHECK == 0)):
		print 'ToolBed1: '+str(TOOL_BED1);
		zoneON1 = "B16 P0 " + "S" + str(TOOL_BED1) + " E1\n"
		zoneON2 = "B16 P1 " + "S" + str(TOOL_BED1) + " E1\n"
		zoneON3 = "B16 P2 " + "S" + str(TOOL_BED1) + " E1\n"
		zoneON4 = "B16 P3 " + "S" + str(TOOL_BED1) + " E1\n"
		zoneON5 = "B16 P4 " + "S" + str(TOOL_BED1) + " E1\n"
		zoneON6 = "B16 P5 " + "S" + str(TOOL_BED1) + " E1\n"
		zoneON7 = "B16 P6 " + "S" + str(TOOL_BED1) + " E1\n"
		zoneON8 = "B16 P7 " + "S" + str(TOOL_BED1) + " E1\n"
		zoneON9 = "B16 P8 " + "S" + str(TOOL_BED1) + " E1\n"
		zoneON10 = "B16 P9 " + "S" + str(TOOL_BED1) + " E1\n"
		zoneON11 = "B16 P10 " + "S" + str(TOOL_BED1) + " E1\n"
		zoneON12 = "B16 P11 " + "S" + str(TOOL_BED1) + " E1\n"
		zoneON13 = "B16 P12 " + "S" + str(TOOL_BED1) + " E1\n"
		zoneON14 = "B16 P13 " + "S" + str(TOOL_BED1) + " E1\n"
		zoneON15 = "B16 P14 " + "S" + str(TOOL_BED1) + " E1\n"
		zoneON16 = "B16 P15 " + "S" + str(TOOL_BED1) + " E1\n"

	elif ((BedType == "reveal3D") or (BedType == "FRANK3") and (DUPE_CHECK > 0)):
		zoneON1 = "B16 P0 " + "S" + str(TOOL_BED1) + " E1\n"
		zoneON2 = "B16 P1 " + "S" + str(TOOL_BED1) + " E1\n"
		zoneON3 = "B16 P2 " + "S" + str(TOOL_BED2) + " E1\n"
		zoneON4 = "B16 P3 " + "S" + str(TOOL_BED2) + " E1\n"
		zoneON5 = "B16 P4 " + "S" + str(TOOL_BED2) + " E1\n"
		zoneON6 = "B16 P5 " + "S" + str(TOOL_BED2) + " E1\n"
		zoneON7 = "B16 P6 " + "S" + str(TOOL_BED1) + " E1\n"
		zoneON8 = "B16 P7 " + "S" + str(TOOL_BED1) + " E1\n"
		zoneON9 = "B16 P8 " + "S" + str(TOOL_BED1) + " E1\n"
		zoneON10 = "B16 P9 " + "S" + str(TOOL_BED1) + " E1\n"
		zoneON11 = "B16 P10 " + "S" + str(TOOL_BED2) + " E1\n"
		zoneON12 = "B16 P11 " + "S" + str(TOOL_BED2) + " E1\n"
		zoneON13 = "B16 P12 " + "S" + str(TOOL_BED2) + " E1\n"
		zoneON14 = "B16 P13 " + "S" + str(TOOL_BED2) + " E1\n"
		zoneON15 = "B16 P14 " + "S" + str(TOOL_BED1) + " E1\n"
		zoneON16 = "B16 P15 " + "S" + str(TOOL_BED1) + " E1\n"


	if ((BedType == "GT") and  (DUPE_CHECK == 0)):
		zoneON1 = "B16 P0 " + "S" + str(TOOL_BED1) + " E1\n"
		zoneON2 = "B16 P1 " + "S" + str(TOOL_BED1) + " E1\n"
		zoneON3 = "B16 P6 " + "S" + str(TOOL_BED1) + " E1\n"
		zoneON4 = "B16 P7 " + "S" + str(TOOL_BED1) + " E1\n"
		zoneOFF1 = "B16 P0 " + "S" + str(BedTemp) + " E0\n"
		zoneOFF2 = "B16 P1 " + "S" + str(BedTemp) + " E0\n"
		zoneOFF3 = "B16 P6 " + "S" + str(BedTemp) + " E0\n"
		zoneOFF4 = "B16 P7 " + "S" + str(BedTemp) + " E0\n"


	elif ((BedType == "GT") and (DUPE_CHECK > 0)):
		zoneON1 = "B16 P0 " + "S" + str(TOOL_BED1) + " E1\n"
		zoneON2 = "B16 P1 " + "S" + str(TOOL_BED2) + " E1\n"
		zoneON3 = "B16 P6 " + "S" + str(TOOL_BED1) + " E1\n"
		zoneON4 = "B16 P7 " + "S" + str(TOOL_BED2) + " E1\n"
		zoneOFF1 = "B16 P0 " + "S" + str(BedTemp) + " E0\n"
		zoneOFF2 = "B16 P1 " + "S" + str(BedTemp) + " E0\n"
		zoneOFF3 = "B16 P6 " + "S" + str(BedTemp) + " E0\n"
		zoneOFF4 = "B16 P7 " + "S" + str(BedTemp) + " E0\n"



	if ((BedType == "reveal3D") or (BedType == "FRANK3")):
		zoneOFF1 = "B16 P0 " + "S" + str(BedTemp) + " E0\n"
		zoneOFF2 = "B16 P1 " + "S" + str(BedTemp) + " E0\n"
		zoneOFF3 = "B16 P2 " + "S" + str(BedTemp) + " E0\n"
		zoneOFF4 = "B16 P3 " + "S" + str(BedTemp) + " E0\n"
		zoneOFF5 = "B16 P4 " + "S" + str(BedTemp) + " E0\n"
		zoneOFF6 = "B16 P5 " + "S" + str(BedTemp) + " E0\n"
		zoneOFF7 = "B16 P6 " + "S" + str(BedTemp) + " E0\n"
		zoneOFF8 = "B16 P7 " + "S" + str(BedTemp) + " E0\n"
		zoneOFF9 = "B16 P8 " + "S" + str(BedTemp) + " E0\n"
		zoneOFF10 = "B16 P9 " + "S" + str(BedTemp) + " E0\n"
		zoneOFF11 = "B16 P10 " + "S" + str(BedTemp) + " E0\n"
		zoneOFF12 = "B16 P11 " + "S" + str(BedTemp) + " E0\n"
		zoneOFF13 = "B16 P12 " + "S" + str(BedTemp) + " E0\n"
		zoneOFF14 = "B16 P13 " + "S" + str(BedTemp) + " E0\n"
		zoneOFF15 = "B16 P14 " + "S" + str(BedTemp) + " E0\n"
		zoneOFF16 = "B16 P15 " + "S" + str(BedTemp) + " E0\n"


# Dimensions set according to BedType

	if BedType == 'GT':
		heatBedsActive = [0]*4
		xCheck = [0]*4
		yCheck = [0]*4


		if DUPE_CHECK > 0:
			MX1 = 0
			MX2 = (MAX_X)*1
			MX3 = (MAX_X)*2
			MX4 = (MAX_X)*3

		else:
			MX1 = 0
			MX2 = (MAX_X/NumberXBeds)*1
			MX3 = (MAX_X/NumberXBeds)*2
			MX4 = (MAX_X/NumberXBeds)*3

	   
		MY1 = 0
		MY2 = (MAX_Y/NumberYBeds)*1
		MY3 = (MAX_Y/NumberYBeds)*2
		MY4 = (MAX_Y/NumberYBeds)*3

		bed1 = [MX1, MY1]
		bed2 = [MX2, MY1]
		bed3 = [MX2, MY2]
		bed4 = [MX1, MY2]



	if BedType == 'FRANK3':
		heatBedsActive = [0]*16
		xCheck = [0]*16
		yCheck = [0]*16

		if DUPE_CHECK > 0:
			MX1 = 0
			MX2 = (MAX_X/2)*1
			MX3 = (MAX_X/2)*2
			MX4 = (MAX_X/2)*3
			# print MX2
			# print MX3
			# print MX4
		else:
			MX1 = 0
			MX2 = (MAX_X/NumberXBeds)*1
			MX3 = (MAX_X/NumberXBeds)*2
			MX4 = (MAX_X/NumberXBeds)*3
			# print MX2
			# print MX3
			# print MX4

		MY1 = 0
		MY2 = (MAX_Y/NumberYBeds)*1
		MY3 = (MAX_Y/NumberYBeds)*2
		MY4 = (MAX_Y/NumberYBeds)*3
		# print MY2
		# print MY3
		# print MY4

		bed1 = [MX1, MY1]
		bed2 = [MX2, MY1]
		bed3 = [MX3, MY1]
		bed4 = [MX4, MY1]
		bed5 = [MX4, MY2]
		bed6 = [MX3, MY2]
		bed7 = [MX2, MY2]
		bed8 = [MX1, MY2]
		bed9 = [MX1, MY3]
		bed10 = [MX2, MY3]
		bed11 = [MX3, MY3]
		bed12 = [MX4, MY3]
		bed13 = [MX4, MY4]
		bed14 = [MX3, MY4]
		bed15 = [MX2, MY4]
		bed16 = [MX1, MY4]



	if BedType == 'reveal3D':

		heatBedsActive = [0]*16
		xCheck = [0]*16
		yCheck = [0]*16

		if DUPE_CHECK > 0:
			MX1 = 0
			MX2 = (MAX_X/2)*1
			MX3 = (MAX_X/2)*2
			MX4 = (MAX_X/2)*3
		#     print MX2
		#     print MX3
		#     print MX4
		else:
			MX1 = 0
			MX2 = (MAX_X/NumberXBeds)*1
			MX3 = (MAX_X/NumberXBeds)*2
			MX4 = (MAX_X/NumberXBeds)*3
			# print MX2
			# print MX3
			# print MX4

		MY1 = 0
		MY2 = (MAX_Y/NumberYBeds)*1
		MY3 = (MAX_Y/NumberYBeds)*2
		MY4 = (MAX_Y/NumberYBeds)*3
		# print MY2
		# print MY3
		# print MY4

		bed1 = [MX1, MY1]
		bed2 = [MX2, MY1]
		bed3 = [MX3, MY1]
		bed4 = [MX4, MY1]
		bed5 = [MX4, MY2]
		bed6 = [MX3, MY2]
		bed7 = [MX2, MY2]
		bed8 = [MX1, MY2]
		bed9 = [MX1, MY3]
		bed10 = [MX2, MY3]
		bed11 = [MX3, MY3]
		bed12 = [MX4, MY3]
		bed13 = [MX4, MY4]
		bed14 = [MX3, MY4]
		bed15 = [MX2, MY4]
		bed16 = [MX1, MY4]



############################# Turns Beds ON  ###########################################
### List order: [Max_X, Min_X, Max_Y, Min_Y]

	if (BedType == "FRANK3") or (BedType == "reveal3D"):
	# Bed 1
		while bed1[0] <= x_16offset:                                # Two while loops, one for x and one for Y.
			if heatBedsActive[0] == 1:                        # sets the scope of values of the bed, Breaks loop if bed is active
				break

			if bed1[0] in range(Min_X,Max_X):                # Checks min/max  x-values in range of the bed dimension
				xCheck[0] = 1                                # ^^ if true, marks the xCheck as TRUE --> '1'.

			bed1[0] += 1

		while bed1[1] <= y_16offset:
			if heatBedsActive[0] == 1:
				break

			if(bed1[1] in range(Min_Y,Max_Y)):
				yCheck[0] = 1

			bed1[1] += 1

		if((xCheck[0] == 1) & (yCheck[0] == 1)):            # if xCheck and yCheck are TRUE, the bed will activate
			print "bed #1 is ON"
			cloneFile.write(zoneON1)                        # writes to manipulate output
			heatBedsActive[0] = 1                            # States the bed has been turned on
			zoneActivatedREVEAL3D[0] = 1
			
			if DUPE_CHECK > 0:
				cloneFile.write(zoneON3)
				heatBedsActive[2] = 2
				zoneActivatedREVEAL3D[2] = 3



	# Bed 2
		print "here's two..."
		print bed2[0]
		print x_16offset
		while (bed2[0]) <= (x_16offset*2):
			# print "looking at 2"
			if heatBedsActive[1] == 1:
				break

			if(bed2[0] in range(Min_X,Max_X)):
				xCheck[1] = 1
				# print "checked off 2!"
			bed2[0] += 1

		while (bed2[1]) <= (y_16offset):
			if heatBedsActive[1] == 1:
				break

			if(bed2[1] in range(Min_Y,Max_Y)):
				yCheck[1] = 1

			bed2[1] += 1

		if((xCheck[1] == 1) & (yCheck[1] == 1)):
			print "bed #2 is ON"
			cloneFile.write(zoneON2)
			heatBedsActive[1] = 1
			zoneActivatedREVEAL3D[1] = 2
			
			if DUPE_CHECK > 0:
				cloneFile.write(zoneON4)
				heatBedsActive[3] = 2  #was heatBedsActive[] = 2
				zoneActivatedREVEAL3D[3] = 4 



	# Bed 3
		while bed3[0] <= x_16offset*3:
			if heatBedsActive[2] == 1:
				break

			if(bed3[0] in range(Min_X,Max_X)):
				xCheck[2] = 1

			bed3[0] += 1

		while bed3[1] <= y_16offset:
			if heatBedsActive[2] == 1:
				break

			if(bed3[1] in range(Min_Y,Max_Y)):
				yCheck[2] = 1

			bed3[1] += 1

		if((xCheck[2] == 1) & (yCheck[2] == 1)):
			print "bed #3 is ON"
			cloneFile.write(zoneON3)
			heatBedsActive[2] = 1
			zoneActivatedREVEAL3D[2] = 3


	# Bed 4
		while bed4[0] <= x_16offset*4:
			if heatBedsActive[3] == 1:
				break

			if(bed4[0] in range(Min_X,Max_X)):
				xCheck[3] = 1

			bed4[0] += 1

		while bed4[1] <= y_16offset:
			if heatBedsActive[3] == 1:
				break

			if(bed4[1] in range(Min_Y,Max_Y)):

				yCheck[3] = 1

			bed4[1] += 1

		if((xCheck[3] == 1) & (yCheck[3] == 1)):
			print "bed #4 is ON"
			cloneFile.write(zoneON4)
			heatBedsActive[3] = 1
			zoneActivatedREVEAL3D[3] = 4


	# Bed 5
		while bed5[0] <= x_16offset*4:
			if heatBedsActive[4] == 1:
				break

			if(bed5[0] in range(Min_X,Max_X)):
				xCheck[4] = 1

			bed5[0] += 1

		while bed5[1] <= y_16offset*2:
			if heatBedsActive[4] == 1:
				break

			if(bed5[1] in range(Min_Y,Max_Y)):
				yCheck[4] = 1

			bed5[1] += 1

		if((xCheck[4] == 1) & (yCheck[4] == 1)):
			print "bed #5 is ON"
			cloneFile.write(zoneON5)
			heatBedsActive[4] = 1
			zoneActivatedREVEAL3D[4] = 5


	# Bed 6
		while bed6[0] <= x_16offset*3:
			if heatBedsActive[5] == 1:
				break

			if(bed6[0] in range(Min_X,Max_X)):
				xCheck[5] = 1

			bed6[0] += 1

		while bed6[1] <= y_16offset*2:
			if heatBedsActive[5] == 1:
				break

			if(bed6[1] in range(Min_Y,Max_Y)):
				yCheck[5] = 1

			bed6[1] += 1

		if((xCheck[5] == 1) & (yCheck[5] == 1)):
			print "bed #6 is ON"
			print 'PRINTS ZONE 6:  '+zoneON6
			cloneFile.write(zoneON6)
			heatBedsActive[5] = 1
			zoneActivatedREVEAL3D[5] = 6


	# Bed 7
		while bed7[0] <= x_16offset*2:
			if heatBedsActive[6] == 1:
				break

			if(bed7[0] in range(Min_X,Max_X)):
				xCheck[6] = 1

			bed7[0] += 1

		while bed7[1] <= y_16offset*2:
			if heatBedsActive[6] == 1:
				break

			if(bed7[1] in range(Min_Y,Max_Y)):
				yCheck[6] = 1

			bed7[1] += 1

		if((xCheck[6] == 1) & (yCheck[6] == 1)):
			print "bed #7 is ON"
			cloneFile.write(zoneON7)
			heatBedsActive[6] = 1
			zoneActivatedREVEAL3D[6] = 7
			if DUPE_CHECK > 0:
				cloneFile.write(zoneON5)
				heatBedsActive[4] = 2
				zoneActivatedREVEAL3D[4] = 5

	# Bed 8
		while bed8[0] <= x_16offset:
			if heatBedsActive[7] == 1:
				break

			if(bed8[0] in range(Min_X,Max_X)):
				xCheck[7] = 1

			bed8[0] += 1

		while bed8[1] <= y_16offset*2:
			if heatBedsActive[7] == 1:
				break

			if(bed8[1] in range(Min_Y,Max_Y)):
				yCheck[7] = 1

			bed8[1] += 1

		if((xCheck[7] == 1) & (yCheck[7] == 1)):
			print "bed #8 is ON"
			cloneFile.write(zoneON8)
			heatBedsActive[7] = 1
			zoneActivatedREVEAL3D[7] = 8
			if DUPE_CHECK > 0:
				cloneFile.write(zoneON6)
				heatBedsActive[5] = 2
				zoneActivatedREVEAL3D[5] = 6


	# Bed 9
		while bed9[0] <= x_16offset:
			if heatBedsActive[8] == 1:
				break

			if(bed9[0] in range(Min_X,Max_X)):
				xCheck[8] = 1

			bed9[0] += 1

		while bed9[1] <= y_16offset*3:
			if heatBedsActive[8] == 1:
				break

			if(bed9[1] in range(Min_Y,Max_Y)):
				yCheck[8] = 1

			bed9[1] += 1

		if((xCheck[8] == 1) & (yCheck[8] == 1)):
			print "bed #9 is ON"
			cloneFile.write(zoneON9)
			heatBedsActive[8] = 1
			zoneActivatedREVEAL3D[8] = 9
			if DUPE_CHECK > 0:
				cloneFile.write(zoneON11)
				heatBedsActive[10] = 2
				zoneActivatedREVEAL3D[10] = 11

	# Bed 10
		while bed10[0] <= x_16offset*2:
			if heatBedsActive[9] == 1:
				break

			if(bed10[0] in range(Min_X,Max_X)):
				xCheck[9] = 1

			bed10[0] += 1

		while bed10[1] <= y_16offset*3:

			if heatBedsActive[9] == 1:
				break

			if(bed10[1] in range(Min_Y,Max_Y)):
				yCheck[9] = 1

			bed10[1] += 1

		if((xCheck[9] == 1) & (yCheck[9] == 1)):
			print "bed #10 is ON"
			cloneFile.write(zoneON10)
			heatBedsActive[9] = 1
			zoneActivatedREVEAL3D[9] = 10
			if DUPE_CHECK > 0:
				cloneFile.write(zoneON12)
				heatBedsActive[11] = 2
				zoneActivatedREVEAL3D[11] = 12

	# Bed 11
		while bed11[0] <= x_16offset*3:
			if heatBedsActive[10] == 1:
				break

			if(bed11[0] in range(Min_X,Max_X)):
				xCheck[10] = 1

			bed11[0] += 1

		while bed11[1] <= y_16offset*3:
			if heatBedsActive[10] == 1:
				break

			if(bed11[1] in range(Min_Y,Max_Y)):
				yCheck[10] = 1

			bed11[1] += 1

		if((xCheck[10] == 1) & (yCheck[10] == 1)):
			print "bed #11 is ON"
			cloneFile.write(zoneON11)
			heatBedsActive[10] = 1
			zoneActivatedREVEAL3D[10] = 11



	# Bed 12
		while bed12[0] <= x_16offset*4:
			if heatBedsActive[11] == 1:
				break
			if(bed12[0] in range(Min_X,Max_X)):
				xCheck[11] = 1

			bed12[0] += 1

		while bed12[1] <= y_16offset*3:
			if heatBedsActive[11] == 1:
				break

			if(bed12[1] in range(Min_Y,Max_Y)):
				yCheck[11] = 1

			bed12[1] += 1

		if((xCheck[11] == 1) & (yCheck[11] == 1)):
			print "bed #12 is ON"
			cloneFile.write(zoneON12)
			heatBedsActive[11] = 1
			zoneActivatedREVEAL3D[11] = 12


	# Bed 13
		while bed13[0] <= x_16offset*4:
			if heatBedsActive[12] == 1:
				break

			if(bed13[0] in range(Min_X,Max_X)):
				xCheck[12] = 1

			bed13[0] += 1

		while bed13[1] <= y_16offset*4:
			if heatBedsActive[12] == 1:
				break

			if(bed13[1] in range(Min_Y,Max_Y)):
				yCheck[12] = 1

			bed13[1] += 1

		if((xCheck[12] == 1) & (yCheck[12] == 1)):
			print "bed #13 is ON"
			cloneFile.write(zoneON13)
			heatBedsActive[12] = 1
			zoneActivatedREVEAL3D[12] = 13


	# Bed 14
		while bed14[0] <= x_16offset*3:
			if heatBedsActive[13] == 1:
				break

			if(bed14[0] in range(Min_X,Max_X)):
				xCheck[13] = 1

			bed14[0] += 1

		while bed14[1] <= y_16offset*4:

			if heatBedsActive[13] == 1:
				break

			if(bed14[1] in range(Min_Y,Max_Y)):
				yCheck[13] = 1

			bed14[1] += 1

		if((xCheck[13] == 1) & (yCheck[13] == 1)):
			print "bed #14 is ON"
			cloneFile.write(zoneON14)
			heatBedsActive[13] = 1
			zoneActivatedREVEAL3D[13] = 14


	# Bed 15
		while bed15[0] <= x_16offset*2:
			if heatBedsActive[14] == 1:
				break

			if(bed15[0] in range(Min_X,Max_X)):
				xCheck[14] = 1

			bed15[0] += 1

		while bed15[1] <= y_16offset*4:

			if heatBedsActive[14] == 1:
				break

			if(bed15[1] in range(Min_Y,Max_Y)):
				yCheck[14] = 1

			bed15[1] += 1

		if((xCheck[14] == 1) & (yCheck[14] == 1)):
			print "bed #15 is ON"
			cloneFile.write(zoneON15)
			heatBedsActive[14] = 1
			zoneActivatedREVEAL3D[14] = 15
			if DUPE_CHECK > 0:
				cloneFile.write(zoneON13)
				heatBedsActive[14] = 2
				zoneActivatedREVEAL3D[12] = 13



	# Bed 16
		while bed16[0] <= x_16offset:
			if heatBedsActive[15] == 1:
				break

			if(bed16[0] in range(Min_X,Max_X)):
				xCheck[15] = 1

			bed16[0] += 1

		while bed16[1] <= y_16offset*4:
			if heatBedsActive[15] == 1:
				break

			if(bed16[1] in range(Min_Y,Max_Y)):
				yCheck[15] = 1

			bed16[1] += 1

		if((xCheck[15] == 1) & (yCheck[15] == 1)):
			print "bed #16 is ON"
			cloneFile.write(zoneON16)
			heatBedsActive[15] = 1
			zoneActivatedREVEAL3D[15] = 16
			if DUPE_CHECK > 0:
				cloneFile.write(zoneON14)
				heatBedsActive[15] = 2
				zoneActivatedREVEAL3D[13] = 14


		# ###  Add WaitTime to beds #### #

		if zoneActivatedREVEAL3D[0] == 1:
			cloneFile.write("B16 P0 " + "S" + str(TOOL_BED1)+waitTime)
		if zoneActivatedREVEAL3D[1] == 2:
			cloneFile.write("B16 P1 " + "S" + str(TOOL_BED2)+waitTime)
		if zoneActivatedREVEAL3D[2] == 3:
			cloneFile.write("B16 P2 " + "S" + str(TOOL_BED3)+waitTime)
		if zoneActivatedREVEAL3D[3] == 4:
			cloneFile.write("B16 P3 " + "S" + str(TOOL_BED4)+waitTime)
		if zoneActivatedREVEAL3D[4] == 5:
			cloneFile.write("B16 P4 " + "S" + str(TOOL_BED5)+waitTime)
		if zoneActivatedREVEAL3D[5] == 6:
			cloneFile.write("B16 P5 " + "S" + str(TOOL_BED6)+waitTime)
		if zoneActivatedREVEAL3D[6] == 7:
			cloneFile.write("B16 P6 " + "S" + str(TOOL_BED7)+waitTime)
		if zoneActivatedREVEAL3D[7] == 8:
			cloneFile.write("B16 P7 " + "S" + str(TOOL_BED8)+waitTime)
		if zoneActivatedREVEAL3D[8] == 9:
			cloneFile.write("B16 P8 " + "S" + str(TOOL_BED9)+waitTime)
		if zoneActivatedREVEAL3D[9] == 10:
			cloneFile.write("B16 P9 " + "S" + str(TOOL_BED10)+waitTime)
		if zoneActivatedREVEAL3D[10] == 11:
			cloneFile.write("B16 P10 " + "S" + str(TOOL_BED11)+waitTime)
		if zoneActivatedREVEAL3D[11] == 12:
			cloneFile.write("B16 P11 " + "S" + str(TOOL_BED12)+waitTime)
		if zoneActivatedREVEAL3D[12] == 13:
			cloneFile.write("B16 P12 " + "S" + str(TOOL_BED13)+waitTime)
		if zoneActivatedREVEAL3D[13] == 14:
			cloneFile.write("B16 P13 " + "S" + str(TOOL_BED14)+waitTime)
		if zoneActivatedREVEAL3D[14] == 15:
			cloneFile.write("B16 P14 " + "S" + str(TOOL_BED15)+waitTime)
		if zoneActivatedREVEAL3D[15] == 16:
			cloneFile.write("B16 P15 " + "S" + str(TOOL_BED16)+waitTime)



########################################  GT  ############################################################


	if BedType == "GT":

	# Bed 1
		while bed1[0] <= x_GToffset:                                # Two while loops, one for x and one for Y.
			if heatBedsActive[0] == 1:                        # sets the scope of values of the bed, Breaks loop if bed is active
				break

			if bed1[0] in range(Min_X,Max_X):                # Checks min/max  x-values in range of the bed dimension
				xCheck[0] = 1                                # ^^ if true, marks the xCheck as TRUE --> '1'.

			bed1[0] += 1

		while bed1[1] <= y_GToffset:
			if heatBedsActive[0] == 1:
				break

			if(bed1[1] in range(Min_Y,Max_Y)):
				yCheck[0] = 1

			bed1[1] += 1

		if((xCheck[0] == 1) & (yCheck[0] == 1)):     # if xCheck and yCheck are TRUE, the bed will activate
			print "bed #1 is ON"
			cloneFile.write(zoneON1)         # writes to manipulate output
			heatBedsActive[0] = 1            # States the bed has been turned on
			zoneActivatedGT[0] = 1
			if DUPE_CHECK > 0:
				cloneFile.write(zoneON2)
				print "im not the double"
				heatBedsActive[1] = 2
				zoneActivatedGT[1] = 2



	# Bed 2
		while bed2[0] <= x_GToffset*2:
			if heatBedsActive[1] == 1:
				break

			if(bed2[0] in range(Min_X,Max_X)):
				xCheck[1] = 1

			bed2[0] += 1

		while bed2[1] <= y_GToffset:
			if heatBedsActive[1] == 1:
				break

			if(bed2[1] in range(Min_Y,Max_Y)):
				yCheck[1] = 1

			bed2[1] += 1

		if((xCheck[1] == 1) & (yCheck[1] == 1)):
			print "bed #2 is ON"
			cloneFile.write(zoneON2)
			print "NO im not the double"
			heatBedsActive[1] = 1
			zoneActivatedGT[1] = 2



	# Bed 3
		while bed3[0] <= x_GToffset*2:
			if heatBedsActive[2] == 1:
				break

			if(bed3[0] in range(Min_X,Max_X)):
				xCheck[2] = 1

			bed3[0] += 1

		while bed3[1] <= y_GToffset*2:
			if heatBedsActive[2] == 1:
				break

			if(bed3[1] in range(Min_Y,Max_Y)):
				yCheck[2] = 1

			bed3[1] += 1

		if((xCheck[2] == 1) & (yCheck[2] == 1)):
			print "bed #3 is ON"
			cloneFile.write(zoneON3)
			cloneFile.write("M109 T2 S"+str(TOOL_BED3));
			heatBedsActive[2] = 1
			zoneActivatedGT[2] = 3



	# Bed 4
		while bed4[0] <= x_GToffset:
			if heatBedsActive[3] == 1:
				break

			if(bed4[0] in range(Min_X,Max_X)):
				xCheck[3] = 1

			bed4[0] += 1

		while bed4[1] <= y_GToffset*2:
			if heatBedsActive[3] == 1:
				break

			if(bed4[1] in range(Min_Y,Max_Y)):
				yCheck[3] = 1

			bed4[1] += 1

		if((xCheck[3] == 1) & (yCheck[3] == 1)):
			print "bed #4 is ON"
			cloneFile.write(zoneON4)
			heatBedsActive[3] = 1
			zoneActivatedGT[3] = 4
			if DUPE_CHECK > 0:
				cloneFile.write(zoneON3)
				heatBedsActive[2] = 2
				zoneActivatedGT[2] = 3

		


		# ###  Add WaitTime to beds #### #

		if zoneActivatedGT[0] == 1:
			print "Added Wait Time for Bed 1"
			cloneFile.write("B16 P0 " + "S" + str(TOOL_BED1)+waitTime)
		if zoneActivatedGT[1] == 2:
			print "Added Wait Time for Bed 2"
			cloneFile.write("B16 P1 " + "S" + str(TOOL_BED2)+waitTime)
		if zoneActivatedGT[2] == 3:
			print "Added Wait Time for Bed 3"
			cloneFile.write("B16 P6 " + "S" + str(TOOL_BED1)+waitTime)
		if zoneActivatedGT[3] == 4:
			print "Added Wait Time for Bed 4"
			cloneFile.write("B16 P7 " + "S" + str(TOOL_BED1)+waitTime)


		print "X-GToffset is: "+str(x_GToffset)
		print "y_GToffset is: "+str(y_GToffset)
		print "\n"

	#
	# if DUPE_CHECK > 0:
	#     dupeBeds.dupBed(heatBedsActive, BedType, FORGOT_BEDS)
	#     print"\nBEDCONTROL recognizes DUPE MODE!"

		

	print "Bed's Enabled:"
	print heatBedsActive
	print "\n"



	#### If hot ends are on, go ahead and write M109 commands ####
	print TOOL_SECLAYER1
	print TOOL_SECLAYER2
	print TOOL_SECLAYER3
	print TOOL_SECLAYER4
	if(TOOL_SECLAYER3 > 0):
		print "i am greater"
	else:
		print "i am less than"
		print TOOL_LAYER3
	if(int(TOOL_SECLAYER3) > 0):
		print "i am greater in int"
	else:
		print "i am less than in int"
		print TOOL_LAYER3
	if ((TOOL_LAYER1 > 0) and (int(TOOL_SECLAYER1) > 0)):
		cloneFile.write("M109 T0 S"+str(TOOL_SECLAYER1)+"\r\n")

	if ((TOOL_LAYER2 > 0) and (int(TOOL_SECLAYER2) > 0)):
		cloneFile.write("M109 T1 S"+str(TOOL_SECLAYER2)+"\r\n")

	if ((TOOL_LAYER3 > 0) and (int(TOOL_SECLAYER3) > 0)):
		cloneFile.write("M109 T2 S"+str(TOOL_SECLAYER3)+"\r\n")

	if ((TOOL_LAYER4 > 0) and (int(TOOL_SECLAYER4) > 0)):
		cloneFile.write("M109 T3 S"+str(TOOL_SECLAYER4)+"\r\n")


	gInject.gInject(Zone_Max_X, Zone_Min_X, Zone_Max_Y, Zone_Min_Y,cloneFile,DUPE_CHECK,BedType,MAX_X, MAX_Y)

#############################################################################################################################
##########################################################################################################################

	f = open(newFileLocation, "r")
	#copy = open("cloneTemp.txt", "w")
	# for line in f:
	#     #copy.write(line)
	#     cloneFile.write(line)
	line = "this is BS"
	while line:
		line = f.readline()
		#print(line)
		cloneFile.write(line)
	f.close()
	#copy.close()


########################################## Turns EXTRUDERS OFF  ###################################################################





########################################## Turns Beds OFF  ###################################################################

	if (BedType == "reveal3D") or (BedType == "FRANK3"):
	# Bed 1
		if heatBedsActive[0] > 0 :                            # If the bed is active, turn OFF, write to manipulate output
			cloneFile.write(zoneOFF1)
			heatBedsActive[0] = 0                             # Sets bed to inactive

	# Bed 2
		if heatBedsActive[1] > 0:
			print heatBedsActive[1]
			print" yea its thru"
			cloneFile.write(zoneOFF2)
			heatBedsActive[1] = 0

	# Bed 3
		if heatBedsActive[2] > 0:
			cloneFile.write(zoneOFF3)
			heatBedsActive[2] = 0

	# Bed 4
		if heatBedsActive[3] > 0:
			print heatBedsActive[3]
			print" yea its thru"
			cloneFile.write(zoneOFF4)
			heatBedsActive[3] = 0

	# Bed 5
		if heatBedsActive[4] > 0:
			cloneFile.write(zoneOFF5)
			heatBedsActive[4] = 0

	# Bed 6
		if heatBedsActive[5] > 0:
			cloneFile.write(zoneOFF6)
			heatBedsActive[5] = 0

	# Bed 7
		if heatBedsActive[6] > 0:
			cloneFile.write(zoneOFF7)
			heatBedsActive[6] = 0

	# Bed 8
		if heatBedsActive[7] > 0:
			cloneFile.write(zoneOFF8)
			heatBedsActive[7] = 0

	# Bed 9
		if heatBedsActive[8] > 0:
			cloneFile.write(zoneOFF9)
			heatBedsActive[8] = 0

	# Bed 10
		if heatBedsActive[9] > 0:
			cloneFile.write(zoneOFF10)
			heatBedsActive[9] = 0

	# Bed 11
		if heatBedsActive[10] > 0:
			cloneFile.write(zoneOFF11)
			heatBedsActive[10] = 0

	# Bed 12
		if heatBedsActive[11] > 0:
			cloneFile.write(zoneOFF12)
			heatBedsActive[11] = 0

	# Bed 13
		if heatBedsActive[12] > 0:
			cloneFile.write(zoneOFF13)
			heatBedsActive[12] = 0

	# Bed 14
		if heatBedsActive[13] > 0:
			cloneFile.write(zoneOFF14)
			heatBedsActive[13] = 0

	# Bed 15
		if heatBedsActive[14] > 0:
			cloneFile.write(zoneOFF15)
			heatBedsActive[14] = 0

	# Bed 16
		if heatBedsActive[15] > 0:
			cloneFile.write(zoneOFF16)
			heatBedsActive[15] = 0


		#print "\nM104 16: " + str(M104_TOOL) + "\n"
		if((M104_TOOL[0] == 1) or (M104_TOOL[0] == 2)):
				print str(M104_TOOL[0]) + " <---- M104 T0"
				cloneFile.write("M104 T0 S0\n")
				# M104_TOOL[0] = 0

		if((M104_TOOL[1] == 1) or (M104_TOOL[1] == 2)):
				print str(M104_TOOL[1]) + " <---- M104 T1"
				cloneFile.write("M104 T1 S0\n")
				# M104_TOOL[1] = 0

		if((M104_TOOL[2] == 1) or (M104_TOOL[2] == 2)):
				print str(M104_TOOL[2]) + " <---- M104 T2"
				cloneFile.write("M104 T2 S0\n")
				# M104_TOOL[2] = 0

		if((M104_TOOL[3] == 1) or (M104_TOOL[3] == 2)):
				print str(M104_TOOL[3]) + " <---- M104 T3"
				cloneFile.write("M104 T3 S0\n")
				# M104_TOOL[3] = 0

		finalFunction.finalFunction(cloneFile)




###################################################################################
	if BedType == "GT":
	# Bed 1
		if heatBedsActive[0] > 0 :                            # If the bed is active, turn OFF, write to manipulate output
			cloneFile.write(zoneOFF1)
			heatBedsActive[0] = 0                             # Sets bed to inactive

	# Bed 2
		if heatBedsActive[1] > 0:
			cloneFile.write(zoneOFF2)
			heatBedsActive[1] = 0

	# Bed 3
		if heatBedsActive[2] > 0:
			cloneFile.write(zoneOFF3)
			heatBedsActive[2] = 0

	# Bed 4
		if heatBedsActive[3] > 0:
			cloneFile.write(zoneOFF4)
			heatBedsActive[3] = 0

		# Turn off Extruders
		#print "\nM104 GT: " + str(M104_TOOL) + "\n"
		if((M104_TOOL[0] == 1) or (M104_TOOL[0] == 2)):
				print str(M104_TOOL[0]) + " <---- M104 T0"
				cloneFile.write("M104 T0 S0\n")
				# M104_TOOL[0] = 0

		if((M104_TOOL[1] == 1) or (M104_TOOL[1] == 2)):
				print str(M104_TOOL[1]) + " <---- M104 T1"
				cloneFile.write("M104 T1 S0\n")
				# M104_TOOL[1] = 0

		if((M104_TOOL[2] == 1) or (M104_TOOL[2] == 2)):
				print str(M104_TOOL[2]) + " <---- M104 T2"
				cloneFile.write("M104 T2 S0\n")
				# M104_TOOL[2] = 0

		if((M104_TOOL[3] == 1) or (M104_TOOL[3] == 2)):
				print str(M104_TOOL[3]) + " <---- M104 T3"
				cloneFile.write("M104 T3 S0\n")
				# M104_TOOL[3] = 0

		finalFunction.finalFunction(cloneFile)

	print "Bed's Disabled:"
	print heatBedsActive

	#open(newFileLocation, 'a').write(open('cloneTemp.txt').read())
	cloneFile.close()



# Destroys File at the end
def killBedData():

	print "tmp files not removed"
	print "nothing is being removed at the moment"
	print "test"
