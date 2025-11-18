import pandas as pd

file_path = r"C:\Users\anush\OneDrive\Desktop\Documents\uber_trip_project\data\uber_analysis_2015_cleaned.csv"
df = pd.read_csv(file_path)

print(df.columns)
