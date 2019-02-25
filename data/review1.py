import os
import sys
import optparse
import random
import numpy
from numpy.random import choice



'''
-------------------------------------DEFAULT TLC LOGIC---------------------------------------------------------

    <tlLogic id="0" type="static" programID="0" offset="0">
        <phase duration="40" state="rrrGGgrrrGGg"/>
        <phase duration="5"  state="rrryyyrrryyy"/>
        <phase duration="40" state="GGgrrrGGgrrr"/>
        <phase duration="5"  state="yyyrrryyyrrr"/>
    </tlLogic>


--------------------------------------GLOBAL VARIABLES----------------------------------------------------------
'''
#Global variables
gamma = 0.9;            #predefined
betaq=1; thetaq = 1.5;  #predefined
betaw=2; thetaw = 1.5;  #predefined
INITIAL_QMATRIX_VALUE=0;
INITIAL_ALPHAMATRIX_VALUE=1;
EPSILON_GREEDY_CHANGE=1/6;
EPSILON_CONTROL_PARAMETER=0.9;

#All the phase indices will be defined in arrphases=[0,1,2,3,4,5,6,7]
arrphases=[0,1,2,3]
#All the phase names will be defined in arrphasenames
arrphasenames=["rrrGGgrrrGGg","rrryyyrrryyy","GGgrrrGGgrrr","yyyrrryyyrrr"] 

statesandactions=dict()
arrayofactions=[6,9,12,15,18,21,24,27,30,33,36,39,42,45,48,51,54,57,60]
sorted(arrayofactions)
statesandactions[0]=arrayofactions; statesandactions[2]=arrayofactions; statesandactions[4]=arrayofactions; statesandactions[6]=arrayofactions;
qmatrix=dict()
alphamatrix=dict()

arrlanesinput=["1i_0","2i_0","3i_0","4i_0"]
arredgesinput=["1i","2i","3i","4i"]

#-----------------------------------------------------------------------------------------------------------------



#We need to import some python modules from the $SUMO_HOME/tools directory
if 'SUMO_HOME' in os.environ:
    tools = os.path.join(os.environ['SUMO_HOME'], 'tools')
    sys.path.append(tools)
else:
    sys.exit("please declare environment variable 'SUMO_HOME'")

from sumolib import checkBinary  # Checks for the binary in environ vars
import traci

#importing usertraci.py containing all TLC User Functions
from usertraci import *

#importing userq.py containing Q Matrix Functions and other tools
from userq import *



# contains TraCI control loop
def run():
    initializeQMatrixAndValues();
    initializeAlphaMatrixAndValues();
    printQMatrixValues();
    printAlphaMatrixValues();
    step = 0
    junctionID="0"
    stepatnextstate=45 #When the next phase 0 or 2 starts
    prevactiontime=-1
    currentphase=0
    x=traci.trafficlight.getIDList() #Only One Junction Intersection
    while traci.simulation.getMinExpectedNumber() > 0:   #Until all vehicles are gone
        traci.simulationStep()
        currentphase=traci.trafficlight.getPhase(junctionID)
        #Check if  Of Phase 1 or 3:
        if currentphase==1 or currentphase==3:
            print("Step:",step," Time:",traci.trafficlight.getNextSwitch(junctionID))
            stepatnextstate=traci.trafficlight.getNextSwitch(junctionID)

        if step==stepatnextstate-1: #Just one step before, thus in one of the yellow phases
            #Print Waiting Time and Queue Length using functions
            printQMatrixValues();
            printAlphaMatrixValues();
            if prevactiontime<0:
                #something
                nextactiontime=updatedQValueAfterAction(currentphase-1,39,junctionID,betaq,thetaq,betaw,thetaw,gamma)
            else:
                nextactiontime=updatedQValueAfterAction(currentphase-1,prevactiontime,junctionID,betaq,thetaq,betaw,thetaw,gamma)

        if step==stepatnextstate:
            traci.trafficlight.setPhaseDuration(junctionID, nextactiontime)
            prevactiontime=nextactiontime

        step += 1

    traci.close()
    sys.stdout.flush()
    sys.exit()






























def get_options():
    opt_parser = optparse.OptionParser()
    opt_parser.add_option("--nogui", action="store_true",
                         default=False, help="run the commandline version of sumo")
    options, args = opt_parser.parse_args()
    return options

# main entry point
if __name__ == "__main__":
    options = get_options()

    # check binary
    if options.nogui:
        sumoBinary = checkBinary('sumo')
    else:
        sumoBinary = checkBinary('sumo-gui')

    # traci starts sumo as a subprocess and then this script connects and runs
    traci.start([sumoBinary, "-c", "review1.sumocfg",
                             "--tripinfo-output", "tripinfo.xml"])
    run()

