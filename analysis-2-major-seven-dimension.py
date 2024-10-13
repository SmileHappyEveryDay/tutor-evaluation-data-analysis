import json
import pandas as pd

# Load the data from the provided JSON
file_path = 'proceed_comments_data_en_v3.json'

# Load JSON data
with open(file_path, 'r', encoding='utf-8') as f:
    data = json.load(f)

# Convert to a pandas dataframe for easier analysis
df = pd.DataFrame(data)

# Filter for relevant columns and group by major
metrics = ["average_score", "Teacher-Student Relationship", "Student Prospects", "Student Allowance",
           "Supervisor's Professional Ability", "Supervisor's Project Attitude", "Supervisor's Lifestyle"]

# Group by 'major' and calculate mean values
grouped_data = df.groupby('major')[metrics].mean().reset_index()

import matplotlib.pyplot as plt

# Set Agg as the backend for Matplotlib (non-GUI backend)
import matplotlib
matplotlib.use('Agg')

# # Set up subplots for each metric
# fig, axes = plt.subplots(7, 1, figsize=(10, 30))
#
# # Plot each metric
# for i, metric in enumerate(metrics):
#     grouped_data.plot(x='major', y=metric, kind='bar', ax=axes[i], legend=False)
#     axes[i].set_title(f'Average {metric} by Major')
#     axes[i].set_ylabel('Average Score')

import seaborn as sns
# Define a color palette for the bars
palette = sns.color_palette("Set2", len(grouped_data['major'].unique()))

# Loop to create and save each bar chart with annotations for the scores on top of each bar
import re
def is_valid_major(major):
    return bool(re.match(r'^[A-Za-z& ]+$', major)) and major != "Unknown"

grouped_data = grouped_data[grouped_data['major'].apply(is_valid_major)]

for i, metric in enumerate(metrics):
    plt.figure(figsize=(10, 6))
    ax = grouped_data.plot(x='major', y=metric, kind='bar', legend=False, color=palette)
    ax.set_title(f'{metric} Value Across Various Major', fontsize=14)
    ax.set_ylabel('Average Score', fontsize=12)
    ax.set_xlabel('Major', fontsize=12)
    # Rotate x-axis labels, reduce font size
    plt.xticks(rotation=45, ha='right', fontsize=10)  # Slant the x-axis labels with reduced font size

    # Annotate each bar with its value
    for p in ax.patches:
        ax.annotate(f'{p.get_height():.2f}', (p.get_x() + p.get_width() / 2., p.get_height()),
                    ha='center', va='center', fontsize=10, color='black', xytext=(0, 10),
                    textcoords='offset points')

    # Save the figure with new color scheme
    plt.tight_layout()
    plt.savefig(f'figs/major_dimensions/metric_{i + 1}_{metric}_colored.png')

# plt.show()
#
# # Display the plots
# plt.tight_layout()
# plt.show()


####################################################################################################################
