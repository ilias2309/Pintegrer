import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from wordcloud import WordCloud
from scipy.stats import chi2_contingency
from scipy.stats import ttest_ind
import numpy as np

# Load data
df = pd.read_csv('projetintegrer.csv')

# Rename columns
df.columns = [
    'timestamp',
    'username',
    'age',
    'gender',
    'education_level',
    'academic_performance_rating',
    'extracurricular_involvement',
    'participating_activities',
    'time_management_strategy',
    'impact_on_time_management',
    'institutional_support',
    'institutional_encouragement_rating',
    'extracurricular_contribution_rating',
    'improved_peer_relations',
    'influence_on_personal_development',
    'preferred_activities',
    'frequency_of_participation',
    'weekly_hours_spent_on_activities',
    'current_overall_average',
    'participation_in_events_last_year',
    'satisfaction_rating',
    'skills_acquired_count'
]

# Remove
df = df.drop_duplicates().drop(columns="username")
df = df.drop_duplicates().drop(columns="timestamp")

# Data cleaning and conversions
df['age'] = df['age'].astype(str).str.extract('(\d+)', expand=False).astype(float)
df['weekly_hours_spent_on_activities'] = df['weekly_hours_spent_on_activities'].astype(str).str.extract('(\d+)', expand=False).astype(float)

df['participation_in_events_last_year'] = df['participation_in_events_last_year'].replace({
    'Pas encore': 0,
    'Une seule fois': 1,
    '2 fois par semaine et parfois plus': 2
})
df['participation_in_events_last_year'] = pd.to_numeric(df['participation_in_events_last_year'], errors='coerce')
df['education_level'] = df['education_level'].str.replace(r'ème année|ère année', '', regex=True)
df = df.fillna(0)

# Set page configuration with layout="wide"
st.set_page_config(layout="wide")

# Display CSV file checkbox in the sidebar
show_csv_checkbox = st.sidebar.checkbox('Show CSV File')

# Display the CSV file if the checkbox is checked
if show_csv_checkbox:
    st.write("### CSV File:")
    st.dataframe(df)

# Disable PyplotGlobalUseWarning
st.set_option('deprecation.showPyplotGlobalUse', False)



# Streamlit App
st.title('Dashboard')

# Create checkboxes for each plot
show_gender_distribution = st.sidebar.checkbox('Show Gender Distribution Plot')
show_education_distribution = st.sidebar.checkbox('Show Education Level Distribution Plot')
show_age_distribution = st.sidebar.checkbox('Show Age Distribution Plot')
show_gender_academic_performance = st.sidebar.checkbox('Show Gender-Academic Performance Plot')
show_time_management_gender = st.sidebar.checkbox('Show Time Management-Gender Plot')
show_gender_education = st.sidebar.checkbox('Show Gender-Education Level Plot')
show_pie_chart_time_management = st.sidebar.checkbox('Show Pie Chart for Time Management Strategy')


col1, col2, col3 = st.columns(3)

# Display Gender Distribution Plot
if show_gender_distribution:
    with col1:
        st.subheader('Gender Distribution:')
        fig, ax = plt.subplots(figsize=(16, 8))
        sns.countplot(x='gender', data=df, ax=ax, palette='Set1')
        st.pyplot(fig)

# Bar plot for education level distribution
        
if show_education_distribution:

    with col2:
        st.subheader('Education Level Distribution:')
        fig, ax = plt.subplots(figsize=(16, 8))
        sns.countplot(x='education_level', data=df, ax=ax, palette='muted')  
        st.pyplot(fig)

# Box plot for age distribution
if show_age_distribution:
    with col3:
            st.subheader('Age Distribution:')
            fig, ax = plt.subplots(figsize=(16, 8))
            sns.boxplot(x='age', data=df, ax=ax, color='skyblue')  
            st.pyplot(fig)


col4, col5 = st.columns(2)

# Grouped bar plot for gender and ACADEMIC PERFORMANCE
if show_gender_academic_performance:
    with col4:
        st.subheader('Gender Distribution by Academic Performance:')
        fig, ax = plt.subplots(figsize=(16, 8))
        sns.countplot(x='academic_performance_rating', hue='gender', data=df, ax=ax, palette='dark')
        st.pyplot(fig)

# Grouped bar plot for time management strategy and gender
if show_time_management_gender:
    with col5:
        st.subheader('Distribution of Time Management Strategies by Gender:')
        fig, ax = plt.subplots(figsize=(16, 8))
        sns.countplot(x='time_management_strategy', hue='gender', data=df, ax=ax, palette='colorblind')
        st.pyplot(fig)


col6, col7, col8 = st.columns(3)

# Grouped bar plot for gender and education level
if show_gender_education:
    with col6:
        st.subheader('Gender Distribution by Education Level:')
        fig, ax = plt.subplots(figsize=(16, 8))
        sns.countplot(x='education_level', hue='gender', data=df, ax=ax)
        st.pyplot(fig)

# Grouped bar plot for gender and ACADEMIC PERFORMANCE
if show_pie_chart_time_management:
    with col7:
        st.subheader('Gender Distribution by Academic Performance:')
        fig, ax = plt.subplots(figsize=(16, 8))
        sns.countplot(x='academic_performance_rating', hue='gender', data=df, ax=ax)
        st.pyplot(fig)

# Grouped bar plot for time management strategy and gender

with col8:
        st.subheader('Distribution of Time Management Strategies by Gender:')
        fig, ax = plt.subplots(figsize=(16, 8))
        sns.countplot(x='time_management_strategy', hue='gender', data=df, ax=ax)
        st.pyplot(fig)


col9, col10 = st.columns(2)

# Pie chart for Time Management Strategy 
with col9:
        st.subheader('Pie chart for Time Management Strategy:')
        strategy_counts = df['time_management_strategy'].value_counts()
        fig, ax = plt.subplots(figsize=(16, 8))  # Adjust the size as needed
        wedges, texts, autotexts = ax.pie(strategy_counts, labels=[''] * len(strategy_counts), autopct='%.2f%%', startangle=90, wedgeprops=dict(width=0.4))

        # Create a separate legend
        legend_labels = [f'{strategy} ({count:.2f}%)' for strategy, count in zip(strategy_counts.index, strategy_counts / strategy_counts.sum() * 100)]
        legend_handles = [plt.Line2D([0], [0], marker='o', color='w', markerfacecolor=sns.color_palette('Set2')[i], markersize=10) for i in range(len(legend_labels))]
        ax.legend(legend_handles, legend_labels, title='Time Management Strategy', loc='center left', bbox_to_anchor=(1, 0.5), frameon=False)

    

        st.pyplot(fig)

# Pie chart for Frequency of Participation 
with col10:
        st.subheader('Frequency of Participation:')
        fig, ax = plt.subplots(figsize=(16, 8))  
        df['frequency_of_participation'].value_counts().plot.pie(autopct='%1.1f%%', ax=ax)
        st.pyplot(fig)



col11, col12 = st.columns(2)

with col11:
        # Grouped bar plot for gender and average grade
        st.subheader('Gender Distribution by Average Grade')
        fig, ax = plt.subplots(figsize=(16, 8))
        sns.countplot(x='current_overall_average', hue='gender', data=df, ax=ax, palette='dark' )
        plt.title('Gender Distribution by Average Grade')
        plt.xticks(rotation=45, ha='right') 
        st.pyplot(fig)

with col12:
        # Violin plot for weekly hours spent on activities
        st.subheader('Weekly hours spent on activities Distribution')
        fig, ax = plt.subplots(figsize=(16, 8))
        sns.violinplot(x='weekly_hours_spent_on_activities', data=df, ax=ax, palette='muted')
        plt.title('Weekly hours spent on activities Distribution')
        st.pyplot(fig)

col13, col14 = st.columns(2)
with col13:
        # Grouped bar plot for weekly hours spent on activities and gender 
        st.subheader('Relationship Between Current Overall Average, Weekly Hours Spent on Activities and Gender')
        fig, ax = plt.subplots(figsize=(16, 8))
        sns.barplot(data=df, x='current_overall_average', y='weekly_hours_spent_on_activities', hue='gender', ax=ax)
        plt.title('Relationship Between Current Overall Average, Weekly Hours Spent on Activities and Gender')
        st.pyplot(fig)

with col14:
        # Grouped bar plot for participation in events last year and gender
        st.subheader('Relationship Between Current Overall Average, Participation in Events Last Year, and Gender')
        fig, ax = plt.subplots(figsize=(16, 8))
        sns.barplot(data=df, x='current_overall_average', y='participation_in_events_last_year', hue='gender', ax=ax)
        plt.title('Relationship Between Current Overall Average, Participation in Events Last Year, and Gender')
        st.pyplot(fig)


column_for_wordcloud = 'preferred_activities'
# Word Cloud of Preferred Activities
st.subheader(f'Word Cloud of {column_for_wordcloud}:')
text = ' '.join(df[column_for_wordcloud].astype(str))
wordcloud = WordCloud(width=800, height=400, background_color='white').generate(text)
st.image(wordcloud.to_array(), use_column_width=True)



# Séparation des données pour les hommes et les femmes
weekly_hours_spent_on_activities_hommes = df[df['gender'] == 'Homme']['weekly_hours_spent_on_activities']
weekly_hours_spent_on_activities_femmes = df[df['gender'] == 'Femme']['weekly_hours_spent_on_activities']
# Effectuer le test t pour comparer les moyennes
t_stat, p_value = ttest_ind(weekly_hours_spent_on_activities_hommes, weekly_hours_spent_on_activities_femmes, equal_var=False)
# Create
st.title("Hypotheses Testing")
col15, col16, col17 = st.columns(3)
with col15:
    st.subheader("Hommes Weekly Hours:")
    st.write(weekly_hours_spent_on_activities_hommes)
with col16:
    st.subheader("Femmes Weekly Hours:")
    st.write(weekly_hours_spent_on_activities_femmes)
with col17:
    st.subheader("Hypotheses Testing Results")
    st.write(f"Test Statistique (t): {t_stat}")
    st.write(f"P-valeur: {p_value}")
# Interpretation
if p_value < 0.05:
    st.write("The difference in weekly hours spent on activities between men and women is statistically significant.")
else:
    st.write("There is not enough evidence to conclude a significant difference in weekly hours spent on activities between men and women.")


# Convert the 'gender' column values to 'male' and 'female'
df['gender'] = df['gender'].replace({'Homme': 'male', 'Femme': 'female'})
# Convert 'Oui' and 'Non' values to numeric (1 and 0) for the 'improved_peer_relations' column
df['improved_peer_relations'] = df['improved_peer_relations'].map({'Oui': 1, 'Non': 0})
# Filter data for male students
homme_data = df[df['gender'] == 'male']
# Calculate the proportion of male students who noticed an improvement
proportion_homme = homme_data['improved_peer_relations'].mean()
# Filter data for female employees
femme_data = df[df['gender'] == 'female']
# Calculate the proportion of female employees who noticed an improvement
proportion_femme = femme_data['improved_peer_relations'].mean()
# Create 
st.title("Proportions Comparison")
# Display 
st.subheader("Data Summary")
st.write("Proportion of Male Students with Improved Peer Relations:")
st.write(proportion_homme)
st.write("Proportion of Female Employees with Improved Peer Relations:")
st.write(proportion_femme)
# Perform a hypothesis test or display the results as needed
# You can include a hypothesis test here if needed
# Interpretation of the results
if proportion_homme > proportion_femme:
    st.write("A higher proportion of male students practice extracurricular activities.")
elif proportion_femme > proportion_homme:
    st.write("A higher proportion of female employees practice extracurricular activities.")
else:
    st.write("There is no significant difference in the proportions of practicing extracurricular activities between genders.")




