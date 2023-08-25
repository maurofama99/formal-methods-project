import subprocess
import os
import shutil
import matplotlib.pyplot as plt
from itertools import product
import re

# Define the range for the varying parameters
NUM_PIECES_range = range(5, 30, 6)
PROCESSING_MEAN_S2_range = range(10,500, 100)
ERROR_PROB_OUTS2_range = range(1, 180, 50)

not_satisfied = []

# Define the fixed parameters
SPEED = 5
NUM_SLOTS = 61
GATE_POS = -1 #there is no gate in these configurations
FIRST_POS_BELT2 = -1
LAST_POS_BELT2 = -1
RULE_CONTROLLER = 10
PROCESSING_MEAN_S1 = 10
PROCESSING_VAR_S1 = 2
PROCESSING_VAR_S2 = 5
PROCESSING_MEAN_S3 = 10
PROCESSING_VAR_S3 = 2
ERROR_PROB_S1 = 1
ERROR_PROB_S2 = 1
ERROR_PROB_S3 = 1
ERROR_PROB_OUTS1 = 1
ERROR_PROB_OUTS3 = 1

NUM_STATIONS = 3
NUM_IN_SENSORS = 3
NUM_OUT_SENSORS = 3

# Initialize lists to store results for plotting
NUM_PIECES_results = []
PROCESSING_MEAN_S2_results = []
ERROR_PROB_OUTS2_results = []
query_results = []

# Loop through all combinations of varying parameters
for NUM_PIECES, PROCESSING_MEAN_S2, ERROR_PROB_OUTS2 in product(NUM_PIECES_range, PROCESSING_MEAN_S2_range, ERROR_PROB_OUTS2_range):
    # Define the parameters string for the UPPAAL model

    # Create a temporary model file with the new parameters
    original_model_path = "conf.xml"
    temp_model_path = f"temp_model_{NUM_PIECES}_{PROCESSING_MEAN_S2}_{ERROR_PROB_OUTS2}.xml"
    shutil.copyfile(original_model_path, temp_model_path)

    with open(temp_model_path, "r") as f:
        model_contents = f.read()

    model_contents = model_contents.replace("const int NUM_PIECES;", f"const int NUM_PIECES = {NUM_PIECES};")
    model_contents = model_contents.replace("const int PROCESSING_MEAN_S1;", f"const int PROCESSING_MEAN_S1 = {PROCESSING_MEAN_S1};")
    model_contents = model_contents.replace("const int PROCESSING_VAR_S1;", f"const int PROCESSING_VAR_S1 = {PROCESSING_VAR_S1};")
    model_contents = model_contents.replace("const int PROCESSING_MEAN_S2;", f"const int PROCESSING_MEAN_S2 = {PROCESSING_MEAN_S2};")
    model_contents = model_contents.replace("const int PROCESSING_VAR_S2;", f"const int PROCESSING_VAR_S2 = {PROCESSING_VAR_S2};")
    model_contents = model_contents.replace("const int PROCESSING_MEAN_S3;", f"const int PROCESSING_MEAN_S3 = {PROCESSING_MEAN_S3};")
    model_contents = model_contents.replace("const int PROCESSING_VAR_S3;", f"const int PROCESSING_VAR_S3 = {PROCESSING_VAR_S3};")
    model_contents = model_contents.replace("const int ERROR_PROB_S1;", f"const int ERROR_PROB_S1 = {ERROR_PROB_S1};")
    model_contents = model_contents.replace("const int ERROR_PROB_S2;", f"const int ERROR_PROB_S2 = {ERROR_PROB_S2};")
    model_contents = model_contents.replace("const int ERROR_PROB_S3;", f"const int ERROR_PROB_S3 = {ERROR_PROB_S3};")
    model_contents = model_contents.replace("const int ERROR_PROB_OUTS1;", f"const int ERROR_PROB_OUTS1 = {ERROR_PROB_OUTS1};")
    model_contents = model_contents.replace("const int ERROR_PROB_OUTS2;", f"const int ERROR_PROB_OUTS2 = {ERROR_PROB_OUTS2};")
    model_contents = model_contents.replace("const int ERROR_PROB_OUTS3;", f"const int ERROR_PROB_OUTS3 = {ERROR_PROB_OUTS3};")
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
    command = f'/Applications/uppaal64-4.1.26/bin-Darwin/verifyta -s -o2 -a 0.01 -B 0.01 -E 0.01 {temp_model_path}' # Comando verifyta
    result = os.popen(command).read()  # Execute the command and capture its output

    lines = result.split('\n')  # Split the output into lines

    print("NUM_PIECES:", NUM_PIECES, " - ", "PROCESSING_MEAN_S2:", PROCESSING_MEAN_S2, " - ", "ERROR_PROB_OUTS2:", ERROR_PROB_OUTS2)
    pattern = r'\[(.*?),(.*)\]'
    match = re.search(pattern, lines[9])
    #print("probability of not deadlock: ", match.group(1), match.group(2))
    integers = re.findall(r'\[([\d.]+),([\d.]+)\]', lines[9])
    # Convert the extracted strings to float numbers
    integers = [(float(match[0]), float(match[1])) for match in integers]
    # Print the extracted integers

    # Calculate the average for each pair of integers
    averages = [(pair[0] + pair[1]) / 2 for pair in integers]

    print (averages)

    os.remove(temp_model_path)

    NUM_PIECES_results.append(NUM_PIECES)
    PROCESSING_MEAN_S2_results.append(PROCESSING_MEAN_S2)
    ERROR_PROB_OUTS2_results.append(ERROR_PROB_OUTS2)
    query_results.append(averages)

# Plot the results in a 3D scatter plot
fig = plt.figure()
ax = fig.add_subplot(111, projection='3d', proj_type = 'ortho')
sc = ax.scatter(NUM_PIECES_results, PROCESSING_MEAN_S2_results, ERROR_PROB_OUTS2_results, c=query_results, cmap='coolwarm')
plt.colorbar(sc)
ax.set_xlabel('NUM_PIECES')
ax.set_ylabel('PROCESSING_MEAN_S2')
ax.set_zlabel('ERROR_PROB_OUTS2')
plt.show()
