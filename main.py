"""
I have to use BeautifulSoup to scrap the web page. Since the html file is local,
I don't need the requests module
"""
from bs4 import BeautifulSoup
import pandas as pd
import numpy as np
import csv
from collections import Counter
import random
from sqlalchemy import create_engine


"""
Datebase, instead of postgresql, I'm having issues configuring it on my machine, I guess it's because of it's version.
"""
import sqlite3

# opening the html file with python open function
# I'm using with just to make sure I don't leave the file open after I'm done opening it
with open('home.html') as file:
    # reading the content of the file
    file_content = file.read()


# making a soup object from the file_content using BeautifulSoup method from bs4
# the "html.parser" is to tell indicate the format the file_content is written in
soup = BeautifulSoup(file_content, "html.parser")

data = []

for row in soup.find_all('tr'):
    columns = row.find_all('td')
    data.append({
        "Day": columns[0].text,
        "Colour": columns[1].text
    })

# Convert the list of dictionaries to a DataFrame
df = pd.DataFrame(data)

# Save the DataFrame to a CSV file
df.to_csv('output.csv', index=False)

csv_columns = ["Day", "Colour"]

try:
    with open("output.csv", mode="w", newline="") as data_file:
        writer = csv.DictWriter(data_file, fieldnames=csv_columns)
        writer.writeheader()
        for i in data:
            writer.writerow(i)
except IOError:
    print("I/O error")

colour_counts = {}
for colours in df["Colour"]:
    for colour in colours.split(','):
        colour_counts[colour] = colour_counts.get(colour, 0) + 1
# Convert the counts to a DataFrame
color_counts_df = pd.DataFrame(list(colour_counts.items()), columns=['Colour', 'Count'])


counts = list(color_counts_df["Count"])
colors = list(color_counts_df["Colour"])

# Calculate the weighted sum of color indices
weighted_sum = sum(index * count for index, count in enumerate(counts))

# Calculate the total count of colors
total_count = sum(counts)

# Calculate the mean index
mean_index = weighted_sum / total_count

# Round to the nearest integer to get the index of the mean color
mean_index = round(mean_index)

# Retrieve the mean color from the list
mean_color = colors[mean_index]

print("Mean Color:", mean_color)

new_dict = pd.read_csv("output.csv").to_dict(orient='records')

# Flatten the list of dictionaries to create a single list of all colors
all_colours = [colour.strip() for day in new_dict for colour in day["Colour"].split(',')]

# Count the occurrences of each color
colour_counts = Counter(all_colours)

# Find the color with the maximum count
most_frequent_colour = colour_counts.most_common(1)[0][0]
print("Most Frequent Colour:", most_frequent_colour)

# Split the string of colors into individual colors
# Sort the list of colors
sorted_colors = sorted(all_colours)

# Find the median color
n = len(sorted_colors)
if n % 2 == 1:
    median_color = sorted_colors[n // 2]
else:
    median_color = sorted_colors[n // 2 - 1 : n // 2 + 1]

print("Median Colour:", median_color)

# Count the occurrences of each color
color_counts = dict(zip(*np.unique(all_colours, return_counts=True)))

# Calculate the mean of the colors
mean_count = np.mean(list(color_counts.values()))

# Calculate the squared differences of each color from the mean
squared_diffs = [(count - mean_count) ** 2 for count in color_counts.values()]

# Calculate the variance
variance = np.mean(squared_diffs)

print("Variance of Colors:", variance)

# Generate random colour from the colour list
random_colour = random.randint(0, len(colors))
colour_chosen = colors[random_colour]

# Count the occurrences of red
colour_count = all_colours.count(colour_chosen)

# Calculate the total number of occurrences of all colors
total_count = len(all_colours)

# Calculate the probability of choosing red
probability = colour_count / total_count

print(f"Probability of choosing {colour_chosen}", probability)

data = {'Colour': colors,
        'Frequency': counts
}

d_file = pd.DataFrame(data)


# Connection to MySQL DB
engine = create_engine('mysql://skibo:jayboy99@localhost:5432/interview')

# Insert the DataFrame intp MySQL DB
df.to_sql('interview', engine, if_exists='replace', index=False)
