# Fix incorrect CSV file headers.
# For each .csv file in the test_data directory, read the file, and replace the current header with
# "Nozzle 1 state, Nozzle 2 state, Time, Gyro X, Gyro Y, Gyro Z, Accel X, Accel Y, Accel Z\n"

import os
import csv

# Directory containing the CSV files
directory = 'test_data'

# New header to replace the first line
new_header = ["Nozzle 1 state", "Nozzle 2 state", "Time", "Gyro X", "Gyro Y", "Gyro Z", "Accel X", "Accel Y", "Accel Z"]

# Iterate over every file in the directory
for filename in os.listdir(directory):
    if filename.endswith(".csv"):
        filepath = os.path.join(directory, filename)

        # Read the CSV file
        with open(filepath, 'r') as file:
            reader = list(csv.reader(file))
            # Replace the first line with the new header
            reader[0] = new_header
        
        # Write the modified content back to the same CSV file
        with open(filepath, 'w', newline='') as file:
            writer = csv.writer(file)
            writer.writerows(reader)

print("CSV headers replaced successfully.")
