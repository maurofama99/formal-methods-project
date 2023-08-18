import subprocess
import os
import shutil
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from itertools import product

# Define the range for the varying parameters
NUM_PIECES_range = range(2, 10, 2)
PROCESSING_TIME_S2_range = range(10, 100, 20)
SPEED_range = range(5, 25, 5)

not_satisfied = []

# Define the fixed parameters
NUM_SLOTS = 32
GATE_POS = -1
FIRST_POS_BELT2 = -1
LAST_POS_BELT2 = -1
RULE_CONTROLLER = 10
PROCESSING_TIME_S1 = 10
PROCESSING_TIME_S3 = 10

NUM_STATIONS = 3
NUM_IN_SENSORS = 3
NUM_OUT_SENSORS = 3

# Initialize lists to store results for plotting
NUM_PIECES_results = []
PROCESSING_TIME_S2_results = []
SPEED_results = []
deadlock_results = []

# Loop through all combinations of varying parameters
for NUM_PIECES, PROCESSING_TIME_S2, SPEED in product(NUM_PIECES_range, PROCESSING_TIME_S2_range, SPEED_range):
    # Define the parameters string for the UPPAAL model

    # Create a temporary model file with the new parameters
    original_model_path = "/Users/valeria/Desktop/formal-methods-project/sim/conf.xml"
    temp_model_path = f"temp_model_{NUM_PIECES}_{PROCESSING_TIME_S2}_{SPEED}.xml"
    shutil.copyfile(original_model_path, temp_model_path)

    with open(temp_model_path, "r") as f:
        model_contents = f.read()

    model_contents = model_contents.replace("const int NUM_PIECES;", f"const int NUM_PIECES = {NUM_PIECES};")
    model_contents = model_contents.replace("const int PROCESSING_TIME_S1;", f"const int PROCESSING_TIME_S1 = {PROCESSING_TIME_S1};")
    model_contents = model_contents.replace("const int PROCESSING_TIME_S2;", f"const int PROCESSING_TIME_S2 = {PROCESSING_TIME_S2};")
    model_contents = model_contents.replace("const int PROCESSING_TIME_S3;", f"const int PROCESSING_TIME_S3 = {PROCESSING_TIME_S3};")
    model_contents = model_contents.replace("const int SPEED;", f"const int SPEED = {SPEED};")
    model_contents = model_contents.replace("const int NUM_SLOTS;", f" const int NUM_SLOTS = {NUM_SLOTS};")
    model_contents = model_contents.replace("const int GATE_POS;", f" const int GATE_POS = {GATE_POS};")
    model_contents = model_contents.replace("const int FIRST_POS_BELT2;", f"const int FIRST_POS_BELT2 = {FIRST_POS_BELT2};")
    model_contents = model_contents.replace("const int LAST_POS_BELT2;", f"const int LAST_POS_BELT2 = {LAST_POS_BELT2};")
    model_contents = model_contents.replace("const int RULE_CONTROLLER;", f"const int RULE_CONTROLLER = {RULE_CONTROLLER};")

    model_contents = model_contents.replace("const int NUM_STATIONS;", f"const int NUM_STATIONS = {NUM_STATIONS};")
    model_contents = model_contents.replace("const int NUM_IN_SENSORS;", f"const int NUM_IN_SENSORS = {NUM_IN_SENSORS};")
    model_contents = model_contents.replace("const int NUM_OUT_SENSORS;", f"const int NUM_OUT_SENSORS = {NUM_OUT_SENSORS};")


    with open(temp_model_path, "w") as f:
        f.write(model_contents)
    
    # Run UPPAAL model with verifyta
    #verifyta_path = "/Applications/uppaal64-4.1.26/bin-Darwin/verifyta" # Path to the verifyta executable
    command = f'/Applications/uppaal64-4.1.26/bin-Darwin/verifyta -s -o2 /Users/valeria/Desktop/formal-methods-project/sim/{temp_model_path}' # Comando verifyta
    result = os.popen(command).read()  # Execute the command and capture its output

    lines = result.split('\n')  # Split the output into lines

    # Print lines 8 and 9 (assuming indices are 7 and 8, since indexing starts from 0)
    if len(lines) >= 9:
        print("NUM_PIECES:", NUM_PIECES, " - ", "PROCESSING_TIME_S2:", PROCESSING_TIME_S2, " - ", "SPEED:", SPEED)
        #print results of query 6: the one veryfying the max length of the queue
        print(lines[22])
        print(lines[23]) 
        if ('NOT' in lines[23]):
            not_satisfied.append(1)
        else: 
            not_satisfied.append(0)
    else:
        print("Output does not contain enough lines.")
        # Remove the temporary model file
    
    os.remove(temp_model_path)

    NUM_PIECES_results.append(NUM_PIECES)
    PROCESSING_TIME_S2_results.append(PROCESSING_TIME_S2)
    SPEED_results.append(SPEED)

# Plot the results in a 3D scatter plot
fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')
sc = ax.scatter(NUM_PIECES_results, PROCESSING_TIME_S2_results, SPEED_results, c=not_satisfied, cmap='viridis')
plt.colorbar(sc)
ax.set_xlabel('NUM_PIECES')
ax.set_ylabel('PROCESSING_TIME_S2')
ax.set_zlabel('SPEED')
plt.show()
