# These functions can be used to create some of the required information for devices.py

import math

def makeExample ( num, pairs ):
    
    # takes 'num' and 'pairs' for a device and returns 'example' (see devices.py for more on what these are)
    
    example = [0]*num
    from QuantumAwesomeness import getDisjointPairs
    import random
    matchingPairs = getDisjointPairs ( pairs, [], {} )
    for pair in matchingPairs:
        example[ pairs[pair][0] ] = random.random()/2
        example[ pairs[pair][1] ] = example[ pairs[pair][0] ] + 0.05 * random.random()
        
    return example

def makeLayout (pattern):
    
    # The input is a string that specifies a type of pattern device ('line, 'ladder', 'square' or 'web') and the number of qubits
    # This is done in the form:    pattern = type + str(num)
    # Given this information, this function determines the corresponding 'area', 'pairs, 'pos' and 'example for devices.py
    # The type specifies the connectivity graph:
    #     - 'line' is a 1D, open-ended line connectivity
    #     - 'ladder' is a 2 X (num/2) open-ended square lattice (so num needs to be even)
    #     - 'square' is a sqrt(num) X sqrt(num) square lattice with open boundaries (so num needs to be square)
    #     - 'web' is all-to-all connectivity
    
    if pattern[0:4]=="line":
        
        num = int(pattern[4:])
        
        if (num%2)==1: # we can continue only num is odd
            area = [num,1]
            entangleType = "CZ"
            pairs = {}
            for qubit in range(num-1):
                pairs[chr(65+qubit)] = [qubit,qubit+1]
            pos = {}
            for qubit in range(num):
                pos[qubit] = [qubit,0]
            runs = {True:{'shots':[100],'move':['C','R'],'maxScore':20,'samples':100},False:{'shots':[],'move':[],'maxScore':0,'samples':0}}
        else:
            print("Try again with a valid number of qubits for this configuration")
        
    elif pattern[0:6] in ["ladder","square"]:
        
        num = int(pattern[6:])
        
        if pattern[0:6]=="ladder":
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
            
        
    elif pattern[0:3]=="web":
        
        num = int(pattern[3:])
        
        L = int(math.sqrt(num))
            
        area = [L,L]
        pairs = {}
        pos = {}
            
        char = 65
        for q0 in range(num-1):
            for q1 in range(q0+1,num):
                pairs[chr(char)] = [q0,q1]
                char+=1
        
        for q0 in range(num):
            pos[q0] = [L*math.cos(q0*(2*math.pi)/num),L*math.sin(q0*(2*math.pi)/num)]
            
    else:
        
        print("\nWarning: " + str(device) + " is not a known device or pattern.\n")
    
    example = makeExample ( num, pairs )
    
    return area, pairs, pos, example