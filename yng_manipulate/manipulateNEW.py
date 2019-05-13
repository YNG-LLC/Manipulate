#push from ErikK

#tab = 4 spaces
import MySQLdb
import os
import sys
import time
import logging


##### custom imports #######
import lookupNew
import bedControl
import writeBeds
import gInject

############################

# run



################# This is for strings and other variables needed for 'translating' B-code to G-code ##############

MAX_X = 880         # set for max X direction
MAX_Y = 880         # set max Y direction
MAX_Z = 430         # set max Z direction
NumberXBeds = 4
NumberYBeds = 4
Zone_Min_X = 880    # set min X zoning dimension
Zone_Max_X = 0      # set max X zoning dimension
Zone_Min_Y = 880    # set min Y zoning dimension
Zone_Max_Y = 0      # set min X zoning dimension
Zone_Min_Z = 0      # set min Z zoning dimension
Zone_Max_Z = 430    # set max Z zoning dimension

# degree_sign= u'\N{DEGREE SIGN}'
Temperature_Max = 0     # Variable for a Maximum Temperature Value
Temperature_Min = 0     # Variable for a Minimum Temperature Value
Temperature_Con = 0     # Variable for Keeping constant Temperature
Temperature_Rng = 0     # variable for Temperature to remain within a selected range.(Probably not needed)

file_done = 0
getNumberX = 0
getNumberY = 0
getNumberZ = 0
numbersFound = 0      # variable to store numbers were found
tempX = ['']*1000     # store temporary X values
tempY = ['']*1000     # store temporary Y values
tempZ = ['']*1000     # store temporary Z values
tempZfloat = 0.000
CurrentMaxHeight = -1.0

writeStart = 0              # variable to see if writing to file should start
tmpLineStart = ['']*250     # Stores first part of current line read
tmpLineEnd = ['']*250       # Stores last part of current line read
tlCount = 0                 # Stores count of number of lines

tc = 0

tmpSX = ""                  # more temp values for storing and manipulating values
tmpSY = ""
tmpSZ = ""
tmpS = ""
tmpFullS = ""

LineDone = 0                # flag to show when it is done reading a line

zone_beds = [0]*20

BedTemp = 0                 # passing Bed temperatures

bedCharArry = ['']*64       # stores X & Y Min/Max

nozzleMode = ""				# check for uplaoded file if set for Single/Dupe
nozCheck = 0


x_16offset = 0.0000
y_16offset = 0.0000
y_GToffset = 0.0000
x_GToffset = 0.0000


############################# MANIPULATE SQL##########################

#### Start Logging #######
try:
######################

	################  Must Establish mysql DB connection to pull necessary file info ##############
	db = MySQLdb.connect(host="localhost", user="printerUser", passwd="yngprinter17!", db="manipulate")
	cur = db.cursor()


	if len(sys.argv)<2:
		print "Fatal: You forgot to include the directory name on the command line."
		print "Usage:  python %s <directoryname>" % sys.argv[0]
		logging.basicConfig(format='%(asctime)s %(message)s',datefmt='%m/%d/%Y %I:%M:%S %p', filename=str(fileEdit+'.log'),level=logging.DEBUG)
		logging.warning('---- manipulateNEW.py encountered a mySQL DB Connection ERROR!:\r\n')

		try:

			with open(str(fileEdit+'.log'), 'r') as myfile: 
				data = myfile.read().replace('\n', '')

			cur.execute("UPDATE yngPrints SET errorLog = %s WHERE task_id = %s""", (data, TASKID))
			db.commit()
			cur.close()
			db.close()

		except Exception as e:
			logging.basicConfig(format='%(asctime)s %(levelname)-8s %(message)s',datefmt='%m/%d/%Y %I:%M:%S %p', filename=str(fileEdit+'.log'),level=logging.DEBUG)
			logger = logging.getLogger()
			handler = logging.StreamHandler()
			formatter = logging.Formatter(
			        '%(asctime)s %(name)-12s %(levelname)-8s %(message)s')
			handler.setFormatter(formatter)
			logger.addHandler(handler)			# Prints to console###
			logger.setLevel(logging.DEBUG)
			logger.exception("---> Fatal error in Manipulate <---")
			logger.debug('-------------------END------------------------\n\n\n')
			# logging.shutdown()
			raise

		
		os.remove(str(fileEdit+'.log'))

		sys.exit(1)

	########## The next section is the argument set used to run the command #####
	#"Third" command input, zone = zone number
	zone = int(sys.argv[1])
	#"Fourth" command input for location of the file
	fileLocation = str(sys.argv[2])
	#"Fourth" command input, task_id from DB to help us keep track of queries we are using
	BedType = str(sys.argv[3])          # may need to swap with TASKID
	print "Printer Selected:" + " " + str(BedType)
	TASKID = str(sys.argv[4]) # pass task ID via argument
	d = 1    #counter for beds



	# Select SQL query - try to select the file from DB in order to grab variables
	try:
		ts = "SELECT file FROM yngPrints WHERE task_id = " + TASKID
		findFile = cur.execute(ts)
		#queryFile = the fetched sql "file" name fom yngPrints DB
		queryFile = cur.fetchone()
		#fileName is result from "file" column, must take it from the queryFile array
		fileName = queryFile[0]

	# exception used for try, prints errors if sql fails
	except MySQLdb.Error, e:
		try:
			print "MySQL Error [%d]: %s" % (e.args[0], e.args[1])
		except IndexError:
			print "MySQL Error: %s" % str(e)

	print "Global name declared: " + fileName



	# For the temperature selection
	# Select SQL query - try to select the material from DB in order to grab variables
	try:
		ts = "SELECT MaterialType FROM yngPrints WHERE task_id = " +TASKID
		Material = cur.execute(ts)
		#queryFile = the fetched sql "file" name fom yngPrints DB
		queryFile = cur.fetchone()
		#fileName is result from "file" column, must take it from the queryFile array
		Material = queryFile[0]

	# exception used for try, prints errors if sql fails
	except MySQLdb.Error, e:
		try:
			print "MySQL Error [%d]: %s" % (e.args[0], e.args[1])
		except IndexError:
			print "MySQL Error: %s" % str(e)

	print "Global Material declared: " + Material




	#### Check if File was UPLOADED for Duplication or Single Printing #######
	try:
		ts = "SELECT nozzleMode FROM yngPrints WHERE task_id = " + TASKID
		nozzle = cur.execute(ts)
		#queryFile = the fetched sql "file" name fom yngPrints DB
		queryFile = cur.fetchone()
		#fileName is result from "file" column, must take it from the queryFile array
		nozzleMode = queryFile[0]

	# exception used for try, prints errors if sql fails
	except MySQLdb.Error, e:
		try:
			print "MySQL Error [%d]: %s" % (e.args[0], e.args[1])
		except IndexError:
			print "MySQL Error: %s" % str(e)

	print "Global NozzleMode declared: " + nozzleMode



	# I think this variable is used to send new file to .octoprint...should double check
	newFileLocation = os.path.splitext(fileLocation)[0]
	# file edit replaces ".gcode" with nothing, format necessary for transfers
	fileEdit = fileName.replace(".gcode", "")
	# print "----Edit----"
	# print fileEdit
	# newFileLocation var used for combining parameters to send to .octoprint with a .gco tag at end
	newFileLocation = os.path.splitext(fileLocation)[0]

	# newFileLocation = "/home/odroid/.octoprint/uploads/" + fileEdit +"zone"+ str(zone) + ".gco"



	piDir = "/home/pi/.octoprint/uploads/"
	odroidDir = "/home/odroid/.octoprint/uploads/"

	####  Q(taskID)_(print file name)_(MaterialUsed)__(zone_#)   ####

	###### Customer Printers ######   
	if (os.path.isdir(piDir)):

		# FinalFileLocation = "/home/pi/.octoprint/uploads/" + fileEdit +"__zone"+ str(zone) + ".gcode"
		FinalFileLocation = "/home/pi/.octoprint/uploads/" + "Q"+ TASKID +"_"+fileEdit+"_"+Material+"_zone"+str(zone) + ".gcode"
		newFileLocation = newFileLocation + "temp_"+ "Q"+ TASKID +"__zone"+ str(zone) +".tmp" #make it a temp instead of final



	# ##### OFFICE PRINTERS #####
	if os.path.isdir(odroidDir):
		# FinalFileLocation = "/home/odroid/.octoprint/uploads/" + fileEdit +"__zone"+ str(zone) + ".gcode"
		FinalFileLocation = "/home/odroid/.octoprint/uploads/" + "Q"+ TASKID +"_"+fileEdit+"_"+Material+"_zone"+str(zone) + ".gcode"
		newFileLocation = newFileLocation + "temp_"+ "Q"+ TASKID +"__zone"+ str(zone) +".tmp" #make it a temp instead of final
	


	# print newFileLocation

	####################################################################################################



	# ##########  The next section is the argument set used to run the command  ############################
	# zone = int(sys.argv[1])
	# print "\n" + "Zone Slected:" + " " + str(zone)
	# fileLocation = str(sys.argv[2])
	# BedType = str(sys.argv[3])          # will need to change to '4' when enabling the SQL code
	# print "Printer Selected:" + " " + str(BedType)
	# newFileLocation = os.path.splitext(fileLocation)[0]
	# FinalFileLocation = newFileLocation + str(zone) + ".gco"
	# newFileLocation = newFileLocation + "temp.tmp" #make it a temp instead of final
	# d = 1    #counter for beds



	################################# MODDING TEMPS ###################################################

	'''
	 # if z < .6 and seceding layer has been found, this is now the first layer. <-- This is to change the temp back to the required temp for the first layer!!!

	 # I'll need to clear all arrays at the end before nmanipoulate is processeed again.

	 # Added z layer change at the end.


	'''


	
	# if z < .6 and seceding layer has been found, this is now the first layer


	####### Next, populate Arrays #################
	print "Active Filament: " + str(Material)
	#print "test1lasdkjfla"
	dbbedArray = 0
	queryArray = 0
	try:
	#   findTemps = cur.execute("SELECT Bed_First_Layer,Bed_Sec_Layer,HotEnd_First_Layer,HotEnd_Sec_Layer FROM materialDB WHERE Material = %s",(Material))
		ts = "SELECT Bed0_First_Layer, Bed0_Sec_Layer, HotEnd0_First_Layer, HotEnd0_Sec_Layer, Bed1_First_Layer, Bed1_Sec_Layer, HotEnd1_First_Layer, HotEnd1_Sec_Layer, Bed2_First_Layer, Bed2_Sec_Layer, HotEnd2_First_Layer, HotEnd2_Sec_Layer, Bed3_First_Layer, Bed3_Sec_Layer, HotEnd3_First_Layer, HotEnd3_Sec_Layer FROM materialDB WHERE Material = '" + Material + "'"
		print ts
		cur.execute(ts)
		# queryFile = the fetched sql "file" name fom yngPrints DB
		queryTemps = cur.fetchone()
	#    dbbedArray = [queryArray[0] for queryArray in cur.fetchone()]
	#    print dbbedArray
		# fileName is result from "file" column, must take it from the queryFile array
		# print queryTemps
	#    tempfl = int(queryTemps[0])
	#    dtempfl = int(queryTemps[1])
		# print queryTemps[0]
		# print queryTemps[1]
		# print queryTemps[2]
		# print queryTemps[3]
		# print queryTemps[4]
		# print queryTemps[5]
		# print queryTemps[6]
		# print queryTemps[7]
		# print queryTemps[8]
		# print queryTemps[9]
		# print queryTemps[10]
		# print queryTemps[11]
		# print queryTemps[12]
		# print queryTemps[13]
		# print queryTemps[14]
		# print queryTemps[15]
		# print "-----------now type casting commences--------"
		# print int(queryTemps[0])
		# print int(queryTemps[1])
		# print int(queryTemps[2])
		# print int(queryTemps[3])
		# print int(queryTemps[4])
		# print int(queryTemps[5])
		# print int(queryTemps[6])
		# print int(queryTemps[7])
		# print int(queryTemps[8])
		# print int(queryTemps[9])
		# print int(queryTemps[10])
		# print int(queryTemps[11])
		# print int(queryTemps[12])
		# print int(queryTemps[13])
		# print int(queryTemps[14])
		# print int(queryTemps[15])

	# exception used for try, prints errors if sql fails
	except MySQLdb.Error, e:
		try:
			print "MySQL Error [%d]: %s" % (e.args[0], e.args[1])
		except IndexError:
			print "MySQL Error: %s" % str(e)

	# print "Temperature called: "



	#### First Part: Make sure Temps have been populated


	print("\n" + "Array is Empty. Populating...")


	#FIRST_LAYER = int(queryTemps[2])                 # Array to store Temperatures
	#SEC_LAYER = int(queryTemps[3])

	#BED_FIRST = int(queryTemps[0])
	#BED_SEC = int(queryTemps[1])

	FIRST_LAYER_CHECK = ['']*4           # Check if the layers have been populated, if so move on to the seceding layer
	SEC_LAYER_CHECK = ['']*4

	TOOL1 = str(queryTemps[2])             # tool = extruder Temperature
	TOOL2 = str(queryTemps[6])
	TOOL3 = str(queryTemps[10])
	TOOL4 = str(queryTemps[14])

	TOOL_LAYER1 = str(queryTemps[2])         # Extruder First Layer is always hotter than seceding layer. Tool = extruder
	TOOL_LAYER2 = str(queryTemps[6])
	TOOL_LAYER3 = str(queryTemps[10])
	TOOL_LAYER4 = str(queryTemps[14])
	print "tools first"
	print TOOL_LAYER1
	print TOOL_LAYER2
	print TOOL_LAYER3
	print TOOL_LAYER4
	TOOL_SECLAYER1 = str(queryTemps[3])        # Extruder Seceding Layer Temp pulled from DB
	TOOL_SECLAYER2 = str(queryTemps[7])
	TOOL_SECLAYER3 = str(queryTemps[11])
	TOOL_SECLAYER4 = str(queryTemps[15])
	print "tools SEC"
	print TOOL_SECLAYER1
	print TOOL_SECLAYER2
	print TOOL_SECLAYER3
	print TOOL_SECLAYER4

	BED_FIRST_CHECK = [0]*4              # used in M109 commands
	BED_SEC_CHECK = [0]*4
	M104_FIRST_CHECK = [0]*4
	M104_SEC_CHECK = [0]*4



	TOOL_BED1 = str(queryTemps[0])
	TOOL_BED2 = str(queryTemps[4])           # First Bed Layer Temp must match
	TOOL_BED3 = str(queryTemps[8])
	TOOL_BED4 = str(queryTemps[12])

	TOOL_SECBED1 = str(queryTemps[1])          # Seceding Bed Layer Temp
	TOOL_SECBED2 = str(queryTemps[5])
	TOOL_SECBED3 = str(queryTemps[9])
	TOOL_SECBED4 = str(queryTemps[13])

	M104_TOOL = [0]*4
	M109_TOOL = [0]*4


	writeHeatBedsActive = [0]*16

	FORGOT_BEDS = [0]*16
	WRITE_BEDS = 0      # execute writeBeds.py
	DUPE_CHECK = 0
	writeBedsCheck = 0
	w_Check = 0
	layer_Check = 0
	bedCheck = 0




	if(TOOL1 == 0):                                     # TOOL1 should always have a value, checks for value
		print("ERROR: EXTRUDER TEMP = 0")
		logging.basicConfig(format='%(asctime)s %(message)s',datefmt='%m/%d/%Y %I:%M:%S %p', filename=str(fileEdit+'.log'),level=logging.DEBUG)
		logging.warning('---- manipulateNEW.py encountered an EXTRUDER ERROR on REVEAL3D!:  TOOL1 is SET EQUAL TO zero\r\n')

		try:

			with open(str(fileEdit+'.log'), 'r') as myfile: 
				data = myfile.read().replace('\n', '')
			ts = "UPDATE yngPrints SET errorLog = " + data +" WHERE task_id = " + TASKID
			cur.execute(ts)
			db.commit()
			cur.close()
			db.close()


		except Exception as e:
			logging.basicConfig(format='%(asctime)s %(levelname)-8s %(message)s',datefmt='%m/%d/%Y %I:%M:%S %p', filename=str(fileEdit+'.log'),level=logging.DEBUG)
			logger = logging.getLogger()
			handler = logging.StreamHandler()
			formatter = logging.Formatter(
			        '%(asctime)s %(name)-12s %(levelname)-8s %(message)s')
			handler.setFormatter(formatter)
			logger.addHandler(handler)			# Prints to console###
			logger.setLevel(logging.DEBUG)
			logger.exception("---> Fatal error in Manipulate <---")
			logger.debug('-------------------END------------------------\n\n\n')
			# logging.shutdown()
			raise
		os.remove(str(fileEdit+'.log'))
		sys.exit

	if(TOOL1 < 0):
		print("ERROR: EXTRUDER TEMP < 0")
		logging.basicConfig(datefmt='%m/%d/%Y %I:%M:%S %p', filename=str(fileEdit+'.log'),level=logging.DEBUG)
		logging.warning('manipulateNEW.py encountered an EXTRUDER ERROR on REVEAL3D!:  TOOL1 has a value LESS THAN zero\r\n')

		try:

			with open(str(fileEdit+'.log'), 'r') as myfile: 
				data = myfile.read().replace('\n', '')
			ts = "UPDATE yngPrints SET errorLog = " + data + " WHERE task_id = " + TASKID
			cur.execute(ts)
			db.commit()
			cur.close()
			db.close()

		except Exception as e:
			logging.basicConfig(format='%(asctime)s %(levelname)-8s %(message)s',datefmt='%m/%d/%Y %I:%M:%S %p', filename=str(fileEdit+'.log'),level=logging.DEBUG)
			logger = logging.getLogger()
			handler = logging.StreamHandler()
			formatter = logging.Formatter(
			        '%(asctime)s %(name)-12s %(levelname)-8s %(message)s')
			handler.setFormatter(formatter)
			logger.addHandler(handler)			# Prints to console###
			logger.setLevel(logging.DEBUG)
			logger.exception("---> Fatal error in Manipulate <---")
			logger.debug('-------------------END------------------------\n\n\n')
			# logging.shutdown()
			raise
		os.remove(str(fileEdit+'.log'))
		sys.exit



	if(TOOL2 < 0):                                      # if -1, make zero. if zero, make previous extruder's value.
		print("TOOL2:" + " " + str(TOOL2))
		TOOL2 = 0

	if((TOOL2 == 0) & (TOOL1 != 0)):
		TOOL2 = TOOL1
		print("TOOL2:" + " " + str(TOOL2))

	if(TOOL3 < 0):
		print("TOOL3:" + " " + str(TOOL3))
		TOOL3 = 0

	if((TOOL3 == 0) & (TOOL2 != 0)):
		TOOL3 = TOOL2
		print("TOOL3:" + " "  + str(TOOL3))

	if(TOOL4 < 0):
		print("TOOL4:" + " " + str(TOOL4))
		TOOL4 = 0

	if((TOOL4 == 0) & (TOOL3 != 0)):
		TOOL4 = TOOL3
		print("TOOL4:" + " " + str(TOOL4))



	# ### Third, Apply Bed Temps for First & Second Layers. Also, place a check if seceding layer returns to first layer to adjsut the temperature needed ### #






	######### BedType Error Check #####################################################################
	# if BedType not in ("reveal3D","GT","FRANK3"):
	#     print "\n\n\nPlease Input the correct Printer name!"
	#     print "\n\n"
	#     print "Valid printers are: reveal3D, GT, FRANK3 "
	#     print "\n\n\n"
	#     sys.exit()


	if ((BedType in ("GT")) & (zone not in (1,2,3,4))):
		print "\n"
		print "BedType entered: " + str(BedType)
		print "Zone Entered: " + str(zone)
		print "You entered an invalid zone for this Printer"
		print "Valid zones for the GT are: 1,2,3,4"
		print "\n    GT Graphic"
		print " ------------------"
		print " |       |        |"
		print " |   4   |   3    |"
		print " |       |        |"
		print " ------------------"
		print " |       |        |"
		print " |   1   |   2    |"
		print " |       |        |"
		print " ------------------\n\n"
		logging.basicConfig(format='%(asctime)s %(message)s',datefmt='%m/%d/%Y %I:%M:%S %p', filename=str(fileEdit+'.log'),level=logging.DEBUG)
		logging.warning('---- Manipulate encountered a ZONE ERROR on the GT!:\r\n\n        "The zone that you entered is not valid for DUPLICATION!"\n        "Valid zones are 1,2,3,4"\r\n\n         BedType: ' + str(BedType)+'\r\n         Zone Entered: '+ str(zone)+'\r\n\n')

		try:

			with open(str(fileEdit+'.log'), 'r') as myfile: 
				data = myfile.read().replace('\n', '')


			ts = "UPDATE yngPrints SET errorLog = " + data +" WHERE task_id = " + TASKID
			cur.execute(ts)
			db.commit()
			cur.close()
			db.close()



		except Exception as e:
			logging.basicConfig(format='%(asctime)s %(levelname)-8s %(message)s',datefmt='%m/%d/%Y %I:%M:%S %p', filename=str(fileEdit+'.log'),level=logging.DEBUG)
			logger = logging.getLogger()
			handler = logging.StreamHandler()
			formatter = logging.Formatter(
			        '%(asctime)s %(name)-12s %(levelname)-8s %(message)s')
			handler.setFormatter(formatter)
			logger.addHandler(handler)			# Prints to console###
			logger.setLevel(logging.DEBUG)
			logger.exception("---> Fatal error in Manipulate <---")
			logger.debug('-------------------END------------------------\n\n\n')
			# logging.shutdown()
			raise
		os.remove(str(fileEdit+'.log'))
		sys.exit()


	#####SHOW AN ERROR IF NOT IN THE CORRECT ZONE NUMBER SET ################
	if((BedType in ("reveal3D","FRANK3")) & (zone not in (1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16))):
		print "\n"
		print "BedType entered: " + str(BedType)
		print "Zone Entered: " + str(zone)
		print "\n"
		print "You entered an invalid zone for" + " " + str(BedType)
		print "Valid zones are between 1 and 16!"
		print "\n               Zone Graphic"
		print " ------------------------------------"
		print " |       |        |        |        |"
		print " |   16  |   15   |   14   |   13   |"
		print " |       |        |        |        |"
		print " ------------------------------------"
		print " |       |        |        |        |"
		print " |   9   |   10   |   11   |   12   |"
		print " |       |        |        |        |"
		print " ------------------------------------"
		print " |       |        |        |        |"
		print " |   8   |   7    |    6   |    5   |"
		print " |       |        |        |        |"
		print " ------------------------------------"
		print " |       |        |        |        |"
		print " |   1   |   2    |    3   |    4   |"
		print " |       |        |        |        |"
		print " ------------------------------------\n\n"
		logging.basicConfig(format='%(asctime)s %(message)s',datefmt='%m/%d/%Y %I:%M:%S %p', filename=str(fileEdit+'.log'),level=logging.DEBUG)
		logging.warning('---- Manipulate encountered a ZONE ERROR on REVEAL3D!:\r\n\n        "The zone that you entered is not valid for DUPLICATION!"\n        "Valid zones are 1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16"\r\n\n         BedType: ' + str(BedType)+'\r\n         Zone Entered: '+ str(zone)+'\r\n\n')

		try:

			with open(str(fileEdit+'.log'), 'r') as myfile: 
				data = myfile.read().replace('\n', '')


			ts = "UPDATE yngPrints SET errorLog = " + data +" WHERE task_id = " + TASKID
			cur.execute(ts)
			db.commit()
			cur.close()
			db.close()



		except Exception as e:
			logging.basicConfig(format='%(asctime)s %(levelname)-8s %(message)s',datefmt='%m/%d/%Y %I:%M:%S %p', filename=str(fileEdit+'.log'),level=logging.DEBUG)
			logger = logging.getLogger()
			handler = logging.StreamHandler()
			formatter = logging.Formatter(
			        '%(asctime)s %(name)-12s %(levelname)-8s %(message)s')
			handler.setFormatter(formatter)
			logger.addHandler(handler)			# Prints to console###
			logger.setLevel(logging.DEBUG)
			logger.exception("---> Fatal error in Manipulate <---")
			logger.debug('-------------------END------------------------\n\n\n')
			# logging.shutdown()
			raise
		os.remove(str(fileEdit+'.log'))
		sys.exit()

	if  BedType == "GT":
		MAX_X = 480         # set for max X direction
		MAX_Y = 525         # set max Y direction
		MAX_Z = 430         # set max Z direction
		NumberXBeds = 2
		NumberYBeds = 2
		Zone_Min_X = 480    # set min X zoning dimension
		Zone_Max_X = 0      # set max X zoning dimension
		Zone_Min_Y = 525    # set min Y zoning dimension
		Zone_Max_Y = 0      # set min X zoning dimension
		Zone_Min_Z = 0    # set min Z zoning dimension
		Zone_Max_Z = 430      # set max Z zoning dimension
		#MAX_Z = 300        # Z tracking is not implemented yet

	if  BedType == "FRANK3":
		MAX_X = 880         # set for max X direction
		MAX_Y = 880         # set max Y direction
		MAX_Z = 430         # set max Z direction
		NumberXBeds = 4
		NumberYBeds = 4
		Zone_Min_X = 880    # set min X zoning dimension
		Zone_Max_X = 0      # set max X zoning dimension
		Zone_Min_Y = 880    # set min Y zoning dimension
		Zone_Max_Y = 0      # set min X zoning dimension
		Zone_Min_Z = 0    # set min Z zoning dimension
		Zone_Max_Z = 430      # set max Z zoning dimension
		#MAX_Z = 300        # Z tracking is not implemented yet

	if  BedType == "reveal3D":
		MAX_X = 1000         # set for max X direction
		MAX_Y = 1000         # set max Y direction
		MAX_Z = 430         # set max Z direction
		NumberXBeds = 4
		NumberYBeds = 4
		Zone_Min_X = 1000    # set min X zoning dimension
		Zone_Max_X = 0      # set max X zoning dimension
		Zone_Min_Y = 1000    # set min Y zoning dimension
		Zone_Max_Y = 0      # set min X zoning dimension
		Zone_Min_Z = 0    # set min Z zoning dimension
		Zone_Max_Z = 430      # set max Z zoning dimension
		#MAX_Z = 300        # Z tracking is not implemented yet
	print "THIS IS BEDTYPE: "+BedType
	print "\n"
	print "\n"
	print "Values are set as:"
	print "Max_X:" + str(MAX_X)
	print "Max_Y:" + str(MAX_Y)
	print "Max_Z:" + str(MAX_Z)
	print "\n"
	print "\n"

	########################################################################################

	#file = open(fileLocation, 'r')
	newFile = open(newFileLocation, 'w')    #open a new file to write in
	'''
	newFile.write("G21\n")                  #send the start of the basic commands
	newFile.write("G90\n")
	newFile.write("M82\n")
	newFile.write("M106 S0\n")
	newFile.write("G1 Z+25 F2000\n")
	#newFile.write("G28 X0 Y0\n"            #home x and y axis
	#newFile.write("G1 Z15 F1000\n")        #move Z to 15mm
	'''
	########## THIS SECTION SETS PROBE POINT ################
	#pdb.set_trace()
	'''
	if(zone == 1):
		newFile.write("G1 X120 Y150 F2500\n")
		#newFile.write("B16 P0 S80 E1\n")
		newFile.write("G4 S240\n")
	if(zone == 2):
		newFile.write("G1 X350 Y150 F2500\n")
		#newFile.write("B16 P1 S80 E1\n")
		newFile.write("G4 S240\n")
	if(zone == 3):
		newFile.write("G1 X580 Y150 F2500\n")
		#newFile.write("B16 P2 S80 E1\n")
		newFile.write("G4 S240\n")
	if(zone == 4):
		newFile.write("G1 X810 Y150 F2500\n")
		#newFile.write("B16 P3 S80 E1\n")
		newFile.write("G4 S240\n")
	if(zone == 5):
		newFile.write("G1 X810 Y350 F2500\n")
		#newFile.write("B16 P4 S80 E1\n")
		newFile.write("G4 S240\n")
	if(zone == 6):
		newFile.write("G1 X580 Y350 F2500\n")
		#newFile.write("B16 P5 S80 E1\n")
		newFile.write("G4 S240\n")
	if(zone == 7):
		newFile.write("G1 X350 Y350 F2500\n")
		#newFile.write("B16 P6 S80 E1\n")
		newFile.write("G4 S240\n")
	if(zone == 8):
		newFile.write("G1 X120 Y350 F2500\n")
		#newFile.write("B16 P7 S80 E1\n")
		newFile.write("G4 S240\n")
	if(zone == 9):
		newFile.write("G1 X120 Y580 F2500\n")
		#newFile.write("B16 P8 S80 E1\n")
		newFile.write("G4 S240\n")
	if(zone == 10):
		newFile.write("G1 X350 Y580 F2500\n")
		#newFile.write("B16 P9 S80 E1\n")
		newFile.write("G4 S240\n")
	if(zone == 11):
		newFile.write("G1 X580 Y580 F2500\n")
		#newFile.write("B16 P10 S80 E1\n")
		newFile.write("G4 S240\n")
	if(zone == 12):
		newFile.write("G1 X810 Y580 F2500\n")
		#newFile.write("B16 P11 S80 E1\n")
		newFile.write("G4 S240\n")
	if(zone == 13):
		newFile.write("G1 X810 Y810 F2500\n")
		#newFile.write("B16 P12 S80 E1\n")
		newFile.write("G4 S240\n")
	if(zone == 14):
		newFile.write("G1 X580 Y810 F2500\n")
		#newFile.write("B16 P13 S80 E1\n")
		newFile.write("G4 S240\n")
	if(zone == 15):
		newFile.write("G1 X350 Y810 F2500\n")
		#newFile.write("B16 P14 S80 E1\n")
		newFile.write("G4 S240\n")
	if(zone == 16):
		newFile.write("G1 X120 Y810 F2500\n")
		#newFile.write("B16 P15 S80 E1\n")
		newFile.write("G4 S240\n")

	'''

	zone_beds[d] = zone - 1




	########## END PROBE POINT SECTION ###############################

	#newFile.write("G29\n")
	#newFile.write("G28 Z0\n")           #home the Z axis
	#newFile.write("G30\n")              #probe single point for offset from Z0
	#newFile.write("G92 Z-0.15\n")       #implement button offset from known value
	#newFile.write("G1 Z15 F2000\n")     #move Z axis up to 20 mm
	#newFile.write("M109 T0 S240\n")
	#newFile.write("M109 T1 S240\n")
	# newFile.write("G92 E0\n")

	#for line in open(fileLocation, 'r'):
	# if((line == "M107\n") | (line == "M82\n")):
	#   writeStart = 1
	# if(writeStart == 1):
	#   newFile.write(line)

	writeStart = 0
	count = 0
	tmpCustom = [""]*5
	tmpCustomFull = ""
	c = 0                   #I had to add a counter.......thanks python



	for line in open(fileLocation, 'r'):    #now to start reading the input file
		#time.sleep(.2)
		#if (zone == 1):             #this is easy for zone 1 since the item should have been sliced for zone 1
		#print line
		#newFile.write(line)
		#if((line == "M107\n") | (line == "M82\n")):    #check for a known command before actual printing section starts
		# if(writeStart == 0):
		#    newFile.write(line)
		# if("B16" in line):
		#     print "found the bug"
		#     print line



		
		# #### Check if Nozzle is Single or Duplication, apply B0 if Dupe, delete line if Single  #### # 
		
		if nozzleMode == "Single" and nozCheck == 0:
			if line[0] =="B" and line[1]=="0":
				# print "Found B0 For DELETION"
				line = line.replace(line, "; removed B0\r\n")
				print "DELETED B0"
				nozCheck = 1
			elif ((line == "B0\n") | (line == "B0\r\n")):
				# print "Found B0 For DELETION"
				line = line.replace(line, "; removed B0\r\n")
				print "DELETED B0"
				nozCheck = 1
			


		if nozzleMode == "Duplication" and nozCheck == 0:
			print "nozzleMode is Duplication"
			newFile.write("B0\r\n");
			DUPE_CHECK = 2
			print "DUPE_CHECK is: " + str(DUPE_CHECK)
			MAX_X = ((MAX_X/2)-10)
			nozCheck = 1


			if((BedType in ("reveal3D","FRANK3")) & (zone not in (1,2,7,8,9,10,15,16))):
				print "BedType entered: " + str(BedType)
				print "Zone Entered: " + str(zone)
				print  "\n\n\nThe zone that you entered is not valid for DUPLICATION!!!"
				print "Valid zones for Duplication are 1,2,8,7,9,10,15 and 16"
				print "\n Zone graphic For Duplicate Mode"
				print " -------------------------"
				print " |           |           |"
				print " |    16     |    15     |"
				print " |           |           |"
				print " -------------------------"
				print " |           |           |"
				print " |     9     |    10     |"
				print " |           |           |"
				print " -------------------------"
				print " |           |           |"
				print " |     8     |     7     |"
				print " |           |           |"
				print " -------------------------"
				print " |           |           |"
				print " |     1     |     2     |"
				print " |           |           |"
				print " -------------------------\n\n"
				print "Duplication Print Failed!"
				logging.basicConfig(format='%(asctime)s %(message)s',datefmt='%m/%d/%Y %I:%M:%S %p', filename=str(fileEdit+'.log'),level=logging.DEBUG)
				logging.warning('---- Manipulate encountered a DUPLICATION ERROR on the REVEAL3D!:\r\n\n        "The zone that you entered is not valid for DUPLICATION!"\n        "Valid zones for Duplication are 1,2,8,7,9,10,15 and 16"\r\n\n         BedType: ' + str(BedType)+'\r\n         Zone Entered: '+ str(zone)+'\r\n\n')

				try:

					with open(str(fileEdit+'.log'), 'r') as myfile: 
						data = myfile.read().replace('\n', '')


					ts = "UPDATE yngPrints SET errorLog = " + data +" WHERE task_id = " + TASKID
					cur.execute(ts)
					db.commit()
					cur.close()
					db.close()



				except Exception as e:
					logging.basicConfig(format='%(asctime)s %(levelname)-8s %(message)s',datefmt='%m/%d/%Y %I:%M:%S %p', filename=str(fileEdit+'.log'),level=logging.DEBUG)
					# logging.warning('manipulateNEW.py encountered an ERROR!:  "'+str(e)+'"')
					# logging.debug('Debug: '+ str(e))
					# logging.info("Here's some INFO: \r\n")
					logger = logging.getLogger()
					handler = logging.StreamHandler()
					formatter = logging.Formatter(
					        '%(asctime)s %(name)-12s %(levelname)-8s %(message)s')
					handler.setFormatter(formatter)
					logger.addHandler(handler)			# Prints to console###
					logger.setLevel(logging.DEBUG)
					logger.exception("---> Fatal error in Manipulate <---")
					logger.debug('-------------------END------------------------\n\n\n')
					# logging.shutdown()
					raise
				os.remove(str(fileEdit+'.log'))
				sys.exit()

			if((BedType in ("GT")) & (zone not in (1,4))):
				print "\n"
				print "BedType entered: " + str(BedType)
				print "Zone Entered: " + str(zone)
				print "You entered an invalid zone for DUPLICATION!!!"
				print "Valid zones for the GT are: 1,4"
				print "\n    GT Graphic"
				print " ---------"
				print " |       |"
				print " |   4   |"
				print " |       |"
				print " ---------"
				print " |       |"
				print " |   1   |"
				print " |       |"
				print " ---------\n\n"
				print "Duplication Print Failed!"
				logging.basicConfig(format='%(asctime)s %(message)s',datefmt='%m/%d/%Y %I:%M:%S %p', filename=str(fileEdit+'.log'),level=logging.DEBUG)
				logging.warning('---- Manipulate encountered a DUPLICATION ERROR on the GT!:\r\n\n        "The zone that you entered is not valid for DUPLICATION!"\n        "Valid zones for Duplication are 1 and 4"\r\n\n         BedType: ' + str(BedType)+'\r\n         Zone Entered: '+ str(zone)+'\r\n\n')
				
				try:

					with open(str(fileEdit+'.log'), 'r') as myfile: 
						data = myfile.read().replace('\n', '')


					ts = "UPDATE yngPrints SET errorLog = " + data +" WHERE task_id = " + TASKID
					cur.execute(ts)
					db.commit()
					cur.close()
					db.close()



				except Exception as e:
					logging.basicConfig(format='%(asctime)s %(levelname)-8s %(message)s',datefmt='%m/%d/%Y %I:%M:%S %p', filename=str(fileEdit+'.log'),level=logging.DEBUG)
					# logging.warning('manipulateNEW.py encountered an ERROR!:  "'+str(e)+'"')
					# logging.debug('Debug: '+ str(e))
					# logging.info("Here's some INFO: \r\n")
					logger = logging.getLogger()
					handler = logging.StreamHandler()
					formatter = logging.Formatter(
					        '%(asctime)s %(name)-12s %(levelname)-8s %(message)s')
					handler.setFormatter(formatter)
					logger.addHandler(handler)			# Prints to console###
					logger.setLevel(logging.DEBUG)
					logger.exception("---> Fatal error in Manipulate <---")
					logger.debug('-------------------END------------------------\n\n\n')
					# logging.shutdown()
					raise
				os.remove(str(fileEdit+'.log'))
				sys.exit()





		# if((line == "B0\n") | (line == "B0\r\n")):                    # check for Duplication in line
		if((line[0] =="B")and(line[1]=="0")):                              # check for B0 without comments bugging it up (Updated^^)
			print "***YNG*** Found B0 in Line"
			# print line + "\n Printing in Duplciation Mode... "
			# DUPE_CHECK = 2
			# print "DUPE_CHECK is: " + str(DUPE_CHECK)
			# MAX_X = ((MAX_X/2)-10)
			# newFile.write(line)
			#if(Z < .6):
			#    print "saw Z"

			####SHOW AN ERROR IF NOT IN THE CORRECT ZONE NUMBER SET ############
			#if ((zone < 1) | (zone > 16)):
			# if((BedType in ("reveal3D","FRANK3")) & (zone not in (1,2,7,8,9,10,15,16))):
			#     print "BedType entered: " + str(BedType)
			#     print "Zone Entered: " + str(zone)
			#     print  "\n\n\nThe zone that you entered is not valid for DUPLICATION!!!"
			#     print "Valid zones for Duplication are 1,2,8,7,9,10,15 and 16"
			#     print "\n Zone graphic For Duplicate Mode"
			#     print " -------------------------"
			#     print " |           |           |"
			#     print " |    16     |    15     |"
			#     print " |           |           |"
			#     print " -------------------------"
			#     print " |           |           |"
			#     print " |     9     |    10     |"
			#     print " |           |           |"
			#     print " -------------------------"
			#     print " |           |           |"
			#     print " |     8     |     7     |"
			#     print " |           |           |"
			#     print " -------------------------"
			#     print " |           |           |"
			#     print " |     1     |     2     |"
			#     print " |           |           |"
			#     print " -------------------------\n\n"
			#     print "Duplication Print Failed!"
			#     sys.exit()

			# if((BedType in ("GT")) & (zone not in (1,4))):
			#     print "\n"
			#     print "BedType entered: " + str(BedType)
			#     print "Zone Entered: " + str(zone)
			#     print "You entered an invalid zone for DUPLICATION!!!"
			#     print "Valid zones for the GT are: 1,2,3,4"
			#     print "\n    GT Graphic"
			#     print " ---------"
			#     print " |       |"
			#     print " |   4   |"
			#     print " |       |"
			#     print " ---------"
			#     print " |       |"
			#     print " |   1   |"
			#     print " |       |"
			#     print " ---------\n\n"
			#     print "Duplication Print Failed!"
			#     sys.exit()


		elif((line == "B1\n") | (line == "B1\r\n")):  #B1 Command (TRIPLE COMMAND) Needs ZONE RANGE, Must be in "Y", nothing in "X"
			print line + "TRIPLE!"
			MAX_X = ((MAX_X/3)-30)

		elif((line == "B2\n") | (line == "B2\r\n")): #B2 Command (QUAD COMMAND) Needs Zone range, Must be in 'Y', Nothing in 'X'
			print line + "QUAD!"
			MAX_X = ((MAX_X/4)-40)

		elif((line == "B3\n") | (line == "B3\r\n")): #B3 command (QUINTUPLE!)
			print line + "QUINTUPLE!"
			MAX_X = ((MAX_X/5)-50)








		

		#         #####SHOW AN ERROR IF NOT IN THE CORRECT ZONE NUMBER SET ############
		# #if ((zone < 1) | (zone > 16)):
		# if zone not in (1,2,7,8,9,10,15,16):
		#     print  "\n\n\nThe zone that you entered is not valid!"
		#     print "Valid zones for Duplication are 1,2,8,7,9,10,15 and 16"
		#     print "Zone entered: " +str(zone)
		#     print "\n Zone graphic For Duplicate Mode"
		#     print " -------------------------"
		#     print " |           |           |"
		#     print " |    16     |    15     |"
		#     print " |           |           |"
		#     print " -------------------------"
		#     print " |           |           |"
		#     print " |     9     |    10     |"
		#     print " |           |           |"
		#     print " -------------------------"
		#     print " |           |           |"
		#     print " |     8     |     7     |"
		#     print " |           |           |"
		#     print " -------------------------"
		#     print " |           |           |"
		#     print " |     1     |     2     |"
		#     print " |           |           |"
		#     print " -------------------------\n\n"
		#     #sys.exit()

		if ((line[0] ==';') and (writeStart == 0)):         # adds the comments to the beginning of the file, also prevetns duplciaitng comments at the end
			newFile.write(line)
			# pass
		if ((line[0] =='^')):         # adds the comments to the beginning of the file, also prevetns duplciaitng comments at the end
			print line[0]
			print'found ^M'
		elif((line == "B98\n") | (line == "B98\r\n")):      # check for a known command before actual printing section starts
		# elif((line[0] =="B")and(line[1]=="9")and(line[2]=="8")):    ######################################
			newFile.write(line)
			print "\n"
			# print line + "First line found"
			print "Manipulating..."
			writeStart = 1              #^^^^^^lat
			#B commands for known command^^
	#    if(writeStart == 0):
	#       newFile.write(line)
	#   newFile.write(line)
	#   else:
	#       print "test"
		elif((line == "B99\n") | (line == "B99\r\n")):            # check for a known command before actual printing section starts
		# elif((line[0] =="B")and(line[1]=="9")and(line[2]=="9")):        # ^^ check without comments bugging it up
			print line + "Last Line Found"
			newFile.write(line)
			newFile.write("M104 T0 S0\n")       # extruder 0 off
			newFile.write("M104 T1 S0\n")
	####>>> newFile.write(the put together string from above commands) ie B10 T0 S150 being newFile.write("M104 T0 S150")
			# newFile.write("G91\n")                                      #relative positioning
			# newFile.write("G1 E-1 F300\n")                              #take pressure off nozzle
			# newFile.write("G1 Z+10 E-5 X-20 Y-20 F4200\n")              #Move up reduce more pressure move away from print
			# newFile.write("G90\n")                                      #Absolute positioning
			#newFile.write("B16 P0 S70 E0\n")                           #Disable Bed 1
			#newFile.write("B16 P1 S80 E0\n")
			#newFile.write("B16 P2 S70 E0\n")                           #Disable Bed 2
			#newFile.write("B16 P3 S80 E0\n")
			#newFile.write("B16 P4 S80 E0\n")
			#newFile.write("B16 P5 S80 E0\n")
			#newFile.write("B16 P6 S80 E0\n")
			#newFile.write("B16 P7 S80 E0\n")
			#newFile.write("B16 P8 S80 E0\n")
			#newFile.write("B16 P9 S80 E0\n")
			#newFile.write("B16 P10 S80 E1\n")
			#newFile.write("B16 P11 S80 E1\n")
			#newFile.write("B16 P12 S80 E1\n")
			#newFile.write("B16 P13 S80 E1\n")
			#newFile.write("B16 P14 S80 E0\n")
			#newFile.write("B16 P15 S80 E0\n"
			file_done = 1

		else:

			if((line[0] == 'B') | (line[0] == 'b')):
				#print "found AB"
				# print "this is the error" + line
				COMMAND, SUBARRAY, SUBPHRASEARRAY = lookupNew.Bcommand_lookup(line)
				#print COMMAND
				#print SUBARRAY
				#print SUBPHRASEARRAY
				c = 0

				if (COMMAND == 10):     #B command #10
					#print "B10"
					tmpCustom[0] = "M109 T" #Start making the first part of the gcode
					for x in SUBARRAY:
						c = c + 1
						if ((x == 'T')):
							tmpCustom[1] = str(SUBPHRASEARRAY[c-2])     #inject tool number
						# print "it found T"
						if ((x == 'S')):
							tmpCustom[2] = " S" + str(SUBPHRASEARRAY[c-2]) #inject space and temp value
						# print "it found S"
						if ((x == 'A')):        #This is currently wrong, but for show needs to be after dup,trip, quad to work properly
							tmpCustom[3] = " A" + str(SUBPHRASEARRAY[c-2])
						#   print "it found A"
					tmpCustomFull = tmpCustom[0] + tmpCustom[1] + tmpCustom[2] + tmpCustom[3]  #put it all together in order...
					#print tmpCustomFull
					#print what was made
					# newFile.write(tmpCustomFull + "\n") # was being written after bedcontrol.py implemented

				if (COMMAND == 16):
					bedCheck = 1
					print "B16"
					tmpCustom[0] = "B16 P"    # Start making the first part of the B-Code that the MC recognizes
					for x in SUBARRAY: #keep track of active beds, turn off at the endcustom array of 16 values, inject a 1 to each bed#?
						c = c + 1
						if ((x == 'P')):
							#print SUBPHRASEARRAY
							#print c
							#tmpCustom[1] = str(SUBPHRASEARRAY[c-2])   #inject possible new bed/zone number
							tmpCustom[1] = str(zone_beds[d])
							#print zone_beds
							#print tmpCustom[1]
							#print "found P"
						if ((x == 'S')):
							tmpCustom[2] = "S" + str(SUBPHRASEARRAY[c-2]) #inject space and bed temp value
							if(BedTemp <= 0):
								BedTemp = (SUBPHRASEARRAY[c-2])
							if(str(SUBPHRASEARRAY[c-2]) == 35):
								print "heres the culprit"
							# print 'Bed Temp is' + ' ' + str(SUBPHRASEARRAY[c-2])

						if ((x == 'E')):
							tmpCustom[3] = "E" + str(SUBPHRASEARRAY[c-2])
							#print "found E"
						tmpCustomFull = tmpCustom[0] + tmpCustom[1] + tmpCustom[2] + tmpCustom[3]  #put it all together in order...

	

		if((writeStart == 1) & (file_done == 0)):
			tempX = ['']*100000
			tempY = ['']*100000
			tempZ = ['']*100000
			tmpSX = ""
			tmpSY = ""
			tmpSZ = ""
			tmpS = ""
			tmpFullS = ""

	#if(((line == "M107\n") | (line == "M82\n") | (line == "M107\r\n") | (line == "M82\r\n")) & (writeStart == 0)): #check for known vlaue and start
		#if((line == ";start\n") & (writeStart == 0))): #check for known value and start
	#   writeStart = 1
	#   print "Test"    #This was a testing output hook so I could test if it was catching it
			if(writeStart == 1):
				getGCode = 0
				getNumberX = 0
				getNumberY = 0
				tc = 0
				numbersFound = 0
				tlCount = 0
				LineDone = 0
				tmpLineStart = ['']*250
				tmpLineEnd =['']*250
				semiColon = 0
				lineStepCounter = -1
				ModCode = 0
				bedFlag = 0
				writeBedLayer = 0
				writeDupeBed = 0
				sec_layer = 0
				if ((w_Check > 0) & (w_Check < 15)):
					# print str(w_Check) + 'isnt working'
					w_Check = w_Check + 1
				else:
					w_Check = 0
				#print "start" + line
				for x in line:              #lets find some numbers with the correct letters (X & Y)
					lineStepCounter = lineStepCounter + 1
					if(lineStepCounter == 0):
						if((tlCount == 0) & ((x == "M") | (x == "m"))):
							writeStart = 1
							# newFile.write(line)      # Was duplicating command (Pickleready project)
							if((tlCount == 0) & ((x == "M105") | (x == "m105"))):
								temperatureNEW = (tlCount == 0) & ((x =="M105") | (x == "m105"))
								# print temperatureNEW
								print "M commands are passed through"

	#####################################  M104 & M109 Write to manipulated file  ###################################################################
							if ((("M104" in line) | ("M109" in line)) & (w_Check == 0)):
								print "M104 & M109 Check " + line + str(w_Check)
								w_Check = 1
								if "S0" in line:
									if int(TOOL_LAYER1) > 0:
										if "M109" in line:
											newFile.write("M109 T0 S" + "0" + "\r\n")
										if "M104" in line:
											newFile.write("M104 T0 S" + "0" + "\r\n")
											print "M104 Extruder T0 Turned off"
									if int(TOOL_LAYER2) > 0:
										if "M109" in line and ("S0" not in line):
											newFile.write("M109 T1 S" + "0" + "\r\n")
											#M109_T1_Check = 1
										if "M104" in line:
											newFile.write("M104 T1 S" + "0" + "\r\n")
											print "M104 Extruder T1 Turned off"
									if int(TOOL_LAYER3) > 0:
										if "M109" in line and ("S0" not in line):
											newFile.write("M109 T2 S" + "0" + "\r\n")
										if "M104" in line:
											newFile.write("M104 T2 S" + "0" + "\r\n")
											print "M104 Extruder T2 Turned off"
									if int(TOOL_LAYER4) > 0:
										if "M109" in line and ("S0" not in line):
											newFile.write("M109 T3 S" + "0" + "\r\n")
										if "M104" in line:
											newFile.write("M104 T3 S" + "0" + "\r\n")
											print "M104 Extruder T3 Turned off"



								elif layer_Check == 0:
									if int(TOOL_LAYER1) > 0:
										if "M109" in line: #and ("S0" not in line):
											newFile.write("M109 T0 S" + TOOL_LAYER1 + "\r\n")
										if "M104" in line:
											newFile.write("M104 T0 S" + TOOL_LAYER1 + "\r\n")
									if int(TOOL_LAYER2) > 0:
										if "M109" in line: #and ("S0" not in line):
											newFile.write("M109 T1 S" + TOOL_LAYER2 + "\r\n")
											#M109_T1_Check = 1
										if "M104" in line:
											newFile.write("M104 T1 S" + TOOL_LAYER2 + "\r\n")
									if int(TOOL_LAYER3) > 0:
										if "M109" in line: #and ("S0" not in line):
											newFile.write("M109 T2 S" + TOOL_LAYER3 + "\r\n")
										if "M104" in line:
											newFile.write("M104 T2 S" + TOOL_LAYER3 + "\r\n")
									if int(TOOL_LAYER4) > 0:
										if "M109" in line: #and ("S0" not in line):
											newFile.write("M109 T3 S" + TOOL_LAYER4 + "\r\n")
										if "M104" in line:
											newFile.write("M104 T3 S" + TOOL_LAYER4 + "\r\n")
									layer_Check = 2
	######################################### FIRST LAYER TEMP AFTER THE VERY FIRST LAYER!!! #########################################################################
								elif (layer_Check == 1): #and (tempZfloat < .6): # Secondary First Layer. First after the First lAYER
									print "layer check 2"
									bedFlag = 1
									sec_layer = 0
									if int(TOOL_LAYER1) > 0:
										if "M109" in line and ("S0" not in line):
											newFile.write("M109 T0 S" + TOOL_LAYER1 + "\r\n")
										if "M104" in line:
											# M104_TOOL[0] = 1
											newFile.write("M104 T0 S" + TOOL_LAYER1 + "\r\n")
									if int(TOOL_LAYER2) > 0:
										if "M109" in line and ("S0" not in line):
											newFile.write("M109 T1 S" + TOOL_LAYER2 + "\r\n")
										if "M104" in line:
											# M104_TOOL[1] = 1
											newFile.write("M104 T1 S" + TOOL_LAYER2 + "\r\n")
									if int(TOOL_LAYER3) > 0:
										if "M109" in line and ("S0" not in line):
											newFile.write("M109 T2 S" + TOOL_LAYER3 + "\r\n")
										if "M104" in line:
											# M104_TOOL[2] = 1
											newFile.write("M104 T2 S" + TOOL_LAYER3 + "\r\n")
									if int(TOOL_LAYER4) > 0:
										if "M109" in line and ("S0" not in line):
											# M104_TOOL[3] = 1
											newFile.write("M109 T3 S" + TOOL_LAYER4 + "\r\n")
										if "M104" in line:
											newFile.write("M104 T3 S" + TOOL_LAYER4 + "\r\n")
									layer_Check = 2

	##################################### TRUE SECEDING LAYER #####################################################################################
								elif layer_Check >= 1: # True Seceding Layer
									print "Sec layer"
									bedFlag = 1
									sec_layer = 1
									if int(TOOL_SECLAYER1) > 0:
										if "M109" in line and ("S0" not in line):
											newFile.write("M109 T0 S" + TOOL_SECLAYER1 + "\r\n")
										if "M104" in line:
											newFile.write("M104 T0 S" + TOOL_SECLAYER1 + "\r\n")
											#M104_TOOL[0] = 1
									if int(TOOL_SECLAYER2) > 0:
										if "M109" in line and ("S0" not in line):
											newFile.write("M109 T1 S" + TOOL_SECLAYER2 + "\r\n")
										if "M104" in line:
											newFile.write("M104 T1 S" + TOOL_SECLAYER2 + "\r\n")
											#M104_TOOL[1] = 1
									if int(TOOL_SECLAYER3) > 0:
										if "M109" in line and ("S0" not in line):
											newFile.write("M109 T2 S" + TOOL_SECLAYER3 + "\r\n")
										if "M104" in line:
											newFile.write("M104 T2 S" + TOOL_SECLAYER3 + "\r\n")
											#M104_TOOL[2] = 1
									if int(TOOL_SECLAYER4) > 0:
										if "M109" in line and ("S0" not in line):
											newFile.write("M109 T3 S" + TOOL_SECLAYER4 + "\r\n")
										if "M104" in line:
											newFile.write("M104 T3 S" + TOOL_SECLAYER4 + "\r\n")
											#M104_TOOL[3] = 1
									layer_Check = 1
								else:
									print "WTF"

						


								if bedFlag == 1:
									print "this is DUPE_CHECK: "+str(DUPE_CHECK)
									if ((BedType == "reveal3D") and (DUPE_CHECK > 0)):
										print'1111DUPE_CHECK!!!!!!!!!!!!!!!!!!!:'+str(DUPE_CHECK)
										writeBedLayer = TOOL_BED1
										writeDupeBed = TOOL_BED2
										print'LAYER!!!!!!!!!:'+str(writeBedLayer)
										print'DUPE!!!!!!!!!!:'+str(writeDupeBed)

										if sec_layer == 1:
											writeBedLayer = TOOL_SECBED1
											writeDupeBed = TOOL_SECBED2
											print'1111LAYER!!!!!!!!!:'+str(writeBedLayer)
											print'11111DUPE!!!!!!!!!!:'+str(writeDupeBed)

									elif ((BedType == "reveal3D") and (DUPE_CHECK == 0)):
										# print'2222DUPE_CHECK!!!!!!!!!!!!!!!!!!!:'+str(DUPE_CHECK)
										writeBedLayer = TOOL_BED1
										writeDupeBed = TOOL_BED1
										# print'2222LAYER!!!!!!!!!:'+str(writeBedLayer)
										# print'22222DUPE!!!!!!!!!!:'+str(writeDupeBed)

										if sec_layer == 1:
											writeBedLayer = TOOL_SECBED1
											writeDupeBed = TOOL_SECBED1
											# print'seclayers Write!!!!!!!!!:'+str(writeBedLayer)
											# print'secLayers DUPE!!!!!!!!!!:'+str(writeDupeBed)

									if BedType == "reveal3D" or BedType == "FRANK3":
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
										# print "end of # 1"
										writeBeds.writeBeds(Zone_Max_X, Zone_Min_X, Zone_Max_Y, Zone_Min_Y, NumberXBeds, NumberYBeds, MAX_X, MAX_Y, x_16offset, x_GToffset, y_16offset, y_GToffset, BedType, DUPE_CHECK, writeHeatBedsActive, FORGOT_BEDS)
										if((FORGOT_BEDS[0] == 1) or (FORGOT_BEDS[0] == 2)):
											newFile.write("B16 P0 " + "S" + str(writeBedLayer) + " E1\n")
											print "Bed No.1 Seceding Layer Temp Updated!"
										if((FORGOT_BEDS[1] == 1) or (FORGOT_BEDS[1] == 2)):
											newFile.write("B16 P1 " + "S" + str(writeBedLayer) + " E1\n")
											print "Bed No.2 Seceding Layer Temp Updated!"
										if((FORGOT_BEDS[2] == 1) or (FORGOT_BEDS[2] == 2)):
											newFile.write("B16 P2 " + "S" + str(writeDupeBed) + " E1\n")
											print "Bed No.3 Seceding Layer Temp Updated!"
										if((FORGOT_BEDS[3] == 1) or (FORGOT_BEDS[3] == 2)):
											newFile.write("B16 P3 " + "S" + str(writeDupeBed) + " E1\n")
											print "Bed No.4 Seceding Layer Temp Updated!"
										if((FORGOT_BEDS[4] == 1) or (FORGOT_BEDS[4] == 2)):
											newFile.write("B16 P4 " + "S" + str(writeDupeBed) + " E1\n")
											print "Bed No.5 Seceding Layer Temp Updated!"
										if((FORGOT_BEDS[5] == 1) or (FORGOT_BEDS[5] == 2)):
											newFile.write("B16 P5 " + "S" + str(writeDupeBed) + " E1\n")
											print "Bed No.6 Seceding Layer Temp Updated!"
											print'writeBedLayer is the culprit????: '+str(writeDupeBed)
										if((FORGOT_BEDS[6] == 1) or (FORGOT_BEDS[6] == 2)):
											newFile.write("B16 P6 " + "S" + str(writeBedLayer) + " E1\n")
											print "Bed No.7 Seceding Layer Temp Updated!"
										if((FORGOT_BEDS[7] == 1) or (FORGOT_BEDS[7] == 2)):
											newFile.write("B16 P7 " + "S" + str(writeBedLayer) + " E1\n")
											print "Bed No.8 Seceding Layer Temp Updated!"
										if((FORGOT_BEDS[8] == 1) or (FORGOT_BEDS[8] == 2)):
											newFile.write("B16 P8 " + "S" + str(writeBedLayer) + " E1\n")
											print "Bed No.9 Seceding Layer Temp Updated!"
										if((FORGOT_BEDS[9] == 1) or (FORGOT_BEDS[9] == 2)):
											newFile.write("B16 P9 " + "S" + str(writeBedLayer) + " E1\n")
											print "Bed No.10 Seceding Layer Temp Updated!"
										if((FORGOT_BEDS[10] == 1) or (FORGOT_BEDS[10] == 2)):
											newFile.write("B16 P10 " + "S" + str(writeDupeBed) + " E1\n")
											print "Bed No.11 Seceding Layer Temp Updated!"
										if((FORGOT_BEDS[11] == 1) or (FORGOT_BEDS[11] == 2)):
											newFile.write("B16 P11 " + "S" + str(writeDupeBed) + " E1\n")
											print "Bed No.12 Seceding Layer Temp Updated!"
										if((FORGOT_BEDS[12] == 1) or (FORGOT_BEDS[12] == 2)):
											newFile.write("B16 P12 " + "S" + str(writeDupeBed) + " E1\n")
											print "Bed No.13 Seceding Layer Temp Updated!"
										if((FORGOT_BEDS[13] == 1) or (FORGOT_BEDS[13] == 2)):
											newFile.write("B16 P13 " + "S" + str(writeDupeBed) + " E1\n")
											print "Bed No.14 Seceding Layer Temp Updated!"
										if((FORGOT_BEDS[14] == 1) or (FORGOT_BEDS[14] == 2)):
											newFile.write("B16 P14 " + "S" + str(writeBedLayer) + " E1\n")
											print "Bed No.15 Seceding Layer Temp Updated!"
										if((FORGOT_BEDS[15] == 1) or (FORGOT_BEDS[15] == 2)):
											newFile.write("B16 P15 " + "S" + str(writeBedLayer) + " E1\n")
											print "Bed No.16 Seceding Layer Temp Updated!"

									if (BedType == "GT") and (DUPE_CHECK == 2):
										writeBedLayer = TOOL_BED1
										writeDupeBed = TOOL_BED2
										if sec_layer == 1:
											writeBedLayer = TOOL_SECBED1
											writeDupeBed = TOOL_SECBED2

									elif (BedType == "GT") and (DUPE_CHECK == 0):
										writeBedLayer = TOOL_BED1
										writeDupeBed = TOOL_BED1
										if sec_layer == 1:
											writeBedLayer = TOOL_SECBED1
											writeDupeBed = TOOL_SECBED1
									if BedType == "GT":
										# print "WritebedLayer is : " + str(writeBedLayer)
										# print "SEC0 WritebedLayer is : " + str(writeBedLayer)
										# print "WritebedLayer is : " + str(writeBedLayer)
										# print "SEC1 WritebedLayer is : " + str(writeBedLayer)

										writeBeds.writeBeds(Zone_Max_X, Zone_Min_X, Zone_Max_Y, Zone_Min_Y, NumberXBeds, NumberYBeds, MAX_X, MAX_Y, x_16offset, x_GToffset, y_16offset, y_GToffset, BedType, DUPE_CHECK, writeHeatBedsActive, FORGOT_BEDS)
										if((FORGOT_BEDS[0] == 1) or (FORGOT_BEDS[0] == 2)):
											newFile.write("B16 P0 " + "S" + str(writeBedLayer) + " E1\n")
											print "Bed No.1 Seceding Layer Temp Updated!"
										if((FORGOT_BEDS[1] == 1) or (FORGOT_BEDS[1] == 2)):
											newFile.write("B16 P1 " + "S" + str(writeDupeBed) + " E1\n")
											print "Bed No.2 Seceding Layer Temp Updated!"
										if((FORGOT_BEDS[2] == 1) or (FORGOT_BEDS[2] == 2)):
											newFile.write("B16 P6 " + "S" + str(writeDupeBed) + " E1\n")
											print "Bed No.3 Seceding Layer Temp Updated!"
										if((FORGOT_BEDS[3] == 1) or (FORGOT_BEDS[3] == 2)):
											newFile.write("B16 P7 " + "S" + str(writeBedLayer) + " E1\n")
											print "Bed No.4 Seceding Layer Temp Updated!"
	##################################################################################################
						if((tlCount == 0) & ((x == "G") | (x == "g"))):
							getGCode = 0
							if((tlCount == 0) & ((x != "G1 ") | (x != "g1 ") | (x != "G0 ") | (x != "g0 "))):
								 getGCode = 1
							# writeStart = 1
							# print "found G_Code"
							# newFile.write("ICU")
							# if((line[tlCount] != '1') & (line[tlCount] != '0')):           #Was duplicatiing G21 & G90 commands (PickleReady Project)
								# newFile.write("alsjlfjasldjflaskdjflajsdlfjalsjdf")
								# print x
								# print "not 0 or 1"
								# newFile.write(line)
								# print newFile.write(line)
								# break
						# if((getGCode == 1) & ((line[1] == "0") | (line[1] == "1") )):

						if((tlCount == 0) & (x == ";")):
							# writeStart = 1
							semiColon = semiColon + 1
							# print semiColon
							# print "we found a semi colon at the begininng throwing it away \n"
							# break
							# print tlCount
							# print line
					if((getGCode == 1) & (lineStepCounter == 1)):
						if ((x == "0") | (x == "1")):
							# print "I found 1 or 0 char"
							getGCode = 1
						else:
							getGCode = 2
					if((getGCode == 1) & (lineStepCounter == 2)):
						if (x == " "):
							# print "I found a space"
							getGCode = 1
						else:
							getGCode = 2
					if((getGCode == 1) & (semiColon < 1)):
						# print "ICU"
						# print tlCount
						if(semiColon == 0):
							if((getNumberY == 2) & (x != "\n") & (x != "\r")):    #this checks for line ending
								# print "found the end"
								tmpLineEnd[tlCount] = x
								tlCount = tlCount + 1
								getGCode = 1
							elif ((getNumberX == 0) & (x != "X") & (x != "\n") & (x != "\r")):
								# print line
								# print "tlCount"
								# print tlCount
								# print tmpLineStart
								tmpLineStart[tlCount] = x
								tlCount = tlCount + 1
								# print "get # X"
								getGCode = 1

							if (getNumberX == 1):
								if(x == ' '):
									getNumberX = 2
									numbersFound = numbersFound + 1
									# print "spaceX"
						#  if((tlCount == 1) & (getGCode == 1)):
								else:
									tempX[tc] = x
									# print tempX
									tc = tc + 1

							elif (getNumberY == 1):
								if((x == ' ') | (x == "\n") | (x == "\r")):
									getNumberY = 2
									numbersFound = numbersFound + 1
									# print "spaceY"
									tc = tc + 1
								else:
									# print x
									tempY[tc] = x
									# print tempY
									tc = tc + 1

							if (x == "X"):
								getNumberX = 1
								tc = 0
								tlCount = 0
							if (x == "Y"):
								getNumberY = 1
								tc = 0
								tlCount = 0
							if ((x == "\n") | (x == "\r")):
								LineDone = 1
								count = count + 1

							if ((numbersFound == 2) & (LineDone == 1)):
								numbersFound = 3 # changed from 0 to 3
								tempZ = lookupNew.Z_lookup(tmpLineEnd)
								if(CurrentMaxHeight < tempZ):
									CurrentMaxHeight = tempZ


								#To find your Z take tmpLineEnd and parse to look for Z like above with X and Y
									#you could send to a seperate function in order to make it a bit cleaner


								#print "debug line Start"
								#print line
								#print tempX
								#print tempY
								tmpSX = str(''.join(tempX))
								tmpSY = str(''.join(tempY))
								# print line
								# print tmpSX
								# print tmpSY
								if DUPE_CHECK > 0:
									x_16offset = (MAX_X/2)
									y_16offset = (MAX_Y/4)
								else:
									x_16offset = (MAX_X/4)
									y_16offset = (MAX_Y/4)
								# print "X16 OFFSET :" + str(x_16offset)
								# print "Y16 OFFSET :" + str(y_16offset)

								x_GToffset = (MAX_X/2) # dynamaic for reveal3D & FRANK3
								y_GToffset = (MAX_Y/2) # dynamic for GT (4-bed model)
								# print "x_GToffset :" + str(x_GToffset)
								# print "y_GToffset:" + str(y_GToffset)


								####16 bed start

								if((NumberYBeds*NumberXBeds) == 16):
									if((zone == 1) | (zone == 2) | (zone == 3) | (zone == 4)):
										tmpSY = str(float(tmpSY) + 0.0)
									if((zone == 5) | (zone == 6) | (zone == 7) | (zone == 8)):
										#tmpSY = str(float(tmpSY) + 214.0)
										tmpSY = str(float(tmpSY) + y_16offset)
									if((zone == 9) | (zone == 10) | (zone == 11) | (zone == 12)):
										#tmpSY = str(float(tmpSY) + 428.0)
										tmpSY = str(float(tmpSY) + (y_16offset*2))
									if((zone == 13) | (zone == 14) | (zone == 15) | (zone == 16)):
										#tmpSY = str(float(tmpSY) + 642.0)
										tmpSY = str(float(tmpSY) + (y_16offset*3))

									if((zone == 1) | (zone == 8) | (zone == 9) | (zone == 16)):
										#tmpSX = str(float(tmpSX) + 0.0)
										tmpSX = str(float(tmpSX))
										tmpS = str(''.join(tmpLineStart))
										#tmpS = "start " + str(''.join(tmpLineStart))
										tmpFullS = tmpS
										tmpS = tmpSX
										tmpFullS = tmpFullS + "X" + tmpS + " "
										tmpS = tmpSY
										tmpFullS = tmpFullS + "Y" + tmpS + " "
										tmpS = str(''.join(tmpLineEnd))
										tmpFullS = tmpFullS + tmpS + "\n"
										#tmpFullS = tmpFullS + tmpS + "end" + "\n"
										# print tmpFullS
										newFile.write(tmpFullS)
										#print tmpSY + "what Y"
										#print tmpSX + "what X"


									if((zone == 2) | (zone == 7) | (zone == 10) | (zone == 15)):
										# tmpSX = str(float(tmpSX) + 214.0)
										tmpSX = str(float(tmpSX) + x_16offset)
										tmpS = str(''.join(tmpLineStart))
										tmpFullS = tmpS
										tmpS = tmpSX
										tmpFullS = tmpFullS + "X" + tmpS + " "
										tmpS = tmpSY
										tmpFullS = tmpFullS + "Y" + tmpS + " "
										tmpS = str(''.join(tmpLineEnd))
										tmpFullS = tmpFullS + tmpS + "\n"
										#print tmpFullS
										newFile.write(tmpFullS)


									elif((zone == 3) | (zone == 6) | (zone == 11) | (zone == 14)):
										tmpSX = str(float(tmpSX) + x_16offset*2)
										tmpS = str(''.join(tmpLineStart))
										tmpFullS = tmpS
										tmpS = tmpSX
										tmpFullS = tmpFullS + "X" + tmpS + " "
										tmpS = tmpSY
										tmpFullS = tmpFullS + "Y" + tmpS + " "
										tmpS = str(''.join(tmpLineEnd))
										tmpFullS = tmpFullS + tmpS + "\n"
										# print tmpFullS
										newFile.write(tmpFullS)

									#print tmpSY + "what Y"
									#print tmpSX + "what X"


									elif ((zone == 4) | (zone == 5) | (zone == 12) | (zone == 13)):
										tmpSX = str(float(tmpSX) + x_16offset*3)
										tmpS = str(''.join(tmpLineStart))
										tmpFullS = tmpS
										tmpS = tmpSX
										tmpFullS = tmpFullS + "X" + tmpS + " "
										tmpS = tmpSY
										tmpFullS = tmpFullS + "Y" + tmpS + " "
										tmpS = str(''.join(tmpLineEnd))
										tmpFullS = tmpFullS + tmpS + "\n"
										#print tmpFullS
										newFile.write(tmpFullS)
								###### 16 bed end
								####4 bed start

								if((NumberYBeds*NumberXBeds) == 4):
									if((zone == 1) | (zone == 2)):# | (zone == 3) | (zone == 4)):
										tmpSY = str(float(tmpSY) + 0.0)
	#                                if((zone == 5) | (zone == 6) | (zone == 7) | (zone == 8)):
									if((zone == 3) | (zone == 4)):
										#tmpSY = str(float(tmpSY) + 214.0)
										tmpSY = str(float(tmpSY) + y_GToffset)
									#if((zone == 9) | (zone == 10) | (zone == 11) | (zone == 12)):
										#tmpSY = str(float(tmpSY) + 428.0)
									#    tmpSY = str(float(tmpSY) + (y_offset*2))
									#if((zone == 13) | (zone == 14) | (zone == 15) | (zone == 16)):
										#tmpSY = str(float(tmpSY) + 642.0)
									 #   tmpSY = str(float(tmpSY) + (y_offset*3))

									if((zone == 1) | (zone == 4)):# | (zone == 9) | (zone == 16)):
										#tmpSX = str(float(tmpSX) + 0.0)
										tmpSX = str(float(tmpSX))
										tmpS = str(''.join(tmpLineStart))
										#tmpS = "start " + str(''.join(tmpLineStart))
										tmpFullS = tmpS
										tmpS = tmpSX
										tmpFullS = tmpFullS + "X" + tmpS + " "
										tmpS = tmpSY
										tmpFullS = tmpFullS + "Y" + tmpS + " "
										tmpS = str(''.join(tmpLineEnd))
										tmpFullS = tmpFullS + tmpS + "\n"
										#tmpFullS = tmpFullS + tmpS + "end" + "\n"
										# print tmpFullS
										newFile.write(tmpFullS)
										#print tmpSY + "what Y"
										#print tmpSX + "what X"


									if((zone == 2) | (zone == 3)):# | (zone == 10) | (zone == 15)):
										# tmpSX = str(float(tmpSX) + 214.0)
										tmpSX = str(float(tmpSX) + x_GToffset)
										tmpS = str(''.join(tmpLineStart))
										tmpFullS = tmpS
										tmpS = tmpSX
										tmpFullS = tmpFullS + "X" + tmpS + " "
										tmpS = tmpSY
										tmpFullS = tmpFullS + "Y" + tmpS + " "
										tmpS = str(''.join(tmpLineEnd))
										tmpFullS = tmpFullS + tmpS + "\n"
										#print tmpFullS
										newFile.write(tmpFullS)


									

								if((float(tmpSY) > MAX_Y) | (float(tmpSX) > MAX_X)):
									print "Value exceeded the maximum print area allowed\n"
									print "X: " + tmpSX + "\n"
									print "Y: " + tmpSY + "\n"
									print "Z: " + tmpSZ + "\n"
									print "The program will now terminate !!!\n"
									print "MAX_X " +str(MAX_X)+ "\n"
									print "MAX_Y " +str(MAX_Y)+ "\n"
									ts = "UPDATE yngPrints SET statusValue = TERMINATED WHERE task_id = " + TASKID
									cur.execute(ts)

									db.commit()
									cur.close()
									db.close()

									newFile.close()
									logging.basicConfig(format='%(asctime)s %(message)s',datefmt='%m/%d/%Y %I:%M:%S %p', filename=str(fileEdit+'.log'),level=logging.DEBUG)
									logging.warning('---- Manipulate has encountered an ERROR on REVEAL3D!:\r\n\n'+'       ERROR: "Value exceeded the Maximum print area allowed"\r\n\n'+'    X: ' + tmpSX + '\n'+'    Y: ' + tmpSY + '\n'+'    Z: ' + tmpSZ + '\n'+'    MAX_X: ' +str(MAX_X)+ '\n'+'    MAX_Y: ' +str(MAX_Y)+ '\n\n')

									try:

										with open(str(fileEdit+'.log'), 'r') as myfile: 
											data = myfile.read().replace('\n', '')
										ts = "UPDATE yngPrints SET errorLog = " + data +" WHERE task_id = " + TASKID
										cur.execute(ts)
										db.commit()
										cur.close()
										db.close()



									except Exception as e:
										logging.basicConfig(format='%(asctime)s %(levelname)-8s %(message)s',datefmt='%m/%d/%Y %I:%M:%S %p', filename=str(fileEdit+'.log'),level=logging.DEBUG)
										logger = logging.getLogger()
										handler = logging.StreamHandler()
										formatter = logging.Formatter(
										        '%(asctime)s %(name)-12s %(levelname)-8s %(message)s')
										handler.setFormatter(formatter)
										logger.addHandler(handler)			# Prints to console###
										logger.setLevel(logging.DEBUG)
										logger.exception("---> Fatal error in Manipulate <---")
										logger.debug('-------------------END------------------------\n\n\n')
										# logging.shutdown()
										raise
									os.remove(str(fileEdit+'.log'))
									sys.exit()

								if(float(tmpSY) > Zone_Max_Y):
									Zone_Max_Y = float(tmpSY)
								if(float(tmpSY) < Zone_Min_Y):
									Zone_Min_Y = float(tmpSY)
								if(float(tmpSX) > Zone_Max_X):
									Zone_Max_X = float(tmpSX)
								if(float(tmpSX) < Zone_Min_X):
									Zone_Min_X = float(tmpSX)

								# print Zone_Max_X
								# print Zone_Max_Y
								# print Zone_Min_X
								# print Zone_Min_Y

				if((numbersFound == 0) & (LineDone == 1) & (semiColon == 0)):
					# print "calling at 2"
					# ### For Debugging Logs### #
						# if not UPS:
						# 	FedEx
					tempZ = lookupNew.Z_lookup(tmpLineStart)
					if "E" in line:
						# print "this is E: " + line
						newFile.write(line)
					if (tempZ != -1):
						tempZfloat = tempZ
						# print "this is the missing Z: " + line
						newFile.write(line)
					if ((getGCode >= 1) & ("Z" not in line) & ("E" not in line) & ("X" not in line) & ("Y" not in line)):
						newFile.write(line)
						print "we found something without XY or Z"
						print line
					# if(tempZ != -1):
					#     print tempZ                       # Z values while ignoring the -1 from Lookup.py
					#     if(tempZ < .6):
					#         FIRST_LAYER_CHECK[0] == 1
					#         print "found first layer"

					#     if((tempZ < .6) & (SEC_LAYER_CHECK[0] == 1)):
					#         FIRST_LAYER_CHECK[0] == 2
					#         print "This is the first layer....again"
					#         # print line

					#     if("M104" in line):
					#         SEC_LAYER_CHECK[0] = 1
					#         print "This is a seceding layer"
					#         # print tempZ
					#         # print line

					if(CurrentMaxHeight < tempZ):
						CurrentMaxHeight = tempZ





				if (((semiColon == 1) | (getGCode > 1) | (getGCode == 0)) & (ModCode == 0)):
					# if(("M104" in line) or ("M109" in line)):
					if((line[0] =="M")and(line[1]=="1")and(line[2]=="0")&(line[3]=="4") or (line[0] =="M")and(line[1]=="1")and(line[2]=="0")and(line[3]=="9") or (bedCheck == 1)):
						print "make it go away POOF " + line
						bedCheck = 0
					else:
						newFile.write(line)
						# print "here's the line: " + line
						semiColon = 2
					# print "semi"+line
				# time.sleep(1) # 1 second sleep


	if d > 0:
		for T in range(d):
			print "zone" + " " + str(zone_beds[T])
	else:
		print "zone" + str(d)



	print "\n" + "Max X: " + str(Zone_Max_X)
	print "Min X: " + str(Zone_Min_X) + "\n"
	print "Max Y: " + str(Zone_Max_Y)
	print "Min Y: " + str(Zone_Min_Y) + "\n"
	print "Max Z: " + str(CurrentMaxHeight) + "\n"

	# print "Manipulate's M-Command Values:"
	# print "M104 T0: " + str(M104_TOOL[0])
	# print "M104 T1: " + str(M104_TOOL[1])
	# print "M104 T2: " + str(M104_TOOL[2])
	# print "M104 T3: " + str(M104_TOOL[3])
	#
	# print "M109 T0: " + str(M109_TOOL[0])
	# print "M109 T1: " + str(M109_TOOL[1])
	# print "M109 T2: " + str(M109_TOOL[2])
	# print "M109 T3: " + str(M109_TOOL[3])



	##################################### BedControl Functions #######################################################



	newFile.close()
	# bedControl.zoneValues(Zone_Max_X, Zone_Min_X, Zone_Max_Y, Zone_Min_Y, newFile, newFileLocation)     # Writes Values to tempFile
	# bedControl.createTemp(newFile, newFileLocation)

	print "passing bed temp: " + str(BedTemp)
	bedControl.activateBeds(Zone_Max_X, Zone_Min_X, Zone_Max_Y, Zone_Min_Y, newFile, newFileLocation,FinalFileLocation, BedTemp, BedType, NumberXBeds, NumberYBeds, MAX_X, MAX_Y, x_16offset, x_GToffset, y_16offset, y_GToffset, TOOL_BED1, TOOL_BED2, TOOL_BED3, TOOL_BED4, DUPE_CHECK, TOOL_LAYER1, TOOL_LAYER2, TOOL_LAYER3, TOOL_LAYER4, TOOL_SECLAYER1, TOOL_SECLAYER2, TOOL_SECLAYER3, TOOL_SECLAYER4, M104_TOOL, M109_TOOL)     # Checks which to turn ON/OFF
	# gInject.gInject(Zone_Max_X, Zone_Min_X, Zone_Max_Y, Zone_Min_Y)
	# bedControl.killBedData()                                                                            # Deletes tempFile


	##################################################################################################################



	####################################################################################
	#Following variables are used to send data to DB
	bigmaxX = str(Zone_Max_X)
	smallminX = str(Zone_Min_X)
	bigmaxY = str(Zone_Max_Y)
	smallminY = str(Zone_Min_Y)
	bigmaxZ = str(CurrentMaxHeight)
	statusValue = "done"
	printerType = str(BedType)


	# Try block attempts to update table with new values from output of manipulate
	try:
	   ts = "UPDATE yngPrints SET statusValue = " + statusValue + ", bigmaxX=" + bigmaxX +", smallminX=" + smallminX + ", bigmaxY=" +bigmaxY +", smallminY=" + smallminY +", bigmaxZ=" + bigmaxZ +", printerType="+printerType+" WHERE task_id = " + TASKID 
	   cur.execute(ts)
	   db.commit()
	   print TASKID + " TASKID UPDATING " + statusValue
	   print BedType + "BedType UPDATING" + statusValue
	#Exception prints sql errors
	except MySQLdb.Error, e:
		try:
			print "MySQL Error [%d]: %s" % (e.args[0], e.args[1])
		except IndexError:
			print "MySQL Error: %s" % str(e)



	# cur.close()
	# db.close()
######################################################################################

### logging exception ###
except Exception as e:
	logging.basicConfig(format='%(asctime)s %(levelname)-8s %(message)s',datefmt='%m/%d/%Y %I:%M:%S %p', filename='asdas',level=logging.DEBUG)
	# logging.warning('manipulateNEW.py encountered an ERROR!:  "'+str(e)+'"')
	# logging.debug('Debug: '+ str(e))
	# logging.info("Here's some INFO: \r\n")
	logger = logging.getLogger()
	handler = logging.StreamHandler()
	formatter = logging.Formatter(
	        '%(asctime)s %(name)-12s %(levelname)-8s %(message)s')
	handler.setFormatter(formatter)
	logger.addHandler(handler)			# Prints to console###
	logger.setLevel(logging.DEBUG)
	logger.exception("---> Fatal error in Manipulate <---")
	logger.debug('-------------------END------------------------\n\n\n')
	# logging.shutdown()



try:

	if os.path.isfile(str(fileEdit+'.log')):
		print "Log Exists....Sending to DB"
		with open(str(fileEdit+'.log'), 'r') as myfile: 
			data = myfile.read().replace('\n', '')
		ts = "UPDATE yngPrints SET errorLog = " + data +" WHERE task_id = " + TASKID
		cur.execute(ts)
		db.commit()
		cur.close()
		db.close()
	else:
		print "No Errors Detected... Log Not sent to DB"



except Exception as e:
	logging.basicConfig(format='%(asctime)s %(levelname)-8s %(message)s',datefmt='%m/%d/%Y %I:%M:%S %p', filename=str(fileEdit+'.log'),level=logging.DEBUG)
	logger = logging.getLogger()
	handler = logging.StreamHandler()
	formatter = logging.Formatter(
	        '%(asctime)s %(name)-12s %(levelname)-8s %(message)s')
	handler.setFormatter(formatter)
	logger.addHandler(handler)			# Prints to console###
	logger.setLevel(logging.DEBUG)
	logger.exception("---> Fatal error in Manipulate <---")
	logger.debug('-------------------END------------------------\n\n\n')
	# logging.shutdown()
	raise


#print line
#print count
#file.close()

# ### Check if Log Exists, Delete Log File After Upload ### #

if os.path.isfile(str(fileEdit+'.log')):
	os.remove(str(fileEdit+'.log'))
	print "Log Existed"
else:
	print "No Error Log to Remove"


cur.close()
db.close()

sys.exit()
