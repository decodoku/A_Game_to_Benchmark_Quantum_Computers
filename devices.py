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

	return ["ibmqx4","ibmqx5","19Q-Acorn","8Q-Agave","ibm_kyiv","ibm_torino"]


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
        area = [6.5,2.15]
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
        sdk = "ManualQISKit"
        runs = {True:{'shots':[8192],'move':['C'],'maxScore':10,'samples':500}}

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

    elif device=="ibm_kyiv":
        # 127 qubit device by IBM Quantum
    
        num = 127
        area = [15,13]
        entangleType = "CX"
        pairs = {'AA': [1, 0], 'AB': [1, 2], 'AC': [3, 2], 'AD': [4, 3], 'AE': [4, 15], 'AF': [5, 4], 'AG': [6, 5], 'AH': [7, 6], 'AI': [7, 8], 'AJ': [8, 9], 'AK': [10, 9], 'AL': [10, 11], 'AM': [11, 12], 'AN': [12, 13], 'AO': [14, 0], 'AP': [14, 18], 'AQ': [16, 8], 'AR': [17, 12], 'AS': [17, 30], 'AT': [18, 19], 'AU': [19, 20], 'AV': [20, 33], 'AW': [21, 20], 'AX': [21, 22], 'AY': [22, 15], 'AZ': [23, 22], 'BA': [23, 24], 'BB': [25, 24], 'BC': [26, 16], 'BD': [26, 25], 'BE': [26, 27], 'BF': [28, 27], 'BG': [29, 28], 'BH': [29, 30], 'BI': [31, 30], 'BJ': [31, 32], 'BK': [32, 36], 'BL': [33, 39], 'BM': [34, 24], 'BN': [35, 28], 'BO': [35, 47], 'BP': [36, 51], 'BQ': [37, 38], 'BR': [38, 39], 'BS': [40, 39], 'BT': [41, 40], 'BU': [41, 53], 'BV': [42, 41], 'BW': [43, 34], 'BX': [43, 42], 'BY': [43, 44], 'BZ': [45, 44], 'CA': [45, 46], 'CB': [47, 46], 'CC': [47, 48], 'CD': [49, 48], 'CE': [49, 50], 'CF': [50, 51], 'CG': [52, 37], 'CH': [53, 60], 'CI': [54, 45], 'CJ': [55, 49], 'CK': [56, 52], 'CL': [56, 57], 'CM': [57, 58], 'CN': [59, 58], 'CO': [59, 60], 'CP': [61, 60], 'CQ': [61, 62], 'CR': [63, 62], 'CS': [63, 64], 'CT': [64, 54], 'CU': [64, 65], 'CV': [66, 65], 'CW': [67, 66], 'CX': [68, 55], 'CY': [68, 67], 'CZ': [69, 68], 'DA': [69, 70], 'DB': [71, 58], 'DC': [71, 77], 'DD': [72, 62], 'DE': [73, 66], 'DF': [73, 85], 'DG': [74, 70], 'DH': [75, 76], 'DI': [77, 76], 'DJ': [78, 77], 'DK': [78, 79], 'DL': [79, 91], 'DM': [80, 79], 'DN': [80, 81], 'DO': [81, 72], 'DP': [81, 82], 'DQ': [82, 83], 'DR': [84, 83], 'DS': [85, 84], 'DT': [86, 85], 'DU': [86, 87], 'DV': [87, 88], 'DW': [89, 74], 'DX': [89, 88], 'DY': [90, 75], 'DZ': [90, 94], 'EA': [92, 83], 'EB': [92, 102], 'EC': [93, 87], 'ED': [93, 106], 'EE': [95, 94], 'EF': [95, 96], 'EG': [97, 96], 'EH': [97, 98], 'EI': [98, 91], 'EJ': [99, 98], 'EK': [99, 100], 'EL': [101, 100], 'EM': [101, 102], 'EN': [102, 103], 'EO': [104, 103], 'EP': [105, 104], 'EQ': [106, 105], 'ER': [107, 106], 'ES': [107, 108], 'ET': [109, 96], 'EU': [110, 100], 'EV': [110, 118], 'EW': [111, 104], 'EX': [112, 108], 'EY': [112, 126], 'EZ': [113, 114], 'FA': [114, 109], 'FB': [114, 115], 'FC': [116, 115], 'FD': [117, 116], 'FE': [117, 118], 'FF': [119, 118], 'FG': [119, 120], 'FH': [120, 121], 'FI': [121, 122], 'FJ': [122, 111], 'FK': [123, 122], 'FL': [124, 123], 'FM': [125, 124], 'FN': [126, 125]}
        pos = {0: [0, 0], 1: [0, 1], 2: [0, 2], 3: [0, 3], 4: [0, 4], 5: [0, 5], 6: [0, 6], 7: [0, 7], 8: [0, 8], 9: [0, 9], 10: [0, 10], 11: [0, 11], 12: [0, 12], 13: [0, 13], 14: [1, 0], 15: [1, 4], 16: [1, 8], 17: [1, 12], 18: [2, 0], 19: [2, 1], 20: [2, 2], 21: [2, 3], 22: [2, 4], 23: [2, 5], 24: [2, 6], 25: [2, 7], 26: [2, 8], 27: [2, 9], 28: [2, 10], 29: [2, 11], 30: [2, 12], 31: [2, 13], 32: [2, 14], 33: [3, 2], 34: [3, 6], 35: [3, 10], 36: [3, 14], 37: [4, 0], 38: [4, 1], 39: [4, 2], 40: [4, 3], 41: [4, 4], 42: [4, 5], 43: [4, 6], 44: [4, 7], 45: [4, 8], 46: [4, 9], 47: [4, 10], 48: [4, 11], 49: [4, 12], 50: [4, 13], 51: [4, 14], 52: [5, 0], 53: [5, 4], 54: [5, 8], 55: [5, 12], 56: [6, 0], 57: [6, 1], 58: [6, 2], 59: [6, 3], 60: [6, 4], 61: [6, 5], 62: [6, 6], 63: [6, 7], 64: [6, 8], 65: [6, 9], 66: [6, 10], 67: [6, 11], 68: [6, 12], 69: [6, 13], 70: [6, 14], 71: [7, 2], 72: [7, 6], 73: [7, 10], 74: [7, 14], 75: [8, 0], 76: [8, 1], 77: [8, 2], 78: [8, 3], 79: [8, 4], 80: [8, 5], 81: [8, 6], 82: [8, 7], 83: [8, 8], 84: [8, 9], 85: [8, 10], 86: [8, 11], 87: [8, 12], 88: [8, 13], 89: [8, 14], 90: [9, 0], 91: [9, 4], 92: [9, 8], 93: [9, 12], 94: [10, 0], 95: [10, 1], 96: [10, 2], 97: [10, 3], 98: [10, 4], 99: [10, 5], 100: [10, 6], 101: [10, 7], 102: [10, 8], 103: [10, 9], 104: [10, 10], 105: [10, 11], 106: [10, 12], 107: [10, 13], 108: [10, 14], 109: [11, 2], 110: [11, 6], 111: [11, 10], 112: [11, 14], 113: [12, 1], 114: [12, 2], 115: [12, 3], 116: [12, 4], 117: [12, 5], 118: [12, 6], 119: [12, 7], 120: [12, 8], 121: [12, 9], 122: [12, 10], 123: [12, 11], 124: [12, 12], 125: [12, 13], 126: [12, 14]}
        example = [0.25]*num
        sdk = "ManualQISKit"
        runs = {False:{'shots':[8192],'move':['C'],'maxScore':50,'samples':20}}

    elif device=="ibm_torino":
        # 133 qubit device by IBM Quantum

        num = 133
        area = [15,14]
        entangleType = "CZ"
        pairs = {'AA': [0, 1], 'AB': [0, 15], 'AC': [1, 2], 'AD': [2, 3], 'AE': [3, 4], 'AF': [4, 5], 'AG': [4, 16], 'AH': [5, 6], 'AI': [6, 7], 'AJ': [7, 8], 'AK': [8, 9], 'AL': [8, 17], 'AM': [9, 10], 'AN': [10, 11], 'AO': [11, 12], 'AP': [12, 13], 'AQ': [12, 18], 'AR': [13, 14], 'AS': [15, 19], 'AT': [16, 23], 'AU': [17, 27], 'AV': [18, 31], 'AW': [19, 20], 'AX': [20, 21], 'AY': [21, 22], 'AZ': [21, 34], 'BA': [22, 23], 'BB': [23, 24], 'BC': [24, 25], 'BD': [25, 26], 'BE': [25, 35], 'BF': [26, 27], 'BG': [27, 28], 'BH': [28, 29], 'BI': [29, 30], 'BJ': [29, 36], 'BK': [30, 31], 'BL': [31, 32], 'BM': [32, 33], 'BN': [33, 37], 'BO': [34, 40], 'BP': [35, 44], 'BQ': [36, 48], 'BR': [37, 52], 'BS': [38, 39], 'BT': [38, 53], 'BU': [39, 40], 'BV': [40, 41], 'BW': [41, 42], 'BX': [42, 43], 'BY': [42, 54], 'BZ': [43, 44], 'CA': [44, 45], 'CB': [45, 46], 'CC': [46, 47], 'CD': [46, 55], 'CE': [47, 48], 'CF': [48, 49], 'CG': [49, 50], 'CH': [50, 51], 'CI': [50, 56], 'CJ': [51, 52], 'CK': [53, 57], 'CL': [54, 61], 'CM': [55, 65], 'CN': [56, 69], 'CO': [57, 58], 'CP': [58, 59], 'CQ': [59, 60], 'CR': [59, 72], 'CS': [60, 61], 'CT': [61, 62], 'CU': [62, 63], 'CV': [63, 64], 'CW': [63, 73], 'CX': [64, 65], 'CY': [65, 66], 'CZ': [66, 67], 'DA': [67, 68], 'DB': [67, 74], 'DC': [68, 69], 'DD': [69, 70], 'DE': [70, 71], 'DF': [71, 75], 'DG': [72, 78], 'DH': [73, 82], 'DI': [74, 86], 'DJ': [75, 90], 'DK': [76, 77], 'DL': [76, 91], 'DM': [77, 78], 'DN': [78, 79], 'DO': [79, 80], 'DP': [80, 81], 'DQ': [80, 92], 'DR': [81, 82], 'DS': [82, 83], 'DT': [83, 84], 'DU': [84, 85], 'DV': [84, 93], 'DW': [85, 86], 'DX': [86, 87], 'DY': [87, 88], 'DZ': [88, 89], 'EA': [88, 94], 'EB': [89, 90], 'EC': [91, 95], 'ED': [92, 99], 'EE': [93, 103], 'EF': [94, 107], 'EG': [95, 96], 'EH': [96, 97], 'EI': [97, 98], 'EJ': [97, 110], 'EK': [98, 99], 'EL': [99, 100], 'EM': [100, 101], 'EN': [101, 102], 'EO': [101, 111], 'EP': [102, 103], 'EQ': [103, 104], 'ER': [104, 105], 'ES': [105, 106], 'ET': [105, 112], 'EU': [106, 107], 'EV': [107, 108], 'EW': [108, 109], 'EX': [109, 113], 'EY': [110, 116], 'EZ': [111, 120], 'FA': [112, 124], 'FB': [113, 128], 'FC': [114, 115], 'FD': [114, 129], 'FE': [115, 116], 'FF': [116, 117], 'FG': [117, 118], 'FH': [118, 119], 'FI': [118, 130], 'FJ': [119, 120], 'FK': [120, 121], 'FL': [121, 122], 'FM': [122, 123], 'FN': [122, 131], 'FO': [123, 124], 'FP': [124, 125], 'FQ': [125, 126], 'FR': [126, 127], 'FS': [126, 132], 'FT': [127, 128]}
        pos = {0: [0, 0], 1: [0, 1], 2: [0, 2], 3: [0, 3], 4: [0, 4], 5: [0, 5], 6: [0, 6], 7: [0, 7], 8: [0, 8], 9: [0, 9], 10: [0, 10], 11: [0, 11], 12: [0, 12], 13: [0, 13], 14: [0, 14], 15: [1, 0], 16: [1, 4], 17: [1, 8], 18: [1, 12], 19: [2, 0], 20: [2, 1], 21: [2, 2], 22: [2, 3], 23: [2, 4], 24: [2, 5], 25: [2, 6], 26: [2, 7], 27: [2, 8], 28: [2, 9], 29: [2, 10], 30: [2, 11], 31: [2, 12], 32: [2, 13], 33: [2, 14], 34: [3, 2], 35: [3, 6], 36: [3, 10], 37: [3, 14], 38: [4, 0], 39: [4, 1], 40: [4, 2], 41: [4, 3], 42: [4, 4], 43: [4, 5], 44: [4, 6], 45: [4, 7], 46: [4, 8], 47: [4, 9], 48: [4, 10], 49: [4, 11], 50: [4, 12], 51: [4, 13], 52: [4, 14], 53: [5, 0], 54: [5, 4], 55: [5, 8], 56: [5, 12], 57: [6, 0], 58: [6, 1], 59: [6, 2], 60: [6, 3], 61: [6, 4], 62: [6, 5], 63: [6, 6], 64: [6, 7], 65: [6, 8], 66: [6, 9], 67: [6, 10], 68: [6, 11], 69: [6, 12], 70: [6, 13], 71: [6, 14], 72: [7, 2], 73: [7, 6], 74: [7, 10], 75: [7, 14], 76: [8, 0], 77: [8, 1], 78: [8, 2], 79: [8, 3], 80: [8, 4], 81: [8, 5], 82: [8, 6], 83: [8, 7], 84: [8, 8], 85: [8, 9], 86: [8, 10], 87: [8, 11], 88: [8, 12], 89: [8, 13], 90: [8, 14], 91: [9, 0], 92: [9, 4], 93: [9, 8], 94: [9, 12], 95: [10, 0], 96: [10, 1], 97: [10, 2], 98: [10, 3], 99: [10, 4], 100: [10, 5], 101: [10, 6], 102: [10, 7], 103: [10, 8], 104: [10, 9], 105: [10, 10], 106: [10, 11], 107: [10, 12], 108: [10, 13], 109: [10, 14], 110: [11, 2], 111: [11, 6], 112: [11, 10], 113: [11, 14], 114: [12, 0], 115: [12, 1], 116: [12, 2], 117: [12, 3], 118: [12, 4], 119: [12, 5], 120: [12, 6], 121: [12, 7], 122: [12, 8], 123: [12, 9], 124: [12, 10], 125: [12, 11], 126: [12, 12], 127: [12, 13], 128: [12, 14], 129: [13, 0], 130: [13, 4], 131: [13, 8], 132: [13, 12]}
        example = [0.25]*num
        sdk = "ManualQISKit"
        runs = {False:{'shots':[8192],'move':['C'],'maxScore':50,'samples':20}}

    elif device=="ibm_fez":
        # 156 qubit device by IBM Quantum

        num = 156
        area = [16,16]
        entangleType = "CZ"
        pairs = {'AA': [0, 1], 'AB': [1, 2], 'AC': [2, 3], 'AD': [3, 4], 'AE': [3, 16], 'AF': [4, 5], 'AG': [5, 6], 'AH': [6, 7], 'AI': [7, 8], 'AJ': [7, 17], 'AK': [8, 9], 'AL': [9, 10], 'AM': [10, 11], 'AN': [11, 12], 'AO': [11, 18], 'AP': [12, 13], 'AQ': [13, 14], 'AR': [14, 15], 'AS': [15, 19], 'AT': [16, 23], 'AU': [17, 27], 'AV': [18, 31], 'AW': [19, 35], 'AX': [20, 21], 'AY': [21, 22], 'AZ': [21, 36], 'BA': [22, 23], 'BB': [23, 24], 'BC': [24, 25], 'BD': [25, 26], 'BE': [25, 37], 'BF': [26, 27], 'BG': [27, 28], 'BH': [28, 29], 'BI': [29, 30], 'BJ': [29, 38], 'BK': [30, 31], 'BL': [31, 32], 'BM': [32, 33], 'BN': [33, 34], 'BO': [33, 39], 'BP': [34, 35], 'BQ': [36, 41], 'BR': [37, 45], 'BS': [38, 49], 'BT': [39, 53], 'BU': [40, 41], 'BV': [41, 42], 'BW': [42, 43], 'BX': [43, 44], 'BY': [43, 56], 'BZ': [44, 45], 'CA': [45, 46], 'CB': [46, 47], 'CC': [47, 48], 'CD': [47, 57], 'CE': [48, 49], 'CF': [49, 50], 'CG': [50, 51], 'CH': [51, 52], 'CI': [51, 58], 'CJ': [52, 53], 'CK': [53, 54], 'CL': [54, 55], 'CM': [55, 59], 'CN': [56, 63], 'CO': [57, 67], 'CP': [58, 71], 'CQ': [59, 75], 'CR': [60, 61], 'CS': [61, 62], 'CT': [61, 76], 'CU': [62, 63], 'CV': [63, 64], 'CW': [64, 65], 'CX': [65, 66], 'CY': [65, 77], 'CZ': [66, 67], 'DA': [67, 68], 'DB': [68, 69], 'DC': [69, 70], 'DD': [69, 78], 'DE': [70, 71], 'DF': [71, 72], 'DG': [72, 73], 'DH': [73, 74], 'DI': [73, 79], 'DJ': [74, 75], 'DK': [76, 81], 'DL': [77, 85], 'DM': [78, 89], 'DN': [79, 93], 'DO': [80, 81], 'DP': [81, 82], 'DQ': [82, 83], 'DR': [83, 84], 'DS': [83, 96], 'DT': [84, 85], 'DU': [85, 86], 'DV': [86, 87], 'DW': [87, 88], 'DX': [87, 97], 'DY': [88, 89], 'DZ': [89, 90], 'EA': [90, 91], 'EB': [91, 92], 'EC': [91, 98], 'ED': [92, 93], 'EE': [93, 94], 'EF': [94, 95], 'EG': [95, 99], 'EH': [96, 103], 'EI': [97, 107], 'EJ': [98, 111], 'EK': [99, 115], 'EL': [100, 101], 'EM': [101, 102], 'EN': [101, 116], 'EO': [102, 103], 'EP': [103, 104], 'EQ': [104, 105], 'ER': [105, 106], 'ES': [105, 117], 'ET': [106, 107], 'EU': [107, 108], 'EV': [108, 109], 'EW': [109, 110], 'EX': [109, 118], 'EY': [110, 111], 'EZ': [111, 112], 'FA': [112, 113], 'FB': [113, 114], 'FC': [113, 119], 'FD': [114, 115], 'FE': [116, 121], 'FF': [117, 125], 'FG': [118, 129], 'FH': [119, 133], 'FI': [120, 121], 'FJ': [121, 122], 'FK': [122, 123], 'FL': [123, 124], 'FM': [123, 136], 'FN': [124, 125], 'FO': [125, 126], 'FP': [126, 127], 'FQ': [127, 128], 'FR': [127, 137], 'FS': [128, 129], 'FT': [129, 130], 'FU': [130, 131], 'FV': [131, 132], 'FW': [131, 138], 'FX': [132, 133], 'FY': [133, 134], 'FZ': [134, 135], 'GA': [135, 139], 'GB': [136, 143], 'GC': [137, 147], 'GD': [138, 151], 'GE': [139, 155], 'GF': [140, 141], 'GG': [141, 142], 'GH': [142, 143], 'GI': [143, 144], 'GJ': [144, 145], 'GK': [145, 146], 'GL': [146, 147], 'GM': [147, 148], 'GN': [148, 149], 'GO': [149, 150], 'GP': [150, 151], 'GQ': [151, 152], 'GR': [152, 153], 'GS': [153, 154], 'GT': [154, 155]}
        pos = {0: [0, 0], 1: [1, 0], 2: [2, 0], 3: [3, 0], 4: [4, 0], 5: [5, 0], 6: [6, 0], 7: [7, 0], 8: [8, 0], 9: [9, 0], 10: [10, 0], 11: [11, 0], 12: [12, 0], 13: [13, 0], 14: [14, 0], 15: [15, 0], 16: [3, 1], 17: [7, 1], 18: [11, 1], 19: [15, 1], 20: [0, 2], 21: [1, 2], 22: [2, 2], 23: [3, 2], 24: [4, 2], 25: [5, 2], 26: [6, 2], 27: [7, 2], 28: [8, 2], 29: [9, 2], 30: [10, 2], 31: [11, 2], 32: [12, 2], 33: [13, 2], 34: [14, 2], 35: [15, 2], 36: [1, 3], 37: [5, 3], 38: [9, 3], 39: [13, 3], 40: [0, 4], 41: [1, 4], 42: [2, 4], 43: [3, 4], 44: [4, 4], 45: [5, 4], 46: [6, 4], 47: [7, 4], 48: [8, 4], 49: [9, 4], 50: [10, 4], 51: [11, 4], 52: [12, 4], 53: [13, 4], 54: [14, 4], 55: [15, 4], 56: [3, 5], 57: [7, 5], 58: [11, 5], 59: [15, 5], 60: [0, 6], 61: [1, 6], 62: [2, 6], 63: [3, 6], 64: [4, 6], 65: [5, 6], 66: [6, 6], 67: [7, 6], 68: [8, 6], 69: [9, 6], 70: [10, 6], 71: [11, 6], 72: [12, 6], 73: [13, 6], 74: [14, 6], 75: [15, 6], 76: [1, 7], 77: [5, 7], 78: [9, 7], 79: [13, 7], 80: [0, 8], 81: [1, 8], 82: [2, 8], 83: [3, 8], 84: [4, 8], 85: [5, 8], 86: [6, 8], 87: [7, 8], 88: [8, 8], 89: [9, 8], 90: [10, 8], 91: [11, 8], 92: [12, 8], 93: [13, 8], 94: [14, 8], 95: [15, 8], 96: [3, 9], 97: [7, 9], 98: [11, 9], 99: [15, 9], 100: [0, 10], 101: [1, 10], 102: [2, 10], 103: [3, 10], 104: [4, 10], 105: [5, 10], 106: [6, 10], 107: [7, 10], 108: [8, 10], 109: [9, 10], 110: [10, 10], 111: [11, 10], 112: [12, 10], 113: [13, 10], 114: [14, 10], 115: [15, 10], 116: [1, 11], 117: [5, 11], 118: [9, 11], 119: [13, 11], 120: [0, 12], 121: [1, 12], 122: [2, 12], 123: [3, 12], 124: [4, 12], 125: [5, 12], 126: [6, 12], 127: [7, 12], 128: [8, 12], 129: [9, 12], 130: [10, 12], 131: [11, 12], 132: [12, 12], 133: [13, 12], 134: [14, 12], 135: [15, 12], 136: [3, 13], 137: [7, 13], 138: [11, 13], 139: [15, 13], 140: [0, 14], 141: [1, 14], 142: [2, 14], 143: [3, 14], 144: [4, 14], 145: [5, 14], 146: [6, 14], 147: [7, 14], 148: [8, 14], 149: [9, 14], 150: [10, 14], 151: [11, 14], 152: [12, 14], 153: [13, 14], 154: [14, 14], 155: [15, 14]}
        example = [0.25]*num
        sdk = "ManualQISKit"
        runs = {False:{'shots':[8192],'move':['C'],'maxScore':50,'samples':20}}

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
