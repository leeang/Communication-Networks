# -*- coding: utf-8 -*-
"""
Created on Mon Jul 14 18:42:28 2014

HINTS: 
1) Analyse the script from bottom to top
2) Fill in the blanks marked with ???



@author: alpcan
"""

import numpy as np
from wsmmphelper import *
#parameters

maxsteps=int(1E5)   # simulation steps
srate=3             # service rate
arate=5             # arrival rate
parallel=2          # nbr of parallel mm1's

simulation=DESmm1parallel(srate,arate,parallel,maxsteps)

for i in range(maxsteps):
    intarrive=np.random.exponential(1.0/arate)  # interarrival time
    simulation.packetarrival(intarrive)
    servetime=np.random.exponential(1.0/srate)  # service time
    simulation.nextstep(servetime)
    
simulation.practicalcalc(parallel)
