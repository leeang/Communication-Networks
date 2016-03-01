# -*- coding: utf-8 -*-
"""
Created on Tue Jul 15 11:43:50 2014

Classes to help ELEN90061 Workshop Simulation

@author: alpcan
"""

import math
import numpy as np
import heapq as hq
from collections import deque as dq
import matplotlib.pylab as plt

class EventQueue:
    # This is a priority queue
    
    #initevents    
    def __init__(self,initevents):
        self.events=initevents
        hq.heapify(self.events)
        
    def size(self):
        return len(self.events)
    
    def get(self):
        return hq.heappop(self.events)
        
    def put(self,item):
        hq.heappush(self.events,item)
        
    def reset(self):
        self.events=[]
    
    def isempty(self):
        if len(self.events)==0:
            return True
        else:
            return False
        
class Queue:
    
    #initevents    
    def __init__(self,inputitems):
        self.queue=dq(inputitems)
        self.busy=0     # is the queue busy? 
        # system occupancy evolution for each Q: (timestamp, size)
        self.Qevolution=[(0.,0)] 
        self.arrtimes=[]     # arrival times
        self.deptimes=[]     # departure times
        self.delays=[]       # delays
        
    def size(self):
        return len(self.queue)
    
    def get(self):
        return self.queue.pop()
        
    def put(self,item):
        self.queue.appendleft(item)
        
    def reset(self):
        self.queue.clear()

    def isempty(self):
        if len(self.queue)==0:
            return True
        else:
            return False
    
    def setbusy(self,untiltime):
        # set it busy until current packet is processed
        self.busy=untiltime 
    
    def setfree(self):
        self.busy=0



class DESmm1parallel:
    
    #init   
    def __init__(self,srate,arate,parallel,maxsteps):
        
        ## internal variables
        self.simtime=0.0     # simulation time
        self.simtimes=[0.0]
        self.packetnbr=0     # packet number
        self.simarrtimes=[0.0]
        self.parallel=parallel
        
        #input
        self.maxsteps=maxsteps
        self.srate=srate
        self.arate=arate

        # event queue
        self.Events=EventQueue([])   # events
        
        # init mm1 Queues
        self.Q=[Queue([]) for i in range(parallel)]
     
        
        
    def packetarrival(self,intarrivaltime):
        # packet arrival
        arrtime=self.simarrtimes[-1]+intarrivaltime
        self.packetnbr +=1
        self.simarrtimes.append(arrtime)
        
        # assign packet to one of the queues
        intervals=np.linspace(0.,1.,self.parallel+1)
        randval=np.random.random()
        qindex=sum([1 for x in intervals if randval>x])-1
        self.Events.put((arrtime,self.packetnbr,qindex,'queued'))

        
    def processqueue(self,Q,currevent,simtime,servetime):

        Q.arrtimes.append(currevent[0])
        
        # if an arrival event
        if 'queued' in currevent:
            #print "queued at"+str(currevent[0]) 
        
                  
            # determine departure time
            #servetime=np.random.exponential(1.0/srate)
            
            # process it if queue is not busy                    
            if Q.busy==0:
                # packet is immediately processed, not queued!
                deptime=simtime+servetime
                #print "process to finish at"+str(deptime)
            else: # the queue is busy 
                Q.put(currevent)
                # packet is queued!
                
                # determine departure time
                deptime=Q.deptimes[-1]+servetime
            
            # create departure event and time
            Q.setbusy(deptime) #### !!!!!!!!!!!!!!!!!!!!!!!

            # record timestamp and system size
            # as seen by the arrival!!
            # either zero or Qsize+1 (one currently served)
            Q.Qevolution.append((currevent[0],Q.size()))
            
            
            # update events
            self.Events.put((deptime,currevent[1],currevent[2],'served'))  
            Q.deptimes.append(deptime)
            Q.delays.append(deptime-simtime)
            #print "arr at"+str(simtime)+" dept at "+str(deptime)
        
        # process departure event  
        else:
            # if the queue is not empty
            # get next one
            if not Q.isempty():        
                Q.get()
                # if you want do something here, e.g. forward
            # if the server is not busy, mark it as such
            if simtime>=Q.busy:
                Q.setfree()
            #print "departure at"+str(currevent[0])
        
    def nextstep(self,servicetime):
                      
        # process current event
        currevent=self.Events.get()
        # update simulation time
        self.simtime=currevent[0]
        self.simtimes.append(self.simtime)
        
        self.processqueue(self.Q[currevent[2]],currevent,self.simtime,servicetime)
        
    def practicalcalc(self,parallel):
        
        avgpracticaldelay=np.zeros(parallel)
        avgpracticalsize=np.zeros(parallel)
        for i in range(parallel):
            delays=np.array(self.Q[i].delays)
            avgpracticaldelay[i]=np.mean(delays)
        
            # extract queue evolution
            times,qsize=zip(*self.Q[i].Qevolution) 
            
            systemsize=np.array(qsize)
            # take into account only the processed portion
            systemsize=systemsize[0:len(self.Q[i].delays)]
            avgpracticalsize[i]=np.mean(systemsize)
        

            print 'Q{} mean practical delay: {:4f} \n'.format(i,
                                                        avgpracticaldelay[i])
            print 'Q{} mean practical size : {:4f} \n'.format(i,
                                                        avgpracticalsize[i])             
        

        avgdelaycombined=np.mean(avgpracticaldelay)
        avgsizecombined=sum(avgpracticalsize)
        
        print 'Combined mean practical delay: {:4f} \n'.format(
                                                        avgdelaycombined)
        print 'Combined mean practical size : {:4f} \n'.format(
                                                        avgsizecombined)