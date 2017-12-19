# tools from quantum awesomeness directory
from devices import *# info on supported devices
try:
    import mwmatching as mw # perfect matching
except:
    pass

# other tools
import random, numpy, math, time, copy, os, subprocess
import networkx as nx
import matplotlib.pyplot as plt
from itertools import product
import warnings
warnings.filterwarnings('ignore')

# import the required SDKs
try:
    from qiskit import QuantumProgram
    import Qconfig
except:
    pass#print("QISKit is not installed. This is not a problem if you don't plan to use it, but a big one if you do.")

try:
    import projectq
    from projectq.ops import H, Measure, CNOT, C, Z, Rx, Ry
except:
    pass#print("Project Q is not installed. This is not a problem if you don't plan to use it, but a big one if you do.")

try:
    from pyquil.quil import Program
    import pyquil.api as api
    from pyquil.gates import I, H, CNOT, CZ, RX, RY
except:
    pass#print("Forest is not installed. This is not a problem if you don't plan to use it, but a big one if you do.")

def initializeQuantumProgram ( device ):
    
    # *This function contains SDK specific code.*
    # 
    # Input:
    # * *device* - String specifying the device on which the game is played.
    #              Details about the device will be obtained using getLayout.
    # Process:
    # * Initializes everything required by the SDK for the quantum program. The details depend on which SDK is used.
    # Output:
    # * *q* - Register of qubits (needed by both QISKit and ProjectQ).
    # * *c* - Register of classical bits (needed by QISKit only).
    # * *engine* - Class required to create programs in QISKit, ProjectQ and Forest.
    # * *script* - The quantum program, needed by QISKit and Forest.

    num, area, entangleType, pairs, pos, example, sdk, runs = getLayout(device)
    
    if sdk in ["QISKit","ManualQISKit"]:
        engine = QuantumProgram()
        engine.set_api(Qconfig.APItoken, Qconfig.config["url"]) # set the APIToken and API url
        q = engine.create_quantum_register("q", num)
        c = engine.create_classical_register("c", num)
        script = engine.create_circuit("script", [q], [c]) 
    elif sdk=="ProjectQ":
        engine = projectq.MainEngine()
        q = engine.allocate_qureg( num )
        c = None
        script = None
    elif sdk=="Forest":
        engine = api.QVMConnection(use_queue=True)
        script = Program()
        q = range(num)
        c = range(num)
        
    return q, c, engine, script


def implementGate (device, gate, qubit, script, frac = 0 ):
    
    # *This function contains SDK specific code.*
    # 
    # Input:
    # * *device* - String specifying the device on which the game is played.
    #              Details about the device will be obtained using getLayout.
    # * *gate* - String that specifies gate type.
    # * *qubit* - Qubit, list of two qubits or qubit register on which the gate is applied.
    # * *script* - 
    # * *frac* -  
    # 
    # Process:
    # * For gates of type 'X', 'Z' and 'XX', the gate $U = \exp(-i \,\times\, gate \,\times\, frac )$ is implemented on the qubit or pair of qubits in *qubit*.
    # * *gate='Finish'* implements the measurement command on the qubit register required for ProjectQ to not complain.
    # 
    # Output:
    # * None are returned, but modifications are made to the classes that contain the quantum program.
    
    num, area, entangleType, pairs, pos, example, sdk, runs = getLayout(device)
    
    if sdk in ["QISKit","ManualQISKit"]:
        if gate=='X':
            script.u3(frac * math.pi, -math.pi/2,math.pi/2, qubit )
        elif gate=='Z': # actually a Y axis rotation
            script.u3(frac * math.pi, 0,0, qubit )
        elif gate=='XX':
            if entangleType=='CX':
                script.cx( qubit[0], qubit[1] )
                script.u3(frac * math.pi, -math.pi/2,math.pi/2, qubit[0] )
                script.cx( qubit[0], qubit[1] )
            elif entangleType=='CZ':
                script.h( qubit[1] )
                script.cz( qubit[0], qubit[1] )
                script.u3(frac * math.pi, -math.pi/2,math.pi/2, qubit[0] )
                script.cz( qubit[0], qubit[1] )
                script.h( qubit[1] )
            else:
                print("Support for this is yet to be added")
    
    elif sdk=="ProjectQ":
        if gate=='X':
            Rx( frac * math.pi ) | qubit
        elif gate=='Z': # actually a Y axis rotation
            Ry( frac * math.pi ) | qubit
        elif gate=='XX':
            if entangleType=='CX':
                CNOT | ( qubit[0], qubit[1] )
                Rx( frac * math.pi ) | qubit[0]
                CNOT | ( qubit[0], qubit[1] )
            elif entangleType=='CZ':
                H | qubit[1]
                C(Z) | ( qubit[0], qubit[1] )
                Rx( frac * math.pi ) | qubit[0]
                C(Z) | ( qubit[0], qubit[1] )
                H | qubit[1]
            else:
                print("Support for this is yet to be added")
        elif gate=='finish':
            Measure | qubit
            
    elif sdk=="Forest":
        if gate=='X':
            script.inst( RX ( frac * math.pi, qubit ) )
        elif gate=='Z': # actually a Y axis rotation
            script.inst( RY ( frac * math.pi, qubit ) )
        elif gate=='XX':
            if entangleType=='CX':
                script.inst( CNOT( qubit[0], qubit[1] ) )
                script.inst( RX ( frac * math.pi, qubit[0] ) )
                script.inst( CNOT( qubit[0], qubit[1] ) )
            elif entangleType=='CZ':
                script.inst( H (qubit[1]) )
                script.inst( CZ( qubit[0], qubit[1] ) )
                script.inst( RX ( frac * math.pi, qubit[0] ) )
                script.inst( CZ( qubit[0], qubit[1] ) )
                script.inst( H (qubit[1]) )
            else:
                print("Support for this is yet to be added")

def getResults ( device, sim, shots, q, c, engine, script ):
    
    # *This function contains SDK specific code.*
    # 
    # Input:
    # * *device* - String specifying the device on which the game is played.
    #              Details about the device will be obtained using getLayout.
    # 
    # Process:
    # * Implements all unitary quantum operations used in the program.
    # 
    # Output:
    # * None are returned, but modifications are made to the classes that contain the quantum program.
    
    num, area, entangleType, pairs, pos, example, sdk, runs = getLayout(device)
    
    if sdk=="QISKit":
        # pick the right backend
        if sim:
            backend = 'ibmqx_qasm_simulator'
        else:
            backend = device
        # add measurement for all qubits
        for n in range(num):
            script.measure( q[n], c[n] )
          
        # make sure the qasm compiles properly (commented out because of https://github.com/QISKit/qiskit-sdk-py/issues/157)
        #cmap = engine.get_backend_configuration(device)['coupling_map']
        #qobj = engine.compile(["script"], backend=device, coupling_map=cmap)
        #print(engine.get_compiled_qasm(qobj,"script"))
           
        # execute job
        noResults = True
        while noResults:
            try: # try to run, and wait for 5 mins if it fails
                executedJob = engine.execute(["script"], backend=backend, shots=shots, max_credits = 5, wait=2, timeout=600, silent=False)
                # get results
                resultsVeryRaw = executedJob.get_counts("script")
                if ('status' not in resultsVeryRaw.keys()): # see if it actually is data, and wai for 5 mins if not
                    noResults = False
                else:
                    print(resultsVeryRaw)
                    print("This is not data, so we'll wait and try again")
                    time.sleep(300)
            except:
                print("Job failed. We'll wait and try again")
                time.sleep(300)
                
        # invert order of the bit string and turn into probs
        resultsRaw = {}
        for string in resultsVeryRaw.keys():
            invertedString = string[::-1]
            resultsRaw[ invertedString ] = resultsVeryRaw[string]/shots
            
    elif sdk=="ManualQISKit":
        # add measurement for all qubits
        for n in range(num):
            script.measure( q[n], c[n] )
        qasm = engine.get_qasm("script")
        input("\nYou'll now be given the QASM representation of the circuit. Find a way to run it, and then copy the results in the input box...\n")
        input("The results you provide should be in the form of a dictionary, with bit strings as keys and the fraction of times these occurred as a result as values...")
        input("Well, actually you should find some way to do this programatically. The function 'getResults' is what you need to look at. But copy and paste will do for now....\n")
        resultsRaw = eval(input(qasm+"\n"))
    
    elif sdk=="ProjectQ":
        engine.flush()
        # list of bit strings
        strings = [''.join(x) for x in product('01', repeat=num)]
        # get prob for each bit string to make resultsRaw
        resultsRaw = {}
        for string in strings:
            resultsRaw[ string ] = engine.backend.get_probability( string, q )
            
    elif sdk=="Forest":
        
        # add measurement for all qubits
        for qubit in range (num):
            script.measure(qubit, [qubit] )
        # get results
        resultsVeryRaw = engine.run(script, range(num), trials=shots)
        # convert them the correct form
        resultsRaw = {}
        for sample in resultsVeryRaw:
            bitString = ""
            for bit in sample:
                bitString += str(bit)
            if bitString not in resultsRaw.keys():
                resultsRaw[bitString] = 0
            resultsRaw[bitString] += 1/shots 
    
    return resultsRaw


def printM ( string, move ):
    
    # If *move=M*, this is just *print()*. Otherwise it does nothing.

    if move=="M":
        print(string)


def entangle( device, move, shots, sim, gates, conjugates ):
    
    # Input:
    # * *device* - String specifying the device on which the game is played.
    #              Details about the device will be obtained using getLayout.
    # * *move* -
    # * *shots* -
    # * *sim* -
    # * *gates* - Entangling gates applied so far. Each round of the game corresponds to two 'slices'. *gates* is a list with a dictionary for each slice. The dictionary has pairs of qubits as keys and fractions of pi defining a corresponding entangling gate as values.
    # * *conjugates* - List of single qubit gates to conjugate entangling gates of previous rounds. Each is specified by a two element list. First is a string specifying the rotation axis ('X' or 'Z'), and the second specifies the fraction of pi for the rotation.
    #
    # Process:
    # * Sets up and runs a quantum circuit consisting of all gates thus far.
    #
    # Output:
    # * *oneProb* - A list with an entry for each qubit. Each entry is the fraction of samples for which the measurement of that qubit returns *1*.
    
    num, area, entangleType, pairs, pos, example, sdk, runs = getLayout(device)
    
    q, c, engine, script = initializeQuantumProgram(device)

    # apply all gates
    # gates has two entries for each round, except for the current round which has only one
    rounds = int( (len(gates)+1)/2 )
    
    # loop over past rounds and apply the required gates
    for r in range(rounds-1):

        # do the first part of conjugation (the inverse)
        for n in range(num):
            implementGate ( device, conjugates[r][n][0], q[n], script, frac=-conjugates[r][n][1] )

        # get the sets of gates that create and (attempt to) remove the puzzle for this round
        gates_create = gates[2*r]
        gates_remove = gates[2*r+1]
        
        # determine which pairs are for both, and which are unique
        pairs_both = list( set(gates_create.keys()) & set(gates_remove.keys()) )
        pairs_create = list( set(gates_create.keys()) - set(gates_remove.keys()) )
        pairs_remove = list( set(gates_remove.keys()) - set(gates_create.keys()) )
              
        # then do the exp[ i XX * frac ] gates accordingly
        for p in pairs_both:
            #print([r,p,gates_create[p]+gates_remove[p]] )
            implementGate ( device, "XX", [ q[pairs[p][0]], q[pairs[p][1]] ], script, frac=(gates_create[p]+gates_remove[p]) )
        for p in pairs_create:
            #print([r,p,gates_create[p]] )
            implementGate ( device, "XX", [ q[pairs[p][0]], q[pairs[p][1]] ], script, frac=(gates_create[p]) )
        for p in pairs_remove:
            #print([r,p,gates_remove[p]] )
            implementGate ( device, "XX", [ q[pairs[p][0]], q[pairs[p][1]] ], script, frac=(gates_remove[p]) )
            
        # do the second part of conjugation
        for n in range(num):
            implementGate ( device, conjugates[r][n][0], q[n], script, frac=conjugates[r][n][1] )
    
    # then the same for the current round (only needs the exp[ i XX * (frac - frac_inverse) ] )
    r = rounds-1
    for p in gates[2*r].keys():
        implementGate ( device, "XX", [ q[ pairs[p][0] ], q[ pairs[p][1] ] ], script, frac=gates[2*r][p] )
    
    
    resultsRaw = getResults( device, sim, shots, q, c, engine, script )
    
    strings = list(resultsRaw.keys())
    
    if sim==True:
        # sample from this prob dist shots times to get results
        results = {}
        for string in strings:
            results[string] = 0
        for shot in range(shots):
            j = numpy.random.choice( len(strings), p=list(resultsRaw.values()) )
            results[strings[j]] += 1/shots
    else:
        results = resultsRaw
        
    # determine the fraction of results that came out as 1 (instead of 0) for each qubit
    oneProb = [0]*num
    for bitString in strings:
        for v in range(num):
            if (bitString[v]=="1"):
                oneProb[v] += results[bitString]
    
    implementGate ( device, "finish", q, script )
    
    return oneProb


def calculateEntanglement( oneProb ):
    
    E = 1-2*abs( 0.5-oneProb )
    
    return E


def calculateFuzz ( oneProb, pairs, matchingPairs ):
    
    # Input:
    # * *oneProb* - A list with an entry for each qubit.
    #               Each entry is the fraction of samples for which the measurement of that qubit returns *1*.
    # * *matchingPairs* - The pairing of qubits in the current round.
    # 
    # Process:
    # * The two qubits of the same pair should have the same oneProb value. If they don't, it is because of fuzz.
    #   The fuzz is therefore quantified by the average difference between these values.
    # 
    # Output:
    # * *fuzzAv* - As described above.
    
    fuzzAv = 0
    for p in matchingPairs:
        fuzzAv += abs( oneProb[pairs[p][0]] - oneProb[pairs[p][1]] )/len(matchingPairs)
 
    return fuzzAv


def printPuzzle ( device, oneProb, move ):
    
    # ### *printPuzzle*
    # 
    # Input:
    # * *device* - String specifying the device on which the game is played.
    #              Details about the device will be obtained using getLayout.
    # * *oneProb* - A list with an entry for each qubit.
    #               Each entry is the fraction of samples for which the measurement of that qubit returns *1*.
    #
    # Process:
    # * The contents of *oneProb* contains some basic clues about the circuit that has been performed. It is the player's job to use those clues to guess the circuit. This means we have to print *oneProb* to screen. In order to make the game a pleasant experience and help build intuition about the device, this is done visually. The networkx package is used to visualize the layout of the qubits, and the oneProb information is conveyed using colour. 
    # 
    # Output:
    # * None returned, but the above described image is printed to screen.
    
    num, area, entangleType, pairs, pos, example, sdk, runs = getLayout(device)
    
    if move=="M":
        
        # create a graph with qubits as vertices and possible entangling gates as edges

        G=nx.Graph()

        for p in pairs:
            G.add_edge(pairs[p][0],pairs[p][1])

        for p in pairs:
            G.add_edge(pairs[p][0],p)
            G.add_edge(pairs[p][1],p)
            pos[p] = [(pos[pairs[p][0]][dim] + pos[pairs[p][1]][dim])/2 for dim in range(2)]

        # colour and label the edges with the oneProb data

        colors = []
        sizes = []
        labels = {}
        for node in G:
            if type(node)!=str:
                if (oneProb[node]>1): # if oneProb is out of bounds (due to this node having already been selected) make it grey
                    colors.append( (0.5,0.5,0.5) )
                else: # otherwise it is on the spectrum between red and blue
                    E = calculateEntanglement( oneProb[node] ) # colour is determined by entanglement
                    colors.append( (1-E,0,E) )
                sizes.append( 3000 )
                if oneProb[node]>1:
                    labels[node] = ""
                elif oneProb[node]==0.5:
                    labels[node] = "99"
                else:
                    labels[node] = "%.0f" % ( 100 * ( E ) )
            else:
                colors.append( "black" )
                sizes.append( 1000 )
                labels[node] = node

        # show it

        plt.figure(2,figsize=(2*area[0],1.25*area[1])) 
        nx.draw(G, pos, node_color = colors, node_size = sizes, labels = labels, with_labels = True,
                font_color ='w', font_size = 22.5)

        plt.show()


def getDisjointPairs ( pairs ):

    # Input:
    # * *pairs* - A dictionary with names of pairs as keys and lists of the two qubits of each pair as values
    # 
    # Process:
    # * A graph is created using the pairs as edges, and is assigned random weights.
    #   These max weight matched to find a disjoint set of pairs.
    # 
    # Output:
    # * *matchingPairs* - A list of the names of a random set of disjoint pairs included in the matching.
    
    edges = []
    for p in pairs.keys():
        edges.append( (pairs[p][0], pairs[p][1], random.randint(0,100) ) )
    
    # match[j] = k means that edge j and k are matched
    match = mw.maxWeightMatching(edges, maxcardinality=True)

    # get a list of the pair names for each pair in the matching
    matchingPairs = []
    for v in range(len(match)):
        for p in pairs.keys():
            if (pairs[p]==[v,match[v]]):
                matchingPairs.append(p)
                
    return matchingPairs


def runGame ( device, move, shots, sim, maxScore, dataNeeded=True ):
    
    # Input:
    # * *device* - String specifying the device on which the game is played.
    #              Details about the device will be obtained using getLayout.
    # * *move* -
    # * *shots* -
    # * *sim* -
    #
    # Process:
    # * Run the game!
    #
    # Output:
    # * *score* - score reached by the player at game over
    # * *gates*
    # * *conjugates*
    # * *totalFuzz* - the fuzz for each level (see calculateFuzz)
    
    num, area, entangleType, pairs, pos, example, sdk, runs = getLayout(device)
    
    gates = []
    conjugates = []
    totalFuzz = []
    oneProbs = []
    
    # if we are running off data, load up oneProbs for a move='C' run and see what the right answers are
    if dataNeeded==False:
        # oneProbs
        filename = 'move=C_shots=' + str(shots) + '_sim=' + str(sim) + '.txt'
        saveFile = open('results_' + device + '/oneProbs_'+filename)
        oneProbSamples = saveFile.readlines()
        saveFile.close()
        # gates
        filename = 'move=C_shots=' + str(shots) + '_sim=' + str(sim) + '.txt'
        saveFile = open('results_' + device + '/gates_'+filename)
        gateSamples = saveFile.readlines()
        saveFile.close()
        # choose a game
        game = random.randint( 0, len(oneProbSamples)-1 )
        oneProbs = eval( oneProbSamples[ game ] )
        gates = eval( gateSamples[ game ] )
        if maxScore==0: # in this case, we run to the end of the list
            maxScore = len( oneProbs )
    
    gameOn = True
    score = 0
    while gameOn:
        
        score += 1
        
        # Step 1: et a new puzzle
        
        if dataNeeded:
          
            # if running anew, we generate a new set of gates
  
            # gates applied are of the form
            # CNOT | (j,k)
            # Rx(frac*pi) | j
            # CNOT | (j,k)
            # and so are specified by a pair p=[j,k] and a random fraction frac
  
            # first we generate a random set of edges
            matchingPairs = getDisjointPairs( pairs )
          
            # then we add gates these to the list of gates
            appliedGates = {}
            for p in matchingPairs:
                frac = random.random() / 2 # this will correspond to a 0 \leq frac*pi \leq pi/2 rotation 
                appliedGates[p] = frac
            gates.append(appliedGates)
          
            # all gates so far are then run
            oneProb = entangle( device, move, shots, sim, gates, conjugates)
          
        else:
            
            oneProb = oneProbs[score-1]
            matchingPairs = list(gates[ 2*(score-1) ].keys())
        
        
        # Step 2: Get player to guess pairs
        
        displayedOneProb = copy.copy( oneProb )
        
        # prepare grid and print to screen
        printM("",move)
        printM("Round "+str(score), move)
        printPuzzle( device, displayedOneProb, move )

        guessedPairs = []

        # if choices are all correct, we just give the player the right answer
        if (move=="C"):
            guessedPairs = matchingPairs
        # if choices are random, we generate a set of random pairs
        if (move=="R"):
            guessedPairs = getDisjointPairs( pairs )
        # if choices are manual, let's get choosing
        if (move=="M"):

            # get the player choosing until the choosing is done
            unpaired = num
            while (unpaired>1):  

                pairGuess = input("\nChoose a pair\n")

                if (pairGuess in pairs.keys()) and (pairGuess not in guessedPairs) :

                    guessedPairs.append(pairGuess)

                    # set them both to grey on screen (set the corresponding oneProb value to >1)
                    for j in [0,1]:
                        displayedOneProb[ pairs[pairGuess][j] ] = 2
                    printM("\n\n\n", move)

                else:
                    printM("That isn't a valid pair. Try again.\n(Note that input is case sensitive)", move)

                # check if all vertices have been covered
                unpaired = 0
                for n in range(num):
                    unpaired += ( displayedOneProb[n] <= 1 )
            
                printPuzzle ( device, displayedOneProb, move )
        
        
        # get the fuzz for this level
        totalFuzz.append( calculateFuzz( oneProb, pairs, matchingPairs ) )  
        # store the oneProb
        oneProbs.append( oneProb )
        
        # see whether the game over condition is satisfied (totalFuzz for this level > 0.1)
        gameOn = (score<maxScore)
        
        # given the chosen pairs, the gates are now deduced from oneProb
        guessedGates = {}

        for p in guessedPairs:

            guessedOneProb = 0
            for j in range(2):
                guessedOneProb += oneProb[ pairs[p][j] ] / 2
            
            # Prob(1) = sin(frac*pi/2)^2
            # therefore frac = asin(sqrt(oneProb)) *2 /pi
            guessedFrac = math.asin(math.sqrt(guessedOneProb)) * 2 / math.pi

            # since the player wishes to apply the inverse gate, the opposite frac is stored
            guessedGates[p] = -guessedFrac

        # now we can add to the list of all gates
        gates.append(guessedGates)
        
        # finally randomly generate X or Z rotation to conjugate this round with
        newconjugates = []
        for n in range(num):
            newconjugates.append( [ numpy.random.choice(['X','Z']) , random.random() ] )
        conjugates.append(newconjugates)
                
        printM("", move)
        printM("", move)
        printM("Pairs you guessed for this round", move)
        printM(sorted(guessedPairs), move)
        printM("Correct pairs for this round", move)
        printM(sorted(matchingPairs), move)
        printM("Fuzziness for this round", move)
        printM(str(round(200*totalFuzz[-1])) +"%" , move)
        printM("", move)
        printM("", move)
        if move=='M':
            input(">Press Enter for the next round...\n")
    
    if move=="M":
        input("> The data has run out :( Press Enter to restart...\n")
    
    return gates, conjugates, totalFuzz, oneProbs


def MakeGraph(X,Y,y,axisLabel,labels=[],verbose=False,log=False):
    
    plt.rcParams.update({'font.size': 30})
    
    # convert the variances of varY into widths of error bars
    for j in range(len(y)):
        for k in range(len(y[j])):
            y[j][k] = math.sqrt(y[j][k]/2)
    
    plt.figure(figsize=(20,10))
    
    # add in the series
    for j in range(len(Y)):
        if labels==[]:
            plt.errorbar(X, Y[j], marker = "x", markersize=20, yerr = y[j], linewidth=5)
        else:
            plt.errorbar(X, Y[j], label=labels[j], marker = "x", markersize=20, yerr = y[j], linewidth=5)
    
    plt.legend(bbox_to_anchor=(1.05, 1), loc=2, borderaxespad=0.)
    
    # label the axes
    plt.xlabel(axisLabel[0])
    plt.ylabel(axisLabel[1])
    
    # make sure X axis is fully labelled
    plt.xticks(X)

    # logarithms if required
    if log==True:
        plt.yscale('log')

    # make the graph
    plt.show()
    
    plt.rcParams.update(plt.rcParamsDefault)
    
    # if verbose, print the numbers to screen
    if verbose==True:
        print("\nX values")
        print(X)
        for j in range(len(Y)):
            print("\nY values for series "+str(j))
            print(Y[j])
            print("\nError bars")
            print(y[j])
            print("")


def GetData ( device, move, shots, sim, samples, maxScore ):

    for sample in range(samples):

        print("move="+move+", shots="+str(shots)+", sample=" + str(sample+1) )

        gates, conjugates, totalFuzz, oneProbs = runGame( device, move, shots, sim, maxScore )

        # make a directory for this device if it doesn't already exist
        if not os.path.exists('results_' + device):
            os.makedirs('results_' + device)

        filename = 'move=' + move + '_shots=' + str(shots) + '_sim=' + str(sim) + '.txt'

        saveFile = open('results_' + device + '/totalFuzz_'+filename, 'a')
        saveFile.write( str(totalFuzz)+'\n' )
        saveFile.close()

        saveFile = open('results_' + device + '/oneProbs_'+filename, 'a')
        saveFile.write( str(oneProbs)+'\n' )
        saveFile.close()

        saveFile = open('results_' + device + '/gates_'+filename, 'a')
        saveFile.write( str(gates)+'\n' )
        saveFile.close()

        saveFile = open('results_' + device + '/conjugates_'+filename, 'a')
        saveFile.write( str(conjugates)+'\n' )
        saveFile.close()
        

def ProcessData ( device, move, shots, sim ):
    
    num, area, entangleType, pairs, pos, example, sdk, runs = getLayout(device)
    
    filename = 'move=' + move + '_shots=' + str(shots) + '_sim=' + str(sim) + '.txt'
    
    # get fuzz data
    saveFile = open('results_' + device + '/totalFuzz_'+filename)
    fuzzSamples = saveFile.readlines()
    saveFile.close()
    
    # get oneprob data
    saveFile = open('results_' + device + '/oneProbs_'+filename)
    oneProbSamples = saveFile.readlines()
    saveFile.close()
    # for each round, get mean of all Es
    # note, variable names make it sound like we are averaging oneProb, but we aren't: hacky mess :(
    meanOneProbSamples = []
    for sample in oneProbSamples:
        sample = eval(sample)
        meanOneProbs = []
        for roundOneProbs in sample:
            mean = 0
            for oneProb in roundOneProbs:
                mean += calculateEntanglement(oneProb)/num
            meanOneProbs.append( mean )
        meanOneProbSamples.append( meanOneProbs )
    
    # find number of samples
    samples = len(fuzzSamples)
    
    # find number of round in samples (assume same for all)
    maxScore = len(eval(fuzzSamples[0]))
    
    fuzzAv = [[0]*maxScore for _ in range(2)]
    for totalFuzz in fuzzSamples:
        totalFuzz = eval(totalFuzz)
        for score in range(maxScore):
            fuzzAv[0][score] += totalFuzz[score]/samples
            fuzzAv[1][score] += totalFuzz[score]**2/samples
    for score in range(maxScore):
        fuzzAv[1][score] -= fuzzAv[0][score]**2
        
    entangleAv = [[0]*maxScore for _ in range(2)]
    for meanOneProbs in meanOneProbSamples:
        for score in range(maxScore):
            entangleAv[0][score] += meanOneProbs[score]/samples
            entangleAv[1][score] += meanOneProbs[score]**2/samples
    for score in range(maxScore):
        entangleAv[1][score] -= entangleAv[0][score]**2
        

    return fuzzAv, entangleAv

def PlayGame():
    
    print("")
    print("")
    print("            __   _  _   __   __ _  ____  _  _  _  _               ")          
    print("           /  \\ / )( \\ / _\\ (  ( \\(_  _)/ )( \\( \\/ )              ")          
    print("          (  O )) \\/ (/    \\/    /  )(  ) \\/ (/ \\/ \\              ")          
    print("           \\__\\)\\____/\\_/\\_/\\_)__) (__) \\____/\\_)(_/              ")         
    print("  __   _  _  ____  ____   __   _  _  ____  __ _  ____  ____  ____ ") 
    print(" / _\\ / )( \\(  __)/ ___) /  \\ ( \\/ )(  __)(  ( \\(  __)/ ___)/ ___)") 
    print("/    \\\\ /\\ / ) _) \\___ \\(  O )/ \\/ \\ ) _) /    / ) _) \\___ \\\\___ \\") 
    print("\\_/\\_/(_/\\_)(____)(____/ \\__/ \\_)(_/(____)\\_)__)(____)(____/(____/") 
    print("")
    print("            A GAME TO BENCHMARK QUANTUM COMPUTERS")
    print("                     by James R. Wootton")
    print("                University of Basel/Decodoku")
    print("")
    print("")

    input("> Press Enter to continue...\n")
    
    intro = str.upper(input("\n> Do you want to read the introduction? (y/n)...\n"))
    if intro!="N":
        input("> This game let's you tackle puzzles that were forged on quantum computers...\n")
        input("> You don't need to know about quantum stuff to play...\n")
        input("> Nor will you learn any of the mysteries of the quantum world by playing...\n")
        input("> But you will get a bit of hands on experience of real prototype devices...\n")
        input("> And get an idea of how different devices compare...\n")
    deviceNotChosen = True
    attempt = 0
    deviceList = ""
    for device in supportedDevices():
        deviceList += device + " "
    while deviceNotChosen:
        message = "> The devices you can play on are\n\n  " + deviceList + "\n\n> Type the one you'd like below...\n"
        message = "\n> I'm afraid I didn't understand that.\n"*(attempt>0) + message
        device = input(message)
        if device in supportedDevices():
            deviceNotChosen = False
        else:
            attempt += 1
    
    num, area, entangleType, pairs, pos, example, sdk, runs = getLayout( device )
    
    tut = str.upper(input("> Do you want to read the tutorial? (y/n)...\n"))
    if tut!="N":
        printPuzzle(device,example,"M")
        input("> The game is a series of puzzles, which look something like this...\n")
        input("> Each circle" + ((num%2)==1)*" except one" + " is part of a pair...\n")
        input("> Your job is to find these pairs...\n")
        input("> All the possible ways that the circles can pair are labelled by letters...\n")
        input("> The colours and numbers for paired circles should be similar...\n")
        input("> But as the game progresses, these things get a bit fuzzy...\n")
        input("> They will become less and less similar, and the puzzle will become harder...\n")
        input("> The nature of the puzzles depends strongly on the quantum device that runs them...\n")
        input("> The possible pairings depend on the connectivity of the quantum device...\n")
        input("> A better connected device means more possibilities, and so a better puzzle...\n")
        input("> The device also influences the way the fuzziness, and hence the difficulty, increases...\n")
        input("> The game is designed to have a nice gentle increase in difficulty...\n")
        input("> This would be due to a process that has been proposed\n  to prove that quantum computers can be better than normal ones...\n")
        input("> But noise increases difficulty too, and can do so in a faster and dirtier way...\n")
        input("> If you want to see how potent noise is, compare a run on the real device with one on a (noiseless) simulator...\n")
        input("> Do the simulator first, to get an idea for how things are supposed to be...\n")  
        
            
    s = str.upper(input("> Do you want to play a game from the real device? (y/n)...\n"))
    sim = (s!='Y')
    if sim:
        input("> The following game data will be from a simulated run...\n")
    
    shots = min( runs[sim]['shots'] )
        
    try:
        runGame ( device, 'M', shots, sim, 0, dataNeeded=False )
    except:
        input("> Something went wrong. This probably means there is no saved data to play the game you requested.\n> Try choosing a different device...\n")

