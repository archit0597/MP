#user.py
import os
import sys
import optparse
import random
from userq import *
if 'SUMO_HOME' in os.environ:
    tools = os.path.join(os.environ['SUMO_HOME'], 'tools')
    sys.path.append(tools)
else:
    sys.exit("please declare environment variable 'SUMO_HOME'")

from sumolib import checkBinary  # Checks for the binary in environ vars
import traci



#Function to get number of lanes of that edge
def getNumberOfLanes(edgeID):
	x=traci.edge.getLaneNumber(edgeID);
	print("--Number of Lanes in Edge ",edgeID, " is ",x,".\n")
	return x;

#Function to get total halting vehicles of given edge
def getHaltedVehiclesOfEdge(edgeID):
	x=traci.edge.getLastStepHaltingNumber(edgeID);
	print("--Total Halted Vehicles in Edge ",edgeID, " is ",x,".\n")
	return x;

#function to get total waiting time of given edge
def getWaitingTimeOfEdge(edgeID):
    x= traci.edge.getWaitingTime(edgeID)
    print("--Total Waiting Time in Edge ",edgeID, " is ",x,".\n")
    return x;

#Function to print Density of all edges //define edges in arredgesinput
def printDensity():
    for edge in arredgesinput:
        num = traci.edge.getLastStepVehicleNumber(edge)
        density = num / traci.lane.getLength(edge + "_0")
        #Divide Density by 1000 for per km
        print("\nEdge: ",edge," >Density: ",density)

#Function to get Current Phase for given Junction ID
def getCurrentTLCPhase(junctionID):
	return traci.trafficlight.getPhase(junctionID)

#Function to get Next TLC Phase of a given Junction
def getNextTLCPhase(junctionID):
	phase=getCurrentTLCPhase(junctionID)
	lenx=len(arrphases)
	if phase==lenx-1:
		return 0;
	else:
		return arrphases[phase+1];

'''
Q-Learning Methods
'''

def getQiOfEdge(edgeID):
	return getHaltedVehiclesOfEdge(edgeID);

def getWiOfEdge(edgeID):
	return getWaitingTimeOfEdge(edgeID);

#Function to calculate reward at that step
def getReward(betaq,thetaq,betaw,thetaw):
	sumall=0;
	for edge in arredgesinput:
		product1=betaq*(pow(getQiOfEdge(edge),thetaq));
		product2=betaw*(pow(getWiOfEdge(edge),thetaw));
		sumall+=product1+product2;
	return (0-sumall);

#Function to return max Q Value of the next State 
'''
def getMaxQValueOfNextState(junctionID):
	#Implement Selection Policy
	arr=qmatrix[getNextTLCPhase(junctionID)]
	#Replace the above with arr=qmatrix[getNextTLCPhase(junctionID)]
	max = arr[0]
	index=0; 
	for i in range(1, len(arr)): 
		if arr[i] > max: 
			max = arr[i] 
	return max
'''

def getActionForMaxQValueOfNextState(junctionID):
	#Implement Selection Policy
	state=getNextTLCPhase(junctionID)
	arr=qmatrix[state]
	temparr=[]
	#arr=getAllActionsForState(state)
	#Replace the above with arr=qmatrix[getNextTLCPhase(junctionID)]
	max = arr[0]
	index=0; 
	for i in range(1, len(arr)): 
		if arr[i] > max: 
			max = arr[i]
			index=i
	print("ActionForMaxQNextState: ",statesandactions[state][index],"\n")
	finalactiontime=statesandactions[state][index]
	#Implementing Selection Pilcy
	alphaval=getAlpha(state,statesandactions[state][index])
	#Firstly, getAlphaval to check if n(s,a) iud developed, ie. if value <= 1/10, stored in EPSILON_GREEDY_CHANGE
	#getActionValueSelectionPolicy(state,index)
	if alphaval<=EPSILON_GREEDY_CHANGE:
		finalactiontime=getActionValueSelectionPolicy(state,index,1) #GREEDY
	elif alphaval>EPSILON_GREEDY_CHANGE:
		finalactiontime=getActionValueSelectionPolicy(state,index,0) #SOFT
	temparr.append(finalactiontime);
	temparr.append(max);
	return temparr #returns the action time (eg 15s) for the corresponding max Qvalue of next state 


def getBellmanEquation(junctionID,betaq,thetaq,betaw,thetaw,gamma):
	somearr=[]
	temparr=[]
	temparr=getActionForMaxQValueOfNextState(junctionID)
	actiontime=temparr[0]
	value=(getReward(betaq,thetaq,betaw,thetaw) +gamma*(temparr[1]));
	somearr.append(actiontime)
	somearr.append(value)
	return somearr

#def getAlpha(state,action) returns  a double Value

def updatedQValueAfterAction(state,action,junctionID,betaq,thetaq,betaw,thetaw,gamma):
	print("UPDATING QM: State:",state, " Action:",action,"\n")
	alpha=getAlpha(state,action)
	qvalue=getQValue(state,action)
	temp=1-alpha
	print("Before: ",qvalue,"\t")
	temparr=[]
	temparr=getBellmanEquation(junctionID,betaq,thetaq,betaw,thetaw,gamma)
	actiontime=temparr[0]
	bellmanvalue=temparr[1]
	setQValue(state,action,temp*qvalue+alpha*bellmanvalue)
	print("After: ",getQValue(state,action),"\n")
	setAlpha(state,action)
	return actiontime;
	#Return true for if executed succcessfully?


#qi is queue length of the stopped vehicles its edge at that step 
#wi is waiting time of that edge at that step for all vehicles 

#-------------------------------------SOME INITIAL FUNCTIONS DEPRECATED DONT USE----------------------------------------------------------------
def printWaitingTimeAllLanes(step):
    sumall=0;
    for lane in arrlanesinput:
        sumall+=traci.lane.getWaitingTime(lane)
    print("Step: ",step, " Waiting Time: ", sumall)

def printWaitingTimeAllLanes(step):
    sumall=0;
    for lane in arrlanesinput:
        sumall+=traci.lane.getWaitingTime(lane)
    print("Step: ",step, " Waiting Time: ", sumall)

def printQueueLengthAllLanes(step):
    print("\nStep:",step)
    for edge in arredgesinput:
        num = traci.edge.getLastStepVehicleNumber(edge)
        density = num / traci.lane.getLength(edge + "_0")
        #Divide Density by 1000 for per km
        print("\nEdge: ",edge," >Density: ",density)



'''
def run():
    """execute the TraCI control loop"""
    step = 0
    # we start with phase 2 where EW has green
    traci.trafficlight.setPhase("0", 3)
    while traci.simulation.getMinExpectedNumber() > 0:
        traci.simulationStep()
        if traci.trafficlight.getPhase("0") == 2:
            # we are not already switching
            if traci.inductionloop.getLastStepVehicleNumber("0") > 0:
                # there is a vehicle from the north, switch
                traci.trafficlight.setPhase("0", 3)
            else:
                # otherwise try to keep green for EW
                traci.trafficlight.setPhase("0", 2)

        #det_vehs = traci.inductionloop.getLastStepVehicleIDs("det_0")
        #for veh in det_vehs:
        #    print(veh)
        #    traci.vehicle.changeLane(veh, 2, 25)

        # if step == 100:
        #     traci.vehicle.changeTarget("1", "e9")
        #     traci.vehicle.changeTarget("3", "e9")                
        step += 1
    traci.close()
    sys.stdout.flush()
'''


'''

def run():

    step = 0
    x=traci.trafficlights.getIDList()
    while traci.simulation.getMinExpectedNumber() > 0:   #Until all vehicles are gone
        traci.simulationStep()
        #print(step)
        printWaitingTimeAllLanes(step);
        printQueueLengthAllLanes(step);
        if step==85:
            traci.trafficlight.setPhase("0", 0)  #Junction Id is "0" and we're setting the phase to be 0 from <tlLogic>
            traci.trafficlight.setPhaseDuration("0",5) #Junction ID is "0" and we're setting the current phase's duration in seconds temporarily not affecting tllogic

        print("\n")
        step += 1

    traci.close()
    sys.stdout.flush()
    sys.exit()


'''

#-----------------------------------------------------------------------------------------------------------------------------

