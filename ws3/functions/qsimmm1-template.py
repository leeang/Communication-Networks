# -*- coding: utf-8 -*-
"""
Created on Tue Jul 15 12:16:53 2014

HINTS: 
1) Analyse the script from bottom to top
2) Fill in the blanks marked with ???

@author: alpcan
"""

import numpy as np
import matplotlib.pylab as plt
from wsmm1helper import *



def Theoreticalmm1(srate,arate):
    ''' 
    Theoretically calculates and prints mean delay and system size. 
    
    Inputs: service and arrival rates.
    '''
    
    '''
    ??? 'You can optionally do this in Matlab, if you wish!'
    '''
    
    # Hint for display...
    #print 'Mean theoretical delay: {:4f} \n'.format(meandelay)
    #print 'Mean theoretical size : {:4f} \n'.format(meansize)


###########################################################
## Main program

# parameters

maxsteps=????    # simulation steps
srate=???        # service rate
arate=???        # arrival rate


# create simulation
simulation=DESmm1(srate,arate,maxsteps)

# main loop
for i in range(maxsteps):
    intarrive=????  # interarrival time
    simulation.packetarrival(intarrive)
    servetime=???   # service time
    simulation.nextstep(servetime)

# calculate and print theoretical values
# you can also do this in Matlab if you prefer!
Theoreticalmm1(srate,arate)

# calculate and print practical delay, size values
# optionally visualise
simulation.practicalcalc(True,True)




