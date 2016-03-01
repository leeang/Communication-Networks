# -*- coding: utf-8 -*-
"""
Created on Tue Jul 15 11:43:50 2014

Classes to help ELEN90061 Workshop MMc Simulation

@author: alpcan
"""

import math
import numpy as np
import heapq as hq
from collections import deque as dq

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
            
            
class QueueMS:
    '''
    A basic FIFO Queue with a multiple servers. 
    Implementation is based on collections.deque, and is a list.
    
    Methods: size, get, put, reset, isempty, setserverbusy, setserverfree
    
    '''       
    #initevents    
    def __init__(self,inputitems,nbrserver):
        ''' initialise Queue with a list of items  '''
        self.nbrserver=nbrserver
        self.queue=dq(inputitems)
        self.server=[0 for i in range(self.nbrserver)]   # servers busy?   
        
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
    
    def setserverbusy(self,untiltime,serverind):
        ''' set the server with serverind busy until given time  '''
        # set it busy until current packet is processed
        self.server[serverind]=untiltime 
    
    def setserverfree(self,serverind):
        ''' set the server with serverind free '''
        self.server[serverind]=0
        

class DESmmc:
    
    #init   
    def __init__(self,srate,arate,nbrserver,maxsteps):
        
        ## internal variables
        self.simtime=0.0     # simulation time
        self.simtimes=[0.0]
        self.arrtimes=[]     # arrival times
        self.deptimes=[]     # departure times
        self.delays=[]       # delays
        self.packetnbr=0     # packet number
        # system occupancy evolution: (timestamp, size)
        self.Sysevolution=[(0.,0)]  
        
        #input
        self.maxsteps=maxsteps
        self.srate=srate
        self.arate=arate

        # event queue
        self.Events=EventQueue([])   # events
        
        # init mm2 Queue
        self.Q=QueueMS([],nbrserver)     # queue       
        
        # first packet arrives in the beginning 
        # just a choice, doesn't have to be so...
        self.Events.put((self.simtime,self.packetnbr,'queued'))
        self.packetnbr +=1
        self.arrtimes.append(self.simtime)
        
    def packetarrival(self,Q,interarrival):
        # packet arrival
        arrtime=self.arrtimes[-1]+interarrival
        self.Events.put((arrtime,self.packetnbr,'queued'))
        self.packetnbr +=1
        self.arrtimes.append(arrtime)

        
    def processqueue(self,Q,currevent,simtime,servetime):
        
#        # this is just as a shorthand
#        Q=self.Q
#        simtime=self.simtime
        
        # if an arrival event
        if 'queued' in currevent:
            #print "queued at"+str(currevent[0])  
            # determine departure time
            
            # process it if a free server is available 
            if 0 in Q.server:               
                # packet is immediately processed, not queued!
                deptime=simtime+servetime
                serverind=Q.server.index(0)
                # currently served
                # this is zero in mm1
                currserved=sum([1 for x in Q.server if x>0])

            else: # all servers are busy
                # packet is queued!
                Q.put(currevent)
                # determine departure time
                serverind=Q.server.index(min(Q.server))
                deptime=Q.server[serverind]+servetime
                # currently served, all servers occupied
                # subtract one because we put incoming packet
                # otherwise it would be double counting!
                # this is zero in mm1
                currserved=len(Q.server)-1
            
            # create departure event and time
            Q.setserverbusy(deptime,serverind) #### !!!!!!!!!!!!!!!!!!!!!!!
            
            # record timestamp and queue size
            # as seen by the arrival!!
            self.Sysevolution.append((currevent[0],Q.size()+currserved))
            
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

            # if a server is not busy, free it
            for i in range(Q.nbrserver):
                if simtime>=Q.server[i]:
                    Q.setserverfree(i)
            #print "departure at"+str(currevent[0])
        
    def nextstep(self,servicetime):
                      
        # process current event
        currevent=self.Events.get()
        # update simulation time
        self.simtime=currevent[0]
        self.simtimes.append(self.simtime)
        
        self.processqueue(self.Q,currevent,self.simtime,servicetime)
        
    def practicalcalc(self):
          
        avgpracticaldelay=np.mean(np.array(self.delays))
    
        # extract queue evolution
        times,qsize=zip(*self.Sysevolution)      
        systemsize=np.array(qsize)
        # take into account only the processed portion
        systemsize=systemsize[0:len(self.delays)]
        avgpracticalsize=np.mean(systemsize)
        
        print 'Mean practical delay: {:4f} \n'.format(avgpracticaldelay)
        print 'Mean practical size : {:4f} \n'.format(avgpracticalsize)
        
        
        return avgpracticaldelay,avgpracticalsize
