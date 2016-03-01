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

maxsteps==int(1E5)      # simulation steps
srate=3                 # service rate
arate=5                 # arrrival rate
nbrservers=2            # number of servers

simulation=DESmmc(srate,arate,nbrservers,maxsteps)

for i in range(maxsteps):
    intarrive=1.0/arate  # interarrival time
    simulation.packetarrival(simulation.Q,intarrive)
    servetime=1.0/srate  # service time
    simulation.nextstep(servetime)
    
simulation.practicalcalc()
Theoreticalmmk(srate,arate,nbrservers)
