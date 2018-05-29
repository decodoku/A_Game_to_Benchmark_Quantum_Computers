import math

def supportedDevices ():

	# Returns the list of all supported devices

	return ["ibmqx5","19Q-Acorn"]

def getLayout (device):

	# Input:
	# 
	# * *device* - A string which specifies the device to be used.
	# 
	# Process:
	# 
	# * Look up the details of that device.
	# 
	# Output:
	# 
	# * *num* - The number of qubits in the device.
	# * *area* - A list with two entries specifying the width and height for the plot of the device. These should be in units of qubits (i.e. *area=[8,2]* for an *8x2* grid of qubits).
	# * *entangleType* - Type of entangling gate ("CX" or "CZ").
	# * *pairs* - A dictionary of pairs of qubits for which an entagling gate is possible. The key is a string which serves as the name of the pair. The value is a two element list with the qubit numbers of the two qubits in the pair. For controlled-NOTs, the control qubit is listed first.
	# * *pos* - A dictionary of positions for the qubits in the plot. Keys are qubit numbers and values are a two element list of coordinates.
	# * *example* - An example set of noisy entanglement results for use in the tutorial.
	# * *sdk* - The SDK to be used when running jobs on this device.
    # * *runs* - Data that has been obtained. As a dictionary with values of *sim* as keys.
    
    
    
    ######## IBM DEVICES ########
    
    
    if device=="ibmqx5":
        # A 16 qubit device by IBM
        # https://github.com/QISKit/ibmqx-backend-information/tree/master/backends/ibmqx5
    
        # the positions of qubits on the device (numbers), and names of pairs (letters) for ibmqx5
        #    [1]---(A)---[2]---(B)---[3]---(C)---[4]---(D)---[5]---(E)---[6]---(F)---[7]---(G)---[8]
        #     |           |           |           |           |           |           |           |
        #    (H)         (I)         (J)         (K)         (L)         (M)         (N)         (O)
        #     |           |           |           |           |           |           |           |
        #    [0]---(P)--[15]---(Q)--[14]---(R)--[13]---(S)--[12]---(T)--[11]---(U)--[10]---(V)---[9]

        num = 16
        area = [8,2]
        entangleType = "CX"
        pairs = { 'A': [1,2], 'B': [2,3], 'C': [3,4], 'D': [5,4], 'E': [6,5], 'F': [6,7], 'G': [8,7],
                 'H': [1,0], 'I': [15,2], 'J': [3,14], 'K': [13,4], 'L': [12,5], 'M': [6,11], 'N': [7,10], 'O': [9,8],
                 'P': [15,0], 'Q': [15,14], 'R': [13,14], 'S': [12,13], 'T': [12,11], 'U': [11,10], 'V': [9,10]}
        pos = { 0: [0,0], 1: [0,1],  2: [1,1],  3: [2,1],  4: [3,1],  5: [4,1],  6: [5,1],  7: [6,1],
               8: [7,1], 9: [7,0], 10: [6,0],  11: [5,0],  12: [4,0],  13: [3,0],  14: [2,0],  15: [1,0] }
        example = [0.11, 0.09, 0.49, 0.52, 0.31, 0.89, 0.15, 0.18, 0.47, 0.43, 0.67, 0.62, 0.93, 0.29, 0.77, 0.73]
        sdk = "QISKit"
        runs = {True:{'shots':[100,8192],'move':['C','R'],'maxScore':20,'samples':100},False:{'shots':[8192],'move':['C'],'maxScore':10,'samples':53}}

    
    elif device=="ibmqx2": #
        # A 5 qubit device by IBM
        # https://github.com/QISKit/ibmqx-backend-information/tree/master/backends/ibmqx2
    
        # the positions of qubits on the device (numbers), and names of pairs (letters) for ibmqx2
        #    [4]         [0]
        #     | \       / |
        #     | (D)   (B) | 
        #     |   \   /   |
        #    (F)   [2]   (A)
        #     |   /  \    |
        #     | (E)  (C)  |
        #     | /       \ |
        #    [3]         [1]
    
        num = 5
        area = [3,3]
        entangleType = "CX"
        pairs = { 'A': [0,1], 'B': [0,2], 'C': [1,2], 'D': [4,2], 'E': [3,2], 'F': [3,4] }
        pos = { 0: [1,1], 1: [1,0],  2: [0.5,0.5],  3: [0,0],  4: [0,1] }
        example = [0.11,0.09,0.49,0.52,0.31]
        sdk = "QISKit"
        runs = {True:{'shots':[100,8192],'move':['C','R'],'maxScore':20,'samples':100},False:{'shots':[8192],'move':['C'],'maxScore':10,'samples':20}}
       
    elif device=="ibmqx4":
        # A 5 qubit device by IBM
        # https://github.com/QISKit/ibmqx-backend-information/tree/master/backends/ibmqx4
    
        # the positions of qubits on the device (numbers), and names of pairs (letters) for ibmqx4
        #    [4]         [0]
        #     | \       / |
        #     | (D)   (B) | 
        #     |   \   /   |
        #    (F)   [2]   (A)
        #     |   /  \    |
        #     | (E)  (C)  |
        #     | /       \ |
        #    [3]         [1]
    
        num = 5
        area = [3,3]
        entangleType = "CX"
        pairs = { 'A': [1,0], 'B': [2,0], 'C': [2,1], 'D': [2,4], 'E': [3,2], 'F': [3,4] }
        pos = { 0: [1,1], 1: [1,0],  2: [0.5,0.5],  3: [0,0],  4: [0,1] }
        example = [0.11,0.09,0.49,0.52,0.31]
        sdk = "QISKit"
        runs = {True:{'shots':[100,8192],'move':['C','R'],'maxScore':20,'samples':100},False:{'shots':[8192],'move':['C'],'maxScore':10,'samples':100}}

    elif device=="QS1_1":
        # A 20 qubit device by IBM
        # https://quantumexperience.ng.bluemix.net/qx/devices
    
        num = 20
        area = [7,7]
        entangleType = "CX"
        pairs = { 'a': [0,1], 'b': [1,2], 'c': [3,4],
                 'd': [0,5], 'e': [1,6], 'f': [2,7], 'g': [3,8], 'h': [3,9], 'i': [4,8], 'j': [4,9],
                 'k': [5,6], 'l': [6,7], 'm': [8,9],
                 'n': [5,10], 'o': [5,11], 'p': [6,10], 'q': [6,11], 'r': [7,12], 's': [7,13], 't': [8,12], 'u': [8,13], 'v': [9,14],
                 'w': [10,11], 'x': [11,12], 'y': [12,13], 'z': [13,14],
                 'A': [10,15], 'B': [11,16], 'C': [11,17], 'D': [12,16], 'E': [12,17], 'F': [13,18], 'G': [13,19], 'H': [14,18], 'I': [14,19],
                 'J': [15,16], 'K': [16,17], 'L': [17,18], 'M': [18,19]}
        pos = { 0: [0,3], 1: [1,4], 2: [2,4], 3: [3,4], 4: [4,4],
                5: [-1,2.5], 6: [1,2.5], 7: [2,2.5], 8: [3.5,2], 9: [5,2],
               10: [-1,0.5], 11: [1,1], 12: [2,1], 13: [3,1], 14: [5,1],
               15: [0,0], 16: [0.5,-1], 17: [2,-1], 18: [3,0], 19: [5,-1] }
        example = [.32, .33, .92, .82, .11, .16, .15, .91, .12, .84, .52, .43, .78, .19, .47, .52, .78, .42, .48, .18]
        #          0    1    2    3    4    5     6   7    8    9    10   11   12   13   14   15   16   17   18   19
        sdk = "QISKit"
        runs = {True:{'shots':[100,8192],'move':['C','R'],'maxScore':20,'samples':100},False:{'shots':[8192],'move':['C'],'maxScore':10,'samples':20}}
    
    
    
    ######## RIGETTI DEVICES ########
    
    
    elif device=="19Q-Acorn":
        # A device by Rigetti with 20 qubits, but since one is isolated it is effectively 19
        # https://arxiv.org/abs/1712.05771
        # http://pyquil.readthedocs.io/en/latest/qpu_overview.html#acorn-qpu-properties
    
        num = 20
        area = [10,4]
        entangleType = "CZ"
        pairs = { 'A': [0,5], 'B': [0,6], 'C': [1,6], 'D': [1,7], 'E': [2,7], 'F': [2,8], 'G': [4,9],
                  'H': [5,10], 'I': [6,11], 'J': [7,12], 'K': [8,13], 'L': [9,14],
                  'M': [10,15], 'N': [10,16], 'O': [11,16], 'P': [11,17], 'Q': [12,17], 'R': [12,18], 'S': [13,18], 'T': [13,19], 'U': [14,19] }
        pos = { 0: [1,3], 1: [3,3], 2: [5,3], 4: [9,3],
                5: [0,2], 6: [2,2], 7: [4,2], 8: [6,2], 9: [8,2],
               10: [1,1], 11: [3,1], 12: [5,1], 13: [7,1], 14: [9,1],
               15: [0,0], 16: [2,0], 17: [4,0], 18: [6,0], 19: [8,0] }
        example = [.32, .48, .58, None,.15, .52, .33, .47, .59, .17, .51, .76, .89, .23, .65, .02, .78, .91, .25, .64]
        #          0    1    2    3    4    5     6   7    8    9    10   11   12   13   14   15   16   17   18   19
        sdk = "Forest"
        runs = {True:{'shots':[100,10000],'move':['C','R'],'maxScore':20,'samples':100},False:{'shots':[10000],'move':['C'],'maxScore':10,'samples':1000}}
    
    
    
    ######## ALIBABA DEVICES ########
    
    
    elif device=="11Q-Alibaba":
        # 11 qubit superconducting device from Chinese Academy of Sciences Innovative Center in Quantum Information and Quantum Physics (Shanghai)
        # http://quantumcomputer.ac.cn
    
        num = 12 # actually there are 11. But they number from 1, so 0 is unused
        area = [11,1]
        entangleType = "CZ"
        pairs = { 'A': [1,2], 'B': [2,3], 'C': [3,4], 'D': [4,5], 'E': [5,6], 'F': [6,7], 'G': [7,8], 'H': [8,9], 'I': [9,10],  'J': [10,11] }
        pos = { 1: [0,1], 2: [1,1], 3: [2,1], 4: [3,1], 5: [4,1], 6: [5,1], 7: [6,1], 8: [7,1], 9: [8,1], 10: [9,1], 11: [10,1] }
        example = [None, .48, .50, .12, .15, .35, .33, .47, .45, 0.02, 0.24, 0.28]
        sdk = "ManualQISKit"
        runs = {True:{'shots':[100,9000],'move':['C','R'],'maxScore':20,'samples':100},False:{'shots':[9000],'move':['C'],'maxScore':2,'samples':20}}
    
    
    
    ######## DEVICES NOT ON THE CLOUD ########
    
    
    elif device=="8Q-Wallraff":
        # A device from the group of A. Wallraff at ETH
        # https://arxiv.org/abs/1801.07904
    
        num = 9 # actually there are 8. But they number from 1, so 0 is unused
        area = [4,2]
        entangleType = "CZ"
        pairs = { 'A': [1,2], 'B': [2,3], 'C': [3,4], 'D': [4,5], 'E': [5,6], 'F': [6,7], 'G': [7,8],
                  'fake1':[0,1], 'fake1':[0,2], 'fake1':[0,3], 'fake1':[0,4], 'fake1':[0,5], 'fake1':[0,6], 'fake1':[0,7], 'fake1':[0,8] }
        pos = { 1: [0,1], 2: [1,1], 3: [2,1], 4: [3,1],
                8: [0,0], 7: [1,0], 6: [2,0], 5: [3,0] }
        example = [None, .48, .50, .12, .15, .35, .33, .47, .45]
        sdk = "ProjectQ"
        runs = {True:{'shots':[100,10000],'move':['C','R'],'maxScore':20,'samples':100},False:{'shots':[10000],'move':['C'],'maxScore':5,'samples':20}}
    
    
    
    ######## EXAMPLE DEVICES (FOR SIMULATION ONLY) ########
    
    elif device[0:4]=="line":
        
        num = int(device[4:])
        
        if (num%2)==1: # we can continue only num is odd
            area = [num,1]
            entangleType = "CZ"
            pairs = {}
            for qubit in range(num-1):
                pairs[chr(65+qubit)] = [qubit,qubit+1]
            pos = {}
            for qubit in range(num):
                pos[qubit] = [qubit,0]
            example = [0.5]*num
            sdk = "QISKit"
            runs = {True:{'shots':[100],'move':['C','R'],'maxScore':20,'samples':100},False:{'shots':[],'move':[],'maxScore':0,'samples':0}}
        else:
            print("Try again with a valid number of qubits for this configuration")
        
    elif device[0:6] in ["ladder","square"]:
        
        num = int(device[6:])
        
        if device[0:6]=="ladder":
            Lx = int(num/2)
            Ly = 2
            good_num = ((num%2)==0) # we can continue only num is even
        else:
            Lx = int(math.sqrt(num))
            Ly = Lx
            good_num = (type(Lx) is int) # we can continue only num is square
        
        if good_num: 
            
            area = [Lx,Ly]
            entangleType = "CZ"
            pairs = {}
            pos = {}
            example = [0.5]*num
            sdk = "QISKit"
            runs = {True:{'shots':[100],'move':['C','R'],'maxScore':20,'samples':100},False:{'shots':[],'move':[],'maxScore':0,'samples':0}}
            
            char = 65
            for y in range(Ly):
                for x in range(Lx):
                    q = y*Lx+x
                    if x<(Lx-1): # pair for (x,y) and (x+1,y)
                        pairs[chr(char)] = [q,q+1]
                        char+=1
                    if y<(Ly-1): # pair for (x,y) and (x,y+Lx)
                        pairs[chr(char)] = [q,q+Lx]
                        char+=1
                    pos[q] = [x,y]
                    
        else:
            print("Try again with a valid number of qubits for this configuration")
            
    elif device[0:3]=="web":
        
        num = int(device[3:])
        
        L = int(math.sqrt(num))
            
        area = [L,L]
        entangleType = "CZ"
        pairs = {}
        pos = {}
        example = [0.5]*num
        sdk = "QISKit"
        runs = {True:{'shots':[100],'move':['C','R'],'maxScore':20,'samples':100},False:{'shots':[],'move':[],'maxScore':0,'samples':0}}
            
        char = 65
        for q0 in range(num-1):
            for q1 in range(q0+1,num):
                pairs[chr(char)] = [q0,q1]
                char+=1
        
        for q0 in range(num):
            pos[q0] = [L*math.cos(q0*(2*math.pi)/num),L*math.sin(q0*(2*math.pi)/num)]

    
    
    ######## NO MORE DEVICES ########
    
    
    else:
        
        print("\nWarning: This is not a known device.\n")
    
    
    return num, area, entangleType, pairs, pos, example, sdk, runs
