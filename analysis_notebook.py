# analysis_notebook.py
# Basic analysis of CORD-19 metadata.csv
# ---------------------------------------------------

import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from wordcloud import WordCloud

# Load dataset
df = pd.read_csv("metadata.csv")

# Inspect dataset
print("Shape of dataset:", df.shape)
print(df.info())
print(df.isnull().sum().head(20))  # check missing values

# Handle missing values
df = df.dropna(subset=['title', 'abstract', 'publish_time'])  # keep only important rows

# Convert publish_time to datetime
df['publish_time'] = pd.to_datetime(df['publish_time'], errors='coerce')
df['year'] = df['publish_time'].dt.year

# Add abstract word count
df['abstract_word_count'] = df['abstract'].apply(lambda x: len(str(x).split()))

# --- ANALYSIS ---

# 1. Publications by year
year_counts = df['year'].value_counts().sort_index()
plt.figure(figsize=(8,5))
sns.barplot(x=year_counts.index, y=year_counts.values, color="skyblue")
plt.title("Publications by Year")
plt.xlabel("Year")
plt.ylabel("Number of Papers")
plt.xticks(rotation=45)
plt.tight_layout()
plt.show()

# 2. Top journals
top_journals = df['journal'].value_counts().head(10)
plt.figure(figsize=(8,5))
sns.barplot(y=top_journals.index, x=top_journals.values, color="green")
plt.title("Top 10 Journals Publishing COVID-19 Research")
plt.xlabel("Number of Papers")
plt.ylabel("Journal")
plt.tight_layout()
plt.show()

# 3. Word Cloud from titles
titles = " ".join(df['title'].dropna().astype(str))
wordcloud = WordCloud(width=800, height=400, background_color='white').generate(titles)

plt.figure(figsize=(10,6))
plt.imshow(wordcloud, interpolation="bilinear")
plt.axis("off")
plt.title("Word Cloud of Paper Titles")
plt.show()

# 4. Distribution by source_x
source_counts = df['source_x'].value_counts().head(10)
plt.figure(figsize=(8,5))
sns.barplot(y=source_counts.index, x=source_counts.values, color="purple")
plt.title("Top Sources of Papers")
plt.xlabel("Number of Papers")
plt.ylabel("Source")
plt.tight_layout()
plt.show()

print("Analysis complete ✅")