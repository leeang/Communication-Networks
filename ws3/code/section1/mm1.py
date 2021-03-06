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
    meandelay = 1/(srate-arate)
    rho = float(arate)/float(srate)
    meansize = rho/(1-rho)
    
    # Hint for display...
    print 'Mean theoretical delay: {:4f} \n'.format(meandelay)
    print 'Mean theoretical size : {:4f} \n'.format(meansize)


###########################################################
## Main program

# parameters

maxsteps=int(1E5)   # simulation steps
srate=4             # service rate
arate=3             # arrival rate


# create simulation
simulation=DESmm1(srate,arate,maxsteps)

# main loop
for i in range(maxsteps):
    intarrive=np.random.exponential(1.0/arate)  # interarrival time
    simulation.packetarrival(intarrive)
    servetime=np.random.exponential(1.0/srate)  # service time
    simulation.nextstep(servetime)

# calculate and print theoretical values
# you can also do this in Matlab if you prefer!
Theoreticalmm1(srate,arate)

# calculate and print practical delay, size values
# optionally visualise
simulation.practicalcalc(True,True)
