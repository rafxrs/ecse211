import csv
import statistics

# File path to the CSV file
file_path = r"C:\ecse211\lab2\lab2-starter-code_w23\data_analysis\color_sensor_red.csv"

# Read the data from the first column of the CSV file into a list
data = []
with open(file_path, 'r') as file:
    reader = csv.reader(file)
    for row in reader:
        data.append(float(row[2]))

# Calculate the minimum, maximum, mean, and standard deviation
minimum = min(data)
maximum = max(data)
mean = sum(data) / len(data)
stddev = statistics.stdev(data)

# Print the results
print("Minimum:", minimum)
print("Maximum:", maximum)
print("Mean:", mean)
print("Standard Deviation:", stddev)
