import MySQLdb
import sys
import os
import datetime
import time
import subprocess
import multiprocessing
from multiprocessing import Pool


######  This is our CronJob management program   #######


#This file will run inside the 'CronJob' area to upload printer files 


#  Below, we connect to our SQL DB
db = MySQLdb.connect(host="localhost", user="printerUser", passwd="yngprinter17!", db="manipulate")

#python-mysqldb
#Cursor object will execute queries
cur = db.cursor()

#SQL Query to select all 'new' uploaded files--------------------------------

cur.execute("SELECT * FROM yngPrints WHERE statusValue = 'new' LIMIT 3")

#Below, we have different lists to hold values we will use to upload info to our DB
taskNumList = []
locList = []
zoneList = []
progList = []
statusList = []
bedList = []

#This for loop will sort through th entire query return, and add information to the different lists
for row in cur.fetchall():
    print row
    taskNumList.append(str(row[0]))
    locList.append(str(row[2]))
    statusList.append(str(row[4]))
    progList.append(row[10])
    bedList.append(str(row[12]))
    zoneList.append(str(int(row[3])))

    
#These print statements will print out info based on what is being used, where it's printing, and the progress of the print
print '\n'
print ("Printer selcted:")
print bedList
print '\n'
print "Location List is:"
print locList
print "\n"
print "Zone Array is: "
print zoneList
print "\n"
print "Progress Check is:"
print progList
print "Current status is"
print statusList


#---- Second Select Query for "IN PROGRESS" files ------

#our next Query will grab all products in progress
#These files are in progress because the printer has not told us tha they are finished printing
cur.execute("SELECT * FROM yngPrints WHERE statusValue = 'INPROGRESS'")

updateID = []
updateTaskID = []
updateProgCheck = []

#for loop will fetch important information regarding each INPROGRESS file
for row in cur.fetchall():
    print "Prog row values ----: "
    print row
    updateTaskID.append(str(row[0]))
    updateID.append(str(row[4]))
    updateProgCheck.append(str(row[10]))        

print '\n'
#Print out all files in Progress
print "LIST --- InProgress: "
print updateID

#Now that all checks are over, we use a function called 'f' to make asynchronouse calls to our 'manipulate' file
#This way, we can process up to 3 files at the same time which increase speed of upload/appends on the server
def f(x):
    #First, we make our DB SQL connection
    db = MySQLdb.connect(host="localhost", user="printerUser", passwd="yngprinter17!", db="manipulate")
    cur = db.cursor()
    #after a successful connection...try...
    try:
        #if we have elements in statusList...
        if statusList:
        #if the statusList element is 'new'...
	    if statusList[x] == "new":
                print "Status of row was new"
                #update progess in DB to show file is now INPROGRESS
                cur.execute("UPDATE yngPrints SET statusValue = %s WHERE task_id=%s", ("INPROGRESS", taskNumList[x]))
                db.commit()
	if updateID:
        #if elements are in updateID...
	    print "update array accessed"
            print "TaskID  is " + updateTaskID[x]
            #if the updateID file is "INPROGRESS", we know the file is till being processed by manipulate
            if updateID[x] == "INPROGRESS":
                #if updateProgCheck has elements in it...we know the progess check has changed
                if updateProgCheck:
                    print "=========================== terminate cuz progCheck = " + updateProgCheck[x]
                    #each time the cronjob runs, it will add a value to the 'updateProgcheck'
                    #we use this to check how long the files are being progressed, and if it takes to long, we terminate it
                    #so other files have a chance to process
                    progValue = int(updateProgCheck[x])
                    #So, if the progValue is less then 11...
                    if progValue < 11:
                        #update the progValue by 1
                        cur.execute("UPDATE yngPrints SET progCheck = progCheck + 1 WHERE task_id = %s", (updateTaskID[x]))
                        #print Debug info to show interval updated
                        printVar = ""
                        print ".....Interval Update......"
                        db.commit()
                        print "++++++++++++++++"
                    else:
                        #else, update DB if progValue is over max capactity, terminating the file 
                        cur.execute("UPDATE yngPrints SET statusValue = %s WHERE task_id=%s", ("TERMINATED", updateTaskID[x]))
                        db.commit()
                        print ".....Delete Update......"
    
    #if our try fails, print out errors
    except MySQLdb.Error, e:
        try:
            print "MySQL Error [%d]: %s" % (e.args[0], e.args[1])
        except IndexError:
            print "MySQL Error: %s" % str(e)

    #Call Subprocess
    print "************"
    #declare our bash command 'printVar' variable that will call on 'manipulate' to process file
    #the command must have the zone area(zoneList[x]), location(locList[x]), and bed(bedList[x]) where the print is used 
    printVar = "python /var/www/html/Manipulate/yng_manipulate/manipulateNEW.py " + zoneList[x] + " " + "'"+locList[x] +"'"+ " " + " " + bedList[x] + " " + taskNumList[x]
    print printVar
    #Below, we call on our subprocess to start the manipulation
    subprocess.call(printVar, shell=True)
    print "subprocess called"
    return printVar
    #close our db connections
    cur.close
    db.close

#result_list is an array used for gathering the results of all our async calls
#not really necessary at this point, we used them for debugging
result_list= []
def log_result(result):
    result_list.append(result)
    #This print statement shows end of the RunManip.py file
    print "callback reached, all pools processed"

#  the 'apply_async_with_callback() function will run all of our multiprocessing files
def apply_async_with_callback():
    #declare 'pool' as our mutliprocess reference
    pool = multiprocessing.Pool()
    #print a line to show async call accessed - DEBUG -
    print "Async call back accessed"
    #this loop will run 4 times, calling on our 'f' function each
    for i in range(4):
         pool.apply_async(f, args = (i, ), callback = log_result)
    #after multiprocessing ends, we close the pool, and our DB conenctions again to be safe
    pool.close()
    pool.join()
    cur.close()
    db.close()

#our MAIN call, which runs the async function
if __name__ == '__main__':
    #call to our function
    apply_async_with_callback()

print '\n'
