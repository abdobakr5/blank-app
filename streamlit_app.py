import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from wordcloud import WordCloud
import numpy as np

st.set_page_config(layout="wide", page_title="💼 Job Listings Analysis Dashboard")


# Load data
@st.cache_data
def load_data():
    return pd.read_excel("Job_cleaned.xlsx")

df = load_data()

st.title("💼 Job Listings Analysis Dashboard")

# Sidebar Filters
st.sidebar.header("Filters")
location_filter = st.sidebar.multiselect("Select Locations:", df['location'].dropna().unique(), default=df['location'].dropna().unique())
type_filter = st.sidebar.multiselect("Select Job Types:", df['jobs_type'].dropna().unique(), default=df['jobs_type'].dropna().unique())

# Apply filters
df_filtered = df[df['location'].isin(location_filter) & df['jobs_type'].isin(type_filter)]

# Top Job Titles
st.subheader("📊 Top 10 Job Titles")
top_titles = df_filtered['job_title'].value_counts().nlargest(10)
fig1, ax1 = plt.subplots()
sns.barplot(x=top_titles.values, y=top_titles.index, palette="mako", ax=ax1)
ax1.set_title("Top 10 Job Titles")
st.pyplot(fig1)

# Word Cloud for Companies
st.subheader("☁️ Top Hiring Companies")
company_freq = df_filtered['company'].value_counts().to_dict()
wordcloud = WordCloud(width=800, height=400, background_color='white').generate_from_frequencies(company_freq)
fig2, ax2 = plt.subplots(figsize=(10, 5))
ax2.imshow(wordcloud, interpolation='bilinear')
ax2.axis("off")
st.pyplot(fig2)

# Pie Chart for Location
st.subheader("📍 Job Distribution by Location")
top_locations = df_filtered['location'].value_counts().nlargest(6)
fig3, ax3 = plt.subplots()
ax3.pie(top_locations, labels=top_locations.index, autopct='%.1f%%', startangle=140, colors=sns.color_palette('pastel'))
ax3.axis('equal')
st.pyplot(fig3)

# Donut Chart for Job Types
st.subheader("🕒 Job Types")
job_types_main = df_filtered['jobs_type'].value_counts().nlargest(5)
fig4, ax4 = plt.subplots()
ax4.pie(job_types_main, labels=job_types_main.index, startangle=90, autopct='%1.1f%%', wedgeprops={'width':0.5}, colors=sns.color_palette("Set2"))
ax4.axis('equal')
st.pyplot(fig4)

# Heatmap: Job Type by Location
st.subheader("🔥 Job Type vs Location")
top5_locations = df_filtered['location'].value_counts().nlargest(5).index
pivot = df_filtered[df_filtered['location'].isin(top5_locations)].pivot_table(index='location', columns='jobs_type', aggfunc='size', fill_value=0)
fig5, ax5 = plt.subplots(figsize=(10, 6))
sns.heatmap(pivot, annot=True, fmt='d', cmap="YlGnBu", ax=ax5)
ax5.set_title("Job Type Distribution Across Top 5 Locations")
st.pyplot(fig5)

# Posting Trend Line Chart
st.subheader("📈 Job Postings Over Time")
def extract_days(text):
    try:
        if isinstance(text, str):
            if 'day' in text:
                return int(text.split()[0])
            elif 'month' in text:
                return int(text.split()[0]) * 30
            elif 'hour' in text:
                return 0
        return np.nan
    except:
        return np.nan

df_filtered['days_ago'] = df_filtered['published_time'].apply(extract_days)
posting_trend = df_filtered['days_ago'].value_counts().sort_index()
fig6, ax6 = plt.subplots()
sns.lineplot(x=posting_trend.index, y=posting_trend.values, marker='o', color='coral', ax=ax6)
ax6.set_xlabel("Days Ago")
ax6.set_ylabel("Number of Postings")
ax6.set_title("Job Postings Over Time")
ax6.grid(True)
st.pyplot(fig6)
