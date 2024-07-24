'''
This is the file where you need to make changes to add a new device.

The supportedDevices() function returns a list of all devices that are ready to play offline, using Play_Quantum_Awesomeness.ipynb.
This means that the notebooks/GetData.ipynb must have already been run (sim=True and sim=False) for any device added to this.

The getLayout() function is where the details of a device must be entered, including name, number of qubits, connectivity, SDK, etc.
'''

from devicePrep import *

def supportedDevices ():

	# Returns a list of all devices that can be selected in the Play_Quantum_Awesomeness.ipynb file
    # 

	return ["ibmqx4","ibmqx5","19Q-Acorn","8Q-Agave"]


def getLayout (device):

	# Input:
	# 
	# * *device* - A string which specifies the device to be used.
	# 
	# Output:
	# 
	# * *num* - The number of qubits in the device.
    #           NOTE: If the SDK refers to qubits by numbers, this program assumes that qubits are numbered from 0.
    #           If your device has qubits numbered from 1, and you don't think the compiler will translate,
    #           set num to one greater than the number of qubits in your device, and don't use qubit 0. 
    #
    # * *area* - A list with two entries specifying the width and height to be used in the plots for the game.
    #            These should be in units of qubits (i.e. *area=[8,2]* for an *8x2* grid of qubits).
    #
	# * *entangleType* - Type of entangling gate ("CX" or "CZ").
    #                    This does not affect the gates used in the program. With a good compiler, it doesn't matter what you choose.
    #
	# * *pairs* - A dictionary of pairs of qubits for which an entagling gate is possible.
    #             The key is a string which serves as the name of the pair.
    #             The value is a two element list with the qubit numbers of the two qubits in the pair.
    #             For controlled-NOTs, the control qubit is listed first.
    #
	# * *pos* - A dictionary of positions for the qubits to be used in the plots for the game.
    #           Keys are qubit numbers and values are a two element list of coordinates.
    #
	# * *example* - An example set of noisy entanglement results for use in the tutorial.
    #               This can be generated using the makeExample() function of devicePrep.py.
    #
	# * *sdk* - The SDK to be used when running jobs on this device.
    #           'QISKit', 'ProjectQ', 'Forest' and 'Cirq' are currently supported.
    #           To add another SDK, see the functions with *This function contains SDK specific code.* in QuantumAwesomeness.py.
    #
    # * *runs* - Specification of the data that should be obtained when run.
    #            Also serves as a description of the data expected to exist for devices listed in supportedDevices().
    #            We recommend using
    #            runs = {True:{'shots':[100],'move':['C','R'],'maxScore':20,'samples':100},
    #                    False:{'shots':[10000],'move':['C'],'maxScore':10,'samples':1000}}
    #            - The True/False keys denote simulated/real runs.
    #            - 'shots' is the number of times each given instance is repeated for statistics
    #            - 'move' is the way moves are chosen in the game ('C' for correct, 'R' for random).
    #            - 'maxScore' is the number of rounds each game goes on for.
    #            - 'samples' is the number of times a game defined by a given set of the above paramaters is repeated.

    
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
        example = [0.055, 0.045, 0.25, 0.26, 0.15, 0.45, 0.8, 0.9, 0.24, 0.22, 0.33, 0.31, 0.46, 0.15, 0.42, 0.41]
        sdk = "QISKit"
        runs = {True:{'shots':[100],'move':['C','R'],'maxScore':20,'samples':100},False:{'shots':[8192],'move':['C'],'maxScore':10,'samples':53}}

    
    elif device=="ibmqx2":
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
        runs = {True:{'shots':[100],'move':['C','R'],'maxScore':20,'samples':100},False:{'shots':[8192],'move':['C'],'maxScore':10,'samples':20}}
       
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
        pairs = { 'A': [1,0], 'B': [2,0], 'C': [2,1], 'D': [4,2], 'E': [3,2], 'F': [3,4] }
        pos = { 0: [1,1], 1: [1,0],  2: [0.5,0.5],  3: [0,0],  4: [0,1] }
        example = [0.11,0.09,0.49,0.47,0.31]
        sdk = "QISKit"
        runs = {True:{'shots':[100],'move':['C','R'],'maxScore':20,'samples':100},False:{'shots':[8192],'move':['C'],'maxScore':10,'samples':100}}

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
        example = [0.16, 0.165, 0.46, 0.41, 0.055, 0.08, 0.075, 0.455, 0.06, 0.42, 0.26, 0.215, 0.39, 0.095, 0.235, 0.26, 0.39, 0.21, 0.24, 0.09]
        #          0    1    2    3    4    5     6   7    8    9    10   11   12   13   14   15   16   17   18   19
        sdk = "QISKit"
        runs = {True:{'shots':[100],'move':['C','R'],'maxScore':20,'samples':100},False:{'shots':[8192],'move':['C'],'maxScore':10,'samples':100}}
    
    
    
    ######## RIGETTI DEVICES ########
    
    
    elif device=="19Q-Acorn":
        # A device by Rigetti with 20 qubits, but since one is isolated it is effectively 19
        # https://arxiv.org/abs/1712.05771
        # http://pyquil.readthedocs.io/en/latest/qpu.html
    
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
        example = [0.16, 0.24, 0.29, None, 0.075, 0.26, 0.165, 0.235, 0.295, 0.085, 0.255, 0.38, 0.445, 0.115, 0.325, 0.01, 0.39, 0.455, 0.125, 0.32]
        #          0    1    2    3    4    5     6   7    8    9    10   11   12   13   14   15   16   17   18   19
        sdk = "Forest"
        runs = {True:{'shots':[100],'move':['C','R'],'maxScore':20,'samples':100},False:{'shots':[10000],'move':['C'],'maxScore':10,'samples':1000}}
    
    elif device=="8Q-Agave":
        # A device by Rigetti with 8 qubits
        # http://pyquil.readthedocs.io/en/latest/qpu.html
    
        num = 8
        area = [3,3]
        entangleType = "CZ"
        pairs = { 'A': [0,1], 'B': [1,2], 'C': [2,3], 'D': [3,4], 'E': [4,5], 'F': [5,6], 'G': [6,7],
                  'H': [7,0] }
        pos = { 0: [1,2], 1: [0,2], 2: [0,1], 3: [0,0],
                4: [1,0], 5: [2,0], 6: [2,1], 7: [2,2] }
        example = [0.44, 0.45, 0.06, 0.075, 0.175, 0.165, 0.235, 0.225]
        sdk = "Forest"
        runs = {True:{'shots':[100],'move':['C','R'],'maxScore':20,'samples':100},False:{'shots':[10000],'move':['C'],'maxScore':10,'samples':1000}}
    
    ######## ALIBABA DEVICES ########
    
    
    elif device=="11Q-Alibaba":
        # 11 qubit superconducting device from Chinese Academy of Sciences Innovative Center in Quantum Information and Quantum Physics (Shanghai)
        # http://quantumcomputer.ac.cn
    
        num = 12 # actually there are 11. But they number from 1, so 0 is unused
        area = [11,1]
        entangleType = "CZ"
        pairs = { 'A': [1,2], 'B': [2,3], 'C': [3,4], 'D': [4,5], 'E': [5,6], 'F': [6,7], 'G': [7,8], 'H': [8,9], 'I': [9,10],  'J': [10,11] }
        pos = { 1: [0,1], 2: [1,1], 3: [2,1], 4: [3,1], 5: [4,1], 6: [5,1], 7: [6,1], 8: [7,1], 9: [8,1], 10: [9,1], 11: [10,1] }
        example = [None, 0.24, 0.25, 0.06, 0.075, 0.175, 0.165, 0.235, 0.225, 0.01, 0.12, 0.14]
        sdk = "ManualQISKit"
        runs = {True:{'shots':[100],'move':['C','R'],'maxScore':20,'samples':100},False:{'shots':[9000],'move':['C'],'maxScore':2,'samples':20}}
    
    
    ######## GOOGLE DEVICES ########
    
    elif device=="9Q-Google":
        
        area, pairs, pos, example = makeLayout ("line9")
        
        num = 9
        entangleType = "CZ"
        sdk = "Cirq"
        runs = {True:{'shots':[100],'move':['C','R'],'maxScore':20,'samples':100},False:{'shots':[8192],'move':['C'],'maxScore':10,'samples':100}}
        
    elif device=="Foxtail":
        
        area, pairs, pos, example = makeLayout ("ladder22")
        
        num = 22
        entangleType = "CZ"
        sdk = "Cirq"
        runs = {True:{'shots':[100],'move':['C','R'],'maxScore':20,'samples':100},False:{'shots':[8192],'move':['C'],'maxScore':10,'samples':100}}
    
    elif device=="Bristlecone":
        
        num = 72
        
        area = [11,11]
        
        import cirq
        coords = sorted(cirq.google.Bristlecone.qubits)
        
        pos = {}
        for q in range(num):
            pos[q] = [coords[q].row, coords[q].col]
            
        pairs = {}
        char = 33
        for q1 in range(num):
            for q2 in range(num):
                if coords[q1].is_adjacent(coords[q2]) and [q2,q1] not in pairs.values():
                        pairs[chr(char)] = [q1,q2]
                        char+=1
            
        example = makeExample ( num, pairs )
        
        entangleType = "CZ"
        sdk = "Cirq"
        runs = {True:{'shots':[100],'move':['C','R'],'maxScore':20,'samples':100},False:{'shots':[8192],'move':['C'],'maxScore':10,'samples':100}}
    
    
    ######## DEVICES NOT ON THE CLOUD ########
    
    
    elif device=="8Q-Wallraff":
        # A device from the group of A. Wallraff at ETH
        # https://arxiv.org/abs/1801.07904
    
        # Note: Since this is an even number of qubits on a line, only one pairing is possible using the standard method.
        #       To spice things up a bit, a fake qubit is added, along with fake entangling gates.
        #       QuantumAwesomeness.py knows to not implement entangling gates whose name starts with 'fake'.
        #       But they will allow pairings to occur in which two (non-neighbouring) qubits are left unpaired.
    
        num = 9 # actually there are 8. But they number from 1, so 0 is unused
        area = [4,2]
        entangleType = "CZ"
        pairs = { 'A': [1,2], 'B': [2,3], 'C': [3,4], 'D': [4,5], 'E': [5,6], 'F': [6,7], 'G': [7,8],
                  'fake1':[0,1], 'fake2':[0,2], 'fake3':[0,3], 'fake4':[0,4], 'fake5':[0,5], 'fake6':[0,6], 'fake7':[0,7], 'fake8':[0,8] }
        pos = { 1: [0,1], 2: [1,1], 3: [2,1], 4: [3,1],
                8: [0,0], 7: [1,0], 6: [2,0], 5: [3,0] }
        example = [None, 0.24, 0.25, 0.06, 0.075, 0.175, 0.165, 0.235, 0.225]
        sdk = "ProjectQ"
        runs = {True:{'shots':[100],'move':['C','R'],'maxScore':20,'samples':100},False:{'shots':[8192],'move':['C'],'maxScore':10,'samples':100}}
    
    
    
    ######## PATTERN DEVICES (FOR SIMULATION ONLY) ########
    
    # See devicePrep.py for the types of pattern devices that have currently been defined.
    
    else:
        
        area,  pairs, pos, example = makeLayout (device)
        entangleType = "CZ"
        sdk = "QISKit" # any could be used, but QISKit is the best sdk
        runs = {True:{'shots':[100],'move':['C','R'],'maxScore':20,'samples':100},False:{'shots':[],'move':[],'maxScore':0,'samples':0}}
    
    
    return num, area, entangleType, pairs, pos, example, sdk, runs
