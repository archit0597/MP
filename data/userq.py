'''
#Global variables
gamma = 0.9;            #predefined
betaq=1; thetaq = 1.5;  #predefined
betaw=2; thetaw = 1.5;  #predefined
INITIAL_QMATRIX_VALUE=0;
INITIAL_ALPHAMATRIX_VALUE=1;


#All the phase indices will be defined in arrphases=[0,1,2,3,4,5,6,7]
arrphases=[0,1,2,3]
#All the phase names will be defined in arrphasenames
arrphasenames=["rrrGGgrrrGGg","rrryyyrrryyy","GGgrrrGGgrrr","yyyrrryyyrrr"] 


statesandactions=dict()
arrayofactions=[6,9,12,15,18,21,24,27,30,33,36,39,42,45,48,51,54,57,60]
sorted(arrayofactions)
statesandactions[0]=arrayofactions;
statesandactions[2]=arrayofactions;
statesandactions[4]=arrayofactions;
statesandactions[6]=arrayofactions;


qmatrix=dict()
alphamatrix=dict()
'''

'''
NOTES:
1. 
All the arrays including arrphases and arrphasenames have been presumed to be set at time of execution

2.
Any Phase name with 'y' or 'Y' should be having an odd index

3. The StatesAndActions Dictionary shall be of format like below:

Index:                 0,1,2,3,4,5,6,7,8............

statesandactions={	0:[6,9,12,15,18,21,24,27,30,33,36,39,42,45,48,51,54,57,60],
					2:[6,9,12,15,18,21,24,27,30,33,36,39,42,45,48,51,54,57,60]
					4?:[6,9,12,15,18,21,24,27,30,33,36,39,42,45,48,51,54,57,60],
					6?:[6,9,12,15,18,21,24,27,30,33,36,39,42,45,48,51,54,57,60] }

4. THE Q MATRIX will be of the above format too, just replacing the Action Values with Q Values
NOTE>>>>>>>>>>>>>>>>> the getActionInfdexFor(state,action) returns and index for the pair (state,action) 
example:: index 5 corresponds to Action Value 18 for state 2, thus getActionInfdexFor(2,18)=5 returns.

5.Qmatrix And AlphaMatrix are declared Globally

'''
from review1 import *
def initializeQMatrixAndValues():
	for state in arrphases:
		if state%2==0:
			temp=[];
			action_array=statesandactions[state];
			index=0;
			for action in action_array:
				print("State: ",state," Action: ",action," Index: ",index)
				temp.append(INITIAL_QMATRIX_VALUE)
				index+=1;
				qmatrix[state]=temp;
		else:
			#do Nothing
			print("\n DOING NOTHING--INIT Q MATRIX\n")
	print("\nINITIALIZED Q-----\n")	

def printQMatrixValues():
	print("\nPrinting QMatrix:")
	for state in arrphases:
		if state%2==0:
			print("State: ",state,"\n")
			index=0;
			for i in statesandactions[state]:
				print(i," : ",qmatrix[state][index],"\t")
				index+=1;

			print("\n")

def initializeAlphaMatrixAndValues():		
	print("\nINITIALIZING ALPHA-----\n")   #alpha matrix initialization
	for state in arrphases:
		if state%2==0:
			temp=[]; action_array = statesandactions[state]; index=0;
			for action in action_array:
				temp.append(INITIAL_ALPHAMATRIX_VALUE);
				print("AlphaState: ",state," AplhaAction: ",action," AplhaIndex: ",index)
				index+=1;
			alphamatrix[state]=temp
		else:
			#donothing
			print("\nDOING NOTHING--INIT ALPHA MATRIX\n")	
 
def printAlphaMatrixValues():
	print("\nPrinting AlphaMatrix:")
	for state in arrphases:
		if state%2==0:
			print("State: ",state,"\n")
			index=0;
			for i in statesandactions[state]:
				print(i," : ",alphamatrix[state][index],"\t")
				index+=1;

			print("\n")

def setQValue(state,action,value):    #modification of Qvalue using traversal
	for x,y in qmatrix.items():
		if x==state:
			action_index=getActionIndexFor(state,action)
			print("SETQVAL> State:",x," Action: ",action, " Index: ",action_index,"\n")
			index=0;
			for p in y:
				if index==action_index:
					print("SETQVAL> ActionIndex:",index)
					qmatrix[x][index] = value;
					break;
				else:
					index+=1;
			

def getQValue(state,action):
	#state value could be 0,2,4,6 and action value could be 6,9,12 etc
	action_index=getActionIndexFor(state,action)
	if state%2==0:
		for value in qmatrix:
			if value==state:
				print("GETQVAL> State: ",value," Action: ",action, " Index: ",action_index," Value=",qmatrix[state][action_index],"\n")
				return qmatrix[state][action_index]
				#return the garbage/actual q value
		
	else:
		#donothing
		print("\nDOING NOTHING--GET Q VALUE\n")		
	
	
def setAlpha(state,action):               #modification of alpha using the earlier alpha matrix update
	for x,y in alphamatrix.items():
		if x==state:
			action_index=getActionIndexFor(state,action)
			print("SETALPHAVAL> State:",x," Action: ",action, " Index: ",action_index,"\n")
			index=0
			for p in y:
				if index==action_index:
					prev=alphamatrix[x][index]; 
					after=(1/prev)+1; 
					alphamatrix[x][index]=1/after;
					print("SETALPHAVAL> Before:",prev," After:",alphamatrix[x][index])
					break;
				else:
					index+=1		


#The below function is for getting an Alpha value (1,1/2,1/3 etc) from the matrix
			
def getAlpha(state,action):
	#state value could be 0,2,4,6 and action value could be 6,9,12 etc
	action_index=getActionIndexFor(state,action)
	if state%2==0:
		print("GETALPHAVAL> State: ",state," Action: ",action, " Index: ",action_index," Value=", alphamatrix[state][action_index],"\n")
		return alphamatrix[state][action_index]
		#return the garbage/actual q value	
	else:
		#donothing
		print("\nDOING NOTHING--GET Q VALUE\n")		


def getActionIndexFor(state,action):  #This returns the index of the action for the corresponding state via the format states and actions which contains the actual values
	index=0;
	if state%2==0:
		#something
		for value in statesandactions:
			if state==value:
				for val in statesandactions[state]:
					if val==action:
						return index;
					else:
						index=index+1;
	else:
		#do Nothing
		print("\nDOING NOTHING--GET ACTION INDEX FOR\n")

def getActionValueSelectionPolicy(state,index,choice):
	#choice defines if time to switch from soft to greedy
	if choice==0: #SOFT
		#Something
		arractions=statesandactions[state]; 
		arrweights = []
		i=0;
		temp=1-EPSILON_CONTROL_PARAMETER;
		lenx=len(arractions)
		tempprob=(1-temp)/(lenx-1)
		for time in arractions:
			if i==index:
				arrweights.append(temp)
			else:
				arrweights.append(tempprob)
			i=i+1; 
		finalaction=numpy.random.choice(arractions, p=arrweights)
		return finalaction
	else: #GREEDY
		#Something
		arractions=statesandactions[state]; 
		arrweights = []
		i=0;
		temp=EPSILON_CONTROL_PARAMETER;
		lenx=len(arractions)
		tempprob=(1-temp)/(lenx-1)
		for time in arractions:
			if i==index:
				arrweights.append(temp)
			else:
				arrweights.append(tempprob)
			i=i+1; 
		finalaction=numpy.random.choice(arractions, p=arrweights)
		return finalaction

	#Return the Action (Time) for that index.

#print("HELLO WORLD!\n")

'''
	Testing:

print(statesandactions)
initializeQMatrixAndValues();
printQMatrixValues();
setQValue(2,27,777);
printQMatrixValues();
print(getQValue(2,27));
initializeAlphaMatrixAndValues();
printAlphaMatrixValues();
setAlpha(2,51)
printAlphaMatrixValues();
print(getAlpha(2,51))
setAlpha(2,51)
printAlphaMatrixValues()
'''