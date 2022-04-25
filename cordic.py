#####################################################
# Term Project: Cordic Processor    			    #
# Authors: Rory Brennan 18237606                    #
#                                                   #
# python cordic.py                                  #
# Date: 25/02/2022                                  #
#####################################################

# Imports
import math # For cosine, radian etc. functions
import numpy as np # For angles numpy array

# Function to convert floating point to binary 2.16 format
def float_bin(number, places = 16):
    # split() separates whole number and decimal 
    # part and stores it in two separate variables
    list_num = str(number).split(".")
    whole = list_num[0]
    dec = list_num[1]
    
    # Convert both whole number and decimal  
    # part from string type to integer type
    # Convert the whole number part to it's
    # respective binary form and remove the
    # "0b" from it.
    neg = whole[0]
    if neg == "-":
        whole = int(whole[1])
        dec = int(dec)
        if whole < 1:
            res = "10."
        elif whole >= 1:
            res = "11."
    else:
        whole = int(whole)
        dec = int(dec)
        if whole < 1:
            res = "00."
        elif whole >= 1:
            res = "01."
  
    # Iterate the number of times, we want
    # the number of decimal places to be
    for x in range(places):
  
        # Multiply the decimal value by 2 
        # and separate the whole number part
        # and decimal part
        list_num = str((decimal_converter(dec)) * 2).split(".")
        if len(list_num) == 1:
            while len(res) < 17:
                res += str('0')
            return res
        else:
            whole = list_num[0]
            dec = list_num[1]
        
        # Convert the decimal part
        # to integer again
        dec = int(dec)
  
        # Keep adding the integer parts 
        # receive to the result variable
        res += whole
  
    return res
    
# Function converts the value passed as
# parameter to it's decimal representation
def decimal_converter(num): 
    while num > 1:
        num /= 10
    return num

###################################################################################
# The following three functions are a CORDIC processor for a floating point value #
###################################################################################

# Creates tan dictionary containing constants for each iteration (delta a)
def create_tan_table_fp(cycles):
    tan = {}
    for i in range(cycles):
        tan[i] = math.degrees(math.atan(2**(-i)))
    return tan
    
# Calculate K constant
def find_K_fp(n):
    K = ( 1 / math.sqrt(2) )
    for i in range(1, n - 1):
        K = K * (1 / math.sqrt(1 + 2**(-2*i)))
    return K
    
# Cordic Processor
def cordic_fp(input_angle, cycles):

    # Create tan constant reference table for each iteration
    tan_table = create_tan_table_fp(cycles)

    # Initialize parameters and skip first cycle
    if input_angle >= 0:
        A, C, S = tan_table[0], find_K_fp(cycles), find_K_fp(cycles)
    else:
        A, C = -1*tan_table[0], find_K_fp(cycles)
        S = -1*find_K_fp(cycles)
        
    action = "" # Over/Under
    
    # Begin iterating cycles
    for i in range(1, cycles):
        C_old, S_old = C, S
        if A <= input_angle: # undershoot
            action = "under"
            A += tan_table[i]
            C = C_old - (S_old * (2**-i))
            S = S_old + (C_old * (2**-i))
        else: # overshoot
            action = "over"
            A -= tan_table[i]
            C = C_old + (S_old * (2**-i))
            S = S_old - (C_old * (2**-i))
       
    #print('What the angle should be (fp value): {:.5f}'.format(A))
    #print('FP ==> Cos: {} Sin: {}'.format(float_bin(str(C)), float_bin(str(S))))
    return float_bin(str(C)), float_bin(str(S))

#####################################################################################
# The following three functions are a CORDIC processor for a 2.16 fixed point value #
#####################################################################################

# Creates tan dictionary containing constants for each iteration (delta a)               
def create_tan_table(cycles):
    tan = {}
    for i in range(cycles):
        tan[i] = round(math.atan(2**(-i))*2**16)
    return tan
    
# Calculate K constant
def find_K(n):
    K = ( 1 / math.sqrt(2) )
    for i in range(1, n - 1):
        K = K * (1 / math.sqrt(1 + 2**(-2*i)))
    return round(K*2**16)
    
# Cordic Processor
def cordic(input_angle, cycles):

    # Create tan constant reference table for each iteration
    tan_table = create_tan_table(cycles)

    # Initialize parameters and skip first cycle
    if input_angle >= 0:
        A, C, S = tan_table[0], find_K(cycles), find_K(cycles)
    else:
        A, C = -1*tan_table[0], find_K(cycles)
        S = -1*find_K(cycles)
        
    action = "" # Over/Under
    
    # Begin iterating cycles
    #print("i   a     A   C_old C_new S_old S_new Action")
    for i in range(1, cycles):
        C_old, S_old = C, S
        if A <= input_angle: # undershoot
            action = "under"
            A += tan_table[i]
            C = round(C_old - (S_old * (2**-i)))
            S = round(S_old + (C_old * (2**-i)))
        else: # overshoot
            action = "over"
            A -= tan_table[i]
            C = round(C_old + (S_old * (2**-i)))
            S = round(S_old - (C_old * (2**-i)))
        #print('{} {} {} {} {} {} {} {}'.format(i, tan_table[i], A, C_old, C, S_old, S, action))
       
    #print('Final Angle: {} = {} = {}'.format(A, A/(2**16), round(math.degrees(A/(2**16)), 5)))  
    #print('AV ==> Cos: {} Sin: {}'.format(float_bin(str(C/(2**16))), float_bin(str(S/(2**16)))))
    return float_bin(str(C/(2**16))), float_bin(str(S/(2**16)))
    
# Main program entry point
if __name__ == '__main__':
    cycles = 10 # Number of cycles
    total_bits = 10 # Testing accuracy of these bits
    print("Testing " + str(total_bits) + " bits for " + str(cycles) + " cycles!")
    print("Integral Bits: 2 Fractional Bits: " + str(total_bits-2))
    matches = 0
    tests = 0
    angles = np.arange(-89, 89, 0.02) # Generate angles array (-89 to 89)
    for angle in angles:
        tests += 1
        # Compute real and approx cosine and sine values and compare
        C_False, S_False = cordic(round(math.radians(angle)*2**16), cycles)
        C_True, S_True = cordic_fp(angle, cycles)
        if C_True[2:total_bits] == C_False[2:total_bits] and S_True[2:total_bits] == S_False[2:total_bits]:
            matches += 1
    
    # Output results
    print("Tests: " + str(tests))
    print("Matches: " + str(matches))
    print("Accuracy: " + str(matches/tests))
        
    