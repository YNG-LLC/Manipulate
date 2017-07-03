# tabs = 4 spaces
##### This finalFunction.py is called in bedControl.py when the heat beds are deactivated.
###### This function will write at the end of all manipulated files.

import os
import sys
import logging

def do_something():
    logging.info('Logging finalFunction.py: ')





def finalFunction(cloneFile):
    cloneFile.write("M18 E0\n")
