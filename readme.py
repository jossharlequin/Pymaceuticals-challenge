readme.txt
# Dependencies and Setup
import matplotlib.pyplot as plt
import pandas as pd
import scipy.stats as st

# Study data files
mouse_metadata_path = "data/Mouse_metadata.csv"
study_results_path = "data/Study_results.csv"

# Read the mouse data and the study results
mouse_metadata = pd.read_csv(mouse_metadata_path)
study_results = pd.read_csv(study_results_path)

# Combine the data into a single DataFrame
#From past class assignments
merged_data = pd.merge(study_results, mouse_metadata, on="Mouse ID", how="left")

# Display the data table for preview
mouse_table = pd.DataFrame(merged_data)
mouse_table.head()

# Checking the number of mice.
num_mice = merged_data["Mouse ID"].nunique()
num_mice

# Identify duplicate mice by Mouse ID and Timepoint
duplicate_mice_ids = merged_data[merged_data.duplicated(subset=["Mouse ID", "Timepoint"], keep=False)]["Mouse ID"].unique()
print(duplicate_mice_ids)

# Optional: Get all the data for the duplicate mouse ID. 
duplicate_mice = merged_data[merged_data.duplicated(subset=["Mouse ID", "Timepoint"], keep=False)]
duplicate_mice

# Create a clean DataFrame by dropping the duplicate mouse by its ID
#I got the help for this from AskBCS
duplicate_mouse = merged_data.loc[merged_data["Mouse ID"] != "g989"]
# Display the clean DataFrame
duplicate_mouse

# Checking the number of mice in the clean DataFrame.
#I got help from AskBCS because I thought it just wanted the duplicates removed, not the duplicate value removed. So when I did it first, the result was 249 instead of the correct 248.
num_mice2 = duplicate_mouse["Mouse ID"].nunique()
num_mice2

# Generate a summary statistics table of mean, median, variance, standard deviation, and SEM of the tumor volume for each regimen

# Use groupby and summary statistical methods to calculate the following properties of each drug regimen: 
regimen_grouped = duplicate_mouse.groupby('Drug Regimen')

# mean, median, variance, standard deviation, and SEM of the tumor volume.
# Help from here: https://stackoverflow.com/questions/65634122/find-mean-mode-and-median-with-python 
summary_stats_df = regimen_grouped['Tumor Volume (mm3)'].agg(['mean', 'median', 'var', 'std', 'sem'])

# Rename the columns for clarity
#Renamed to match the given table
summary_stats_df = summary_stats_df.rename(columns={
    'mean': 'Mean Tumor Volume',
    'median': 'Median Tumor Volume',
    'var': 'Tumor Volume Variance',
    'std': 'Tumor Volume Std. Dev.',
    'sem': 'Tumor Volume Std. Err.'
})

# Assemble the resulting series into a single summary DataFrame.
summary_stats_df

# A more advanced method to generate a summary statistics table of mean, median, variance, standard deviation,
# and SEM of the tumor volume for each regimen (only one method is required in the solution)
# Using the aggregation method, produce the same summary statistics in a single line
#Used this site for help again: https://stackoverflow.com/questions/65634122/find-mean-mode-and-median-with-python
summary_stats_df = duplicate_mouse.groupby('Drug Regimen')['Tumor Volume (mm3)'].agg(['mean', 'median', 'var', 'std', 'sem'])

# Display the summary statistics table
summary_stats_df

# Generate a bar plot showing the total number of rows (Mouse ID/Timepoints) for each drug regimen using Pandas.
# Count the number of rows for each drug regimen
regimen_counts = duplicate_mouse['Drug Regimen'].value_counts()

# Create a bar plot
#Found help in past assignments
regimen_counts.plot(kind='bar', color='orange', alpha=0.7, figsize=(10, 6), rot=45)

# Add labels and title
plt.xlabel('Drug Regimen')
plt.ylabel('Number of Rows')
plt.title('Total Number of Rows for Each Drug Regimen')

# Show the plot
plt.show()

# Generate a bar plot showing the total number of rows (Mouse ID/Timepoints) for each drug regimen using pyplot.
# Count the number of rows for each drug regimen
regimen_counts = duplicate_mouse['Drug Regimen'].value_counts()

# Create a bar plot using pyplot
plt.figure(figsize=(10, 6))
plt.bar(regimen_counts.index, regimen_counts, color='orange', alpha=0.7)

# Add labels and title
plt.xlabel('Drug Regimen')
plt.ylabel('Number of Rows')
plt.title('Total Number of Rows for Each Drug Regimen')

# Rotate x-axis labels for better readability
plt.xticks(rotation=45, ha='right')

# Show the plot
plt.show()

# Count the number of male and female mice
sex_distribution = duplicate_mouse['Sex'].value_counts()

# Create a pie plot using pandas
#Just used this site for help: https://www.geeksforgeeks.org/how-to-create-pie-chart-from-pandas-dataframe/
sex_distribution.plot(kind='pie', autopct='%1.1f%%', colors=['skyblue', 'pink'], startangle=90, figsize=(8, 8))

# Add title
plt.title('Distribution of Female Mice vs Male Mice')

# Show the plot
plt.show()

# Generate a pie plot showing the distribution of female versus male mice using pyplot
# Count the number of male and female mice
sex_distribution = duplicate_mouse['Sex'].value_counts()

# Create a pie plot using pyplot
plt.figure(figsize=(8, 8))
plt.pie(sex_distribution, labels=sex_distribution.index, autopct='%1.1f%%', colors=['skyblue', 'pink'], startangle=90)

# Add title
plt.title('Distribution of Female Mice vs Male Mice')

# Show the plot
plt.show()

# Calculate the final tumor volume of each mouse across four of the treatment regimens:  
# Capomulin, Ramicane, Infubinol, and Ceftamin

# Start by getting the last (greatest) timepoint for each mouse
#Got help from here: https://www.geeksforgeeks.org/find-maximum-values-position-in-columns-and-rows-of-a-dataframe-in-pandas/
last_timepoint = duplicate_mouse.groupby('Mouse ID')['Timepoint'].max()

last_timepoint_df = pd.DataFrame(last_timepoint)

# Merge this group DataFrame with the original DataFrame to get the tumor volume at the last timepoint
final_tumor_volume = pd.merge(last_timepoint_df, duplicate_mouse, on=['Mouse ID', 'Timepoint'], how='left')

# Capomulin, Ramicane, Infubinol, and Ceftamin
selected_regimens = final_tumor_volume[final_tumor_volume['Drug Regimen'].isin(['Capomulin', 'Ramicane', 'Infubinol', 'Ceftamin'])]

# Display the final DataFrame with the last tumor volume for each mouse in the selected treatment regimens
selected_regimens

# Put treatments into a list for a for loop (and later for plot labels)
treatments = ['Capomulin', 'Ramicane', 'Infubinol', 'Ceftamin']

# Create an empty list to fill with tumor volume data (for plotting)
tumor_vol_data = []

# Loop through each treatment
#This was done in class so I used it for help.
for treatment in treatments:
    # Locate the rows which contain mice on each drug and get the tumor volumes
    subset_data = selected_regimens[selected_regimens['Drug Regimen'] == treatment]['Tumor Volume (mm3)']
    
    # Add subset data to the list
    tumor_vol_data.append(subset_data)
    
    # Calculate the IQR and quantitatively determine if there are any potential outliers
    quartiles = subset_data.quantile([0.25, 0.5, 0.75])
    lower_q = quartiles[0.25]
    upper_q = quartiles[0.75]
    iqr = upper_q - lower_q
    
    # Determine outliers using upper and lower bounds
    lower_bound = lower_q - 1.5 * iqr
    upper_bound = upper_q + 1.5 * iqr
    
    # Print results
    print(f"\nTreatment: {treatment}")
    print(f"Interquartile Range (IQR): {iqr}")
    print(f"Lower Bound: {lower_bound}")
    print(f"Upper Bound: {upper_bound}")
    
    # Check for potential outliers
    potential_outliers = subset_data[(subset_data < lower_bound) | (subset_data > upper_bound)]
    print(f"Potential Outliers: {potential_outliers}")

# Display the tumor volume data
tumor_vol_data

# Generate a box plot that shows the distrubution of the tumor volume for each treatment group.
# Create a box plot
#This was done in class
plt.figure(figsize=(10, 6))
plt.boxplot(tumor_vol_data, labels=treatments, sym='r+')  # sym='r+' shows potential outliers as red plus signs

# Add labels and title
plt.xlabel('Treatment Group')
plt.ylabel('Tumor Volume (mm3)')
plt.title('Distribution of Tumor Volume for Each Treatment Group')

# Show the plot
plt.show()

# Generate a line plot of tumor volume vs. time point for a single mouse treated with Capomulin
# Select a single mouse treated with Capomulin
mouse_id_capomulin = 'y793'
capomulin_data = duplicate_mouse[(duplicate_mouse['Drug Regimen'] == 'Capomulin') & (duplicate_mouse['Mouse ID'] == mouse_id_capomulin)]

# Create a line plot for tumor volume vs. time point
plt.figure(figsize=(10, 6))
plt.plot(capomulin_data['Timepoint'], capomulin_data['Tumor Volume (mm3)'], marker='o', color='b', label=f'Mouse ID: {mouse_id_capomulin}')

# Add labels and title
plt.xlabel('Timepoint')
plt.ylabel('Tumor Volume (mm3)')
plt.title(f'Tumor Volume vs. Time Point for Mouse ID: {mouse_id_capomulin} (Capomulin)')
plt.legend()

# Show the plot
plt.grid(True)
plt.show()

# Generate a scatter plot of mouse weight vs. the average observed tumor volume for the entire Capomulin regimen
# Select data for the Capomulin regimen
capomulin_data = duplicate_mouse[duplicate_mouse['Drug Regimen'] == 'Capomulin']

# Calculate the average observed tumor volume for each mouse
average_tumor_volume = capomulin_data.groupby('Mouse ID')['Tumor Volume (mm3)'].mean()

# Merge the average tumor volume with the weight data
merged_data = pd.merge(average_tumor_volume, capomulin_data[['Mouse ID', 'Weight (g)']], on='Mouse ID', how='left').drop_duplicates()

# Create a scatter plot
plt.figure(figsize=(10, 6))
plt.scatter(merged_data['Weight (g)'], merged_data['Tumor Volume (mm3)'], color='b', marker='o')

# Add labels and title
plt.xlabel('Weight (g)')
plt.ylabel('Average Tumor Volume (mm3)')
plt.title('Mouse Weight vs. Average Tumor Volume (Capomulin Regimen)')

# Show the plot
plt.grid(True)
plt.show()

# Calculate the correlation coefficient and a linear regression model 
# for mouse weight and average observed tumor volume for the entire Capomulin regimen
from scipy.stats import pearsonr, linregress

# Assuming your DataFrame is named merged_data

# Calculate the correlation coefficient
correlation_coefficient, _ = pearsonr(duplicate_mouse['Weight (g)'], duplicate_mouse['Tumor Volume (mm3)'])
print(f'Correlation Coefficient: {correlation_coefficient}')

# Perform linear regression
slope, intercept, r_value, p_value, std_err = linregress(duplicate_mouse['Weight (g)'], duplicate_mouse['Tumor Volume (mm3)'])

# Create a linear regression line
regression_line = slope * duplicate_mouse['Weight (g)'] + intercept

# Plot the scatter plot with the regression line
plt.figure(figsize=(10, 6))
plt.scatter(duplicate_mouse['Weight (g)'], duplicate_mouse['Tumor Volume (mm3)'], color='b', marker='o', label='Data')
plt.plot(duplicate_mouse['Weight (g)'], regression_line, color='r', label='Linear Regression')

# Add labels and title
plt.xlabel('Weight (g)')
plt.ylabel('Average Tumor Volume (mm3)')
plt.title('Mouse Weight vs. Average Tumor Volume (Capomulin Regimen)')

# Add legend
plt.legend()

# Show the plot
plt.grid(True)
plt.show()

