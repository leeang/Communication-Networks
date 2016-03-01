# -*- coding: utf-8 -*-
"""
Created on Tue Jul 15 11:43:50 2014

Classes to help ELEN90061 Workshop MM1 Simulation

@author: alpcan
"""

import heapq as hq
from collections import deque as dq
import numpy as np
import matplotlib.pylab as plt

class EventQueue:
    '''
    This class handles discrete events in the simulator. It is a 
    (reverse) priority queue, i.e. the event with the smallest first
    item is output first.
    Methods: size, get, put, reset, isempty
      
    The event objects can be anything but we assume a list with time
    being the first list item. EventQueue returns then the earliers 
    event object/list first.
    
    EventQueue is based on heapq and is a list.
    '''
    
    #initevents    
    def __init__(self,initevents):
        ''' initialise EventQueue with a list of events  '''
        self.events=initevents
        hq.heapify(self.events)
        
    def size(self):
        ''' return EventQueue list size  '''
        return len(self.events)
    
    def get(self):
        ''' get the earliest event from EventQueue.  '''
        return hq.heappop(self.events)
        
    def put(self,item):
        ''' put a new event to EventQueue.  '''
        hq.heappush(self.events,item)
        
    def reset(self):
        ''' clear all events in EventQueue.  '''
        self.events=[]
    
    def isempty(self):
        ''' return True if EventQueue is empty, False otherwise.  '''
        if len(self.events)==0:
            return True
        else:
            return False
        
class Queue:
    '''
    A basic FIFO Queue with a single server. 
    Implementation is based on collections.deque, and is a list.
    
    Methods: size, get, put, reset, isempty, setbusy, setfree
    
    '''    
    
    def __init__(self,inputitems):
        ''' initialise Queue with a list of items  '''
        self.queue=dq(inputitems)
        self.busy=0     # is the queue busy?  
        
    def size(self):
        ''' return Queue size  '''
        return len(self.queue)
    
    def get(self):
        ''' get the first-in item in Queue.  '''
        return self.queue.pop()
        
    def put(self,item):
        ''' put a new item to Queue (will be last out).  '''
        self.queue.appendleft(item)
        
    def reset(self):
        ''' clear all items in Queue.  '''
        self.queue.clear()

    def isempty(self):
        ''' return True if Queue is empty, False otherwise.  '''
        if len(self.queue)==0:
            return True
        else:
            return False
    
    def setbusy(self,untiltime):
        ''' set the server busy until given time  '''
        # set it busy until current packet is processed
        self.busy=untiltime 
    
    def setfree(self):
        ''' set the server free.  '''
        self.busy=0


class DESmm1:
    ''' Main MM1 DES class'''

    def __init__(self,srate,arate,maxsteps):
        ''' 
        Initialise simulation. 
        
        Inputs: servicerate,arrivalrate,maxsteps)   
        '''
        
        ## internal variables
        self.simtime=0.0     # simulation time
        self.simtimes=[0.0]  # record simulation times
        self.arrtimes=[0.0]  # arrival times
        self.deptimes=[]     # departure times
        self.delays=[]       # delays
        self.packetnbr=0     # packet number
        # system occupancy evolution: (timestamp, size)
        self.Sysevolution=[(0.,0)] 
        
        #inputs to internal variables
        self.maxsteps=maxsteps
        self.srate=srate
        self.arate=arate

        # Create an empty event queue
        self.Events=EventQueue([])   # events
        
        # init mm1 Queue
        self.Q=Queue([])     # queue 
        
        # first packet arrives in the beginning 
        # just a choice, doesn't have to be so...
#        self.Events.put((self.simtime,self.packetnbr,'queued'))
#        self.packetnbr +=1
#        self.arrtimes.append(self.simtime)
        
    def packetarrival(self,intarrivaltime):
        ''' One packet randomly arrives with given rate'''
        # packet arrival
        arrtime=self.arrtimes[-1]+intarrivaltime
        self.Events.put((arrtime,self.packetnbr,'queued'))
        self.packetnbr +=1
        self.arrtimes.append(arrtime)

        
    def processqueue(self,Q,currevent,simtime,servetime):
        ''' Update the queue and events'''
        
        # if an arrival event
        if 'queued' in currevent:
            #print "queued at"+str(currevent[0]) 
        
                  
            # determine serve time
            # servetime=np.random.exponential(1.0/srate)
            
            # process it if queue is not busy                    
            if Q.busy==0:
                # packet is immediately processed, not queued!
                deptime=simtime+servetime
                #print "process to finish at"+str(deptime)
            else: # the queue is busy 
                Q.put(currevent)
                # packet is queued!
                
                # determine departure time
                deptime=self.deptimes[-1]+servetime
            
            # create departure event and time
            Q.setbusy(deptime) #### !!!!!!!!!!!!!!!!!!!!!!!

            # record timestamp and system size
            # as seen by the arrival!!
            # either zero or Qsize+1 (one currently served)
            self.Sysevolution.append((currevent[0],Q.size()))
            
            
            # update events
            self.Events.put((deptime,currevent[1],'served'))  
            self.deptimes.append(deptime)
            self.delays.append(deptime-simtime)
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
        ''' Next steps in simulation: 
               * get next event
               * update and record simulation time
               * process queue accrodingly
            
        '''                      
        # process current event
        currevent=self.Events.get()
        # update simulation time
        self.simtime=currevent[0]
        self.simtimes.append(self.simtime)
        
        self.processqueue(self.Q,currevent,self.simtime,servicetime)
        
    def practicalcalc(self,visualsystemsize,visualdelay):
        ''' At the end of simulation, calculate mean delay and system size.
        
        Input: visualise systemsize (True/False), delay (True/False)      
        '''
          
        delays=np.array(self.delays)
        avgpracticaldelay=np.mean(delays)
    
        # extract queue evolution
        times,qsize=zip(*self.Sysevolution) 
        
        systemsize=np.array(qsize)
        # take into account only the processed portion
        systemsize=systemsize[0:len(self.delays)]
        avgpracticalsize=np.mean(systemsize)
        

        print 'Mean practical delay: {:4f} \n'.format(avgpracticaldelay)
        print 'Mean practical size : {:4f} \n'.format(avgpracticalsize)             
  
        length=min(50,len(self.delays))      
        if visualsystemsize:

            plt.figure(1)
            plt.clf()
            plt.plot(times[:length],qsize[:length],color="blue", linewidth=2,
                     drawstyle='steps-pre',label='System size')
            plt.legend()


        length=min(50,len(self.delays))      
        if visualdelay:

            plt.figure(2)
            plt.clf()
            plt.plot(times[:length],delays[:length],color="blue", 
                         linewidth=2,label='Response time')
            plt.legend()

        if visualsystemsize or visualdelay:
            plt.show()
