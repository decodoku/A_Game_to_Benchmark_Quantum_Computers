# first, some tools we'll need from this directory
from devices import * # info on supported devices
from devicePrep import *
try:
    import mwmatching as mw # perfect matching
except:
    pass

# other tools
import random, numpy, math, time, copy, os
from IPython.display import clear_output
import networkx as nx
import matplotlib.pyplot as plt
from itertools import product
import warnings
warnings.filterwarnings('ignore')

path = os.path.dirname(os.path.abspath(__file__))


def importSDK ( device ):
    
    # *This function contains SDK specific code.*
    # 
    # Input:
    # * *device* - String specifying the device on which the game is played.
    #              Details about the device will be obtained using getLayout.
    # Process:
    # * The SDK associated with this device is imported.
    #
    # Output:
    # * Nothing returned, but global variables required by the SDKs are defined
    
    num, area, entangleType, pairs, pos, example, sdk, runs = getLayout(device)

    if sdk in ["QISKit","ManualQISKit"]:
        global ClassicalRegister, QuantumRegister, QuantumCircuit, execute, register, available_backends, get_backend
        from qiskit import ClassicalRegister, QuantumRegister
        from qiskit import QuantumCircuit, execute
        from qiskit import register, available_backends, get_backend
        try:
            import Qconfig
            qx_config = {
                "APItoken": Qconfig.APItoken,
                "url": Qconfig.config['url']}
            register(qx_config['APItoken'], qx_config['url'])
        except:
            pass
    elif sdk=="ProjectQ":
        global projectq, H, Measure, CNOT, C, Z, Rx, Ry
        import projectq
        from projectq.ops import H, Measure, CNOT, C, Z, Rx, Ry
    elif sdk=="Forest":
        global Program, api, I, H, CNOT, CZ, RX, RY
        from pyquil.quil import Program
        import pyquil.api as api
        from pyquil.gates import I, H, CNOT, CZ, RX, RY
    elif sdk=="Cirq":
        global GridQubit, CNOT, CZ, X, Y, Circuit, H, measure, google
        from cirq import GridQubit, CNOT, CZ, X, Y, Circuit, H, measure, google

def initializeQuantumProgram ( device, sim ):
    
    # *This function contains SDK specific code.*
    # 
    # Input:
    # * *device* - String specifying the device on which the game is played.
    #              Details about the device will be obtained using getLayout.
    # * *sim* - Boolean denoting whether this is a simulated run
    # Process:
    # * Initializes everything required by the SDK for the quantum program. The details depend on which SDK is used.
    #
    # Output:
    # * *q* - Register of qubits (used by QISKit, ProjectQ and Circ).
    # * *c* - Register of classical bits (used by QISKit).
    # * *engine* - Class required to create programs (used by ProjectQ and Forest).
    # * *script* - The quantum program (used by QISKit, Forest and Circ).

    num, area, entangleType, pairs, pos, example, sdk, runs = getLayout(device)
    
    importSDK ( device )
    
    if sdk in ["QISKit","ManualQISKit"]:
        engine = None
        q = QuantumRegister(num)
        c = ClassicalRegister(num)
        script = QuantumCircuit(q, c)
    elif sdk=="ProjectQ":
        engine = projectq.MainEngine()
        q = engine.allocate_qureg( num )
        c = None
        script = None
    elif sdk=="Forest":
        if sim:
            engine = api.QVMConnection(use_queue=True)
        else:
            engine = api.QPUConnection(device)   
        script = Program()
        q = range(num)
        c = range(num)
    elif sdk=="Cirq":
        q = []
        for qubit in range(num):
            q.append( GridQubit( pos[qubit][0], pos[qubit][1] ) )
        c = None
        engine = None
        script = Circuit.from_ops()                   
        
        
    return q, c, engine, script


def implementGate (device, gate, qubit, script, frac = None ):
    
    # *This function contains SDK specific code.*
    # 
    # Input:
    # * *device* - String specifying the device on which the game is played.
    #              Details about the device will be obtained using getLayout.
    # * *gate* - String that specifies gate type. Should be 'X', 'Y' or 'XX' rotation, or 'finish'.
    # * *qubit* - Qubit, list of two qubits or qubit register on which the gate is applied.
    # * *script* - Used to store the quantum program in some SDKs
    # * *frac=0* - Fraction of pi for which an X rotation is applied. Not required for gate of type 'finish'.
    # 
    # Process:
    # * For gates of type 'X', 'Y' and 'XX', the gate $U = \exp(-i \,\times\, gate \,\times\, frac )$ is implemented on the qubit or pair of qubits in *qubit*.
    # * *gate='Finish'* implements the measurement command on the qubit register required for ProjectQ to not complain.
    # 
    # Output:
    # * None are returned, but modifications are made to the objects that contain the quantum program.
    
    num, area, entangleType, pairs, pos, example, sdk, runs = getLayout(device)
    
    if sdk in ["QISKit","ManualQISKit"]:
        if gate=='X':
            script.u3(frac * math.pi, -math.pi/2, math.pi/2, qubit )
        elif gate=='Y': # a Y axis rotation
            script.u3(frac * math.pi, 0,0, qubit )
        elif gate=='XX':
            if entangleType=='CX':
                script.cx( qubit[0], qubit[1] )
                script.u3(frac * math.pi, -math.pi/2, math.pi/2, qubit[0] )
                script.cx( qubit[0], qubit[1] )
            elif entangleType=='CZ':
                script.h( qubit[1] )
                script.cz( qubit[0], qubit[1] )
                script.u3(frac * math.pi, -math.pi/2, math.pi/2, qubit[0] )
                script.cz( qubit[0], qubit[1] )
                script.h( qubit[1] )
            else:
                print("Support for this is yet to be added")
    
    elif sdk=="ProjectQ":
        if gate=='X':
            Rx( frac * math.pi ) | qubit
        elif gate=='Y': # a Y axis rotation
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
            if qubit in pos.keys(): # only if qubit is active
                script.inst( RX ( frac * math.pi, qubit ) )
        elif gate=='Y': # a Y axis rotation
            if qubit in pos.keys(): # only if qubit is active
                script.inst( RY ( frac * math.pi, qubit ) )
        elif gate=='XX':
            if entangleType=='CX':
                script.inst( CNOT( qubit[0], qubit[1] ) )
                script.inst( RX ( frac * math.pi, qubit[0] ) )
                script.inst( CNOT( qubit[0], qubit[1] ) )
            elif entangleType=='CZ':
                script.inst( H ( qubit[1] ) )
                script.inst( CZ( qubit[0], qubit[1] ) )
                script.inst( RX ( frac * math.pi, qubit[0] ) )
                script.inst( CZ( qubit[0], qubit[1] ) )
                script.inst( H ( qubit[1] ) )
            elif entangleType=='none':
                script.inst( RX ( frac * math.pi, qubit[0] ) )
                script.inst( RX ( frac * math.pi, qubit[1] ) )
            else:
                print("Support for this is yet to be added")
                
    elif sdk=="Cirq":
        if gate=='X':
            if qubit in pos.keys(): # only if qubit is active
                script.append( X(qubit)**frac )
        elif gate=='Y': # a Y axis rotation
            if qubit in pos.keys(): # only if qubit is active
                script.append( Y(qubit)**frac )
        elif gate=='XX':
            if entangleType=='CX':
                script.append( CNOT(qubit[0],qubit[1]) )        
                script.append( X(qubit[0])**frac )
                script.append( CNOT(qubit[0],qubit[1]) ) 
            elif entangleType=='CZ':
                script.append( H(qubit[1]) )
                script.append( CZ(qubit[0],qubit[1]) ) 
                script.append( X(qubit[0])**frac )
                script.append( CZ(qubit[0],qubit[1]) ) 
                script.append( H(qubit[1]) )
            else:
                print("Support for this is yet to be added")           
                

                
def resultsLoad ( fileType, move, shots, sim, device ) :
    
    # Input:
    # * *fileType* - String describing type of file to load.
    # * *move* - String describing the way moves were chosen for the results to be loaded.
    # * *shots* - Number of shots used in the results to be loaded.
    # * *sim* - Boolean denoting whether a simulator was used for the results to be loaded.
    # * *device* - String specifying the device on which the game is played.
    #
    # Process:
    # * A filename is created using the details given in the input. This file, which will contain and array of arrays, is then loaded, evalulated and stored as an which will contain and array of arrays.
    # If the file doesn't exist, the process will fail and throw and exception. This is a fatal error, so no exception handling is used.
    #
    # Output:
    # * *samples* - Array of arrays of whatever it was the file contained.
    
    filename = 'move='+move+'_shots=' + str(shots) + '_sim=' + str(sim) + '.txt'
    saveFile = open(path+'/results/' + device + '/'+fileType+'_'+filename)
    sampleStrings = saveFile.readlines()
    saveFile.close()
    
    samples = []
    for sampleString in sampleStrings:
        samples.append( eval( sampleString ) )
    
    return samples
                
            
def getResults ( device, sim, move, shots, q, c, engine, script, sample=None, qasm_file=None):
    
    # *This function contains SDK specific code.*
    # 
    # Input:
    # * *device* - String specifying the device on which the game is played.
    #              Details about the device will be obtained using getLayout.
    # * *q* - Register of qubits (used in some SDKs).
    # * *c* - Register of classical bits (used in some SDKs).
    # * *engine* - Class required to create programs (used in some SDKs).
    # * *script* - The quantum program (used in some SDKs).
    # 
    # Process:
    # * This function sends the quantum program to the desired backend to be run, and obtains results.
    # 
    # Output:
    # * *resultsRaw* - A dictionary whose keys are the bit strings obtained as results, and the values are the fraction of shots for which they occurred.
    
    num, area, entangleType, pairs, pos, example, sdk, runs = getLayout(device)
    
    if sdk=="QISKit":
        # pick the right backend
        if sim:
            backend = get_backend('local_qasm_simulator')
        else:
            backend = get_backend(device)
        # add measurement for all qubits
        script.barrier()
        for n in range(num):
            script.measure( q[n], c[n] )
           
        # execute job
        noResults = True
        while noResults:
            try: # try to run, and wait if it fails
                
                if not sim:
                    print('Status of device:',backend.status)
                job = execute(script, backend, shots=shots, skip_translation=True)
                resultsVeryRaw = job.result().get_counts()
                noResults = False
                
            except Exception as e:
                print(e)
                print("Job failed. We'll wait and try again")
                time.sleep(600)
                
        # invert order of the bit string and turn into probs
        resultsRaw = {}
        for string in resultsVeryRaw.keys():
            invertedString = string[::-1]
            resultsRaw[ invertedString ] = resultsVeryRaw[string]/shots
            
    elif sdk=="ManualQISKit":
        # add measurement for all qubits
        script.barrier()
        for n in range(num):
            script.measure( q[n], c[n] )
        qasm = script.qasm()
        qasm = qasm.replace('\n',r'\n')

        qasm_file.write('\n'+qasm)

        resultsRaw = None
    
    elif sdk=="ProjectQ":
        engine.flush()
        # list of bit strings
        strings = [''.join(x) for x in product('01', repeat=num)]
        # get prob for each bit string to make resultsRaw
        resultsRaw = {}
        for string in strings:
            resultsRaw[ string ] = engine.backend.get_probability( string, q )
            
    elif sdk=="Forest":
        
        # get list of active (and therefore plotted) qubits
        qubits_active = list(pos.keys())

        # execute job
        noResults = True
        while noResults:
            try: # try to run, and wait for 5 mins if it fails
                resultsVeryRaw = engine.run_and_measure(script, qubits_active, trials=shots)
                noResults = False
            except Exception as e:
                #print(e)
                print("\nJob failed. We'll wait and try again.\n")
                time.sleep(300)
                
        # convert them the correct form
        resultsRaw = {}
        for sample in resultsVeryRaw:
            bitString = ""
            disabled_so_far = 0
            for qubit in range(num):
                if qubit in qubits_active:
                    bitString += str(sample[qubit-disabled_so_far])
                else:
                    bitString += "0" # fake result for dead qubit
                    disabled_so_far += 1
            if bitString not in resultsRaw.keys():
                resultsRaw[bitString] = 0
            resultsRaw[bitString] += 1/shots 
    
    elif sdk=="Cirq":
                              
        # add measurement for all qubits
        for qubit in range(num):
            script.append( measure(q[qubit],key=qubit) )
                              
        if sim:
            backend = google.XmonSimulator()
        elif device=='Foxtail':
            backend = google.Foxtail
        elif device=='Bristlecone':
            backend = google.Bristlecone

        resultsExtremelyRaw = backend.run(script, repetitions=shots)              

        resultsVeryRaw = []
        for qubit in range(num):
            resultsVeryRaw.append( resultsExtremelyRaw.measurements[qubit][:, 0] )

        resultsRaw = {}
        for shot in range(shots):
            bitString = ""
            for qubit in range(num):
                if resultsVeryRaw[qubit][shot]:
                    bitString += '1'
                else:
                    bitString += '0'
            if bitString not in resultsRaw.keys():
                resultsRaw[bitString] = 0
            resultsRaw[bitString] += 1/shots                     

    
    return resultsRaw


def processResults ( resultsRaw, num, pairs, sim, shots ):
    
    # Input:
    # * *resultsRaw* - String specifying the device on which the game is played. Details about the device will be obtained using getLayout.
    # * *num* - The number of qubits in the device.
    # * *pairs* - A dictionary of pairs of qubits for which an entagling gate is possible. The key is a string which serves as the name of the pair. The value is a two element list with the qubit numbers of the two qubits in the pair. For controlled-NOTs, the control qubit is listed first.
    # * *sim* - Boolean denoting whether a simulator was used.
    # * *shots* - Number of shots used for statistics.
    # 
    # Process:
    # * This function sends the quantum program to the desired backend to be run, and obtains results.
    # 
    # Output:
    # * *oneProb* - A list with an entry for each qubit. Each entry is the fraction of samples for which the measurement of that qubit returns *1*.
    # * *sameProb* - A dictionary with pair names as keys, and probability that the two qubits each pair give the same results as values.
    # * *results* - If results are not from a simulator, this is just resultsRaw. If they are, it is assumed that the simulated effectively gave results with no statistical noise, so a sampling process is used to simulate the effect of the required number of shots.

    
    oneProb = [0]*num
    sameProb = {p: 0 for p in pairs}
    
    if type(resultsRaw) is dict: # try to process only if it is a dict (and so not if a job id)
    
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
            # results is just resultsRaw (but make sure it's normalized)
            results = {}
            for string, samples in resultsRaw.items():
                if type(samples) is int:
                    samples /= shots
                results[string] = samples

        # determine the fraction of results that came out as 1 (instead of 0) for each qubit
        
        for bitString in strings:
            for v in range(num):
                if (bitString[v]=="1"):
                    oneProb[v] += results[bitString]
        
        for bitString in strings:
            for p in pairs:
                if bitString[pairs[p][0]]==bitString[pairs[p][1]]:
                    sameProb[p] += results[bitString]
                    
    else:
        results = resultsRaw
                
    return oneProb, sameProb, results


def printM ( string, move ):
    
    # If *move=M*, this is just *print()*. Otherwise it does nothing.

    if move=="M":
        print(string)


def entangle( device, move, shots, sim, gates, conjugates, sample=None, qasm_file=None):
    
    # Input:
    # * *device* - String specifying the device on which the game is played.
    #              Details about the device will be obtained using getLayout.
    # * *move* - String describing the way moves were chosen when creating the circuit.
    # * *shots* - Number of shots to be taken.
    # * *sim* - Boolean denoting whether a simulator will be used.
    # * *gates* - Entangling gates applied so far. Each round of the game corresponds to two 'slices'. *gates* is a list with a dictionary for each slice. The dictionary has pairs of qubits as keys and fractions of pi defining a corresponding entangling gate as values.
    # * *conjugates* - List of single qubit gates to conjugate entangling gates of previous rounds. Each is specified by a two element list. First is a string specifying the rotation axis ('X' or 'Y'), and the second specifies the fraction of pi for the rotation.
    #
    # Process:
    # * Quantum circuit is created and run given the details (device, gates, etc) provided by the input. The results are then processed to give the final output.
    #
    # Output:
    # * *oneProb*, *sameProb* and *results* - See processResults() for explanation.
    
    num, area, entangleType, pairs, pos, example, sdk, runs = getLayout(device)
    
    q, c, engine, script = initializeQuantumProgram(device,sim)

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

        if sdk in ["QISKit", "ManualQISKit"]:
            script.barrier()
        
    
    # then the same for the current round (only needs the exp[ i XX * (frac - frac_inverse) ] )
    r = rounds-1
    for p in gates[2*r].keys():
        implementGate ( device, "XX", [ q[ pairs[p][0] ], q[ pairs[p][1] ] ], script, frac=gates[2*r][p] )
    
    
    resultsRaw = getResults( device, sim, move, shots, q, c, engine, script, sample, qasm_file)
    
    oneProb, sameProb, results = processResults ( resultsRaw, num, pairs, sim, shots )

    implementGate ( device, "finish", q, script )
    
    return oneProb, sameProb, results


def calculateEntanglement( oneProb, use_oneProb=True):
    
    # Input:
    # * *oneProb* - Float representing the fraction of samples for which the measurement of a qubit returns *1*.
    # * *use_oneProb* - Whether to use oneProb directly.
    # 
    # Process:
    # * Calculates the number that will be shown to the player, based on oneProb. This should be zero when oneProb is zero, 1 when oneProb is 0.5, and monotonic.
    # This is done by first calculating the frac that would result in such a oneProb (oneProb=0 ==> frac=0, oneProb=0.5 ==> frac=1/2, oneProb=1 ==> frac=1), and then doubling it. Since the result can exceed 1 in general (though only due to spurious effects that result in oneprob>0.5), it is capped by 1 before being returned.
    # This quantity is called the 'entanglement' because early versions used the mixedness
    # E = 1-2*abs( 0.5-oneProb )
    # which is a measure of how entangled a qubit is with the rest of the universe. The frac based measure is now used instead such that the resulting values have a more uniform spread.
    # 
    # Output:
    # * *E* - As described above.
    
    if use_oneProb:
        return oneProb
    else:
        E = ( 2 * calculateFrac( oneProb ) )    
        return min( E, 1)

def calculateFrac ( oneProb ):
    
    # Input:
    # * *oneProb* - Float representing the fraction of samples for which the measurement of a qubit returns *1*.
    # 
    # Process:
    # * Calculates the fraction of pi for an X rotation which would result in the given value of oneProb.
    # Prob(1) = sin(frac*pi/2)^2
    # therefore frac = asin(sqrt(oneProb)) *2 /pi
    # 
    # Output:
    # * *frac* - As described above.

    oneProb = max(0,oneProb)
    oneProb = min(1,oneProb)
    frac = math.asin(math.sqrt( oneProb )) * 2 / math.pi
    
    return frac
    

def calculateFuzz ( oneProb, pairs, matchingPairs ):
    
    # Input:
    # * *oneProb* - A list with an entry for each qubit. Each entry is the fraction of samples for which the measurement of that qubit returns *1*.
    # * *pairs* - A dictionary of pairs of qubits for which an entagling gate is possible. The key is a string which serves as the name of the pair. The value is a two element list with the qubit numbers of the two qubits in the pair. For controlled-NOTs, the control qubit is listed first.
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

def calculateEntropy ( probs ):
    
    # Input:
    # * *probs* - Array of probabilities. They are assumed to sum to 1, but this is not checked.
    # 
    # Process:
    # * The Shannon entropy, H, of the probability distribution is calculated
    # 
    # Output:
    # * *H* - As described above.
    
    H = 0
    for prob in probs:
        if prob>0:
            H -= prob * math.log(prob,2)

    return H

def calculateExpect ( probs ):
    
    # Input:
    # * *probs* - Array of probabilities.
    #
    # Process:
    # * For each probability, the expectation value is calculated. The probabilities are takem to be the probability of a value -1 value, with 1-p representing the probability of +1.
    # 
    # Output:
    # * *expect* - Corresponding array of expectation values.
    
    expect = []
    for p in probs:
        expect.append( 1-2*p)
    
    return expect

def calculateMutual ( oneProb, sameProb, pairs ):
    
    # Input:
    # * *oneProb* - A list with an entry for each qubit. Each entry is the fraction of samples for which the measurement of that qubit returns *1*.
    # * *sameProb* - A dictionary with pair names as keys, and probability that the two qubits each pair give the same results as values.
    # * *pairs* - A dictionary of pairs of qubits for which an entagling gate is possible. The key is a string which serves as the name of the pair. The value is a two element list with the qubit numbers of the two qubits in the pair. For controlled-NOTs, the control qubit is listed first.
    #
    # Process:
    # * For each pair, the (classical) mutual information for the measurement results of the two qubits is calculated. This is done using oneProbs and sameProbs, which is a bit of a pain. But this information is sufficient to calculate the probability for the results '00', '01', '10' and '11' for the two qubits of each pair, which the probability distrubution required to calculate the mutual information.
    # 
    # Output:
    # * *I* - Dictionary with pair names as keys and corresponding values of the mutual information as values.
    
    I = {}
    
    for p in sameProb.keys():
        
        p0 = oneProb[pairs[p][0]]
        p1 = oneProb[pairs[p][1]]
        
        expect = calculateExpect( [ p0, p1, 1-sameProb[p] ] )
            
        prob = [0]*4
        prob[0] = ( 1 + expect[0] + expect[1] + expect[2] )/4
        prob[1] = ( 1 - expect[0] + expect[1] - expect[2] )/4
        prob[2] = ( 1 + expect[0] - expect[1] - expect[2] )/4
        prob[3] = ( 1 - expect[0] - expect[1] + expect[2] )/4
                                          
        I[p] = calculateEntropy( [ 1-p0, p0 ] ) + calculateEntropy( [ 1-p1, p1 ] ) - calculateEntropy( prob )
        if I[p]>1e-3:
            I[p] = I[p] / min( calculateEntropy( [ 1-p0, p0 ] ) , calculateEntropy( [ 1-p1, p1 ] ) )
        
    return I

def printPuzzle ( device, oneProb, move='M', ascii=False ):
    
    # Input:
    # * *device* - String specifying the device on which the game is played.
    #              Details about the device will be obtained using getLayout.
    # * *oneProb* - A list with an entry for each qubit. Each entry is the fraction of samples for which the measurement of that qubit returns 1.
    # * *move* - String describing the way moves are chosen.
    # * *ascii* - Boolean to convey whether the image should be purely ascii.
    #
    # Process:
    # * The contents of *oneProb* contains some basic clues about the circuit that has been performed. It is the player's job to use those clues to guess the circuit. This means we have to print *oneProb* to screen. In order to make the game a pleasant experience and help build intuition about the device, this is done visually. The networkx package is used to visualize the layout of the qubits, and the oneProb information is conveyed using colour. This is done only when a player is manually playing, and so when move='M'.
    # * An altenative visualization has been partially implemented. This would use only ascii.
    # 
    # Output:
    # * None returned, but the above described image is printed to screen.
    
    num, area, entangleType, pairs, pos, example, sdk, runs = getLayout(device)
    
    if move=="M":
        
        if ascii:
            
            def change_char (string, char, pos):
                return string[:pos] + char + string[(pos+len(char)):]

            lines = 5
            length = 10

            def get_x (X):
                return int( length * X )

            def get_y (Y):
                return H-1 - int( lines * Y )

            W = length*(area[0]-1)+1
            H = lines*(area[1]-1)+1

            plot = [ "░"*(W+4) for _ in range(H) ]

            for pair in pairs:
                x = get_x( (pos[pairs[pair][0]][0]+pos[pairs[pair][1]][0])/2 )
                y = get_y( (pos[pairs[pair][0]][1]+pos[pairs[pair][1]][1])/2 )
                plot[y] = change_char(plot[y],pair,x)

                xx = [0]*2
                yy = [0]*2
                for j in range(2):
                    xx[j] = get_x( pos[pairs[pair][j]][0] )
                    yy[j] = get_y( pos[pairs[pair][j]][1] )

                for p in range(length):
                    x = int( xx[0] + (p/length)*(xx[1]-xx[0]) )
                    y = int( yy[0] + (p/length)*(yy[1]-yy[0]) )
                    plot[y] = change_char(plot[y]," ",x)

            for qubit in pos:
                x = get_x( pos[qubit][0] )
                y = get_y( pos[qubit][1] )

                num = "("+str(int(100*oneProb[qubit])) +")"

                plot[y] = change_char(plot[y],num,x)  
               
            print("░"*(W+8))
            for line in plot:
                print("░░░░"+line)
            print("░"*(W+8))
        
        else:
        
            # create a graph with qubits as vertices and possible entangling gates as edges

            G=nx.Graph()

            for p in pairs:
                if p[0:4]!='fake':
                    G.add_edge(pairs[p][0],pairs[p][1])

            for p in pairs:
                if p[0:4]!='fake':
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
                        E = calculateEntanglement( oneProb[node], use_oneProb=False)
                        colors.append( (1-E,0,E) )
                    sizes.append( 2500 ) # 1200 is also good (but set the font to 18)
                    if oneProb[node]>1:
                        labels[node] = ""
                    elif oneProb[node]==0.5:
                        labels[node] = "99"
                    else:
                        E = calculateEntanglement( oneProb[node])
                        labels[node] = "%.0f" % ( 100 * ( E ) )
                else:
                    colors.append( "black" )
                    sizes.append( 1000 ) # 600 is also good (but set the font to 18)
                    labels[node] = node

            # show it
            if area[0]>2*area[1]:
                ratio = 0.65
            else:
                ratio = 1

            plt.figure(2,figsize=(2*area[0],2*ratio*area[1])) 
            nx.draw(G, pos, node_color = colors, node_size = sizes, labels = labels, with_labels = True,
                    font_color ='w', font_size = 22.5)
            plt.show()

        
def calculateFracDifference (frac1, frac2):
 
    # Input:
    # * *frac1*, *frac2* - Two values of frac
    # 
    # Process:
    # * Determine the minimum difference between the two, accounting for the fact that frac=0 and frac=2 are equivalent. Note that his means that the 
    # 
    # Output:
    # * *matchingPairs* - A list of the names of a random set of disjoint pairs included in the matching.
    
    delta = max(frac1,frac2) - min(frac1,frac2)
    delta = min( delta, 1-delta )
    return delta  
        

def getDisjointPairs ( pairs, oneProb, weight ):

    # Input:
    # * *pairs* - A dictionary with names of pairs as keys and lists of the two qubits of each pair as values
    # * *oneProb* - A list with an entry for each qubit. Each entry is the fraction of samples for which the measurement of that qubit returns 1.
    # * *weight* - dictionary with pair names as keys and a weight assigned to each pair as the corresponding values.
    # 
    # Process:
    # * A minimum weight perfect matching of the qubits is performed, using the possible pairing and weights provided. If weights are not given, but oneProbs are, the weights are calculated from the oneProbs. If oneProbs aren't given either, the weights are chosen randomly to generate a random pairing.
    # 
    # Output:
    # * *matchingPairs* - A list of the names of a random set of disjoint pairs included in the matching.

    if not weight:
        for p in pairs.keys():
            if oneProb:
                weight[p] = -calculateFracDifference( calculateFrac( oneProb[ pairs[p][0] ] ) , calculateFrac( oneProb[ pairs[p][1] ] ) )
            else:
                weight[p] = random.randint(0,100)

    edges = []
    for p in pairs.keys():
        edges.append( ( pairs[p][0], pairs[p][1], weight[p] ) )
    
    # match[j] = k means that edge j and k are matched
    match = mw.maxWeightMatching(edges, maxcardinality=True)
    
    # get a list of the pair names for each pair in the matching (not including fakes)
    matchingPairs = []
    for v in range(len(match)):
        for p in pairs.keys():
            if pairs[p]==[v,match[v]] and p[0:4]!='fake' :
                matchingPairs.append(p)
    
    
    return matchingPairs


def runGame ( device, move, shots, sim, maxScore=None, dataNeeded=True, cleanup=False, game=None, ascii=False, sample=None, bias=0):
        
    # Input:
    # * *device* - String specifying the device on which the game is played.
    #              Details about the device will be obtained using getLayout.
    # * *move* - String describing the way moves are chosen.
    # * *shots* - Number of shots to be used for statistics.
    # * *sim* - Boolean for whether the simulator is to be used.
    # * *maxScore* - maximum number of rounds to run the game for
    # * *dataNeeded* - Boolean determining whether game need to obtain new data, or will run on old data
    # * *cleanup* - Boolean determining whether error mitigation post-processing is used
    # * *game* - Integer identifiying a specific game to play from a file (can only be True if dataNeeded=True)
    # * *ascii* - Boolean to convey whether the image presented to the player should be purely ascii.
    # * *bias* - Extra angle to add to inverses. 2016 work used 0.1/sqrt(shots). Default is now 0.

    #
    # Process:
    # * Runs the game! Done either by loading up saved data, or running a new instance.
    #
    # Output:
    # * *gates* - Entangling gates applied so far. Each round of the game corresponds to two 'slices'. *gates* is a list with a dictionary for each slice. The dictionary has pairs of qubits as keys and fractions of pi defining a corresponding entangling gate as values.
    # * *conjugates* - List of single qubit gates to conjugate entangling gates of previous rounds. Each is specified by a two element list. First is a string specifying the rotation axis ('X' or 'Y'), and the second specifies the fraction of pi for the rotation.
    # * *oneProbs*: Array of oneProb arrays (see processResults() for explanation of these), with an element for each round of the game.
    # * *sameProbs*: Array of sameProb arrays (see processResults() for explanation of these), with an element for each round of the game.
    # * *resultsDicts*: Array of results arrays (see processResults() for explanation of these), with an element for each round of the game.
    
    num, area, entangleType, pairs, pos, example, sdk, runs = getLayout(device)
    
    if sdk == 'ManualQISKit':
        qasm_file = open(path+'/results/'+device+'/qasm/qasm_'+move+'_'+str(shots)+'_'+str(sample)+'.txt','w')
    else:
        qasm_file = None

    gates = []
    conjugates = []
    oneProbs = []
    sameProbs = []
    resultsDicts = []
    
    # if we are running off data, load up oneProbs for a move='C' run and see what the right answers are
    if dataNeeded==False:
        
        oneProbSamples = resultsLoad ( 'oneProbs', 'C', shots, sim, device )
        sameProbSamples = resultsLoad ( 'sameProbs', 'C', shots, sim, device )
        gateSamples = resultsLoad ( 'gates', 'C', shots, sim, device )
        
        if maxScore is None: # if a maxScore is not given, use the value from the first sample
            maxScore = len( oneProbSamples[ 0 ] )
        
        if cleanup:
            cleaner = getCleaningProfile ( device, move, shots, sim, num, maxScore, gritty=True )
        
        samples = len(oneProbSamples) # find out how many samples there are
        

        
        # choose a game randomly if a specific one was not requested
        if game is None:
            game = random.randint( 0, samples-1 )
        # get the data for this game
        oneProbs = oneProbSamples[ game ]
        sameProbs = sameProbSamples[ game ] 
        originalOneProbs = copy.deepcopy( oneProbs )
        gates = gateSamples[ game ]      
            
    
    gameOn = True
    restart = False
    score = 0
    while gameOn:
        
        score += 1
        
        # Step 1: get a new puzzle
        
        if dataNeeded:
          
            # if running anew, we generate a new set of gates
  
            # gates applied are of the form
            # CNOT | (j,k)
            # Rx(frac*pi) | j
            # CNOT | (j,k)
            # and so are specified by a pair p=[j,k] and a random fraction frac
  
            # first we generate a random set of edges
            matchingPairs = getDisjointPairs( pairs, [], {} )
          
            # then we add gates these to the list of gates
            appliedGates = {}
            for p in matchingPairs:
                frac = ( 0.1+0.9*random.random() ) / 2 # this will correspond to a e^(i theta \sigma_x) rotation with pi/20 \leq frac * pi/2 \leq pi/4
                appliedGates[p] = frac
            gates.append(appliedGates)
          
            # all gates so far are then run
            oneProb, sameProb, results = entangle( device, move, shots, sim, gates, conjugates, sample=sample, qasm_file=qasm_file)
          
        else:
            
            oneProb = oneProbs[score-1]
            sameProb = sameProbs[score-1]
            matchingPairs = list(gates[ 2*(score-1) ].keys())
            
            I = calculateMutual ( oneProb, sameProb, pairs )
            correlatedPairs = getDisjointPairs( pairs, [], I )
            
            rawOneProb = copy.deepcopy( oneProb )
            if cleanup:
                oneProb = CleanData(cleaner[score-1],rawOneProb,sameProb,pairs)
            
            results = []
        
        
        # Step 2: Get player to guess pairs
        
        displayedOneProb = copy.copy( oneProb )
        
        guessedPairs = []

        # if choices are all correct, we just give the player the right answer
        if (move=="C"):
            guessedPairs = matchingPairs
        # if choices are random, we generate a set of random pairs
        if (move=="R"):
            guessedPairs = getDisjointPairs( pairs, [], {} )
        # if choices are via MWPM, we do this
        if (move=="B"):
            guessedPairs = getDisjointPairs( pairs, oneProb, {} )
        # if choices are manual, let's get choosing
        if (move=="M"):
            
            # get the player choosing until the choosing is done
            unpaired = num
            restart = False
            while (unpaired>1):  
                
                clear_output()
                print("")
                print("Round "+str(score))
                if cleanup:
                    printM("\nRaw puzzle",move)    
                    printPuzzle( device, rawOneProb, move, ascii=ascii)
                    printM("\nCleaned puzzle", move)
                printPuzzle( device, displayedOneProb, move, ascii=ascii)                

                pairGuess = input("\nChoose a pair  (or type 'done' to skip to the next round, or 'restart' for a new game)\n")
                if num<=26 : # if there are few enough qubits, we don't need to be case sensitive
                    pairGuess = str.upper(pairGuess)

                if (pairGuess in pairs.keys()) and (pairGuess not in guessedPairs) :

                    guessedPairs.append(pairGuess)

                    # set them both to grey on screen (set the corresponding oneProb value to >1)
                    for j in [0,1]:
                        displayedOneProb[ pairs[pairGuess][j] ] = 2
                    printM("\n\n\n", move)
                    
                    # check if all active (and therefore displayed) vertices have been covered
                    unpaired = 0
                    for n in pos.keys():
                        unpaired += ( displayedOneProb[n] <= 1 )
                
                elif (str.upper(pairGuess)=="DONE") : # player has decided to stop pairing
                    unpaired = 0
                elif (str.upper(pairGuess)=="RESTART") : # player has decided to stop the game
                    unpaired = 0
                    restart = True
                else:
                    printM("That isn't a valid pair. Try again.\n(Note that input can be case sensitive)", move)
        
        
        # store the oneProb and sameProb
        oneProbs.append( oneProb )
        sameProbs.append( sameProb )
        # store the raw data (if it is not too big
        if len(str(results)) < 10000:
            resultsDicts.append( results )
        
        # see whether the game over condition is satisfied
        gameOn = (score<maxScore) and restart==False
        
        # given the chosen pairs, the gates are now deduced from oneProb
        guessedGates = {}

        for p in guessedPairs:
            
            if (move=="C" and sim==False):
                
                guessedFrac = gates[ 2*(score-1) ][p]
            
            else:

                guessedOneProb = 0
                for j in range(2):
                    guessedOneProb += oneProb[ pairs[p][j] ] / 2
                    
                guessedFrac = calculateFrac( guessedOneProb )

            # since the player wishes to apply the inverse gate, the opposite frac is stored
            guessedGates[p] = -guessedFrac

        # now we can add to the list of all gates
        gates.append(guessedGates)
        
        # finally randomly generate X or Z rotation for each active qubit to conjugate this round with
        newconjugates = []
        for n in range(num):
            newconjugates.append( [ numpy.random.choice(['X','Y']) , random.random() ] )
        conjugates.append(newconjugates)
             
        if move=='M':
            clear_output()
        
        if cleanup==True:
            printM("\nRaw puzzle",move)    
            if move=="M":
                printPuzzle( device, rawOneProb, move, ascii=ascii)
            printM("\nCleaned puzzle", move )
        if move=="M":
            printPuzzle( device, oneProb, move, ascii=ascii)
        printM("", move)
        printM("Round "+str(score)+" complete", move)
        printM("", move)
        printM("Pairs you guessed for this round", move)
        printM(sorted(guessedPairs), move)
        printM("Pairs our bot would have guessed", move)
        printM(sorted(getDisjointPairs( pairs, oneProb, {} )), move )
        printM("Correct pairs for this round", move)
        printM(sorted(matchingPairs), move)
        correctGuesses = list( set(guessedPairs).intersection( set(matchingPairs) ) )
        printM("\nYou guessed "+str(len(correctGuesses))+" out of "+str(len(matchingPairs))+" pairs correctly!", move)
        printM("", move)
        printM("", move)
        if move=="M" and restart==False:
            input(">Press Enter for the next round...\n")
    
    if move=="M" and restart==False:
        input("> There is no more data on this game :( Press Enter to restart...\n")
    
    if sdk == 'ManualQISKit':
        qasm_file.close()

    return gates, conjugates, oneProbs, sameProbs, resultsDicts


def MakeGraph(X,Y,y,axisLabel,labels=[],verbose=False,log=False,tall=False):
    
    # Input:
    # * *X* - array of x axis values
    # * *Y* - array of arrays of y axis values for multiple series
    # * *y* - array of arrays of error bar widths for the y axis values for multiple series
    # * *axisLabel* - list of two strings: labels for the x and z axis
    # * *labels* - list of strings, giving the names for each series
    # * *verbose* - when True, the arrays X, Y and y will be printed to screen
    # * *log* - When true, the plot will be a log plot (on the y axis)
    # * *tall* - if true, the plot will be a square to spread out the y axis values a bit more
    # 
    # Process:
    # * Set up the required call to matplotlib and make the graph
    # 
    # Output:
    # * Nothing is returned, but the required graph is output to screen
    
    from matplotlib import pyplot as plt
    plt.rcParams.update({'font.size': 15})
    
    markers = ["o","^","h","D","*"]
    
    # if verbose, print the numbers to screen
    if verbose==True:
        print("\nX values")
        print(X)
        for j in range(len(Y)):
            print("\nY values for "+labels[j])
            print(Y[j])
            print("\nError bars")
            print(y[j])
            print("")
    
    # convert the variances of varY into widths of error bars
    for j in range(len(y)):
        for k in range(len(y[j])):
            if y[j][k]>0: # avoiding domaning error for negative values (though they should only occur for numerical innacuracies anyway)
                y[j][k] = math.sqrt(y[j][k]/2)
            else:
                y[j][k] = 0
            
    if tall:
        plt.figure(figsize=(20,20))
    else:
        plt.figure(figsize=(20,10))
    
    
    # add in the series
    for j in range(len(Y)):
        marker = markers[j%len(markers)]
        if labels==[]:
            plt.errorbar(X, Y[j], marker = marker, markersize=20, yerr = y[j], linewidth=5)
        else:
            plt.errorbar(X, Y[j], label=labels[j], marker = marker, markersize=20, yerr = y[j], linewidth=5)
            plt.legend(loc="upper left", bbox_to_anchor=(1,1))

    
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


def GetData ( device, move, shots, sim, samples, maxScore, bias=0):
    
    # Input:
    # * *device* - String specifying the device on which the game is played.
    #              Details about the device will be obtained using getLayout.
    # * *move* - String describing the way moves are chosen.
    # * *shots* - Number of shots to be used for statistics.
    # * *sim* - Boolean for whether the simulator is to be used.
    # * *samples* - Number of full games to run
    # * *maxScore* - Number of rounds to run each game for
    # * *bias* - Bias angle of runGame
    #
    # Process:
    # * The game is the required number of times with the given specs. The information supplied by runGame() is then saved to file.
    # 
    # Output:
    # * Nothing is returned, but the collected data is saved to file.

    _, _, _, _, _, _, sdk, _ = getLayout(device)
    
    for sample in range(samples):

        print("move="+move+", shots="+str(shots)+", sample=" + str(sample) )

        gates, conjugates, oneProbs, sameProbs, resultsDicts = runGame( device, move, shots, sim, maxScore=maxScore, sample=sample, bias=bias)

        # make a directory for this device if it doesn't already exist
        if not os.path.exists(path+'/results/' + device):
            os.makedirs(path+'/results/' + device)

        filename = 'move=' + move + '_shots=' + str(shots) + '_sim=' + str(sim) + '.txt'

        if sdk!='ManualQISKit':
            saveFile = open(path+'/results/' + device + '/oneProbs_'+filename, 'a')
            saveFile.write( str(oneProbs)+'\n' )
            saveFile.close()
            
            saveFile = open(path+'/results/' + device + '/sameProbs_'+filename, 'a')
            saveFile.write( str(sameProbs)+'\n' )
            saveFile.close()

        saveFile = open(path+'/results/' + device + '/gates_'+filename, 'a')
        saveFile.write( str(gates)+'\n' )
        saveFile.close()

        saveFile = open(path+'/results/' + device + '/conjugates_'+filename, 'a')
        saveFile.write( str(conjugates)+'\n' )
        saveFile.close()
        
        if sim==False and sdk!='ManualQISKit':
            saveFile = open(path+'/results/' + device + '/results_'+filename, 'a')
            saveFile.write( str(resultsDicts)+'\n' )
            saveFile.close()
        
        
def CalculateQuality ( x, oneProbSamples, sameProbSamples, gateSamples, pairs, score ) :
        
    # Input:
    # * *x* - Array of values used to perform an independent linear transformation on each qubit
    # * *oneProbSamples* - oneProbSamples[j][score-1] is the oneProb array for round s of the jth sample
    # * *sameProbSamples* - as above, but for sameProbs
    # * *gateSamples* - as above, but for gates
    # * *pairs* - A dictionary with names of pairs as keys and lists of the two qubits of each pair as values
    # * *score* - The round being played (numbered from 1 instead of 0)
    #
    # Process:
    # * For a given round, the data from all samples are considered. This is used to determine:
    #     * The average fraction of pairs that are guessed correctly by MWPM (see getDisjointPairs() for how this is done)
    #     * The average difference between the frac value we get from calculateFrac(oneProb) and the actual value of frac used
    #       (actually it is the average oneProb for the two qubits in each correct pair that is used)
    # 
    # Output:
    # * *fractionCorrect* - Array of two values: the mean of the fraction of pairs that are correct, and the variance of this
    # * *fracDifference* - Array of two values: the mean of the difference between measured and correct frac values, and the variance of this
        
    # see what fraction of the matchings we have correct
    
    fractionCorrect = [0 for _ in range(2)]
    fracDifference = [0 for _ in range(2)]
    for oneProbs, sameProbs, gates in zip(oneProbSamples, sameProbSamples, gateSamples):
        
        oneProb = oneProbs[score-1]
        sameProb = sameProbs[score-1]
        
        if x!=[]:
            rawOneProb = copy.deepcopy(oneProb)
            oneProb = CleanData ( x, rawOneProb, sameProb, pairs )

        gate = gates[ 2*(score-1) ]
        
        matchingPairs = list(gate.keys())
        guessedPairs = getDisjointPairs( pairs, oneProb, {} )
        correctGuesses = list( set(guessedPairs).intersection( set(matchingPairs) ) )
        dC = len(correctGuesses) / len(matchingPairs)
        fractionCorrect[0] += dC # for mean
        fractionCorrect[1] += ( dC )**2 # for variance
 
        dD = 0
        for p in gate.keys():
            
            guessedOneProb = 0
            for j in range(2):
                guessedOneProb += oneProb[ pairs[p][j] ]/2
            
            dD += abs( calculateFrac(guessedOneProb)-gate[p] ) / len(gate)
        
        fracDifference[0] += dD # for mean
        fracDifference[1] += ( dD )**2 # for variance
            
    sample_num = len( oneProbSamples )
    
    fractionCorrect[0] = fractionCorrect[0] / sample_num
    fractionCorrect[1] = fractionCorrect[1] / sample_num
    fractionCorrect[1] -= fractionCorrect[0]**2
        
    fracDifference[0] = fracDifference[0] / sample_num
    fracDifference[1] = fracDifference[1] / sample_num
    fracDifference[1] -= fracDifference[0]**2
                
    return fractionCorrect, fracDifference


def CleanData ( x, rawOneProb, sameProb, pairs, minI=0):
    
    # Input:
    # * **x* - Array of values used to perform an independent linear transformation on each qubit
    # * *rawOneProb* - A list with an entry for each qubit. Each entry is the fraction of samples for which the measurement of that qubit returns *1*.
    # * *sameProb* - A dictionary with pair names as keys, and probability that the two qubits each pair give the same results as values.
    # * *pairs* - A dictionary with names of pairs as keys and lists of the two qubits of each pair as values
    # * *minI* - Minimum I to make it worth worrying about.
    #
    # Process:
    # * Each oneProb in the input is transformed according to the following linear transformation, given values from x
    # * oneProb[n] = x[3*n] * rawOneProb[n] + x[3*n+1] * rawOneProb[match] + x[3*n+2]
    # * Here n is the qubit to which we are applying the tranformation, and match is the qubit that is most correlated with n
    # 
    # Output:
    # * *oneProb* - The oneProb values after the transform has been applied
    
    I = calculateMutual ( rawOneProb, sameProb, pairs )
    
    matches = {}
    for n in range(len(rawOneProb)):
        maxI = 0
        for p in pairs:
            for j in range(2):
                if n==pairs[p][j]:
                    if I[p]>maxI and I[p]>minI:
                        maxI = I[p]
                        matches[n] = pairs[p][(j+1)%2]

    oneProb = []
        
    for n in range(len(rawOneProb)):
        
        if n in matches.keys():
            match = matches[n]
        else:
            match = n

        newOneProb = x[3*n] * rawOneProb[n] + x[3*n+1] * rawOneProb[match] + x[3*n+2]
        newOneProb = min(1,newOneProb)
        newOneProb = max(0,newOneProb)

        oneProb.append( newOneProb )

    return oneProb


def getCleaningProfile ( device, move, shots, sim, num, maxScore, gritty=False ):
    
    # Input:
    # * *num* - number of qubits
    # * *maxScore* - number of rounds that can be played
    # * *gritty* - Whether to create a cleaning profile optimized for human players
    # * other inputs are those required to address a given saved file
    #
    # Process:
    # * This function obtains an array of cleaning profiles x (see CleanData() for more details on these).
    # * This is done by loading them from a save file if one exists
    # * If not, a generic one is made. This made to not make things look artificially perfect when a human is playing.
    # 
    # Output:
    # * An arrays of cleaning profiles x, with one for each round
    
    try: # see if a specific cleaner file has been made
        cleaner = resultsLoad( 'cleaner', move, shots, sim, device )[0]
    except: # if not, go with the default
        if gritty:
            cleaner = [[0.5,0.5,0]*num]*maxScore
        else:
            cleaner = [[0.45,0.55,0]*num]*maxScore
            
    return cleaner
    

def ProcessData ( device, move, shots, sim, cleanup):
    
    # Input:
    # * *device* - String specifying the device on which the game is played.
    # * *move* - String describing the way moves were chosen for the results to be loaded.
    # * *shots* - Number of shots used in the results to be loaded.
    # * *sim* - Boolean denoting whether a simulator was used for the results to be loaded.- 
    # * *cleanup* - Boolean determining whether error mitigation post-processing is used
    #
    # Process:
    # * The inputs specify data for a given set of runs that are loaded from file, and then used to calculate quantities that tell us how well the game was implemented. These are then returned as outputs.
    # 
    # Output:
    # * *fuzzAvs* - Array of the average and variance of the fuzz (see calculateFuzz() ) for each round
    # * *correctFracs* - Array of fractionCorrect (see calculateQuality() ) for each round
    # * *differenceFracs* - Array of fracDifference (see calculateQuality() ) for each round
    
    num, area, entangleType, pairs, pos, example, sdk, runs = getLayout(device)
    
    filename = 'move=' + move + '_shots=' + str(shots) + '_sim=' + str(sim) + '.txt'
        
    oneProbSamples = resultsLoad ( 'oneProbs', move, shots, sim, device )
    sameProbSamples = resultsLoad ( 'sameProbs', move, shots, sim, device )
    gateSamples = resultsLoad ( 'gates', move, shots, sim, device )
    
    # find number of round in samples (assume same for all)
    maxScore = len(oneProbSamples[0])
    
    if cleanup:
        cleaner = getCleaningProfile ( device, move, shots, sim, num, maxScore )
    
    # find number of samples
    samples = len(oneProbSamples)
    
    fuzzAvs = [[0]*2 for _ in range(maxScore)]
    
    for oneProbSample, sameProbSample, gateSample in zip(oneProbSamples, sameProbSamples, gateSamples):
        for score in range(len(oneProbSample)):
            if cleanup:
                oneProb = CleanData ( cleaner[score], oneProbSample[score], sameProbSample[score], pairs )
            else:
                oneProb = oneProbSample[score]
            fuzz = calculateFuzz ( oneProb, pairs, gateSample[2*score].keys() )
            fuzzAvs[score][0] += fuzz/samples
            fuzzAvs[score][1] += fuzz**2/samples
    for fuzzAv in fuzzAvs:
        fuzzAv[1] -= fuzzAv[0]**2
                
    correctFracs = []
    differenceFracs = []
    for score in range(1,maxScore+1):
        if cleanup:
            x = cleaner[score-1]
        else:
            x = []
        fractionCorrect, fracDifference = CalculateQuality( x, oneProbSamples, sameProbSamples, gateSamples, pairs, score )
        correctFracs.append(fractionCorrect)
        differenceFracs.append(fracDifference)

    return fuzzAvs, correctFracs, differenceFracs

def PlotGraphSet ( devices, sims_to_use ):
    
    # Input:
    # * *devices* - Any array of devices
    # * *sims_to_used* - An array of sims
    #
    # Process:
    # * For a given set of devices and sims, all the processed data produced by ProcessData() is plotted
    # 
    # Output:
    # * None are returned, but graphs are printed to screen
    
    # what follows assumes that 'devices' is a list, so ensure this is true
    if type(devices) is not list:
        devices = [devices]
    
    # we'll set up the x axis according to the first listed device
    num, area, entangleType, pairs, pos, example, sdk, runs = getLayout(devices[0])

    maxMaxScore = 0
    for sim in sims_to_use:
        maxMaxScore = max( maxMaxScore, runs[sim]['maxScore'] )
    
    X = range(1,maxMaxScore+1)
    Yf = []
    yf = []
    Yc = []
    yc = []
    Yd = []
    yd = []
    labels = []
    
    cleanup_for_sim = {True:[False],False:[False,True]}

    for device in devices:
        
        num, area, entangleType, pairs, pos, example, sdk, runs = getLayout(device)

        for sim in sims_to_use:
            for cleanup in cleanup_for_sim[sim]:
                for move in runs[sim]['move']:
                    for shots in runs[sim]['shots']:

                        maxScore = runs[sim]['maxScore']
                        fuzzAvs, correctFracs, differenceFracs = ProcessData( device, move, shots, sim, cleanup )

                        Yf.append( [fuzzAvs[j][0] for j in range(maxScore) ] + [math.nan]*(maxMaxScore-maxScore) )
                        yf.append( [fuzzAvs[j][1] for j in range(maxScore) ] + [math.nan]*(maxMaxScore-maxScore) )
                        Yc.append( [correctFracs[j][0] for j in range(maxScore) ] + [math.nan]*(maxMaxScore-maxScore) )
                        yc.append( [correctFracs[j][1] for j in range(maxScore) ] + [math.nan]*(maxMaxScore-maxScore) )
                        Yd.append( [differenceFracs[j][0] for j in range(maxScore) ] + [math.nan]*(maxMaxScore-maxScore) )
                        yd.append( [differenceFracs[j][1] for j in range(maxScore) ] + [math.nan]*(maxMaxScore-maxScore) )


                        labels.append( device*(sim==False) + ('simulated '+str(device))*sim + ', ' + 'correct'*(move=='C') + 'random'*(move=='R') + ' pairing,\nshots = ' + str(shots) + ' (mitigated)'*cleanup  )
            
    MakeGraph(X,Yf,yf,["Game round","Average Fuzz"],labels=labels)
    MakeGraph(X,Yc,yc,["Game round","Average correctness for MWPM"],labels=labels)
    MakeGraph(X,Yd,yd,["Game round","Average difference from correct values"],labels=labels)
    print(X)
    print(Yf)

def PlayGame ( ):
    
    # Input:
    # * None given, since the required information is taken directly from the player
    #
    # Process:
    # * User is asked to specify a device, and whether they want data from real or simulated runs.
    # * Using this info, a call to runGame() is set up to play the game with existing data.
    # * User is also given the option to view background information.
    # 
    # Output:
    # * None returned, but the game is played onscreen.
    
    clear_output()
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
        input("> There are lots of quantum processors around these days. But how good are they really?...\n")
        input("> How do they compare to each other, and how do they compare to normal computers?...\n")
        input("> To find out, we can run a simple program on them and see what happens...\n")
        input("> So that's what we've done. We made a game, and we are running it on all the quantum computers we can...\n")
              
        input("> Have a play, and see what you think...\n")
        input("> You won't learn anything about the mysteries of the quantum world by playing...\n")
        input("> But you will find out how good current quantum computers are at being computers...\n")
        input("> The larger and fancier a quantum processor is, the better the puzzles in the game will be...\n")
        input("> The noisier that a quantum processor is, the more infuriatingly steep the difficulty curve will be...\n")
        input("> So the quality of the processor is direcly proportional to how much fun you have playing on it...\n")
        input("> Now choose a device to test out...\n")
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
    
    num_active_qubits = len(pos.keys())
    
    tut = str.upper(input("\n> Do you want to read the tutorial? (y/n)...\n"))
    if tut!="N":
        printPuzzle(device,example,"M")
        input("> The game is a series of puzzles, which look something like this...\n")
        input("> All the coloured circles" + ((num_active_qubits%2)==1)*" (except one)" + " are paired up...\n")
        input("> Your job is to identify these pairs...\n")
        input("> You do this by looking at the numbers: Circles should have very similar numbers if they are paired...\n")
        input("> As you proceed through the game, the two numbers in each pair will get less similar. This will make the puzzles harder...\n")
        input("> The game is designed to have a nice gentle increase in difficulty...\n")
        input("> But noise in the quantum processors increases the difficulty much faster...\n")
        input("> If you want to see how potent noise is, compare a run on the real device with one on a (noiseless) simulator...\n")
        input("> You can play some games on the simulator to see how things should be...\n")
        input("> Or you can play using data from the real device...\n")  
        
            
    s = str.upper(input("> Do you want to play a game using data from the real device? (y/n)...\n"))
    sim = (s!='Y')
    if sim:
        input("> The following game data will be from a simulated run...\n")
    
    shots = min( runs[sim]['shots'] )

    try:
        runGame ( device, 'M', shots, sim, cleanup=True, dataNeeded=False )
    except Exception as e:
        print(e)
        input("> Something went wrong. This probably means there is no saved data to play the game you requested.\n> Try choosing a different device...\n")
