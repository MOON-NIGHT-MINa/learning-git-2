 import os
import json
import re
from datetime import datetime
from collections import Counter
import requests
import pandas as pd
import matplotlib.pyplot as plt
import pycountry
COLLECTION_NAME = "jobs"
RAW_JSON_PATH = "jobs_raw.json"
RAW_CSV_PATH = "jobs_raw.csv"
CLEAN_JSON_PATH = "jobs_cleaned.json"
url = "https://remoteok.com/api"
headers = {"User-Agent": "Mozilla/5.0"}
response = requests.get(url, headers=headers, timeout=15)
jobs = response.json()[1:]
with open(RAW_JSON_PATH, "w", encoding="utf-8") as f:
 json.dump(jobs, f, indent=2)
pd.DataFrame(jobs).to_csv(RAW_CSV_PATH, index=False)
print(" Raw data saved")
import pandas as pd
import pycountry

# Assuming 'jobs' is already fetched (from API or loaded from JSON)
df = pd.DataFrame(jobs)

# Clean company names and position titles
df['company'] = df['company'].str.replace(r'[^\w\s]', '', regex=True).str.title()
df['position'] = df['position'].str.strip()

# Calculate average salary
df['salary_avg'] = df[['salary_min', 'salary_max']].mean(axis=1)

# Identify fully remote jobs
df['fully_remote'] = df['location'].str.contains('worldwide', case=False, na=True)

# Extract countries from location
df['countries'] = df['location'].apply(
    lambda loc: [country.name for country in pycountry.countries if country.name.lower() in str(loc).lower()]
)

# Convert 'date' to datetime and make it timezone-naive
df['date_posted'] = pd.to_datetime(df['date'], errors='coerce').dt.tz_localize(None)

# Calculate how many days ago the job was posted
df['days_ago'] = (pd.to_datetime('now').normalize() - df['date_posted']).dt.days

# Clean tags and extract emails and URLs
df['tags'] = df['tags'].apply(lambda tags: [t.strip().title() for t in tags if t.strip()] if isinstance(tags, list) else [])
df['emails'] = df['description'].str.findall(r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}\b')
df['urls'] = df['description'].str.findall(r'https?://[^\s,]+')

# Save cleaned data to a JSON file
df.to_json("jobs_cleaned.json", orient="records", indent=2)
print("✅ Cleaned data saved")

# Show preview
df.head()
import pandas as pd
import pycountry

# Assuming 'jobs' is already fetched (from API or loaded from JSON)
df = pd.DataFrame(jobs)

# Clean company names and position titles
df['company'] = df['company'].str.replace(r'[^\w\s]', '', regex=True).str.title()
df['position'] = df['position'].str.strip()

# Calculate average salary
df['salary_avg'] = df[['salary_min', 'salary_max']].mean(axis=1)

# Identify fully remote jobs
df['fully_remote'] = df['location'].str.contains('worldwide', case=False, na=True)

# Extract countries from location
df['countries'] = df['location'].apply(
    lambda loc: [country.name for country in pycountry.countries if country.name.lower() in str(loc).lower()]
)

# Convert 'date' to datetime and make it timezone-naive
df['date_posted'] = pd.to_datetime(df['date'], errors='coerce').dt.tz_localize(None)

# Calculate how many days ago the job was posted
df['days_ago'] = (pd.to_datetime('now').normalize() - df['date_posted']).dt.days

# Clean tags and extract emails and URLs
df['tags'] = df['tags'].apply(lambda tags: [t.strip().title() for t in tags if t.strip()] if isinstance(tags, list) else [])
df['emails'] = df['description'].str.findall(r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}\b')
df['urls'] = df['description'].str.findall(r'https?://[^\s,]+')

# Save cleaned data to a JSON file
df.to_json("jobs_cleaned.json", orient="records", indent=2)
print("✅ Cleaned data saved")

# Show preview
df.head()

# Step 4: Create DataFrame
df = pd.DataFrame(jobs)

# Step 5: Clean data
df['company'] = df['company'].str.replace(r'[^\w\s]', '', regex=True).str.title()
df['position'] = df['position'].str.strip()
df['salary_avg'] = df[['salary_min', 'salary_max']].mean(axis=1)

df['fully_remote'] = df['location'].str.contains('worldwide', case=False, na=True)

df['countries'] = df['location'].apply(
    lambda loc: [country.name for country in pycountry.countries if country.name.lower() in str(loc).lower()]
)

df['date_posted'] = pd.to_datetime(df['date'], errors='coerce').dt.tz_localize(None)
df['days_ago'] = (pd.to_datetime('now').normalize() - df['date_posted']).dt.days

df['tags'] = df['tags'].apply(lambda tags: [t.strip().title() for t in tags if t.strip()] if isinstance(tags, list) else [])
df['emails'] = df['description'].str.findall(r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}\b')
df['urls'] = df['description'].str.findall(r'https?://[^\s,]+')
print(df.head())
# Step 6: Save cleaned data
df.to_json(CLEAN_JSON_PATH, orient="records", indent=2)
print("✅ Cleaned job data saved")
# Step 8: Quick summary
print(f"Total jobs: {len(df)}")
print(f"% Fully remote: {df['fully_remote'].mean() * 100:.1f}%")
print(f"Average salary: ${df['salary_avg'].mean():,.0f}")
print(f"Jobs with salary info: {df['salary_avg'].notnull().sum()}")
print(f"Jobs with remote info: {df['fully_remote'].notnull().sum()}")
print(f"Max salary: ${df['salary_avg'].max():,.0f}")
print(f"Min salary: ${df['salary_avg'].min():,.0f}")
print(f"Total remote jobs: {df[df['fully_remote'] == 1].shape[0]}")
print(f"Total in-office jobs: {df[df['fully_remote'] == 0].shape[0]}")
from collections import Counter
import pandas as pd

# Basic stats
total_jobs = len(df)
pct_fully_remote = df['fully_remote'].mean() * 100
overall_avg_salary = df['salary_avg'].mean()

# Top categories by tag frequency
top_categories = df.explode('tags')['tags'].value_counts().head(10)

# Average salary by category
cat_salary = (
    df.explode('tags')
    .groupby('tags')['salary_avg']
    .mean()
    .sort_values(ascending=False)
    .head(10)
)

# Top skills (assuming 'tags' field represents skills too)
top_skills = df.explode('tags')['tags'].value_counts().head(10)

# Top countries (assuming 'countries' is a list)
country_counts = Counter(sum(df['countries'], []))
top_countries = pd.Series(country_counts).sort_values(ascending=False).head(10)

# Top hiring companies
top_companies = df['company'].value_counts().head(10)

# Print summary
print(f"Total jobs: {total_jobs}")
print(f"% Fully remote: {pct_fully_remote:.1f}%")
print(f"Average salary: ${overall_avg_salary:,.0f}")
print("\nTop Categories:")
print(top_categories)
print("\nTop Skills:")
print(top_skills)
print("\nTop Countries:")
print(top_countries)
print("\nTop Hiring Companies:")
print(top_companies)
print("\nTop Salary by Category:")
print(cat_salary)
import matplotlib.pyplot as plt

# Bar chart: Top Skills
top_skills.plot(kind='bar', title='Top Skills', figsize=(8, 4))
plt.tight_layout()
plt.show()

# Horizontal bar chart: Highest-Paying Categories
cat_salary.plot(kind='barh', title='Highest-Paying Categories', figsize=(8, 4))
plt.tight_layout()
plt.show()

# Bar chart: Top Countries
top_countries.plot(kind='bar', title='Top Countries', figsize=(8, 4))
plt.tight_layout()
plt.show()

# Bar chart: Top Hiring Companies
top_companies.plot(kind='bar', title='Top Hiring Companies', figsize=(8, 4))
plt.tight_layout()
plt.show()

# Pie chart: Skill Distribution
top_skills.plot(
    kind='pie',
    title='Skill Distribution',
    autopct='%1.1f%%',
    figsize=(6, 6),
    ylabel=''  # Removes default y-label
)
plt.tight_layout()
plt.show()

# Line chart: Salary Trend by Category
cat_salary.sort_values().plot(
    kind='line',
    title='Salary Trend by Category',
    marker='o',
    figsize=(8, 4)
)
plt.tight_layout()
plt.show()
from pymongo import MongoClient
# Connect to MongoDB
client = MongoClient('mongodb://localhost:27017/')
db = client['remote_jobs_db']
collection = db['cleaned_jobs'] # New collection for the cleaned jobs
# Drop the collection if you want a fresh start
# Convert DataFrame to list of dictionaries
job_data = df.to_dict(orient='records')
# Insert cleaned jobs into MongoDB

# Close connection
client.close()
print(" Cleaned job data saved to MongoDB (collection: cleaned_jobs)")


