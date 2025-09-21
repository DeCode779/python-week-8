# app.py
# Streamlit app for CORD-19 dataset
# ---------------------------------------------------

import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from wordcloud import WordCloud

st.title("CORD-19 Data Explorer")
st.write("A simple interactive dashboard to explore COVID-19 research papers metadata.")

# Load data
@st.cache_data
def load_data():
    df = pd.read_csv("metadata.csv")
    df = df.dropna(subset=['title', 'abstract', 'publish_time'])
    df['publish_time'] = pd.to_datetime(df['publish_time'], errors='coerce')
    df['year'] = df['publish_time'].dt.year
    df['abstract_word_count'] = df['abstract'].apply(lambda x: len(str(x).split()))
    return df

df = load_data()

# Sidebar filters
st.sidebar.header("Filters")
min_year = int(df['year'].min())
max_year = int(df['year'].max())
year_range = st.sidebar.slider("Select year range", min_year, max_year, (2020, 2021))

filtered_df = df[(df['year'] >= year_range[0]) & (df['year'] <= year_range[1])]

# Display dataset preview
st.subheader("Sample of Dataset")
st.dataframe(filtered_df.head(20))

# Publications by year
st.subheader("Publications by Year")
year_counts = filtered_df['year'].value_counts().sort_index()
fig, ax = plt.subplots(figsize=(8,4))
sns.barplot(x=year_counts.index, y=year_counts.values, color="skyblue", ax=ax)
plt.xticks(rotation=45)
st.pyplot(fig)

# Top Journals
st.subheader("Top Journals")
top_journals = filtered_df['journal'].value_counts().head(10)
fig, ax = plt.subplots(figsize=(8,4))
sns.barplot(y=top_journals.index, x=top_journals.values, color="green", ax=ax)
st.pyplot(fig)

# Word Cloud of Titles
st.subheader("Word Cloud of Paper Titles")
titles = " ".join(filtered_df['title'].dropna().astype(str))
wordcloud = WordCloud(width=800, height=400, background_color='white').generate(titles)
fig, ax = plt.subplots(figsize=(10,6))
ax.imshow(wordcloud, interpolation="bilinear")
ax.axis("off")
st.pyplot(fig)

# Source distribution
st.subheader("Distribution by Source")
source_counts = filtered_df['source_x'].value_counts().head(10)
fig, ax = plt.subplots(figsize=(8,4))
sns.barplot(y=source_counts.index, x=source_counts.values, color="purple", ax=ax)
st.pyplot(fig)

st.success("Dashboard loaded successfully ✅")