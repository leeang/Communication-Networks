# -*- coding: utf-8 -*-
"""
Created on Mon Jul 14 18:42:28 2014

HINTS: 
1) Analyse the script from bottom to top
2) Fill in the blanks marked with ???


@author: alpcan
"""

import math
import numpy as np
from wsmmchelper import *
   

def Theoreticalmmk(srate,arate,k):

    '''
    ??? 'You can optionally do this in Matlab, if you wish!'
    '''
    
    # Hint for display...
    #print 'Mean theoretical delay: {:4f} \n'.format(meandelay)
    #print 'Mean theoretical size : {:4f} \n'.format(meansize)
    

#parameters

maxsteps=???         # simulation steps
srate=???            # service rate
arate=???            # arrrival rate
nbrservers=???       # number of servers 

simulation=DESmmc(srate,arate,nbrservers,maxsteps)

for i in range(maxsteps):
    intarrive=???    # interarrival time
    simulation.packetarrival(simulation.Q,intarrive)
    servetime=???    # service time
    simulation.nextstep(servetime)
    
simulation.practicalcalc()
Theoreticalmmk(srate,arate,nbrservers)

