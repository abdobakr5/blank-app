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
    df = pd.read_excel("Job_cleaned.xlsx")
    return df

df = load_data()

st.title("Job Listings Analysis Dashboard")

# Sidebar Filters
st.sidebar.header("Filters")

# Get the actual column names
available_cities = df['work_location'].dropna().unique()
available_programs = df['program'].dropna().unique()
available_shifts = df['shift'].dropna().unique()

city_filter = st.sidebar.multiselect("Select Locations:", available_cities, default=available_cities)
program_filter = st.sidebar.multiselect("Select Programs:", available_programs, default=available_programs)
shift_filter = st.sidebar.multiselect("Select Shifts:", available_shifts, default=available_shifts)

# Apply filters
df_filtered = df[
    df['work_location'].isin(city_filter) & 
    df['program'].isin(program_filter) &
    df['shift'].isin(shift_filter)
]

# Top Job Titles
st.subheader("Top 10 Job Titles")
top_titles = df_filtered['job_title'].value_counts().nlargest(10)
fig1, ax1 = plt.subplots(figsize=(10, 6))
sns.barplot(x=top_titles.values, y=top_titles.index, palette="mako", ax=ax1)
ax1.set_title("Top 10 Job Titles")
st.pyplot(fig1)

# Word Cloud for Companies
st.subheader("Top Hiring Companies")
company_freq = df_filtered['company'].value_counts().to_dict()
wordcloud = WordCloud(width=800, height=400, background_color='white').generate_from_frequencies(company_freq)
fig2, ax2 = plt.subplots(figsize=(10, 5))
ax2.imshow(wordcloud, interpolation='bilinear')
ax2.axis("off")
st.pyplot(fig2)

# Distribution by City
st.subheader("Job Distribution by Location")
top_cities = df_filtered['work_location'].value_counts().nlargest(6)
fig3, ax3 = plt.subplots()
ax3.pie(top_cities, labels=top_cities.index, autopct='%.1f%%', startangle=140, colors=sns.color_palette('pastel'))
ax3.axis('equal')
st.pyplot(fig3)

# Donut Chart for Work Shifts
st.subheader("Work Shifts Distribution")
shifts = df_filtered['shift'].value_counts()
total = shifts.sum()
percentages = (shifts / total * 100).round(1)
legend_labels = [f"{shift} ({pct}%)" for shift, pct in zip(shifts.index, percentages)]

fig4, ax4 = plt.subplots(figsize=(10, 6))
patches, _ = ax4.pie(shifts, 
                    labels=None,
                    startangle=90, 
                    wedgeprops={'width':0.5}, 
                    colors=sns.color_palette("Set2"))

# Add a legend with percentages
ax4.legend(patches, legend_labels, 
          title="Shift Types",
          loc="center left",
          bbox_to_anchor=(1, 0, 0.5, 1))
ax4.axis('equal')
plt.tight_layout()
st.pyplot(fig4)

# Posting Trend Line Chart
st.subheader("Job Postings Over Time")
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

# Experience Level Distribution
st.subheader("Experience Years Distribution")
fig7, ax7 = plt.subplots(figsize=(10, 6))

# Handle the experience years data properly
def extract_min_experience(x):
    try:
        if x == 'Undefined':
            return 0
        return float(str(x).split('-')[0])
    except:
        return 0

experience_counts = df_filtered['experience_years'].apply(extract_min_experience).value_counts().sort_index()
sns.barplot(x=experience_counts.index, y=experience_counts.values, palette='viridis', ax=ax7)
ax7.set_xlabel("Minimum Years of Experience")
ax7.set_ylabel("Number of Jobs")
ax7.set_title("Distribution of Minimum Experience Requirements")
plt.xticks(rotation=45)
plt.tight_layout()
st.pyplot(fig7)

# Add back the Program Distribution Heatmap
st.subheader("Program Distribution by City")
top5_cities = df_filtered['work_location'].value_counts().nlargest(5).index
pivot = df_filtered[df_filtered['work_location'].isin(top5_cities)].pivot_table(
    index='work_location', 
    columns='program', 
    aggfunc='size', 
    fill_value=0
)
fig5, ax5 = plt.subplots(figsize=(12, 6))
sns.heatmap(pivot, annot=True, fmt='d', cmap="YlGnBu", ax=ax5)
ax5.set_title("Program Distribution Across Top 5 Cities")
plt.tight_layout()
st.pyplot(fig5)
