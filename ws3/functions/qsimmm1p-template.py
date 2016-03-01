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

maxsteps=???    # simulation steps
srate=???       # service rate
arate=???       # arrrival rate
parallel=???    # nbr of parallel mm1's

simulation=DESmm1parallel(srate,arate,parallel,maxsteps)

for i in range(maxsteps):
    intarrive=???
    simulation.packetarrival(intarrive)
    servetime=???
    simulation.nextstep(servetime)
    
simulation.practicalcalc(parallel)
#theory=Theoreticalmm1(srate,arate,parallel)
#theory.printtheory()